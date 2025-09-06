#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
整合的JSON数据库服务器
功能：
1. 接收客户端连接和JSON数据
2. 处理JSON并操作数据库
3. 将处理结果以JSON格式返回给客户端
"""

import json
import sqlite3
import socket
import struct
import logging
import os
import threading
import signal
import sys
import atexit
import argparse
import time
from datetime import datetime
import hashlib


class JSONDatabaseServer:
    def __init__(self, host='0.0.0.0', port=55000, db_path='/medical/MedicalSystem.db', 
                 log_file='/medical/server.log', pid_file='/medical/server.pid'):
        self.host = host
        self.port = port
        self.db_path = db_path
        self.log_file = log_file
        self.pid_file = pid_file
        self.server_socket = None
        self.running = False
        self.setup_logging()
        self.init_database()
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
        self.stop_server()
    
    def create_pid_file(self):
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
        if self.server_socket:
            self.server_socket.close()
    
    def stop_server(self):
        """停止服务器"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        self.logger.info("服务器已停止")
    
    def init_database(self):
        """初始化数据库和创建必要的表（基于database.md中的医疗系统设计）"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 启用外键约束
            cursor.execute("PRAGMA foreign_keys = ON")
            
            # 1. 创建用户表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,  -- 手机号或工号
                    password_hash TEXT NOT NULL,    -- 密码哈希
                    role TEXT NOT NULL CHECK(role IN ('patient', 'doctor')),  -- 角色
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 2. 创建患者信息表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    birth_date DATE,
                    id_card TEXT,
                    phone TEXT,
                    email TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES users(user_id)
                )
            ''')
            
            # 3. 创建医生信息表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS doctors (
                    doctor_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    employee_id TEXT UNIQUE NOT NULL,
                    department TEXT,
                    photo_path TEXT,
                    max_patients INTEGER DEFAULT 30,
                    fee REAL,
                    work_schedule TEXT,  -- JSON格式
                    is_available BOOLEAN DEFAULT 1,
                    FOREIGN KEY (doctor_id) REFERENCES users(user_id)
                )
            ''')
            
            # 4. 创建预约挂号表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS appointments (
                    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    doctor_id INTEGER NOT NULL,
                    appointment_time TIMESTAMP NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('pending', 'completed', 'cancelled')),
                    fee_paid BOOLEAN DEFAULT 0,
                    queue_number INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
                )
            ''')
            
            # 5. 创建病历表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS medical_records (
                    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    doctor_id INTEGER NOT NULL,
                    diagnosis TEXT,
                    symptoms TEXT,
                    visit_time TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
                )
            ''')
            
            # 6. 创建医嘱表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS medical_orders (
                    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    record_id INTEGER NOT NULL,
                    doctor_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (record_id) REFERENCES medical_records(record_id),
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
                )
            ''')
            
            # 7. 创建处方表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prescriptions (
                    prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    record_id INTEGER NOT NULL,
                    doctor_id INTEGER NOT NULL,
                    content TEXT NOT NULL,  -- 药品、用法
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (record_id) REFERENCES medical_records(record_id),
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
                )
            ''')
            
            # 8. 创建打卡记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS attendance (
                    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    doctor_id INTEGER NOT NULL,
                    check_in_time TIMESTAMP NOT NULL,
                    check_out_time TIMESTAMP,
                    status TEXT NOT NULL CHECK(status IN ('present', 'absent')),
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
                )
            ''')
            
            # 9. 创建聊天记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_messages (
                    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender_id INTEGER NOT NULL,
                    receiver_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_read BOOLEAN DEFAULT 0,
                    FOREIGN KEY (sender_id) REFERENCES users(user_id),
                    FOREIGN KEY (receiver_id) REFERENCES users(user_id)
                )
            ''')
            
            # 10. 创建请假表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS leave_requests (
                    leave_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    doctor_id INTEGER NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    reason TEXT,
                    status TEXT NOT NULL CHECK(status IN ('pending', 'approved', 'rejected')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
                )
            ''')
            
            # 11. 创建住院信息表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS hospitalizations (
                    hospitalization_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    doctor_id INTEGER NOT NULL,
                    ward_number TEXT,
                    bed_number TEXT,
                    admission_date DATE NOT NULL,
                    discharge_date DATE,
                    status TEXT NOT NULL CHECK(status IN ('admitted', 'discharged')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
                )
            ''')
            
            # 创建测试用表（保持兼容性）
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    student_id INTEGER UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS default_table (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 插入示例数据（如果表是空的）
            self.insert_sample_data(cursor)
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"数据库初始化完成: {self.db_path}")
            self.logger.info("已创建医疗系统完整表结构")
            
            # 显示数据库状态
            self.show_database_status()
            
        except Exception as e:
            self.logger.error(f"数据库初始化失败: {e}")
    
    def insert_sample_data(self, cursor):
        """插入示例数据"""
        try:
            # 检查是否需要插入示例数据
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                # 插入患者用户并获取生成的user_id
                patient_users = [
                    ('13800138000', 'hash_patient1', 'patient'),
                    ('13900139000', 'hash_patient2', 'patient'), 
                    ('15800158000', 'hash_patient3', 'patient')
                ]
                
                patient_ids = []
                for username, password_hash, role in patient_users:
                    cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                                 (username, password_hash, role))
                    patient_ids.append(cursor.lastrowid)
                
                # 插入医生用户并获取生成的user_id
                doctor_users = [
                    ('DOC001', 'hash_doctor1', 'doctor'),
                    ('DOC002', 'hash_doctor2', 'doctor'),
                    ('DOC003', 'hash_doctor3', 'doctor')
                ]
                
                doctor_ids = []
                for username, password_hash, role in doctor_users:
                    cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                                 (username, password_hash, role))
                    doctor_ids.append(cursor.lastrowid)
                
                self.logger.info(f"已插入用户示例数据，患者ID: {patient_ids}, 医生ID: {doctor_ids}")
                
                # 插入患者详细信息，使用实际生成的patient_id
                patient_details = [
                    ('张三', '1990-01-01', '110101199001010001', '13800138000', 'zhangsan@example.com'),
                    ('李四', '1985-05-15', '110101198505150002', '13900139000', 'lisi@example.com'),
                    ('王五', '1992-03-20', '110101199203200003', '15800158000', 'wangwu@example.com')
                ]
                
                for i, (name, birth_date, id_card, phone, email) in enumerate(patient_details):
                    cursor.execute("""
                        INSERT INTO patients (patient_id, name, birth_date, id_card, phone, email) 
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (patient_ids[i], name, birth_date, id_card, phone, email))
                
                self.logger.info("已插入患者示例数据")
                
                # 插入医生详细信息，使用实际生成的doctor_id
                doctor_details = [
                    ('王医生', 'DOC001', '内科', 30, 50.0, '{"monday": "9:00-17:00", "tuesday": "9:00-17:00", "wednesday": "9:00-17:00", "thursday": "9:00-17:00", "friday": "9:00-17:00"}', 1),
                    ('刘医生', 'DOC002', '外科', 25, 80.0, '{"monday": "8:00-18:00", "tuesday": "8:00-18:00", "wednesday": "8:00-18:00", "thursday": "8:00-18:00", "friday": "8:00-18:00", "saturday": "9:00-15:00"}', 1),
                    ('陈医生', 'DOC003', '儿科', 40, 60.0, '{"monday": "9:00-17:00", "tuesday": "9:00-17:00", "wednesday": "9:00-17:00", "thursday": "9:00-17:00", "friday": "9:00-17:00"}', 1)
                ]
                
                for i, (name, employee_id, department, max_patients, fee, work_schedule, is_available) in enumerate(doctor_details):
                    cursor.execute("""
                        INSERT INTO doctors (doctor_id, name, employee_id, department, max_patients, fee, work_schedule, is_available) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (doctor_ids[i], name, employee_id, department, max_patients, fee, work_schedule, is_available))
                
                self.logger.info("已插入医生示例数据")
            
                # 插入预约示例数据，使用实际生成的ID
                cursor.execute("SELECT COUNT(*) FROM appointments")
                if cursor.fetchone()[0] == 0:
                    appointments = [
                        (patient_ids[0], doctor_ids[0], '2024-02-01 09:00:00', 'completed', 1, 1),
                        (patient_ids[1], doctor_ids[1], '2024-02-01 10:00:00', 'pending', 0, 2),
                        (patient_ids[2], doctor_ids[2], '2024-02-01 14:00:00', 'pending', 1, 1)
                    ]
                    
                    for patient_id, doctor_id, apt_time, status, fee_paid, queue_number in appointments:
                        cursor.execute("""
                            INSERT INTO appointments (patient_id, doctor_id, appointment_time, status, fee_paid, queue_number) 
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (patient_id, doctor_id, apt_time, status, fee_paid, queue_number))
                    
                    self.logger.info("已插入预约示例数据")
                
                # 插入病历示例数据，使用实际生成的ID
                cursor.execute("SELECT COUNT(*) FROM medical_records")
                if cursor.fetchone()[0] == 0:
                    medical_records = [
                        (patient_ids[0], doctor_ids[0], '感冒', '发热、咳嗽、流涕', '2024-02-01 09:30:00'),
                        (patient_ids[1], doctor_ids[1], '阑尾炎', '右下腹痛', '2024-01-28 10:30:00')
                    ]
                    
                    for patient_id, doctor_id, diagnosis, symptoms, visit_time in medical_records:
                        cursor.execute("""
                            INSERT INTO medical_records (patient_id, doctor_id, diagnosis, symptoms, visit_time) 
                            VALUES (?, ?, ?, ?, ?)
                        """, (patient_id, doctor_id, diagnosis, symptoms, visit_time))
                    
                    self.logger.info("已插入病历示例数据")
                
                # 插入打卡示例数据，使用实际生成的ID
                cursor.execute("SELECT COUNT(*) FROM attendance")
                if cursor.fetchone()[0] == 0:
                    attendance_records = [
                        (doctor_ids[0], '2024-02-01 08:50:00', '2024-02-01 17:10:00', 'present'),
                        (doctor_ids[1], '2024-02-01 07:55:00', '2024-02-01 18:05:00', 'present'),
                        (doctor_ids[2], '2024-02-01 08:58:00', None, 'present')
                    ]
                    
                    for doctor_id, check_in, check_out, status in attendance_records:
                        cursor.execute("""
                            INSERT INTO attendance (doctor_id, check_in_time, check_out_time, status) 
                            VALUES (?, ?, ?, ?)
                        """, (doctor_id, check_in, check_out, status))
                    
                    self.logger.info("已插入打卡示例数据")
            
            # 保持测试表的兼容数据
            cursor.execute("SELECT COUNT(*) FROM students")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO students (name, age, student_id) VALUES ('测试学生', 20, 12345)")
                
        except Exception as e:
            self.logger.error(f"插入示例数据失败: {e}")
    
    def show_database_status(self):
        """显示数据库状态"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 医疗系统主要表
            medical_tables = [
                'users', 'patients', 'doctors', 'appointments', 
                'medical_records', 'medical_orders', 'prescriptions', 
                'attendance', 'chat_messages', 'leave_requests', 'hospitalizations'
            ]
            
            # 测试表
            test_tables = ['students', 'default_table']
            
            self.logger.info("=== 医疗系统数据库状态 ===")
            for table in medical_tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    self.logger.info(f"{table} 表: {count} 条记录")
                except Exception as e:
                    self.logger.warning(f"无法查询表 {table}: {e}")
            
            self.logger.info("=== 测试表状态 ===")
            for table in test_tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    self.logger.info(f"{table} 表: {count} 条记录")
                except Exception as e:
                    self.logger.warning(f"无法查询表 {table}: {e}")
            
            conn.close()
            
        except Exception as e:
            self.logger.error(f"查看数据库状态失败: {e}")
    
    def start_server(self, daemon=False):
        """启动服务器"""
        if daemon:
            if not self.create_pid_file():
                return False
        
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            self.running = True
            self.logger.info(f"服务器已启动，监听端口: {self.host}:{self.port}")
            self.logger.info(f"数据库文件: {self.db_path}")
            self.logger.info(f"日志文件: {self.log_file}")
            if daemon:
                self.logger.info(f"PID文件: {self.pid_file}")
                self.logger.info(f"服务器PID: {os.getpid()}")
            
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
            
            self.logger.info("服务器主循环已退出")
                    
        except Exception as e:
            self.logger.error(f"启动服务器失败: {e}")
            return False
        finally:
            if self.server_socket:
                self.server_socket.close()
            if daemon:
                self.remove_pid_file()
        
        return True
    
    def handle_client(self, client_socket, client_addr):
        """处理单个客户端连接"""
        try:
            # 步骤1: 接收JSON数据
            json_data = self.receive_json(client_socket)
            if json_data is None:
                self.send_error_response(client_socket, "接收JSON数据失败")
                return
            
            self.logger.info(f"从 {client_addr} 接收到JSON数据: {json_data}")
            
            # 步骤2: 处理JSON并操作数据库
            result = self.process_json_data(json_data)
            
            # 步骤3: 将处理结果以JSON格式返回给客户端
            self.send_response(client_socket, result)
            
        except Exception as e:
            self.logger.error(f"处理客户端 {client_addr} 时出错: {e}")
            self.send_error_response(client_socket, f"服务器内部错误: {str(e)}")
        finally:
            time.sleep(1)
            client_socket.close()
            self.logger.info(f"客户端 {client_addr} 连接已关闭")
    
    def receive_json(self, client_socket):
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
    
    def send_response(self, client_socket, result):
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
    
    def send_error_response(self, client_socket, error_message):
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
    
    def process_json_data(self, data):
        """处理JSON数据并执行数据库操作"""
        try:
            # 检查JSON中的操作类型并执行相应操作
            if 'reset_password' in data:
                return self.update_user_password(data)
            #重置密码
            elif'register_patient' in data:
                return self.register_patient(data)
            elif'regiter_doctor' in data:
                return self.register_doctor(data)
            elif 'login' in data:
                return self.login_match(data)
            #登录检查
            elif 'reset_patient_information' in data:
                return self.update_patient_info(data)
            #重置病人信息
            elif 'reset_doctor_information' in data:
                return self.update_doctor_info(data)
            #重置医生信息
            elif 'query_doctor_info' in data:
                return self.query_doctor_info(data)
            #查询医生信息
            elif 'query_patient_info' in data:
                return self.query_patient_info(data)
            #查询患者信息
            elif 'sql_query' in data:
                return self.execute_sql(data)
            #查询操作
            elif 'create_appointment' in data:
                return self.create_appointment(data)
            #创建预约/挂号
            elif 'query_appointments' in data:
                return self.query_appointments(data)
            #查询预约
            elif 'cancel_appointment' in data:
                return self.cancel_appointment(data)
            #取消预约
            elif 'update_appointment_status' in data:
                return self.update_appointment_status(data)
            #更新预约状态
            else:
                # 默认作为插入数据处理
                table_name = data.get('table_name', 'default_table')
                if 'table_name' in data:
                    data_copy = data.copy()
                    del data_copy['table_name']
                else:
                    data_copy = data
                return self.insert_data(data_copy, table_name)
                
        except Exception as e:
            return f"处理JSON数据时出错: {str(e)}"
    
    def insert_data(self, data, table_name):
        """将数据插入到数据库表中"""
        try:
            if not data:
                return "错误: 没有提供数据"

            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?'] * len(data))
            sql_insert = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(sql_insert, list(data.values()))
            conn.commit()
            conn.close()

            return f"成功插入数据到表 {table_name}"

        except Exception as e:
            if 'conn' in locals() and conn:
                conn.rollback()
                conn.close()
            return f"错误: {str(e)}"
    
    def execute_sql(self, data):
        """执行JSON中的SQL查询"""
        try:
            sql_query = data.get('sql_query')
            if not sql_query:
                return "错误: JSON中未找到'sql_query'键"

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(sql_query)

            if sql_query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                conn.close()
                return {"columns": columns, "data": result}
            else:
                conn.commit()
                conn.close()
                return "执行成功"

        except Exception as e:
            if 'conn' in locals() and conn:
                conn.close()
            return f"错误: {str(e)}"
    
    def update_user_password(self, data):
        """更新用户密码（适配新表结构）"""
        try:
            if 'username' not in data:
                return "错误: 需要提供username字段"
            if 'new_password' not in data:
                return "错误: 需要提供new_password字段"

            username = data['username']
            new_password = data['new_password']

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 在新表结构中查找用户
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

            if not user:
                conn.close()
                return f"错误: 未找到用户名为 {username} 的用户"

            # 更新密码哈希
            cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (new_password, username))
            conn.commit()
            conn.close()

            return f"用户 {username} 的密码更新成功"

        except Exception as e:
            if 'conn' in locals() and conn:
                conn.rollback()
                conn.close()
            return f"错误: {str(e)}"
    
    def update_patient_info(self, data):
        """更新患者信息（适配新表结构）"""
        try:
            if 'old_phone' not in data:
                return "错误: 需要提供old_phone字段"

            old_phone = data['old_phone']

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 通过手机号在患者表中查找患者
            cursor.execute("SELECT patient_id FROM patients WHERE phone = ?", (old_phone,))
            patient = cursor.fetchone()

            if not patient:
                conn.close()
                return f"错误: 未找到手机号为 {old_phone} 的患者"

            patient_id = patient[0]
            update_fields = []
            update_values = []

            field_mapping = {
                'new_name': 'name',
                'new_birth_date': 'birth_date',
                'new_id_card': 'id_card',
                'new_phone': 'phone',
                'new_email': 'email'
            }

            for json_key, db_field in field_mapping.items():
                if json_key in data:
                    update_fields.append(f"{db_field} = ?")
                    update_values.append(data[json_key])

            if not update_fields:
                conn.close()
                return "错误: 未提供任何需要更新的字段"

            # 如果更新手机号，也需要更新users表中的username
            if 'new_phone' in data:
                cursor.execute("UPDATE users SET username = ? WHERE user_id = ?", (data['new_phone'], patient_id))

            update_values.append(patient_id)
            sql_update = f"UPDATE patients SET {', '.join(update_fields)} WHERE patient_id = ?"

            cursor.execute(sql_update, update_values)
            conn.commit()
            conn.close()

            return f"患者ID为 {patient_id} 的患者信息更新成功"

        except Exception as e:
            if 'conn' in locals() and conn:
                conn.rollback()
                conn.close()
            return f"错误: {str(e)}"
    
    def update_doctor_info(self, data):
        """更新医生信息（适配新表结构）"""
        try:
            if 'old_employee_id' not in data:
                return "错误: 需要提供old_employee_id字段"

            old_employee_id = data['old_employee_id']

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 通过工号查找医生
            cursor.execute("SELECT doctor_id FROM doctors WHERE employee_id = ?", (old_employee_id,))
            doctor = cursor.fetchone()

            if not doctor:
                conn.close()
                return f"错误: 未找到工号为 {old_employee_id} 的医生"

            doctor_id = doctor[0]
            update_fields = []
            update_values = []

            field_mapping = {
                'new_name': 'name',
                'new_employee_id': 'employee_id',
                'new_department': 'department',
                'new_max_patients': 'max_patients',
                'new_fee': 'fee',
                'new_work_schedule': 'work_schedule',
                'new_is_available': 'is_available',
                'new_photo_path': 'photo_path'
            }

            for json_key, db_field in field_mapping.items():
                if json_key in data:
                    update_fields.append(f"{db_field} = ?")
                    update_values.append(data[json_key])

            if not update_fields:
                conn.close()
                return "错误: 未提供任何需要更新的字段"

            # 如果更新工号，也需要更新users表中的username
            if 'new_employee_id' in data:
                cursor.execute("UPDATE users SET username = ? WHERE user_id = ?", (data['new_employee_id'], doctor_id))

            update_values.append(doctor_id)
            sql_update = f"UPDATE doctors SET {', '.join(update_fields)} WHERE doctor_id = ?"

            cursor.execute(sql_update, update_values)
            conn.commit()
            conn.close()

            return f"医生ID为 {doctor_id} 的医生信息更新成功"

        except Exception as e:
            if 'conn' in locals() and conn:
                conn.rollback()
                conn.close()
            return f"错误: {str(e)}"

    def login_match(self, data):
        """根据user_id和密码验证用户"""
        try:
        # 检查参数是否有效
            if 'user_name' not in data or 'password' not in data:
                return False
            user_name = data['user_name']
            password = data['password']
            print(1)
            # 连接到数据库
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            print(2)
            # 查询用户记录
            sql_select = "SELECT password_hash FROM users WHERE username = ?"
            cursor.execute(sql_select, (user_name,))
            result = cursor.fetchone()
            print(3)
            # 关闭连接
            conn.close()

            # 检查是否找到用户记录
            if result is None:
                return "verificationFalse_bucunzai"

            # 验证密码是否匹配
            if result[0] == password:
                return "verificationSuccess"
            else:
                return "verificationFalse"

        except Exception as e:
            # 发生异常时返回False
            return "verificationFalse_yichang"
    def register_patient(self, data):
        try:
            #检查参数是否有效
            if 'name' not in data or 'password_hash' not in data:
                return {"status": "error", "message": "缺少必要参数"}

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            name = data['name']
            password_hash = data['password_hash']
            birth_date = data.get('birth_date')
            id_card = data.get('id_card')
            phone = data['phone']
            email = data.get('email')
            
            # 先插入用户表，获取自动生成的user_id
            cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                          (phone, password_hash, 'patient'))
            user_id = cursor.lastrowid  # 获取刚插入的user_id
            
            # 再插入患者详细信息表
            cursor.execute("INSERT INTO patients (patient_id, name, birth_date, id_card, phone, email) VALUES (?, ?, ?, ?, ?, ?)",
                          (user_id, name, birth_date, id_card, phone, email))
            conn.commit()
            conn.close()
            return "chenggongcharu"
        except Exception as e:
            return "charuyichang"
    def register_doctor(self, data):
        try:
            if 'name' not in data or 'password_hash' not in data:
                return {"status": "error", "message": "缺少必要参数"}
                
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            name = data['name']
            password_hash = data['password_hash']
            employee_id = data['employee_id']
            department = data.get('department')
            photo_path = data.get('photo_path')
            
            # 先插入用户表，获取自动生成的user_id
            cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                          (employee_id, password_hash, 'doctor'))
            user_id = cursor.lastrowid  # 获取刚插入的user_id
            
            # 再插入医生详细信息表
            cursor.execute("INSERT INTO doctors (doctor_id, name, employee_id, department, photo_path, max_patients) VALUES (?, ?, ?, ?, ?, ?)",
                          (user_id, name, employee_id, department, photo_path, 30))
            conn.commit()
            conn.close()
            return "chenggongcharu"
        except Exception as e:
            return "charuyichang"
    def hash_password(self,password):
        sha_signature = hashlib.sha256(password.encode()).hexdigest()
        return sha_signature
    
    def query_doctor_info(self, data):
        """根据医生姓名查询医生完整信息"""
        try:
            if 'doctor_name' not in data:
                return {
                    "status": "error",
                    "message": "缺少doctor_name参数"
                }
            
            doctor_name = data['doctor_name']
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 联合查询医生信息和用户信息
            sql_query = """
                SELECT 
                    d.doctor_id,
                    d.name,
                    d.employee_id,
                    d.department,
                    d.photo_path,
                    d.max_patients,
                    d.fee,
                    d.work_schedule,
                    d.is_available,
                    u.username,
                    u.role,
                    u.created_at
                FROM doctors d
                INNER JOIN users u ON d.doctor_id = u.user_id
                WHERE d.name = ?
            """
            
            cursor.execute(sql_query, (doctor_name,))
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return {
                    "status": "not_found",
                    "message": f"未找到姓名为 {doctor_name} 的医生"
                }
            
            # 构建返回的医生信息字典
            doctor_info = {
                "doctor_id": result[0],
                "name": result[1],
                "employee_id": result[2],
                "department": result[3],
                "photo_path": result[4],
                "max_patients": result[5],
                "fee": result[6],
                "work_schedule": result[7],
                "is_available": bool(result[8]),
                "username": result[9],
                "role": result[10],
                "created_at": result[11]
            }
            
            return {
                "status": "success",
                "message": "查询成功",
                "doctor_info": doctor_info
            }
            
        except Exception as e:
            if 'conn' in locals() and conn:
                conn.close()
            return {
                "status": "error",
                "message": f"查询医生信息时出错: {str(e)}"
            }
    
    def query_patient_info(self, data):
        """根据患者姓名查询患者完整信息"""
        try:
            if 'patient_name' not in data:
                return {
                    "status": "error",
                    "message": "缺少patient_name参数"
                }
            
            patient_name = data['patient_name']
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 联合查询患者信息和用户信息
            sql_query = """
                SELECT 
                    p.patient_id,
                    p.name,
                    p.birth_date,
                    p.id_card,
                    p.phone,
                    p.email,
                    p.created_at as patient_created_at,
                    u.username,
                    u.role,
                    u.created_at as user_created_at
                FROM patients p
                INNER JOIN users u ON p.patient_id = u.user_id
                WHERE p.name = ?
            """
            
            cursor.execute(sql_query, (patient_name,))
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return {
                    "status": "not_found",
                    "message": f"未找到姓名为 {patient_name} 的患者"
                }
            
            # 构建返回的患者信息字典
            patient_info = {
                "patient_id": result[0],
                "name": result[1],
                "birth_date": result[2],
                "id_card": result[3],
                "phone": result[4],
                "email": result[5],
                "patient_created_at": result[6],
                "username": result[7],
                "role": result[8],
                "user_created_at": result[9]
            }
            
            return {
                "status": "success",
                "message": "查询成功",
                "patient_info": patient_info
            }
            
        except Exception as e:
            if 'conn' in locals() and conn:
                conn.close()
            return {
                "status": "error",
                "message": f"查询患者信息时出错: {str(e)}"
            }
    
    def create_appointment(self, data):
        """创建预约/挂号"""
        try:
            # 验证必需参数
            required_fields = ['patient_phone', 'doctor_name', 'appointment_time']
            for field in required_fields:
                if field not in data:
                    return {
                        "status": "error",
                        "message": f"缺少必要参数: {field}"
                    }
            
            patient_phone = data['patient_phone']
            doctor_name = data['doctor_name']
            appointment_time = data['appointment_time']
            fee_paid = data.get('fee_paid', 0)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 查找患者
            cursor.execute("SELECT patient_id FROM patients WHERE phone = ?", (patient_phone,))
            patient_result = cursor.fetchone()
            if not patient_result:
                conn.close()
                return {
                    "status": "error",
                    "message": f"未找到手机号为 {patient_phone} 的患者"
                }
            patient_id = patient_result[0]
            
            # 查找医生
            cursor.execute("SELECT doctor_id FROM doctors WHERE name = ?", (doctor_name,))
            doctor_result = cursor.fetchone()
            if not doctor_result:
                conn.close()
                return {
                    "status": "error",
                    "message": f"未找到姓名为 {doctor_name} 的医生"
                }
            doctor_id = doctor_result[0]
            
            # 检查医生是否可用
            cursor.execute("SELECT is_available FROM doctors WHERE doctor_id = ?", (doctor_id,))
            doctor_available = cursor.fetchone()[0]
            if not doctor_available:
                conn.close()
                return {
                    "status": "error",
                    "message": f"医生 {doctor_name} 当前不可预约"
                }
            
            # 生成排队号码（当天该医生的预约数+1）
            cursor.execute("""
                SELECT COUNT(*) FROM appointments 
                WHERE doctor_id = ? AND DATE(appointment_time) = DATE(?)
            """, (doctor_id, appointment_time))
            queue_number = cursor.fetchone()[0] + 1
            
            # 创建预约
            cursor.execute("""
                INSERT INTO appointments (patient_id, doctor_id, appointment_time, status, fee_paid, queue_number)
                VALUES (?, ?, ?, 'pending', ?, ?)
            """, (patient_id, doctor_id, appointment_time, fee_paid, queue_number))
            
            appointment_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                "status": "success",
                "message": "预约创建成功",
                "appointment_info": {
                    "appointment_id": appointment_id,
                    "patient_phone": patient_phone,
                    "doctor_name": doctor_name,
                    "appointment_time": appointment_time,
                    "queue_number": queue_number,
                    "status": "pending",
                    "fee_paid": bool(fee_paid)
                }
            }
            
        except Exception as e:
            if 'conn' in locals() and conn:
                conn.close()
            return {
                "status": "error",
                "message": f"创建预约时出错: {str(e)}"
            }
    
    def query_appointments(self, data):
        """查询预约信息"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 根据不同条件查询
            if 'patient_phone' in data:
                # 按患者手机号查询
                patient_phone = data['patient_phone']
                cursor.execute("""
                    SELECT a.appointment_id, p.name as patient_name, p.phone,
                           d.name as doctor_name, d.department,
                           a.appointment_time, a.status, a.fee_paid, a.queue_number,
                           a.created_at
                    FROM appointments a
                    JOIN patients p ON a.patient_id = p.patient_id
                    JOIN doctors d ON a.doctor_id = d.doctor_id
                    WHERE p.phone = ?
                    ORDER BY a.appointment_time DESC
                """, (patient_phone,))
                
            elif 'doctor_name' in data:
                # 按医生姓名查询
                doctor_name = data['doctor_name']
                cursor.execute("""
                    SELECT a.appointment_id, p.name as patient_name, p.phone,
                           d.name as doctor_name, d.department,
                           a.appointment_time, a.status, a.fee_paid, a.queue_number,
                           a.created_at
                    FROM appointments a
                    JOIN patients p ON a.patient_id = p.patient_id
                    JOIN doctors d ON a.doctor_id = d.doctor_id
                    WHERE d.name = ?
                    ORDER BY a.appointment_time ASC
                """, (doctor_name,))
                
            elif 'appointment_date' in data:
                # 按预约日期查询
                appointment_date = data['appointment_date']
                cursor.execute("""
                    SELECT a.appointment_id, p.name as patient_name, p.phone,
                           d.name as doctor_name, d.department,
                           a.appointment_time, a.status, a.fee_paid, a.queue_number,
                           a.created_at
                    FROM appointments a
                    JOIN patients p ON a.patient_id = p.patient_id
                    JOIN doctors d ON a.doctor_id = d.doctor_id
                    WHERE DATE(a.appointment_time) = ?
                    ORDER BY a.appointment_time ASC
                """, (appointment_date,))
                
            else:
                # 查询所有预约
                cursor.execute("""
                    SELECT a.appointment_id, p.name as patient_name, p.phone,
                           d.name as doctor_name, d.department,
                           a.appointment_time, a.status, a.fee_paid, a.queue_number,
                           a.created_at
                    FROM appointments a
                    JOIN patients p ON a.patient_id = p.patient_id
                    JOIN doctors d ON a.doctor_id = d.doctor_id
                    ORDER BY a.appointment_time DESC
                    LIMIT 20
                """)
            
            appointments = cursor.fetchall()
            conn.close()
            
            # 格式化结果
            appointment_list = []
            for apt in appointments:
                appointment_list.append({
                    "appointment_id": apt[0],
                    "patient_name": apt[1],
                    "patient_phone": apt[2],
                    "doctor_name": apt[3],
                    "department": apt[4],
                    "appointment_time": apt[5],
                    "status": apt[6],
                    "fee_paid": bool(apt[7]),
                    "queue_number": apt[8],
                    "created_at": apt[9]
                })
            
            return {
                "status": "success",
                "message": f"查询到 {len(appointment_list)} 条预约记录",
                "appointments": appointment_list
            }
            
        except Exception as e:
            if 'conn' in locals() and conn:
                conn.close()
            return {
                "status": "error",
                "message": f"查询预约信息时出错: {str(e)}"
            }
    
    def cancel_appointment(self, data):
        """取消预约"""
        try:
            if 'appointment_id' not in data:
                return {
                    "status": "error",
                    "message": "缺少必要参数: appointment_id"
                }
            
            appointment_id = data['appointment_id']
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 检查预约是否存在
            cursor.execute("SELECT status FROM appointments WHERE appointment_id = ?", (appointment_id,))
            result = cursor.fetchone()
            if not result:
                conn.close()
                return {
                    "status": "error",
                    "message": f"未找到ID为 {appointment_id} 的预约"
                }
            
            current_status = result[0]
            if current_status == 'cancelled':
                conn.close()
                return {
                    "status": "error",
                    "message": "该预约已经被取消"
                }
            
            if current_status == 'completed':
                conn.close()
                return {
                    "status": "error",
                    "message": "已完成的预约无法取消"
                }
            
            # 更新预约状态为取消
            cursor.execute("""
                UPDATE appointments 
                SET status = 'cancelled' 
                WHERE appointment_id = ?
            """, (appointment_id,))
            
            conn.commit()
            conn.close()
            
            return {
                "status": "success",
                "message": f"预约ID {appointment_id} 已成功取消"
            }
            
        except Exception as e:
            if 'conn' in locals() and conn:
                conn.close()
            return {
                "status": "error",
                "message": f"取消预约时出错: {str(e)}"
            }
    
    def update_appointment_status(self, data):
        """更新预约状态"""
        try:
            required_fields = ['appointment_id', 'new_status']
            for field in required_fields:
                if field not in data:
                    return {
                        "status": "error",
                        "message": f"缺少必要参数: {field}"
                    }
            
            appointment_id = data['appointment_id']
            new_status = data['new_status']
            
            # 验证状态值
            valid_statuses = ['pending', 'completed', 'cancelled']
            if new_status not in valid_statuses:
                return {
                    "status": "error",
                    "message": f"无效的状态值: {new_status}，有效值: {valid_statuses}"
                }
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 检查预约是否存在
            cursor.execute("SELECT status FROM appointments WHERE appointment_id = ?", (appointment_id,))
            result = cursor.fetchone()
            if not result:
                conn.close()
                return {
                    "status": "error",
                    "message": f"未找到ID为 {appointment_id} 的预约"
                }
            
            old_status = result[0]
            
            # 更新预约状态
            cursor.execute("""
                UPDATE appointments 
                SET status = ? 
                WHERE appointment_id = ?
            """, (new_status, appointment_id))
            
            conn.commit()
            conn.close()
            
            return {
                "status": "success",
                "message": f"预约ID {appointment_id} 状态已从 '{old_status}' 更新为 '{new_status}'"
            }
            
        except Exception as e:
            if 'conn' in locals() and conn:
                conn.close()
            return {
                "status": "error",
                "message": f"更新预约状态时出错: {str(e)}"
            }

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


def get_server_pid(pid_file):
    """获取服务器PID"""
    try:
        if os.path.exists(pid_file):
            with open(pid_file, 'r') as f:
                pid = int(f.read().strip())
            # 检查进程是否存在
            os.kill(pid, 0)
            return pid
    except (OSError, ValueError):
        pass
    return None


def start_server(args):
    """启动服务器"""
    pid_file = args.pid_file
    
    # 检查服务器是否已经在运行
    existing_pid = get_server_pid(pid_file)
    if existing_pid:
        print(f"服务器已在运行 (PID: {existing_pid})")
        return False
    
    print("启动JSON数据库服务器...")
    
    if args.daemon:
        print("以守护进程模式启动...")
        daemonize()
    
    # 创建服务器实例
    server = JSONDatabaseServer(
        host=args.host, 
        port=args.port, 
        db_path=args.db_path,
        log_file=args.log_file,
        pid_file=pid_file
    )
    
    try:
        # 启动服务器
        success = server.start_server(daemon=args.daemon)
        if not success:
            return False
    except KeyboardInterrupt:
        if not args.daemon:
            print("\n收到中断信号，正在关闭服务器...")
        server.stop_server()
    except Exception as e:
        print(f"服务器运行时出错: {e}")
        return False
    
    if not args.daemon:
        print("服务器已关闭")
    
    return True


def stop_server(args):
    """停止服务器"""
    pid_file = args.pid_file
    pid = get_server_pid(pid_file)
    
    if not pid:
        print("服务器未在运行")
        return False
    
    try:
        print(f"正在停止服务器 (PID: {pid})...")
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
            print("正常关闭超时，强制终止...")
            os.kill(pid, signal.SIGKILL)
        
        print("服务器已停止")
        return True
        
    except OSError as e:
        print(f"停止服务器失败: {e}")
        return False


def restart_server(args):
    """重启服务器"""
    print("重启服务器...")
    stop_server(args)
    import time
    time.sleep(2)  # 等待2秒确保完全停止
    return start_server(args)


def status_server(args):
    """查看服务器状态"""
    pid_file = args.pid_file
    pid = get_server_pid(pid_file)
    
    if pid:
        print(f"服务器正在运行 (PID: {pid})")
        print(f"配置信息:")
        print(f"  监听地址: {args.host}:{args.port}")
        print(f"  数据库文件: {args.db_path}")
        print(f"  日志文件: {args.log_file}")
        print(f"  PID文件: {pid_file}")
        return True
    else:
        print("服务器未在运行")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='JSON数据库服务器')
    parser.add_argument('action', choices=['start', 'stop', 'restart', 'status'], 
                       help='操作: start(启动), stop(停止), restart(重启), status(状态)')
    parser.add_argument('--host', default='0.0.0.0', help='监听地址 (默认: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=55000, help='监听端口 (默认: 55000)')
    parser.add_argument('--db-path', default='/medical/MedicalSystem.db', help='数据库文件路径')
    parser.add_argument('--log-file', default='/medical/server.log', help='日志文件路径')
    parser.add_argument('--pid-file', default='/medical/server.pid', help='PID文件路径')
    parser.add_argument('--daemon', action='store_true', help='以守护进程模式运行')
    parser.add_argument('--foreground', action='store_true', help='前台运行（覆盖--daemon）')
    
    args = parser.parse_args()
    
    # 如果指定了--foreground，覆盖--daemon设置
    if args.foreground:
        args.daemon = False
    elif args.action == 'start' and not args.foreground:
        # 默认以守护进程模式启动
        args.daemon = True
    
    # 执行相应操作
    actions = {
        'start': start_server,
        'stop': stop_server,
        'restart': restart_server,
        'status': status_server
    }
    
    action_func = actions[args.action]
    success = action_func(args)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
