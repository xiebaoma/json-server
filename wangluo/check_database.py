#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库查看工具
用于查看服务器数据库的内容和状态
"""

import sqlite3
import json
import sys


def check_database(db_path='database.db'):
    """检查数据库内容"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 获取所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"数据库文件: {db_path}")
        print(f"发现 {len(tables)} 个表")
        print("=" * 50)
        
        for (table_name,) in tables:
            print(f"\n表名: {table_name}")
            print("-" * 30)
            
            # 获取表结构
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print("表结构:")
            for col in columns:
                print(f"  {col[1]} ({col[2]})")
            
            # 获取记录数量
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"记录数量: {count}")
            
            # 显示前5条记录
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                records = cursor.fetchall()
                
                print("前5条记录:")
                column_names = [desc[1] for desc in columns]
                
                for i, record in enumerate(records, 1):
                    print(f"  记录 {i}:")
                    for j, value in enumerate(record):
                        print(f"    {column_names[j]}: {value}")
            
            print()
        
        conn.close()
        
    except Exception as e:
        print(f"检查数据库时出错: {e}")


def test_operations(db_path='database.db'):
    """测试数据库操作（适配新表结构）"""
    print("\n" + "=" * 50)
    print("测试数据库操作")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 测试用户查询
        print("\n1. 测试用户表查询:")
        cursor.execute("SELECT user_id, username, role FROM users")
        users = cursor.fetchall()
        for user_id, username, role in users:
            print(f"  用户ID: {user_id}, 用户名: {username}, 角色: {role}")
        
        # 测试患者查询（关联查询）
        print("\n2. 测试患者信息查询:")
        cursor.execute("""
            SELECT p.name, p.phone, p.email, u.username
            FROM patients p 
            JOIN users u ON p.patient_id = u.user_id
        """)
        patients = cursor.fetchall()
        for name, phone, email, username in patients:
            print(f"  患者: {name}, 电话: {phone}, 邮箱: {email}, 用户名: {username}")
        
        # 测试医生查询（关联查询）
        print("\n3. 测试医生信息查询:")
        cursor.execute("""
            SELECT d.name, d.employee_id, d.department, d.fee, u.username
            FROM doctors d
            JOIN users u ON d.doctor_id = u.user_id
        """)
        doctors = cursor.fetchall()
        for name, emp_id, dept, fee, username in doctors:
            print(f"  医生: {name}, 工号: {emp_id}, 科室: {dept}, 费用: {fee}, 用户名: {username}")
        
        # 测试预约查询
        print("\n4. 测试预约信息查询:")
        cursor.execute("""
            SELECT a.appointment_id, p.name AS patient_name, d.name AS doctor_name, 
                   a.appointment_time, a.status, a.fee_paid
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
        """)
        appointments = cursor.fetchall()
        for apt_id, p_name, d_name, apt_time, status, fee_paid in appointments:
            print(f"  预约ID: {apt_id}, 患者: {p_name}, 医生: {d_name}, 时间: {apt_time}, 状态: {status}, 已付费: {fee_paid}")
        
        # 测试病历查询
        print("\n5. 测试病历信息查询:")
        cursor.execute("""
            SELECT m.record_id, p.name AS patient_name, d.name AS doctor_name,
                   m.diagnosis, m.symptoms, m.visit_time
            FROM medical_records m
            JOIN patients p ON m.patient_id = p.patient_id
            JOIN doctors d ON m.doctor_id = d.doctor_id
        """)
        records = cursor.fetchall()
        for rec_id, p_name, d_name, diagnosis, symptoms, visit_time in records:
            print(f"  病历ID: {rec_id}, 患者: {p_name}, 医生: {d_name}, 诊断: {diagnosis}, 症状: {symptoms}, 时间: {visit_time}")
        
        conn.close()
        
    except Exception as e:
        print(f"测试操作时出错: {e}")


def reset_database(db_path='database.db'):
    """重置数据库（删除所有表重新创建）"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 获取所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        # 删除所有表
        for (table_name,) in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f"已删除表: {table_name}")
        
        conn.commit()
        conn.close()
        
        print("数据库已重置，请重新启动服务器以重新初始化数据库")
        
    except Exception as e:
        print(f"重置数据库时出错: {e}")


def main():
    """主函数"""
    db_path = 'database.db'
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--reset':
            print("重置数据库...")
            reset_database(db_path)
            return
        elif sys.argv[1] == '--test':
            check_database(db_path)
            test_operations(db_path)
            return
        else:
            db_path = sys.argv[1]
    
    print("数据库查看工具")
    print("使用方法:")
    print("  python check_database.py           # 查看默认数据库")
    print("  python check_database.py <db_path> # 查看指定数据库")
    print("  python check_database.py --reset   # 重置数据库")
    print("  python check_database.py --test    # 查看并测试数据库")
    print()
    
    check_database(db_path)


if __name__ == "__main__":
    main()
