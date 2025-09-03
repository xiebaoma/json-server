#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
预约管理服务
处理预约创建、查询、取消、状态更新等功能
"""

import sqlite3
import logging
from typing import Dict, Any, List


class AppointmentService:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
    
    def create_appointment(self, data: Dict[str, Any]) -> Dict[str, Any]:
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
            self.logger.error(f"创建预约异常: {e}")
            if 'conn' in locals():
                conn.close()
            return {
                "status": "error",
                "message": f"创建预约时出错: {str(e)}"
            }
    
    def query_appointments(self, data: Dict[str, Any]) -> Dict[str, Any]:
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
            self.logger.error(f"查询预约异常: {e}")
            if 'conn' in locals():
                conn.close()
            return {
                "status": "error",
                "message": f"查询预约信息时出错: {str(e)}"
            }
    
    def cancel_appointment(self, data: Dict[str, Any]) -> Dict[str, Any]:
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
            self.logger.error(f"取消预约异常: {e}")
            if 'conn' in locals():
                conn.close()
            return {
                "status": "error",
                "message": f"取消预约时出错: {str(e)}"
            }
    
    def update_appointment_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
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
            self.logger.error(f"更新预约状态异常: {e}")
            if 'conn' in locals():
                conn.close()
            return {
                "status": "error",
                "message": f"更新预约状态时出错: {str(e)}"
            }
