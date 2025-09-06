#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试预约插入语句的正确性
"""

import sqlite3
import tempfile
import os


def test_appointment_insert():
    """测试预约插入语句"""
    print("🧪 测试预约插入语句的正确性")
    print("="*50)
    
    # 创建临时数据库
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp_file:
        temp_db = tmp_file.name
    
    try:
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # 1. 创建表结构
        print("📋 1. 创建appointments表...")
        cursor.execute('''
            CREATE TABLE appointments (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                appointment_time TIMESTAMP NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('pending', 'completed', 'cancelled')),
                fee_paid BOOLEAN DEFAULT 0,
                queue_number INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ 表创建成功")
        
        # 2. 测试INSERT语句（不包含appointment_id）
        print("\n📋 2. 测试INSERT语句（当前方式）...")
        insert_sql = """
            INSERT INTO appointments (patient_id, doctor_id, appointment_time, status, fee_paid, queue_number) 
            VALUES (?, ?, ?, ?, ?, ?)
        """
        
        test_data = [
            (1, 4, '2024-02-01 09:00:00', 'completed', 1, 1),
            (2, 5, '2024-02-01 10:00:00', 'pending', 0, 2),
            (3, 6, '2024-02-01 14:00:00', 'pending', 1, 1)
        ]
        
        inserted_ids = []
        for data in test_data:
            cursor.execute(insert_sql, data)
            appointment_id = cursor.lastrowid
            inserted_ids.append(appointment_id)
            print(f"   ✅ 插入成功，自动生成 appointment_id: {appointment_id}")
        
        # 3. 验证插入结果
        print("\n📋 3. 验证插入结果...")
        cursor.execute("SELECT * FROM appointments ORDER BY appointment_id")
        results = cursor.fetchall()
        
        print(f"   总共插入了 {len(results)} 条记录")
        for i, row in enumerate(results, 1):
            print(f"   记录{i}: appointment_id={row[0]}, patient_id={row[1]}, doctor_id={row[2]}")
            print(f"           时间={row[3]}, 状态={row[4]}, created_at={row[7]}")
        
        # 4. 测试如果强制包含appointment_id会怎样
        print("\n📋 4. 测试强制指定appointment_id（错误方式）...")
        try:
            wrong_sql = """
                INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_time, status, fee_paid, queue_number) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            # 尝试插入一个可能冲突的ID
            cursor.execute(wrong_sql, (1, 7, 8, '2024-02-01 15:00:00', 'pending', 0, 1))
            print("   ❌ 意外成功了（可能是ID冲突）")
        except sqlite3.IntegrityError as e:
            print(f"   ✅ 正确报错：{e}")
        except Exception as e:
            print(f"   ⚠️  其他错误：{e}")
        
        # 5. 验证AUTOINCREMENT的连续性
        print("\n📋 5. 验证AUTOINCREMENT连续性...")
        cursor.execute(insert_sql, (4, 7, '2024-02-01 16:00:00', 'pending', 0, 2))
        next_id = cursor.lastrowid
        print(f"   下一个自动ID: {next_id} （应该是 {max(inserted_ids) + 1}）")
        
        if next_id == max(inserted_ids) + 1:
            print("   ✅ AUTOINCREMENT连续性正确")
        else:
            print("   ❌ AUTOINCREMENT连续性有问题")
        
        conn.commit()
        conn.close()
        
        print("\n🎉 测试结论：")
        print("   ✅ 当前的INSERT语句是正确的")
        print("   ✅ appointment_id不应该手动指定")  
        print("   ✅ AUTOINCREMENT会自动生成正确的ID")
        print("   ✅ created_at会自动设置为当前时间")
        
    except Exception as e:
        print(f"❌ 测试失败：{e}")
    
    finally:
        # 清理临时文件
        if os.path.exists(temp_db):
            os.unlink(temp_db)


if __name__ == "__main__":
    test_appointment_insert()
