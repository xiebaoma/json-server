#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试挂号功能
"""

import json
import socket
import struct
from datetime import datetime, timedelta


def send_json_data(host, port, data):
    """发送JSON数据并显示详细调试信息"""
    try:
        print("🔗 正在连接服务器...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print("✅ 服务器连接成功")
        
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        json_bytes = json_str.encode('utf-8')
        
        print("📤 发送的数据:")
        print(json_str)
        print(f"数据大小: {len(json_bytes)} 字节")
        
        filename = "debug.json"
        filename_bytes = filename.encode('utf-8')
        client_socket.sendall(struct.pack("!I", len(filename_bytes)))
        client_socket.sendall(filename_bytes)
        
        client_socket.sendall(struct.pack("!I", len(json_bytes)))
        client_socket.sendall(json_bytes)
        
        print("📤 数据发送完成，等待响应...")
        
        raw_response_len = client_socket.recv(4)
        if not raw_response_len:
            print("❌ 未收到响应长度")
            return None
            
        response_len = struct.unpack("!I", raw_response_len)[0]
        print(f"📥 响应长度: {response_len} 字节")
        
        response_data = b""
        while len(response_data) < response_len:
            chunk = client_socket.recv(response_len - len(response_data))
            if not chunk:
                break
            response_data += chunk
        
        print(f"📥 实际接收: {len(response_data)} 字节")
        
        response_str = response_data.decode('utf-8')
        print("📥 原始响应内容:")
        print(response_str)
        print()
        
        response = json.loads(response_str)
        
        client_socket.close()
        return response
        
    except Exception as e:
        print(f"❌ 连接或数据传输错误: {e}")
        return None


def test_server_connection():
    """测试服务器连接"""
    print("=== 🔍 服务器连接测试 ===")
    
    # 简单的查询测试
    data = {
        "query_patient_info": True,
        "patient_name": "张三"
    }
    
    response = send_json_data('8.140.225.6', 55000, data)
    if response:
        print("✅ 服务器响应正常")
        print("响应结构分析:")
        print(f"- status: {response.get('status')}")
        print(f"- timestamp: {response.get('timestamp')}")
        print(f"- result类型: {type(response.get('result'))}")
        if 'result' in response:
            result = response['result']
            print(f"- result内容: {result}")
        return True
    else:
        print("❌ 服务器连接失败")
        return False


def test_appointment_creation():
    """测试挂号创建功能"""
    print("\n=== 📅 挂号创建测试 ===")
    
    tomorrow = datetime.now() + timedelta(days=1)
    appointment_time = tomorrow.replace(hour=9, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")
    
    data = {
        "create_appointment": True,
        "patient_phone": "13800138000",
        "doctor_name": "王医生",
        "appointment_time": appointment_time,
        "fee_paid": 1
    }
    
    print("📋 请求参数:")
    print(f"- 患者手机: {data['patient_phone']}")
    print(f"- 医生姓名: {data['doctor_name']}")
    print(f"- 预约时间: {data['appointment_time']}")
    print()
    
    response = send_json_data('8.140.225.6', 55000, data)
    
    if response:
        print("🔍 响应结构详细分析:")
        print(f"✓ 外层status: {response.get('status')}")
        print(f"✓ 外层timestamp: {response.get('timestamp')}")
        
        if 'result' in response:
            result = response.get('result')
            print(f"✓ result类型: {type(result)}")
            print(f"✓ result内容: {result}")
            
            if isinstance(result, dict):
                print("📋 result字典结构:")
                for key, value in result.items():
                    print(f"  - {key}: {value} ({type(value)})")
                    
                if 'appointment_info' in result:
                    apt_info = result['appointment_info']
                    print("📋 appointment_info详情:")
                    for key, value in apt_info.items():
                        print(f"  - {key}: {value}")
            elif isinstance(result, str):
                print(f"✓ result是字符串: {result}")
        else:
            print("❌ 响应中没有result字段")
            
        return response
    else:
        print("❌ 无响应")
        return None


def main():
    """主函数"""
    print("🔧 挂号功能调试工具")
    print("="*50)
    
    # 1. 测试服务器连接
    if not test_server_connection():
        print("\n❌ 服务器连接失败，请检查：")
        print("1. 服务器是否启动: python integrated_server_loginmatchAdd.py status")
        print("2. 服务器是否监听正确端口: 8.140.225.6:55000")
        print("3. 是否需要重启服务器加载新代码: python integrated_server_loginmatchAdd.py restart")
        return
    
    # 2. 测试挂号功能
    print("\n" + "="*50)
    test_appointment_creation()


if __name__ == "__main__":
    main()
