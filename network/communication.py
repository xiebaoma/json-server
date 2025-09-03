#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络通信层
处理Socket连接和JSON数据传输
"""

import json
import socket
import struct
import logging
import threading
import time
from datetime import datetime
from typing import Dict, Any, Callable, Optional


class NetworkHandler:
    def __init__(self, host: str = '0.0.0.0', port: int = 55000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.logger = logging.getLogger(__name__)
        self.request_handler = None
    
    def set_request_handler(self, handler: Callable[[Dict[str, Any]], Any]):
        """设置请求处理器"""
        self.request_handler = handler
    
    def start_server(self) -> bool:
        """启动服务器"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            self.running = True
            self.logger.info(f"网络服务器已启动，监听端口: {self.host}:{self.port}")
            
            while self.running:
                try:
                    # 设置socket超时，以便能够响应停止信号
                    self.server_socket.settimeout(1.0)
                    client_socket, client_addr = self.server_socket.accept()
                    
                    if not self.running:
                        client_socket.close()
                        break
                    
                    self.logger.info(f"客户端连接: {client_addr}")
                    
                    # 使用线程处理每个客户端连接
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_addr)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.timeout:
                    # 超时是正常的，继续循环检查running状态
                    continue
                except OSError as e:
                    if self.running:
                        self.logger.error(f"接受连接时出错: {e}")
                    break
                except Exception as e:
                    if self.running:
                        self.logger.error(f"接受连接时出错: {e}")
            
            self.logger.info("网络服务器主循环已退出")
            return True
                    
        except Exception as e:
            self.logger.error(f"启动网络服务器失败: {e}")
            return False
        finally:
            if self.server_socket:
                self.server_socket.close()
    
    def stop_server(self):
        """停止服务器"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        self.logger.info("网络服务器已停止")
    
    def handle_client(self, client_socket: socket.socket, client_addr: tuple):
        """处理单个客户端连接"""
        try:
            # 步骤1: 接收JSON数据
            json_data = self.receive_json(client_socket)
            if json_data is None:
                self.send_error_response(client_socket, "接收JSON数据失败")
                return
            
            self.logger.info(f"从 {client_addr} 接收到JSON数据: {json_data}")
            
            # 步骤2: 处理JSON数据
            if self.request_handler:
                result = self.request_handler(json_data)
            else:
                result = "错误: 未设置请求处理器"
            
            # 步骤3: 将处理结果以JSON格式返回给客户端
            self.send_response(client_socket, result)
            
        except Exception as e:
            self.logger.error(f"处理客户端 {client_addr} 时出错: {e}")
            self.send_error_response(client_socket, f"服务器内部错误: {str(e)}")
        finally:
            time.sleep(1)
            client_socket.close()
            self.logger.info(f"客户端 {client_addr} 连接已关闭")
    
    def receive_json(self, client_socket: socket.socket) -> Optional[Dict[str, Any]]:
        """接收JSON数据（不保存到文件，直接在内存中处理）"""
        try:
            # 接收文件名长度
            raw_len = client_socket.recv(4)
            if not raw_len:
                return None
            name_len = struct.unpack("!I", raw_len)[0]
            
            # 接收文件名（虽然不用保存，但需要接收完整协议）
            filename = client_socket.recv(name_len).decode("utf-8")
            
            # 接收文件大小
            raw_size = client_socket.recv(4)
            if not raw_size:
                return None
            filesize = struct.unpack("!I", raw_size)[0]
            
            # 接收文件内容到内存
            json_content = b""
            received = 0
            while received < filesize:
                chunk = client_socket.recv(min(4096, filesize - received))
                if not chunk:
                    break
                json_content += chunk
                received += len(chunk)
            
            # 解析JSON数据
            json_str = json_content.decode('utf-8')
            json_data = json.loads(json_str)
            
            return json_data
            
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON解析错误: {e}")
            return None
        except Exception as e:
            self.logger.error(f"接收JSON数据时出错: {e}")
            return None
    
    def send_response(self, client_socket: socket.socket, result: Any):
        """向客户端发送响应"""
        try:
            response = {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "result": result
            }
            response_json = json.dumps(response, ensure_ascii=False, indent=2)
            response_bytes = response_json.encode('utf-8')
            
            # 发送响应长度
            client_socket.sendall(struct.pack("!I", len(response_bytes)))
            # 发送响应内容
            client_socket.sendall(response_bytes)
            
            self.logger.info(f"响应已发送: {response}")
            
        except Exception as e:
            self.logger.error(f"发送响应时出错: {e}")
    
    def send_error_response(self, client_socket: socket.socket, error_message: str):
        """发送错误响应"""
        try:
            response = {
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": error_message
            }
            response_json = json.dumps(response, ensure_ascii=False, indent=2)
            response_bytes = response_json.encode('utf-8')
            
            # 发送响应长度
            client_socket.sendall(struct.pack("!I", len(response_bytes)))
            # 发送响应内容
            client_socket.sendall(response_bytes)
            
            self.logger.error(f"错误响应已发送: {error_message}")
            
        except Exception as e:
            self.logger.error(f"发送错误响应时出错: {e}")


class JSONProtocolClient:
    """JSON协议客户端（用于测试）"""
    
    def __init__(self, host: str = 'localhost', port: int = 55000):
        self.host = host
        self.port = port
        self.logger = logging.getLogger(__name__)
    
    def send_json_data(self, data: Dict[str, Any], filename: str = "request.json") -> Optional[Dict[str, Any]]:
        """发送JSON数据到服务器"""
        try:
            # 连接到服务器
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            
            # 准备JSON数据
            json_str = json.dumps(data, ensure_ascii=False, indent=2)
            json_bytes = json_str.encode('utf-8')
            
            # 发送文件名长度和文件名
            filename_bytes = filename.encode('utf-8')
            client_socket.sendall(struct.pack("!I", len(filename_bytes)))
            client_socket.sendall(filename_bytes)
            
            # 发送文件大小和内容
            client_socket.sendall(struct.pack("!I", len(json_bytes)))
            client_socket.sendall(json_bytes)
            
            # 接收响应
            response = self.receive_response(client_socket)
            
            # 在关闭连接前稍等片刻，确保数据传输完成
            time.sleep(0.1)
            client_socket.close()
            
            return response
            
        except Exception as e:
            self.logger.error(f"发送JSON数据时出错: {e}")
            return None
    
    def receive_response(self, client_socket: socket.socket) -> Optional[Dict[str, Any]]:
        """接收服务器响应"""
        try:
            # 接收响应长度
            raw_len = client_socket.recv(4)
            if not raw_len:
                return None
            response_len = struct.unpack("!I", raw_len)[0]
            
            # 接收响应内容
            response_content = b""
            received = 0
            while received < response_len:
                chunk = client_socket.recv(min(4096, response_len - received))
                if not chunk:
                    break
                response_content += chunk
                received += len(chunk)
            
            # 解析JSON响应
            response_str = response_content.decode('utf-8')
            response_data = json.loads(response_str)
            
            return response_data
            
        except Exception as e:
            self.logger.error(f"接收响应时出错: {e}")
            return None
