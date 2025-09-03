#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医疗系统主服务器
整合所有服务并提供统一入口
"""

import sys
import os
import logging
from typing import Dict, Any

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import DatabaseManager
from services.auth_service import AuthService
from services.appointment_service import AppointmentService
from network.communication import NetworkHandler
from utils.server_manager import ServerManager, daemonize


class MedicalServer:
    def __init__(self, host='0.0.0.0', port=55000, db_path='/medical/MedicalSystem.db', 
                 log_file='/medical/server.log', pid_file='/medical/server.pid'):
        self.host = host
        self.port = port
        self.db_path = db_path
        self.log_file = log_file
        self.pid_file = pid_file
        
        # 初始化服务器管理器
        self.server_manager = ServerManager(pid_file, log_file)
        self.logger = logging.getLogger(__name__)
        
        # 初始化数据库
        self.db_manager = DatabaseManager(db_path)
        
        # 初始化服务
        self.auth_service = AuthService(db_path)
        self.appointment_service = AppointmentService(db_path)
        
        # 初始化网络处理器
        self.network_handler = NetworkHandler(host, port)
        self.network_handler.set_request_handler(self.process_json_data)
        
        self.running = False
    
    def start_server(self, daemon=False):
        """启动服务器"""
        if daemon:
            if not self.server_manager.create_pid_file():
                return False
            daemonize()
        
        try:
            self.running = True
            self.logger.info(f"医疗系统服务器启动")
            self.logger.info(f"监听地址: {self.host}:{self.port}")
            self.logger.info(f"数据库文件: {self.db_path}")
            self.logger.info(f"日志文件: {self.log_file}")
            if daemon:
                self.logger.info(f"PID文件: {self.pid_file}")
                self.logger.info(f"服务器PID: {os.getpid()}")
            
            # 启动网络服务
            success = self.network_handler.start_server()
            return success
            
        except KeyboardInterrupt:
            if not daemon:
                print("\n收到中断信号，正在关闭服务器...")
            self.stop_server()
        except Exception as e:
            self.logger.error(f"服务器运行时出错: {e}")
            return False
        finally:
            if daemon:
                self.server_manager.remove_pid_file()
        
        return True
    
    def stop_server(self):
        """停止服务器"""
        self.running = False
        if self.network_handler:
            self.network_handler.stop_server()
        self.logger.info("医疗系统服务器已停止")
    
    def process_json_data(self, data: Dict[str, Any]) -> Any:
        """处理JSON数据并执行相应操作"""
        try:
            # 检查JSON中的操作类型并执行相应操作
            if 'reset_password' in data:
                return self.auth_service.update_user_password(data)
            
            elif 'register_patient' in data:
                return self.auth_service.register_patient(data)
            
            elif 'register_doctor' in data:  # 修正拼写错误
                return self.auth_service.register_doctor(data)
            
            elif 'login' in data:
                return self.auth_service.login_match(data)
            
            elif 'reset_patient_information' in data:
                return self.auth_service.update_patient_info(data)
            
            elif 'reset_doctor_information' in data:
                return self.auth_service.update_doctor_info(data)
            
            elif 'query_doctor_info' in data:
                return self.auth_service.query_doctor_info(data)
            
            elif 'query_patient_info' in data:
                return self.auth_service.query_patient_info(data)
            
            elif 'sql_query' in data:
                return self.execute_sql(data)
            
            elif 'create_appointment' in data:
                return self.appointment_service.create_appointment(data)
            
            elif 'query_appointments' in data:
                return self.appointment_service.query_appointments(data)
            
            elif 'cancel_appointment' in data:
                return self.appointment_service.cancel_appointment(data)
            
            elif 'update_appointment_status' in data:
                return self.appointment_service.update_appointment_status(data)
            
            else:
                # 默认作为插入数据处理
                table_name = data.get('table_name', 'default_table')
                if 'table_name' in data:
                    data_copy = data.copy()
                    del data_copy['table_name']
                else:
                    data_copy = data
                return self.db_manager.insert_data(data_copy, table_name)
                
        except Exception as e:
            self.logger.error(f"处理JSON数据时出错: {e}")
            return f"处理JSON数据时出错: {str(e)}"
    
    def execute_sql(self, data: Dict[str, Any]) -> Any:
        """执行JSON中的SQL查询"""
        try:
            sql_query = data.get('sql_query')
            if not sql_query:
                return "错误: JSON中未找到'sql_query'键"
            
            return self.db_manager.execute_sql(sql_query)
            
        except Exception as e:
            return f"错误: {str(e)}"
