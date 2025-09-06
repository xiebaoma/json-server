#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证服务器是否已更新挂号功能
"""

import json
import socket
import struct
from datetime import datetime, timedelta


def send_json_data(host, port, data):
    """发送JSON数据"""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        json_bytes = json_str.encode('utf-8')
        
        filename = "verify.json"
        filename_bytes = filename.encode('utf-8')
        client_socket.sendall(struct.pack("!I", len(filename_bytes)))
        client_socket.sendall(filename_bytes)
        
        client_socket.sendall(struct.pack("!I", len(json_bytes)))
        client_socket.sendall(json_bytes)
        
        raw_response_len = client_socket.recv(4)
        if not raw_response_len:
            return None
        response_len = struct.unpack("!I", raw_response_len)[0]
        
        response_data = b""
        while len(response_data) < response_len:
            chunk = client_socket.recv(response_len - len(response_data))
            if not chunk:
                break
            response_data += chunk
        
        response_str = response_data.decode('utf-8')
        response = json.loads(response_str)
        
        client_socket.close()
        return response
        
    except Exception as e:
        print(f"❌ 连接错误: {e}")
        return None


def main():
    """验证服务器功能"""
    print("🔍 验证服务器挂号功能是否已更新")
    print("="*50)
    
    tomorrow = datetime.now() + timedelta(days=1)
    appointment_time = tomorrow.replace(hour=10, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")
    
    data = {
        "create_appointment": True,
        "patient_phone": "13800138000",
        "doctor_name": "王医生",
        "appointment_time": appointment_time
    }
    
    print("📤 测试挂号功能...")
    response = send_json_data('8.140.225.6', 55000, data)
    
    if response:
        print("📥 服务器响应:")
        print(json.dumps(response, ensure_ascii=False, indent=2))
        print()
        
        if 'result' in response:
            result = response.get('result')
            
            if isinstance(result, dict) and 'appointment_info' in result:
                print("✅ 挂号功能已正确加载！")
                apt_info = result['appointment_info']
                print(f"   预约ID: {apt_info.get('appointment_id')}")
                print(f"   排队号: {apt_info.get('queue_number')}")
                return True
                
            elif isinstance(result, str) and "default_table" in result:
                print("❌ 服务器代码未更新！")
                print("   错误信息:", result)
                print("\n🔧 解决步骤:")
                print("   1. python3 integrated_server_loginmatchAdd.py restart")
                print("   2. 重新运行此验证程序")
                return False
                
            elif isinstance(result, dict) and result.get('status') == 'error':
                print("⚠️  挂号功能已加载，但有业务错误:")
                print(f"   错误: {result.get('message')}")
                print("   这可能是数据问题，功能本身已正常加载")
                return True
                
            else:
                print("❓ 未预期的响应格式:")
                print(f"   result类型: {type(result)}")
                print(f"   result内容: {result}")
                return False
        else:
            print("❌ 响应格式错误：缺少result字段")
            return False
    else:
        print("❌ 服务器无响应或连接失败")
        print("\n🔧 检查项目:")
        print("   1. 服务器是否运行: python3 integrated_server_loginmatchAdd.py status")
        print("   2. 网络连接是否正常")
        return False


if __name__ == "__main__":
    main()
