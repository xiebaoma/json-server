#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新添加的查询医生和患者信息功能
"""

import json
import socket
import struct


def send_json_data(host, port, data):
    """发送JSON数据到服务器并接收响应"""
    try:
        # 创建socket连接
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        
        # 将数据转换为JSON字符串
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        json_bytes = json_str.encode('utf-8')
        
        # 发送文件名长度和文件名
        filename = "test_query.json"
        filename_bytes = filename.encode('utf-8')
        client_socket.sendall(struct.pack("!I", len(filename_bytes)))
        client_socket.sendall(filename_bytes)
        
        # 发送文件大小和文件内容
        client_socket.sendall(struct.pack("!I", len(json_bytes)))
        client_socket.sendall(json_bytes)
        
        # 接收响应长度
        raw_response_len = client_socket.recv(4)
        if not raw_response_len:
            return None
        response_len = struct.unpack("!I", raw_response_len)[0]
        
        # 接收响应内容
        response_data = b""
        while len(response_data) < response_len:
            chunk = client_socket.recv(response_len - len(response_data))
            if not chunk:
                break
            response_data += chunk
        
        # 解析JSON响应
        response_str = response_data.decode('utf-8')
        response = json.loads(response_str)
        
        client_socket.close()
        return response
        
    except Exception as e:
        print(f"发送数据时出错: {e}")
        return None


def test_query_doctor():
    """测试查询医生信息功能"""
    print("=== 测试查询医生信息功能 ===")
    
    # 测试存在的医生
    test_data = {
        "query_doctor_info": True,
        "doctor_name": "王医生"
    }
    
    print("发送的测试数据:")
    print(json.dumps(test_data, ensure_ascii=False, indent=2))
    print()
    
    response = send_json_data('8.140.225.6', 55000, test_data)
    if response:
        print("服务器响应:")
        print(json.dumps(response, ensure_ascii=False, indent=2))
    else:
        print("未收到服务器响应")
    
    print()
    
    # 测试不存在的医生
    test_data2 = {
        "query_doctor_info": True,
        "doctor_name": "不存在的医生"
    }
    
    print("测试不存在的医生:")
    print("发送的测试数据:")
    print(json.dumps(test_data2, ensure_ascii=False, indent=2))
    print()
    
    response2 = send_json_data('8.140.225.6', 55000, test_data2)
    if response2:
        print("服务器响应:")
        print(json.dumps(response2, ensure_ascii=False, indent=2))
    else:
        print("未收到服务器响应")
    
    print("\n" + "="*60 + "\n")


def test_query_patient():
    """测试查询患者信息功能"""
    print("=== 测试查询患者信息功能 ===")
    
    # 测试存在的患者
    test_data = {
        "query_patient_info": True,
        "patient_name": "李四"
    }
    
    print("发送的测试数据:")
    print(json.dumps(test_data, ensure_ascii=False, indent=2))
    print()
    
    response = send_json_data('8.140.225.6', 55000, test_data)
    if response:
        print("服务器响应:")
        print(json.dumps(response, ensure_ascii=False, indent=2))
    else:
        print("未收到服务器响应")
    
    print()
    
    # 测试不存在的患者
    test_data2 = {
        "query_patient_info": True,
        "patient_name": "不存在的患者"
    }
    
    print("测试不存在的患者:")
    print("发送的测试数据:")
    print(json.dumps(test_data2, ensure_ascii=False, indent=2))
    print()
    
    response2 = send_json_data('8.140.225.6', 55000, test_data2)
    if response2:
        print("服务器响应:")
        print(json.dumps(response2, ensure_ascii=False, indent=2))
    else:
        print("未收到服务器响应")
    
    print("\n" + "="*60 + "\n")


def test_missing_parameters():
    """测试缺少参数的情况"""
    print("=== 测试参数验证 ===")
    
    # 测试缺少医生姓名参数
    test_data1 = {
        "query_doctor_info": True
        # 缺少doctor_name参数
    }
    
    print("测试缺少医生姓名参数:")
    print("发送的测试数据:")
    print(json.dumps(test_data1, ensure_ascii=False, indent=2))
    print()
    
    response1 = send_json_data('8.140.225.6', 55000, test_data1)
    if response1:
        print("服务器响应:")
        print(json.dumps(response1, ensure_ascii=False, indent=2))
    else:
        print("未收到服务器响应")
    
    print()
    
    # 测试缺少患者姓名参数
    test_data2 = {
        "query_patient_info": True
        # 缺少patient_name参数
    }
    
    print("测试缺少患者姓名参数:")
    print("发送的测试数据:")
    print(json.dumps(test_data2, ensure_ascii=False, indent=2))
    print()
    
    response2 = send_json_data('8.140.225.6', 55000, test_data2)
    if response2:
        print("服务器响应:")
        print(json.dumps(response2, ensure_ascii=False, indent=2))
    else:
        print("未收到服务器响应")
    
    print("\n" + "="*60 + "\n")


def main():
    """主测试函数"""
    print("开始测试新添加的查询功能...")
    print("注意：请确保服务器已经启动并监听在8.140.225.6:55000端口\n")
    
    try:
        # 测试查询医生信息
        test_query_doctor()
        
        # 测试查询患者信息
        test_query_patient()
        
        # 测试参数验证
        test_missing_parameters()
        
        print("所有测试已完成！")
        
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"测试过程中出错: {e}")


if __name__ == "__main__":
    main()