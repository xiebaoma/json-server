#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试客户端
用于测试医疗系统服务器的各种功能
"""

import sys
import os
import json

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from network.communication import JSONProtocolClient


def test_login():
    """测试登录功能"""
    client = JSONProtocolClient()
    
    # 测试登录
    login_data = {
        "login": True,
        "user_name": "13800138000",
        "password": "hash_patient1"
    }
    
    print("测试登录功能...")
    response = client.send_json_data(login_data)
    if response:
        print(f"登录响应: {response}")
    else:
        print("登录测试失败 - 无法连接到服务器")
    
    return response


def test_query_doctor():
    """测试查询医生信息"""
    client = JSONProtocolClient()
    
    # 测试查询医生信息
    query_data = {
        "query_doctor_info": True,
        "doctor_name": "王医生"
    }
    
    print("\n测试查询医生信息...")
    response = client.send_json_data(query_data)
    if response:
        print(f"查询医生响应: {json.dumps(response, ensure_ascii=False, indent=2)}")
    else:
        print("查询医生测试失败 - 无法连接到服务器")
    
    return response


def test_create_appointment():
    """测试创建预约"""
    client = JSONProtocolClient()
    
    # 测试创建预约
    appointment_data = {
        "create_appointment": True,
        "patient_phone": "13800138000",
        "doctor_name": "王医生",
        "appointment_time": "2024-03-01 10:00:00",
        "fee_paid": 1
    }
    
    print("\n测试创建预约...")
    response = client.send_json_data(appointment_data)
    if response:
        print(f"创建预约响应: {json.dumps(response, ensure_ascii=False, indent=2)}")
    else:
        print("创建预约测试失败 - 无法连接到服务器")
    
    return response


def test_sql_query():
    """测试SQL查询"""
    client = JSONProtocolClient()
    
    # 测试SQL查询
    sql_data = {
        "sql_query": "SELECT COUNT(*) as total_users FROM users"
    }
    
    print("\n测试SQL查询...")
    response = client.send_json_data(sql_data)
    if response:
        print(f"SQL查询响应: {json.dumps(response, ensure_ascii=False, indent=2)}")
    else:
        print("SQL查询测试失败 - 无法连接到服务器")
    
    return response


def main():
    """主测试函数"""
    print("医疗系统服务器测试客户端")
    print("=" * 40)
    
    # 运行各种测试
    try:
        test_login()
        test_query_doctor()
        test_create_appointment()
        test_sql_query()
        
        print("\n" + "=" * 40)
        print("测试完成！")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        print("请确保服务器正在运行：python server.py start --foreground")


if __name__ == "__main__":
    main()
