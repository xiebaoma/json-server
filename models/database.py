#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库模型和操作
包含医疗系统的所有表结构定义和基础数据库操作
"""

import sqlite3
import logging
import os
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_path='/medical/MedicalSystem.db'):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.init_database()
    
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
    
    def execute_sql(self, sql_query):
        """执行SQL查询"""
        try:
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
            raise e
    
    def insert_data(self, data, table_name):
        """将数据插入到数据库表中"""
        try:
            if not data:
                raise ValueError("没有提供数据")

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
            raise e
