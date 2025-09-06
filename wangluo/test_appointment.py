#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试挂号预约功能
"""

import json
import socket
import struct
from datetime import datetime, timedelta


def send_json_data(host, port, data):
    """发送JSON数据到服务器并接收响应"""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        json_bytes = json_str.encode('utf-8')
        
        filename = "test_appointment.json"
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
    """测试创建预约/挂号功能"""
    print("=== 测试创建预约/挂号功能 ===")
    
    # 1. 正常创建预约
    tomorrow = datetime.now() + timedelta(days=1)
    appointment_time = tomorrow.strftime("%Y-%m-%d %H:%M:%S")
    
    test_data = {
        "create_appointment": True,
        "patient_phone": "13800138000",  # 张三的手机号
        "doctor_name": "王医生",         # 已存在的医生
        "appointment_time": appointment_time,
        "fee_paid": 1
    }
    
    print("1. 创建正常预约:")
    print("发送的测试数据:")
    print(json.dumps(test_data, ensure_ascii=False, indent=2))
    print()
    
    response = send_json_data('8.140.225.6', 55000, test_data)
    if response:
        if response.get('status') == 'success':
            appointment_info = response.get('appointment_info', {})
            print(f"✅ 预约创建成功!")
            print(f"   预约ID: {appointment_info.get('appointment_id')}")
            print(f"   患者手机: {appointment_info.get('patient_phone')}")
            print(f"   医生姓名: {appointment_info.get('doctor_name')}")
            print(f"   预约时间: {appointment_info.get('appointment_time')}")
            print(f"   排队号码: {appointment_info.get('queue_number')}")
            print(f"   预约状态: {appointment_info.get('status')}")
            global created_appointment_id
            created_appointment_id = appointment_info.get('appointment_id')
        else:
            print(f"❌ 预约创建失败: {response}")
    else:
        print("❌ 服务器无响应")
    
    print("\n" + "-"*50 + "\n")
    
    # 2. 测试不存在的患者
    test_data2 = {
        "create_appointment": True,
        "patient_phone": "99999999999",  # 不存在的手机号
        "doctor_name": "王医生",
        "appointment_time": appointment_time
    }
    
    print("2. 测试不存在的患者:")
    response2 = send_json_data('8.140.225.6', 55000, test_data2)
    if response2:
        if response2.get('status') == 'error':
            print(f"✅ 正确处理错误: {response2.get('message')}")
        else:
            print(f"❌ 预期错误但成功: {response2}")
    
    print("\n" + "-"*50 + "\n")
    
    # 3. 测试不存在的医生
    test_data3 = {
        "create_appointment": True,
        "patient_phone": "13800138000",
        "doctor_name": "不存在的医生",  # 不存在的医生
        "appointment_time": appointment_time
    }
    
    print("3. 测试不存在的医生:")
    response3 = send_json_data('8.140.225.6', 55000, test_data3)
    if response3:
        if response3.get('status') == 'error':
            print(f"✅ 正确处理错误: {response3.get('message')}")
        else:
            print(f"❌ 预期错误但成功: {response3}")
    
    print("\n" + "-"*50 + "\n")
    
    # 4. 测试缺少必要参数
    test_data4 = {
        "create_appointment": True,
        "patient_phone": "13800138000"
        # 缺少doctor_name和appointment_time
    }
    
    print("4. 测试缺少必要参数:")
    response4 = send_json_data('8.140.225.6', 55000, test_data4)
    if response4:
        if response4.get('status') == 'error':
            print(f"✅ 正确处理错误: {response4.get('message')}")
        else:
            print(f"❌ 预期错误但成功: {response4}")
    
    print("\n" + "="*60 + "\n")


def test_query_appointments():
    """测试查询预约功能"""
    print("=== 测试查询预约功能 ===")
    
    # 1. 按患者手机号查询
    test_data1 = {
        "query_appointments": True,
        "patient_phone": "13800138000"  # 张三的手机号
    }
    
    print("1. 按患者手机号查询:")
    response1 = send_json_data('8.140.225.6', 55000, test_data1)
    if response1:
        if response1.get('status') == 'success':
            appointments = response1.get('appointments', [])
            print(f"✅ 查询成功，找到 {len(appointments)} 条预约记录")
            for i, apt in enumerate(appointments, 1):
                print(f"   预约{i}: ID={apt['appointment_id']}, 医生={apt['doctor_name']}, "
                      f"时间={apt['appointment_time']}, 状态={apt['status']}")
        else:
            print(f"❌ 查询失败: {response1}")
    else:
        print("❌ 服务器无响应")
    
    print("\n" + "-"*50 + "\n")
    
    # 2. 按医生姓名查询
    test_data2 = {
        "query_appointments": True,
        "doctor_name": "王医生"
    }
    
    print("2. 按医生姓名查询:")
    response2 = send_json_data('8.140.225.6', 55000, test_data2)
    if response2:
        if response2.get('status') == 'success':
            appointments = response2.get('appointments', [])
            print(f"✅ 查询成功，找到 {len(appointments)} 条预约记录")
            for i, apt in enumerate(appointments, 1):
                print(f"   预约{i}: ID={apt['appointment_id']}, 患者={apt['patient_name']}, "
                      f"时间={apt['appointment_time']}, 状态={apt['status']}")
        else:
            print(f"❌ 查询失败: {response2}")
    
    print("\n" + "-"*50 + "\n")
    
    # 3. 按日期查询
    today = datetime.now().strftime("%Y-%m-%d")
    test_data3 = {
        "query_appointments": True,
        "appointment_date": today
    }
    
    print(f"3. 按日期查询({today}):")
    response3 = send_json_data('8.140.225.6', 55000, test_data3)
    if response3:
        if response3.get('status') == 'success':
            appointments = response3.get('appointments', [])
            print(f"✅ 查询成功，找到 {len(appointments)} 条预约记录")
            for i, apt in enumerate(appointments, 1):
                print(f"   预约{i}: ID={apt['appointment_id']}, 患者={apt['patient_name']}, "
                      f"医生={apt['doctor_name']}, 状态={apt['status']}")
        else:
            print(f"❌ 查询失败: {response3}")
    
    print("\n" + "-"*50 + "\n")
    
    # 4. 查询所有预约
    test_data4 = {
        "query_appointments": True
    }
    
    print("4. 查询所有预约:")
    response4 = send_json_data('8.140.225.6', 55000, test_data4)
    if response4:
        if response4.get('status') == 'success':
            appointments = response4.get('appointments', [])
            print(f"✅ 查询成功，找到 {len(appointments)} 条预约记录")
            # 只显示前5条
            for i, apt in enumerate(appointments[:5], 1):
                print(f"   预约{i}: ID={apt['appointment_id']}, 患者={apt['patient_name']}, "
                      f"医生={apt['doctor_name']}, 时间={apt['appointment_time'][:16]}, "
                      f"状态={apt['status']}")
            if len(appointments) > 5:
                print(f"   ... 还有 {len(appointments)-5} 条记录")
        else:
            print(f"❌ 查询失败: {response4}")
    
    print("\n" + "="*60 + "\n")


def test_update_appointment_status():
    """测试更新预约状态"""
    print("=== 测试更新预约状态功能 ===")
    
    # 先获取一个预约ID
    query_data = {
        "query_appointments": True,
        "patient_phone": "13800138000"
    }
    
    response = send_json_data('8.140.225.6', 55000, query_data)
    appointment_id = None
    if response and response.get('status') == 'success':
        appointments = response.get('appointments', [])
        if appointments:
            appointment_id = appointments[0]['appointment_id']
    
    if not appointment_id:
        print("❌ 无法获取有效的预约ID进行测试")
        return
    
    # 1. 更新预约状态为已完成
    test_data1 = {
        "update_appointment_status": True,
        "appointment_id": appointment_id,
        "new_status": "completed"
    }
    
    print(f"1. 将预约ID {appointment_id} 状态更新为已完成:")
    response1 = send_json_data('8.140.225.6', 55000, test_data1)
    if response1:
        if response1.get('status') == 'success':
            print(f"✅ 状态更新成功: {response1.get('message')}")
        else:
            print(f"❌ 状态更新失败: {response1}")
    
    print("\n" + "-"*50 + "\n")
    
    # 2. 测试无效的状态值
    test_data2 = {
        "update_appointment_status": True,
        "appointment_id": appointment_id,
        "new_status": "invalid_status"
    }
    
    print("2. 测试无效的状态值:")
    response2 = send_json_data('8.140.225.6', 55000, test_data2)
    if response2:
        if response2.get('status') == 'error':
            print(f"✅ 正确处理错误: {response2.get('message')}")
        else:
            print(f"❌ 预期错误但成功: {response2}")
    
    print("\n" + "-"*50 + "\n")
    
    # 3. 测试不存在的预约ID
    test_data3 = {
        "update_appointment_status": True,
        "appointment_id": 99999,
        "new_status": "pending"
    }
    
    print("3. 测试不存在的预约ID:")
    response3 = send_json_data('8.140.225.6', 55000, test_data3)
    if response3:
        if response3.get('status') == 'error':
            print(f"✅ 正确处理错误: {response3.get('message')}")
        else:
            print(f"❌ 预期错误但成功: {response3}")
    
    print("\n" + "="*60 + "\n")


def test_cancel_appointment():
    """测试取消预约功能"""
    print("=== 测试取消预约功能 ===")
    
    # 先创建一个新预约用于取消测试
    tomorrow = datetime.now() + timedelta(days=1)
    appointment_time = tomorrow.strftime("%Y-%m-%d %H:%M:%S")
    
    create_data = {
        "create_appointment": True,
        "patient_phone": "13900139000",  # 李四的手机号
        "doctor_name": "刘医生",
        "appointment_time": appointment_time
    }
    
    print("先创建一个测试预约...")
    create_response = send_json_data('8.140.225.6', 55000, create_data)
    test_appointment_id = None
    
    if create_response and create_response.get('status') == 'success':
        test_appointment_id = create_response.get('appointment_info', {}).get('appointment_id')
        print(f"✅ 测试预约创建成功，ID: {test_appointment_id}")
    else:
        print("❌ 无法创建测试预约")
        return
    
    print("\n" + "-"*30 + "\n")
    
    # 1. 正常取消预约
    test_data1 = {
        "cancel_appointment": True,
        "appointment_id": test_appointment_id
    }
    
    print(f"1. 取消预约ID {test_appointment_id}:")
    response1 = send_json_data('8.140.225.6', 55000, test_data1)
    if response1:
        if response1.get('status') == 'success':
            print(f"✅ 取消成功: {response1.get('message')}")
        else:
            print(f"❌ 取消失败: {response1}")
    
    print("\n" + "-"*50 + "\n")
    
    # 2. 重复取消同一个预约
    print("2. 重复取消同一个预约:")
    response2 = send_json_data('8.140.225.6', 55000, test_data1)
    if response2:
        if response2.get('status') == 'error':
            print(f"✅ 正确处理错误: {response2.get('message')}")
        else:
            print(f"❌ 预期错误但成功: {response2}")
    
    print("\n" + "-"*50 + "\n")
    
    # 3. 测试不存在的预约ID
    test_data3 = {
        "cancel_appointment": True,
        "appointment_id": 99999
    }
    
    print("3. 测试不存在的预约ID:")
    response3 = send_json_data('8.140.225.6', 55000, test_data3)
    if response3:
        if response3.get('status') == 'error':
            print(f"✅ 正确处理错误: {response3.get('message')}")
        else:
            print(f"❌ 预期错误但成功: {response3}")
    
    print("\n" + "-"*50 + "\n")
    
    # 4. 测试缺少参数
    test_data4 = {
        "cancel_appointment": True
        # 缺少appointment_id参数
    }
    
    print("4. 测试缺少appointment_id参数:")
    response4 = send_json_data('8.140.225.6', 55000, test_data4)
    if response4:
        if response4.get('status') == 'error':
            print(f"✅ 正确处理错误: {response4.get('message')}")
        else:
            print(f"❌ 预期错误但成功: {response4}")
    
    print("\n" + "="*60 + "\n")


def test_appointment_workflow():
    """测试完整的预约流程"""
    print("=== 测试完整的预约流程 ===")
    
    # 1. 创建预约
    tomorrow = datetime.now() + timedelta(days=2)
    appointment_time = tomorrow.strftime("%Y-%m-%d 09:00:00")
    
    create_data = {
        "create_appointment": True,
        "patient_phone": "15800158000",  # 王五的手机号
        "doctor_name": "陈医生",
        "appointment_time": appointment_time,
        "fee_paid": 1
    }
    
    print("步骤1: 创建预约")
    create_response = send_json_data('8.140.225.6', 55000, create_data)
    appointment_id = None
    
    if create_response and create_response.get('status') == 'success':
        appointment_id = create_response.get('appointment_info', {}).get('appointment_id')
        print(f"✅ 预约创建成功，ID: {appointment_id}")
    else:
        print("❌ 预约创建失败")
        return
    
    print("\n步骤2: 查询刚创建的预约")
    query_data = {
        "query_appointments": True,
        "patient_phone": "15800158000"
    }
    
    query_response = send_json_data('8.140.225.6', 55000, query_data)
    if query_response and query_response.get('status') == 'success':
        appointments = query_response.get('appointments', [])
        found = False
        for apt in appointments:
            if apt['appointment_id'] == appointment_id:
                print(f"✅ 找到预约: ID={apt['appointment_id']}, 医生={apt['doctor_name']}, "
                      f"状态={apt['status']}, 排队号={apt['queue_number']}")
                found = True
                break
        if not found:
            print("❌ 未找到刚创建的预约")
    else:
        print("❌ 查询预约失败")
    
    print("\n步骤3: 更新预约状态为已完成")
    update_data = {
        "update_appointment_status": True,
        "appointment_id": appointment_id,
        "new_status": "completed"
    }
    
    update_response = send_json_data('8.140.225.6', 55000, update_data)
    if update_response and update_response.get('status') == 'success':
        print(f"✅ 预约状态更新成功")
    else:
        print("❌ 预约状态更新失败")
    
    print("\n步骤4: 验证状态更新")
    verify_response = send_json_data('8.140.225.6', 55000, query_data)
    if verify_response and verify_response.get('status') == 'success':
        appointments = verify_response.get('appointments', [])
        for apt in appointments:
            if apt['appointment_id'] == appointment_id:
                if apt['status'] == 'completed':
                    print(f"✅ 状态更新验证成功: {apt['status']}")
                else:
                    print(f"❌ 状态更新验证失败: {apt['status']}")
                break
    
    print("\n🎉 完整流程测试完成！")
    print("\n" + "="*60 + "\n")


def main():
    """主测试函数"""
    print("🏥 挂号预约功能测试程序")
    print("📍 服务器地址: 8.140.225.6:55000")
    print("="*60)
    print()
    
    # 全局变量存储创建的预约ID
    global created_appointment_id
    created_appointment_id = None
    
    try:
        # 1. 测试创建预约
        test_create_appointment()
        
        # 2. 测试查询预约
        test_query_appointments()
        
        # 3. 测试更新预约状态
        test_update_appointment_status()
        
        # 4. 测试取消预约
        test_cancel_appointment()
        
        # 5. 测试完整流程
        test_appointment_workflow()
        
        print("🎉 所有挂号预约功能测试完成！")
        
    except KeyboardInterrupt:
        print("\n⏹️  测试已中断")
    except Exception as e:
        print(f"❌ 测试出错: {e}")


if __name__ == "__main__":
    main()
