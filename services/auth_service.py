#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户认证服务
处理用户登录、注册、密码重置、信息更新等功能
"""

import sqlite3
import hashlib
import logging
from typing import Dict, Any


class AuthService:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
    
    def hash_password(self, password: str) -> str:
        """哈希密码"""
        sha_signature = hashlib.sha256(password.encode()).hexdigest()
        return sha_signature
    
    def login_match(self, data: Dict[str, Any]) -> str:
        """根据用户名和密码验证用户"""
        try:
            # 检查参数是否有效
            if 'user_name' not in data or 'password' not in data:
                return "verificationFalse"
            
            user_name = data['user_name']
            password = data['password']
            
            # 连接到数据库
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 查询用户记录
            sql_select = "SELECT password_hash FROM users WHERE username = ?"
            cursor.execute(sql_select, (user_name,))
            result = cursor.fetchone()
            
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
            self.logger.error(f"登录验证异常: {e}")
            return "verificationFalse_yichang"
    
    def register_patient(self, data: Dict[str, Any]) -> str:
        """注册患者"""
        try:
            # 检查参数是否有效
            if 'name' not in data or 'password_hash' not in data or 'phone' not in data:
                return "charuyichang"

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            name = data['name']
            password_hash = data['password_hash']
            birth_date = data.get('birth_date')
            id_card = data.get('id_card')
            phone = data['phone']
            email = data.get('email')
            
            # 检查手机号是否已存在
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (phone,))
            if cursor.fetchone()[0] > 0:
                conn.close()
                return "shoujihaoyicunzai"
            
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
            self.logger.error(f"患者注册异常: {e}")
            if 'conn' in locals():
                conn.rollback()
                conn.close()
            return "charuyichang"
    
    def register_doctor(self, data: Dict[str, Any]) -> str:
        """注册医生"""
        try:
            if 'name' not in data or 'password_hash' not in data or 'employee_id' not in data:
                return "charuyichang"
                
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            name = data['name']
            password_hash = data['password_hash']
            employee_id = data['employee_id']
            department = data.get('department')
            photo_path = data.get('photo_path')
            
            # 检查工号是否已存在
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (employee_id,))
            if cursor.fetchone()[0] > 0:
                conn.close()
                return "gonghaoyicunzai"
            
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
            self.logger.error(f"医生注册异常: {e}")
            if 'conn' in locals():
                conn.rollback()
                conn.close()
            return "charuyichang"
    
    def update_user_password(self, data: Dict[str, Any]) -> str:
        """更新用户密码"""
        try:
            if 'username' not in data or 'new_password' not in data:
                return "错误: 需要提供username和new_password字段"

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
            self.logger.error(f"更新密码异常: {e}")
            if 'conn' in locals():
                conn.rollback()
                conn.close()
            return f"错误: {str(e)}"
    
    def update_patient_info(self, data: Dict[str, Any]) -> str:
        """更新患者信息"""
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
            self.logger.error(f"更新患者信息异常: {e}")
            if 'conn' in locals():
                conn.rollback()
                conn.close()
            return f"错误: {str(e)}"
    
    def update_doctor_info(self, data: Dict[str, Any]) -> str:
        """更新医生信息"""
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
            self.logger.error(f"更新医生信息异常: {e}")
            if 'conn' in locals():
                conn.rollback()
                conn.close()
            return f"错误: {str(e)}"
    
    def query_doctor_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
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
            self.logger.error(f"查询医生信息异常: {e}")
            if 'conn' in locals():
                conn.close()
            return {
                "status": "error",
                "message": f"查询医生信息时出错: {str(e)}"
            }
    
    def query_patient_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
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
            self.logger.error(f"查询患者信息异常: {e}")
            if 'conn' in locals():
                conn.close()
            return {
                "status": "error",
                "message": f"查询患者信息时出错: {str(e)}"
            }
