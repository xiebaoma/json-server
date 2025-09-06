#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试SQL查询语句
"""

import sqlite3
import json
from datetime import datetime


def test_sql_queries():
    """测试查询预约的SQL语句"""
    print("🔍 测试查询预约的SQL语句")
    print("="*50)
    
    try:
        # 连接数据库
        conn = sqlite3.connect('MedicalSystem.db')
        cursor = conn.cursor()
        
        # 1. 检查表是否存在
        print("\n📋 1. 检查表结构...")
        tables = ['appointments', 'patients', 'doctors']
        for table in tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if cursor.fetchone():
                print(f"   ✅ {table} 表存在")
                
                # 检查表中是否有数据
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"      数据条数: {count}")
            else:
                print(f"   ❌ {table} 表不存在")
        
        # 2. 测试患者查询
        print("\n📋 2. 测试按患者手机号查询...")
        patient_phone = "13800138000"
        
        try:
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
            
            results = cursor.fetchall()
            print(f"   ✅ 查询成功，返回 {len(results)} 条记录")
            
            if results:
                for i, result in enumerate(results, 1):
                    print(f"      记录{i}: ID={result[0]}, 患者={result[1]}, 医生={result[3]}")
            else:
                print("   ⚠️  没有找到匹配的预约记录")
                
        except Exception as e:
            print(f"   ❌ 按患者查询失败: {e}")
        
        # 3. 测试医生查询
        print("\n📋 3. 测试按医生姓名查询...")
        doctor_name = "王医生"
        
        try:
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
            
            results = cursor.fetchall()
            print(f"   ✅ 查询成功，返回 {len(results)} 条记录")
            
            if results:
                for i, result in enumerate(results, 1):
                    print(f"      记录{i}: ID={result[0]}, 患者={result[1]}, 时间={result[5]}")
            else:
                print("   ⚠️  没有找到匹配的预约记录")
                
        except Exception as e:
            print(f"   ❌ 按医生查询失败: {e}")
        
        # 4. 测试日期查询（可能的问题点）
        print("\n📋 4. 测试按日期查询...")
        appointment_date = "2025-09-03"  # 明天的日期
        
        try:
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
            
            results = cursor.fetchall()
            print(f"   ✅ DATE函数查询成功，返回 {len(results)} 条记录")
            
        except Exception as e:
            print(f"   ❌ DATE函数查询失败: {e}")
            
            # 尝试替代的日期查询方法
            print("   🔄 尝试替代的日期查询方法...")
            try:
                cursor.execute("""
                    SELECT a.appointment_id, p.name as patient_name, p.phone,
                           d.name as doctor_name, d.department,
                           a.appointment_time, a.status, a.fee_paid, a.queue_number,
                           a.created_at
                    FROM appointments a
                    JOIN patients p ON a.patient_id = p.patient_id
                    JOIN doctors d ON a.doctor_id = d.doctor_id
                    WHERE a.appointment_time LIKE ?
                    ORDER BY a.appointment_time ASC
                """, (f"{appointment_date}%",))
                
                results = cursor.fetchall()
                print(f"   ✅ LIKE查询成功，返回 {len(results)} 条记录")
                
            except Exception as e2:
                print(f"   ❌ LIKE查询也失败: {e2}")
        
        # 5. 测试所有预约查询
        print("\n📋 5. 测试查询所有预约...")
        try:
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
            
            results = cursor.fetchall()
            print(f"   ✅ 查询所有预约成功，返回 {len(results)} 条记录")
            
        except Exception as e:
            print(f"   ❌ 查询所有预约失败: {e}")
        
        # 6. 检查表关联是否正确
        print("\n📋 6. 检查表关联...")
        try:
            cursor.execute("""
                SELECT COUNT(*) as total_appointments,
                       COUNT(p.patient_id) as valid_patients,
                       COUNT(d.doctor_id) as valid_doctors
                FROM appointments a
                LEFT JOIN patients p ON a.patient_id = p.patient_id
                LEFT JOIN doctors d ON a.doctor_id = d.doctor_id
            """)
            
            result = cursor.fetchone()
            print(f"   总预约数: {result[0]}")
            print(f"   有效患者关联: {result[1]}")
            print(f"   有效医生关联: {result[2]}")
            
            if result[0] != result[1]:
                print("   ⚠️  有预约记录的患者ID无法关联到患者表")
            if result[0] != result[2]:
                print("   ⚠️  有预约记录的医生ID无法关联到医生表")
            if result[0] == result[1] == result[2]:
                print("   ✅ 表关联正确")
                
        except Exception as e:
            print(f"   ❌ 检查表关联失败: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        print("\n🔧 可能的原因:")
        print("   1. 数据库文件不存在")
        print("   2. 数据库文件权限问题") 
        print("   3. 需要重置数据库")


if __name__ == "__main__":
    test_sql_queries()

