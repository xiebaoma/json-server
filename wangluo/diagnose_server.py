#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诊断服务器代码版本
"""

import json
import socket
import struct


def test_server_version():
    """测试服务器是否加载了新代码"""
    print("🔍 诊断服务器代码版本...")
    print("="*50)
    
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('8.140.225.6', 55000))
        
        # 发送一个简单的create_appointment请求
        data = {
            "create_appointment": True,
            "patient_phone": "test",
            "doctor_name": "test", 
            "appointment_time": "2025-01-01 09:00:00"
        }
        
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        json_bytes = json_str.encode('utf-8')
        
        filename = "diagnose.json"
        filename_bytes = filename.encode('utf-8')
        client_socket.sendall(struct.pack("!I", len(filename_bytes)))
        client_socket.sendall(filename_bytes)
        
        client_socket.sendall(struct.pack("!I", len(json_bytes)))
        client_socket.sendall(json_bytes)
        
        raw_response_len = client_socket.recv(4)
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
        
        print("📥 服务器响应分析:")
        result = response.get('result', '')
        
        if "default_table" in str(result) and "create_appointment" in str(result):
            print("❌ 服务器运行【旧代码】")
            print(f"   错误信息: {result}")
            print("\n🔧 解决方案:")
            print("   1. python3 integrated_server_loginmatchAdd.py stop")
            print("   2. python3 integrated_server_loginmatchAdd.py start")
            print("   或者:")
            print("   python3 integrated_server_loginmatchAdd.py restart")
            return False
            
        elif isinstance(result, dict) or "未找到" in str(result):
            print("✅ 服务器运行【新代码】")
            print("   挂号功能已正确加载")
            print(f"   响应: {result}")
            return True
            
        else:
            print("❓ 无法确定服务器版本")
            print(f"   响应: {result}")
            return None
            
    except Exception as e:
        print(f"❌ 连接服务器失败: {e}")
        print("\n🔧 检查项目:")
        print("   1. python3 integrated_server_loginmatchAdd.py status")
        print("   2. 确认服务器是否在运行")
        return None


def main():
    """主函数"""
    print("🏥 医疗系统服务器诊断工具")
    print("📍 目标服务器: 8.140.225.6:55000")
    print()
    
    result = test_server_version()
    
    if result is False:
        print("\n" + "="*50)
        print("📋 诊断结果: 服务器运行旧代码")
        print("💡 原因: 服务器进程没有重启，仍使用启动时的代码")
        print("🎯 解决: 重启服务器进程以加载新代码")
        
    elif result is True:
        print("\n" + "="*50)
        print("📋 诊断结果: 服务器代码已更新")
        print("🎉 挂号功能应该可以正常工作")
        
    else:
        print("\n" + "="*50)
        print("📋 诊断结果: 无法确定服务器状态")
        print("🔧 建议手动检查服务器状态")


if __name__ == "__main__":
    main()
