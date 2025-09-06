#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键修复和测试脚本
"""

import os
import subprocess
import time
import json
import socket
import struct
from datetime import datetime, timedelta


def run_command(command, description):
    """执行命令并显示结果"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=".")
        if result.returncode == 0:
            print(f"✅ {description}成功")
            if result.stdout.strip():
                print(f"输出: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description}失败")
            if result.stderr.strip():
                print(f"错误: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ 执行命令时出错: {e}")
        return False


def test_server_connection():
    """测试服务器连接"""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(5)
        client_socket.connect(('8.140.225.6', 55000))
        client_socket.close()
        return True
    except Exception as e:
        print(f"服务器连接失败: {e}")
        return False


def test_appointment_feature():
    """测试挂号功能"""
    try:
        print("🧪 测试挂号功能...")
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('8.140.225.6', 55000))
        
        tomorrow = datetime.now() + timedelta(days=1)
        appointment_time = tomorrow.replace(hour=9, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")
        
        data = {
            "create_appointment": True,
            "patient_phone": "13800138000",
            "doctor_name": "王医生",
            "appointment_time": appointment_time
        }
        
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        json_bytes = json_str.encode('utf-8')
        
        filename = "test.json"
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
        
        # 检查响应
        if 'result' in response:
            result = response.get('result')
            if isinstance(result, dict) and 'appointment_info' in result:
                print("✅ 挂号功能正常工作！")
                apt_info = result['appointment_info']
                print(f"   预约ID: {apt_info.get('appointment_id')}")
                print(f"   排队号: {apt_info.get('queue_number')}")
                return True
            elif isinstance(result, str) and "default_table" in result:
                print("❌ 服务器代码未更新，需要重启服务器")
                return False
            else:
                print(f"⚠️  挂号功能有错误: {result}")
                return False
        else:
            print("❌ 响应格式异常")
            return False
            
    except Exception as e:
        print(f"❌ 测试挂号功能失败: {e}")
        return False


def main():
    """主函数"""
    print("🚀 医疗系统外键修复和测试工具")
    print("="*60)
    
    # 步骤1: 重置数据库
    print("\n📋 步骤1: 重置数据库")
    if not run_command("python3 check_database.py MedicalSystem.db --reset", "重置数据库"):
        print("❌ 数据库重置失败，手动执行: python3 check_database.py MedicalSystem.db --reset")
        return
    
    # 步骤2: 重启服务器
    print("\n📋 步骤2: 重启服务器")
    print("🔄 停止现有服务器...")
    run_command("python3 integrated_server_loginmatchAdd.py stop", "停止服务器")
    
    print("⏱️  等待3秒...")
    time.sleep(3)
    
    print("🚀 启动服务器...")
    if not run_command("python3 integrated_server_loginmatchAdd.py start", "启动服务器"):
        print("❌ 服务器启动失败，请手动启动: python3 integrated_server_loginmatchAdd.py start")
        return
    
    # 步骤3: 等待服务器启动
    print("\n📋 步骤3: 等待服务器启动")
    print("⏱️  等待服务器完全启动...")
    for i in range(10):
        time.sleep(1)
        print(f"   等待中... {i+1}/10")
        if test_server_connection():
            print("✅ 服务器已启动并可连接")
            break
    else:
        print("❌ 服务器启动超时")
        return
    
    # 步骤4: 测试功能
    print("\n📋 步骤4: 测试挂号功能")
    if test_appointment_feature():
        print("\n🎉 所有步骤完成！外键修复成功，挂号功能正常工作！")
        print("\n📝 现在可以使用以下命令测试：")
        print("   python3 test_simple_appointment.py")
        print("   python3 test_appointment.py")
    else:
        print("\n❌ 挂号功能测试失败")
        print("\n🔧 手动排查步骤：")
        print("1. python3 integrated_server_loginmatchAdd.py status")
        print("2. python3 verify_server_update.py")
        print("3. python3 debug_appointment.py")


if __name__ == "__main__":
    main()
