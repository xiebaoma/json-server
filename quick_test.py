#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速远程测试脚本
目标服务器: 8.140.225.6:55000
"""

import sys
import os
import json
import socket
import struct
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def send_json_request(host, port, data, timeout=10):
    """发送JSON请求到远程服务器"""
    try:
        # 创建socket连接
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(timeout)
        client_socket.connect((host, port))
        
        # 准备JSON数据
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        json_bytes = json_str.encode('utf-8')
        filename = "test_request.json"
        filename_bytes = filename.encode('utf-8')
        
        # 发送请求（按照协议格式）
        # 文件名长度 + 文件名 + 数据长度 + 数据
        client_socket.sendall(struct.pack("!I", len(filename_bytes)))
        client_socket.sendall(filename_bytes)
        client_socket.sendall(struct.pack("!I", len(json_bytes)))
        client_socket.sendall(json_bytes)
        
        # 接收响应
        # 响应长度
        raw_len = client_socket.recv(4)
        if not raw_len:
            return None
        response_len = struct.unpack("!I", raw_len)[0]
        
        # 响应内容
        response_content = b""
        received = 0
        while received < response_len:
            chunk = client_socket.recv(min(4096, response_len - received))
            if not chunk:
                break
            response_content += chunk
            received += len(chunk)
        
        client_socket.close()
        
        # 解析JSON响应
        response_str = response_content.decode('utf-8')
        response_data = json.loads(response_str)
        
        return response_data
        
    except Exception as e:
        print(f"请求失败: {e}")
        return None


def test_server_connection():
    """测试服务器连接"""
    print("🔗 测试服务器连接...")
    
    test_data = {"test": "connection"}
    response = send_json_request("8.140.225.6", 55000, test_data)
    
    if response:
        print("✅ 服务器连接成功")
        print(f"响应: {response}")
        return True
    else:
        print("❌ 服务器连接失败")
        return False


def test_user_login():
    """测试用户登录"""
    print("\n👤 测试用户登录...")
    
    # 测试已知用户
    login_data = {
        "login": True,
        "username": "13800138000",
        "password_hash": "hash_patient1"
    }
    
    response = send_json_request("8.140.225.6", 55000, login_data)
    
    if response:
        result = response.get('result', '')
        if result == 'verificationSuccess':
            print("✅ 登录成功")
        else:
            print(f"❌ 登录失败: {result}")
        print(f"完整响应: {response}")
    else:
        print("❌ 登录请求失败")


def test_doctor_query():
    """测试医生查询"""
    print("\n👨‍⚕️ 测试医生查询...")
    
    query_data = {
        "query_doctor_info": True,
        "doctor_name": "王医生"
    }
    
    response = send_json_request("8.140.225.6", 55000, query_data)
    
    if response:
        result = response.get('result', {})
        if result.get('status') == 'success':
            print("✅ 医生查询成功")
            doctor_info = result.get('doctor_info', {})
            print(f"医生信息: {doctor_info.get('name')} - {doctor_info.get('department')}")
        else:
            print(f"❌ 医生查询失败: {result.get('message', '未知错误')}")
    else:
        print("❌ 医生查询请求失败")


def test_sql_query():
    """测试SQL查询"""
    print("\n🗄️ 测试SQL查询...")
    
    sql_data = {
        "sql_query": "SELECT COUNT(*) as total_users FROM users"
    }
    
    response = send_json_request("8.140.225.6", 55000, sql_data)
    
    if response:
        result = response.get('result', {})
        if 'columns' in result and 'data' in result:
            print("✅ SQL查询成功")
            print(f"查询结果: {result}")
        else:
            print(f"❌ SQL查询失败: {result}")
    else:
        print("❌ SQL查询请求失败")


def test_appointment_creation():
    """测试预约创建"""
    print("\n📅 测试预约创建...")
    
    appointment_data = {
        "create_appointment": True,
        "patient_phone": "13800138000",
        "doctor_name": "王医生",
        "appointment_time": "2024-03-20 14:00:00",
        "fee_paid": 1
    }
    
    response = send_json_request("8.140.225.6", 55000, appointment_data)
    
    if response:
        result = response.get('result', {})
        if result.get('status') == 'success':
            print("✅ 预约创建成功")
            appointment_info = result.get('appointment_info', {})
            print(f"预约ID: {appointment_info.get('appointment_id')}")
            print(f"排队号: {appointment_info.get('queue_number')}")
        else:
            print(f"❌ 预约创建失败: {result.get('message', '未知错误')}")
    else:
        print("❌ 预约创建请求失败")


def main():
    """主函数"""
    print("=" * 50)
    print("医疗系统远程服务器快速测试")
    print("目标服务器: 8.140.225.6:55000")
    print("=" * 50)
    
    # 测试服务器连接
    if not test_server_connection():
        print("\n❌ 无法连接到服务器，测试终止")
        return
    
    # 运行各项测试
    test_user_login()
    test_doctor_query()
    test_sql_query()
    test_appointment_creation()
    
    print("\n" + "=" * 50)
    print("测试完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
