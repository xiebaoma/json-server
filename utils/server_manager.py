#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
服务器管理器
处理守护进程、PID文件、信号处理、日志配置等
"""

import os
import sys
import signal
import atexit
import logging
from typing import Optional


class ServerManager:
    def __init__(self, pid_file: str = '/medical/server.pid', log_file: str = '/medical/server.log'):
        self.pid_file = pid_file
        self.log_file = log_file
        self.logger = None
        self.setup_logging()
        self.setup_signal_handlers()
    
    def setup_logging(self):
        """设置日志记录"""
        # 确保日志目录存在
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        # 清除现有的handlers
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                # 守护进程模式下不使用控制台输出
                # logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_signal_handlers(self):
        """设置信号处理器"""
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        if hasattr(signal, 'SIGQUIT'):
            signal.signal(signal.SIGQUIT, self._signal_handler)
        atexit.register(self.cleanup)
    
    def _signal_handler(self, signum, frame):
        """信号处理函数"""
        self.logger.info(f"收到信号 {signum}，准备关闭服务器...")
        # 这里可以添加优雅关闭的逻辑
        self.cleanup()
        sys.exit(0)
    
    def create_pid_file(self) -> bool:
        """创建PID文件"""
        try:
            # 确保PID文件目录存在
            os.makedirs(os.path.dirname(self.pid_file), exist_ok=True)
            
            # 检查是否已经有服务器在运行
            if os.path.exists(self.pid_file):
                with open(self.pid_file, 'r') as f:
                    old_pid = f.read().strip()
                try:
                    os.kill(int(old_pid), 0)  # 检查进程是否存在
                    self.logger.error(f"服务器已在运行 (PID: {old_pid})")
                    return False
                except (OSError, ValueError):
                    # 进程不存在，删除旧的PID文件
                    os.remove(self.pid_file)
            
            # 写入当前进程PID
            with open(self.pid_file, 'w') as f:
                f.write(str(os.getpid()))
            self.logger.info(f"PID文件已创建: {self.pid_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"创建PID文件失败: {e}")
            return False
    
    def remove_pid_file(self):
        """删除PID文件"""
        try:
            if os.path.exists(self.pid_file):
                os.remove(self.pid_file)
                self.logger.info(f"PID文件已删除: {self.pid_file}")
        except Exception as e:
            self.logger.error(f"删除PID文件失败: {e}")
    
    def cleanup(self):
        """清理资源"""
        self.remove_pid_file()
    
    def get_server_pid(self) -> Optional[int]:
        """获取服务器PID"""
        try:
            if os.path.exists(self.pid_file):
                with open(self.pid_file, 'r') as f:
                    pid = int(f.read().strip())
                # 检查进程是否存在
                os.kill(pid, 0)
                return pid
        except (OSError, ValueError):
            pass
        return None
    
    def is_server_running(self) -> bool:
        """检查服务器是否在运行"""
        return self.get_server_pid() is not None
    
    def stop_server(self) -> bool:
        """停止服务器"""
        pid = self.get_server_pid()
        
        if not pid:
            self.logger.info("服务器未在运行")
            return False
        
        try:
            self.logger.info(f"正在停止服务器 (PID: {pid})...")
            os.kill(pid, signal.SIGTERM)
            
            # 等待进程结束
            import time
            for _ in range(30):  # 等待最多30秒
                try:
                    os.kill(pid, 0)
                    time.sleep(1)
                except OSError:
                    break
            else:
                # 如果30秒后仍未结束，使用SIGKILL强制终止
                self.logger.warning("正常关闭超时，强制终止...")
                os.kill(pid, signal.SIGKILL)
            
            self.logger.info("服务器已停止")
            return True
            
        except OSError as e:
            self.logger.error(f"停止服务器失败: {e}")
            return False


def daemonize():
    """将当前进程转为守护进程"""
    try:
        # 第一次fork
        if os.fork() > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write(f"第一次fork失败: {e}\n")
        sys.exit(1)
    
    # 脱离父进程会话
    os.setsid()
    
    # 第二次fork
    try:
        if os.fork() > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write(f"第二次fork失败: {e}\n")
        sys.exit(1)
    
    # 更改工作目录
    os.chdir('/')
    
    # 设置文件权限掩码
    os.umask(0)
    
    # 重定向标准文件描述符
    sys.stdout.flush()
    sys.stderr.flush()
    
    # 重定向到/dev/null
    with open(os.devnull, 'r') as null_in:
        os.dup2(null_in.fileno(), sys.stdin.fileno())
    with open(os.devnull, 'w') as null_out:
        os.dup2(null_out.fileno(), sys.stdout.fileno())
        os.dup2(null_out.fileno(), sys.stderr.fileno())
