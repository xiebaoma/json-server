#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试客户端程序
用于测试整合的JSON数据库服务器
"""

import socket
import struct
import json
import os
import tempfile


class TestClient:
    def __init__(self, host='8.140.225.6', port=55000):
        self.host = host
        self.port = port
    
    def send_json_data(self, json_data):
        """发送JSON数据到服务器并接收响应"""
        try:
            # 连接到服务器
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((self.host, self.port))
            print(f"已连接到服务器 {self.host}:{self.port}")
            
            # 将JSON数据转换为字节
            json_str = json.dumps(json_data, ensure_ascii=False, indent=2)
            json_bytes = json_str.encode('utf-8')
            
            # 创建临时文件名
            filename = "test_data.json"
            filename_bytes = filename.encode('utf-8')
            
            print(f"发送JSON数据: {json_str}")
            
            # 发送文件名长度
            sock.sendall(struct.pack("!I", len(filename_bytes)))
            # 发送文件名
            sock.sendall(filename_bytes)
            # 发送文件大小
            sock.sendall(struct.pack("!I", len(json_bytes)))
            # 发送文件内容
            sock.sendall(json_bytes)
            
            print("JSON数据发送完成，等待服务器响应...")
            
            # 接收响应长度
            raw_len = sock.recv(4)
            if not raw_len:
                print("服务器未返回响应")
                return None
            
            response_len = struct.unpack("!I", raw_len)[0]
            print(f"响应长度: {response_len} 字节")
            
            # 接收响应内容
            response_data = b""
            received = 0
            while received < response_len:
                chunk = sock.recv(min(4096, response_len - received))
                if not chunk:
                    break
                response_data += chunk
                received += len(chunk)
            
            # 解析响应
            response_str = response_data.decode('utf-8')
            response_json = json.loads(response_str)
            
            print("服务器响应:")
            print(json.dumps(response_json, ensure_ascii=False, indent=2))
            
            sock.close()
            return response_json
            
        except Exception as e:
            print(f"发送数据时出错: {e}")
            if 'sock' in locals():
                sock.close()
            return None


def test_insert_data():
    """测试数据插入功能"""
    print("\n=== 测试数据插入功能 ===")
    client = TestClient()
    
    test_data = {
        "table_name": "students",
        "name": "张三",
        "age": 20,
        "student_id": 12345
    }
    
    response = client.send_json_data(test_data)
    return response


def test_sql_query():
    """测试SQL查询功能（适配新表结构）"""
    print("\n=== 测试SQL查询功能 ===")
    client = TestClient()
    
    test_data = {
        "sql_query": "SELECT u.username, u.role, p.name FROM users u LEFT JOIN patients p ON u.user_id = p.patient_id WHERE u.role = 'patient'"
    }
    
    response = client.send_json_data(test_data)
    return response


def test_medical_query():
    """测试医疗系统查询功能"""
    print("\n=== 测试医疗系统查询功能 ===")
    client = TestClient()
    
    test_data = {
        "sql_query": """
        SELECT a.appointment_id, p.name AS patient_name, d.name AS doctor_name, 
               a.appointment_time, a.status 
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        """
    }
    
    response = client.send_json_data(test_data)
    return response


def test_attendance_query():
    """测试打卡记录查询功能"""
    print("\n=== 测试打卡记录查询功能 ===")
    client = TestClient()
    
    test_data = {
        "sql_query": """
        SELECT d.name, d.employee_id, a.check_in_time, a.check_out_time, a.status
        FROM attendance a
        JOIN doctors d ON a.doctor_id = d.doctor_id
        ORDER BY a.check_in_time DESC
        """
    }
    
    response = client.send_json_data(test_data)
    return response


def test_user_password_update():
    """测试用户密码更新功能（适配新表结构）"""
    print("\n=== 测试用户密码更新功能 ===")
    client = TestClient()
    
    test_data = {
        "reset_password": True,
        "user_name": "13800138000",  # 使用示例数据中的患者手机号
        "new_password": "new_password_123"
    }
    
    response = client.send_json_data(test_data)
    return response


def test_patient_info_update():
    """测试患者信息更新功能（适配新表结构）"""
    print("\n=== 测试患者信息更新功能 ===")
    client = TestClient()
    
    test_data = {
        "reset_patient_information": True,
        "old_phone": "13800138000",  # 使用示例数据中的张三的手机号
        "new_name": "张三（已更新）",
        "new_email": "zhangsan_updated@example.com"
    }
    
    response = client.send_json_data(test_data)
    return response


def test_doctor_info_update():
    """测试医生信息更新功能（适配新表结构）"""
    print("\n=== 测试医生信息更新功能 ===")
    client = TestClient()
    
    test_data = {
        "reset_doctor_information": True,
        "old_employee_id": "DOC001",  # 使用示例数据中的王医生工号
        "new_name": "王医生（已更新）",
        "new_department": "心内科",
        "new_fee": 60.0
    }
    
    response = client.send_json_data(test_data)
    return response


def main():
    """主测试函数"""
    print("JSON数据库服务器测试客户端")
    print("确保服务器正在运行在 localhost:55000")
    
    # 执行各种测试
    tests = [
        #test_insert_data,
        #test_sql_query,
        #test_medical_query,
        #test_attendance_query,
        #test_user_password_update,
        test_patient_info_update,
        test_doctor_info_update
    ]
    
    for test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"✓ {test_func.__name__} 测试完成")
            else:
                print(f"✗ {test_func.__name__} 测试失败")
        except Exception as e:
            print(f"✗ {test_func.__name__} 测试异常: {e}")
        
        input("\n按回车键继续下一个测试...")
    
    print("\n所有测试完成!")


if __name__ == "__main__":
    main()
