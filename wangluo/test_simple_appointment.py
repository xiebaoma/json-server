#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版挂号测试程序
"""

import json
import socket
import struct
from datetime import datetime, timedelta


def send_json_data(host, port, data):
    """发送JSON数据到服务器"""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        json_bytes = json_str.encode('utf-8')
        
        filename = "simple_appointment.json"
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
        print(f"连接错误: {e}")
        return None


def test_create_appointment():
    """测试创建挂号"""
    print("=== 📅 挂号预约测试 ===")
    
    # 预约明天上午9点
    tomorrow = datetime.now() + timedelta(days=1)
    appointment_time = tomorrow.replace(hour=9, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")
    
    data = {
        "create_appointment": True,
        "patient_phone": "13800138000",  # 张三
        "doctor_name": "王医生",         # 内科王医生
        "appointment_time": appointment_time,
        "fee_paid": 1  # 已付费
    }
    
    print(f"患者: 张三 (13800138000)")
    print(f"医生: 王医生 (内科)")
    print(f"时间: {appointment_time}")
    print(f"状态: 已付费")
    print()
    
    response = send_json_data('8.140.225.6', 55000, data)
    
    # 显示服务器原始响应用于调试
    print("🔍 服务器原始响应:")
    if response:
        print(json.dumps(response, ensure_ascii=False, indent=2))
    else:
        print("❌ 无响应")
    print()
    
    if response and response.get('status') == 'success':
        # 检查响应结构
        if 'result' in response:
            result = response.get('result', {})
            if isinstance(result, dict) and 'appointment_info' in result:
                apt_info = result.get('appointment_info', {})
            elif isinstance(result, dict):
                apt_info = result  # 可能直接就是appointment_info
            else:
                print(f"⚠️  意外的result类型: {type(result)}")
                apt_info = {}
        else:
            apt_info = response.get('appointment_info', {})
        
        print("✅ 挂号成功！")
        print(f"📋 预约ID: {apt_info.get('appointment_id')}")
        print(f"🎫 排队号: {apt_info.get('queue_number')}")
        print(f"📱 患者手机: {apt_info.get('patient_phone')}")
        print(f"👨‍⚕️ 医生: {apt_info.get('doctor_name')}")
        print(f"⏰ 时间: {apt_info.get('appointment_time')}")
        return apt_info.get('appointment_id')
    else:
        print("❌ 挂号失败!")
        if response:
            print(f"错误: {response.get('message', response)}")
        return None

    print("\n" + "="*50 + "\n")


def test_query_appointments(patient_phone="13800138000"):
    """查询预约记录"""
    print("=== 📋 查询预约记录 ===")
    
    data = {
        "query_appointments": True,
        "patient_phone": patient_phone
    }
    
    print(f"查询患者 {patient_phone} 的预约记录...")
    print()
    
    response = send_json_data('8.140.225.6', 55000, data)
    if response and response.get('status') == 'success':
        appointments = response.get('appointments', [])
        if appointments:
            print(f"✅ 找到 {len(appointments)} 条预约记录:")
            print()
            for i, apt in enumerate(appointments, 1):
                status_icon = {
                    'pending': '⏳',
                    'completed': '✅', 
                    'cancelled': '❌'
                }.get(apt['status'], '❓')
                
                print(f"{i}. {status_icon} 预约ID: {apt['appointment_id']}")
                print(f"   👨‍⚕️ 医生: {apt['doctor_name']} ({apt['department']})")
                print(f"   ⏰ 时间: {apt['appointment_time']}")
                print(f"   🎫 排队号: {apt['queue_number']}")
                print(f"   💰 付费: {'已付费' if apt['fee_paid'] else '未付费'}")
                print(f"   📊 状态: {apt['status']}")
                print()
        else:
            print("📭 没有找到预约记录")
    else:
        print("❌ 查询失败!")
        if response:
            print(f"错误: {response.get('message', response)}")

    print("\n" + "="*50 + "\n")


def test_doctor_schedule():
    """查询医生的预约安排"""
    print("=== 👨‍⚕️ 查询医生预约安排 ===")
    
    data = {
        "query_appointments": True,
        "doctor_name": "王医生"
    }
    
    print("查询王医生的预约安排...")
    print()
    
    response = send_json_data('8.140.225.6', 55000, data)
    if response and response.get('status') == 'success':
        appointments = response.get('appointments', [])
        if appointments:
            print(f"✅ 王医生有 {len(appointments)} 个预约:")
            print()
            for i, apt in enumerate(appointments, 1):
                status_icon = {
                    'pending': '⏳',
                    'completed': '✅', 
                    'cancelled': '❌'
                }.get(apt['status'], '❓')
                
                print(f"{i}. {status_icon} {apt['appointment_time'][:16]} - {apt['patient_name']} ({apt['patient_phone']})")
                print(f"   🎫 排队号: {apt['queue_number']}, 状态: {apt['status']}")
                print()
        else:
            print("📭 王医生暂无预约")
    else:
        print("❌ 查询失败!")

    print("\n" + "="*50 + "\n")


def test_cancel_appointment():
    """测试取消预约"""
    print("=== ❌ 取消预约测试 ===")
    
    # 先创建一个预约用于取消
    tomorrow = datetime.now() + timedelta(days=1)
    appointment_time = tomorrow.replace(hour=14, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")
    
    create_data = {
        "create_appointment": True,
        "patient_phone": "13900139000",  # 李四
        "doctor_name": "刘医生",         # 外科刘医生  
        "appointment_time": appointment_time
    }
    
    print("先创建一个测试预约...")
    create_response = send_json_data('8.140.225.6', 55000, create_data)
    
    if create_response and create_response.get('status') == 'success':
        appointment_id = create_response.get('appointment_info', {}).get('appointment_id')
        print(f"✅ 测试预约创建成功 (ID: {appointment_id})")
        print()
        
        # 取消预约
        cancel_data = {
            "cancel_appointment": True,
            "appointment_id": appointment_id
        }
        
        print(f"正在取消预约 ID: {appointment_id}...")
        cancel_response = send_json_data('8.140.225.6', 55000, cancel_data)
        
        if cancel_response and cancel_response.get('status') == 'success':
            print("✅ 预约取消成功!")
            print(f"信息: {cancel_response.get('message')}")
        else:
            print("❌ 取消失败!")
            if cancel_response:
                print(f"错误: {cancel_response.get('message')}")
    else:
        print("❌ 无法创建测试预约")

    print("\n" + "="*50 + "\n")


def quick_test():
    """快速功能测试"""
    print("🚀 快速挂号功能测试")
    print("="*50)
    print()
    
    # 1. 创建预约
    print("1️⃣ 测试挂号...")
    appointment_id = test_create_appointment()
    
    # 2. 查询患者预约
    print("2️⃣ 查询患者预约记录...")
    test_query_appointments()
    
    # 3. 查询医生安排
    print("3️⃣ 查询医生预约安排...")
    test_doctor_schedule()
    
    # 4. 取消预约
    print("4️⃣ 测试取消预约...")
    test_cancel_appointment()
    
    print("🎉 快速测试完成!")


def main():
    """主函数"""
    print("🏥 挂号预约系统测试工具")
    print("📍 服务器: 8.140.225.6:55000")
    print("="*50)
    print()
    
    try:
        quick_test()
        
    except KeyboardInterrupt:
        print("\n⏹️  测试已停止")
    except Exception as e:
        print(f"❌ 测试错误: {e}")


if __name__ == "__main__":
    main()
