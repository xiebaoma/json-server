#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修改个人信息功能
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
        filename = "test_update_info.json"
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


def test_update_patient_info():
    """测试修改患者信息功能"""
    print("=== 测试修改患者信息功能 ===")
    
    # 1. 测试修改患者姓名和邮箱
    test_data = {
        "reset_patient_information": True,
        "old_phone": "13800138000",  # 张三的手机号
        "new_name": "张三丰",
        "new_email": "zhangsan_new@example.com"
    }
    
    print("1. 修改患者姓名和邮箱:")
    print("发送的测试数据:")
    print(json.dumps(test_data, ensure_ascii=False, indent=2))
    print()
    
    response = send_json_data('8.140.225.6', 55000, test_data)
    if response:
        print("服务器响应:")
        print(json.dumps(response, ensure_ascii=False, indent=2))
    else:
        print("未收到服务器响应")
    
    print("\n" + "-"*50 + "\n")
    
    # 2. 测试修改患者所有信息
    test_data2 = {
        "reset_patient_information": True,
        "old_phone": "13900139000",  # 李四的手机号
        "new_name": "李四海",
        "new_birth_date": "1985-06-20",
        "new_id_card": "110101198506200004",
        "new_phone": "13988139000",
        "new_email": "lisi_updated@example.com"
    }
    
    print("2. 修改患者所有信息:")
    print("发送的测试数据:")
    print(json.dumps(test_data2, ensure_ascii=False, indent=2))
    print()
    
    response2 = send_json_data('8.140.225.6', 55000, test_data2)
    if response2:
        print("服务器响应:")
        print(json.dumps(response2, ensure_ascii=False, indent=2))
    else:
        print("未收到服务器响应")
    
    print("\n" + "-"*50 + "\n")
    
    # 3. 测试修改不存在的患者
    test_data3 = {
        "reset_patient_information": True,
        "old_phone": "99999999999",  # 不存在的手机号
        "new_name": "不存在的患者"
    }
    
    print("3. 测试修改不存在的患者:")
    print("发送的测试数据:")
    print(json.dumps(test_data3, ensure_ascii=False, indent=2))
    print()
    
    response3 = send_json_data('8.140.225.6', 55000, test_data3)
    if response3:
        print("服务器响应:")
        print(json.dumps(response3, ensure_ascii=False, indent=2))
    else:
        print("未收到服务器响应")
    
    print("\n" + "="*60 + "\n")


def test_update_doctor_info():
    """测试修改医生信息功能"""
    print("=== 测试修改医生信息功能 ===")
    
    # 1. 测试修改医生姓名和科室
    test_data = {
        "reset_doctor_information": True,
        "old_employee_id": "DOC001",  # 王医生的工号
        "new_name": "王主任医师",
        "new_department": "心内科"
    }
    
    print("1. 修改医生姓名和科室:")
    print("发送的测试数据:")
    print(json.dumps(test_data, ensure_ascii=False, indent=2))
    print()
    
    response = send_json_data('8.140.225.6', 55000, test_data)
    if response:
        print("服务器响应:")
        print(json.dumps(response, ensure_ascii=False, indent=2))
    else:
        print("未收到服务器响应")
    
    print("\n" + "-"*50 + "\n")
    
    # 2. 测试修改医生费用和最大患者数
    test_data2 = {
        "reset_doctor_information": True,
        "old_employee_id": "DOC002",  # 刘医生的工号
        "new_fee": 100.0,
        "new_max_patients": 35,
        "new_photo_path": "/images/doctors/liudoctor_new.jpg"
    }
    
    print("2. 修改医生费用和最大患者数:")
    print("发送的测试数据:")
    print(json.dumps(test_data2, ensure_ascii=False, indent=2))
    print()
    
    response2 = send_json_data('8.140.225.6', 55000, test_data2)
    if response2:
        print("服务器响应:")
        print(json.dumps(response2, ensure_ascii=False, indent=2))
    else:
        print("未收到服务器响应")
    
    print("\n" + "-"*50 + "\n")
    
    # 3. 测试修改医生工作时间表
    test_data3 = {
        "reset_doctor_information": True,
        "old_employee_id": "DOC003",  # 陈医生的工号
        "new_work_schedule": '{"monday": "8:00-16:00", "tuesday": "8:00-16:00", "wednesday": "8:00-16:00", "thursday": "8:00-16:00", "friday": "8:00-16:00", "saturday": "9:00-12:00"}',
        "new_is_available": True
    }
    
    print("3. 修改医生工作时间表:")
    print("发送的测试数据:")
    print(json.dumps(test_data3, ensure_ascii=False, indent=2))
    print()
    
    response3 = send_json_data('8.140.225.6', 55000, test_data3)
    if response3:
        print("服务器响应:")
        print(json.dumps(response3, ensure_ascii=False, indent=2))
    else:
        print("未收到服务器响应")
    
    print("\n" + "-"*50 + "\n")
    
    # 4. 测试修改不存在的医生
    test_data4 = {
        "reset_doctor_information": True,
        "old_employee_id": "DOC999",  # 不存在的工号
        "new_name": "不存在的医生"
    }
    
    print("4. 测试修改不存在的医生:")
    print("发送的测试数据:")
    print(json.dumps(test_data4, ensure_ascii=False, indent=2))
    print()
    
    response4 = send_json_data('8.140.225.6', 55000, test_data4)
    if response4:
        print("服务器响应:")
        print(json.dumps(response4, ensure_ascii=False, indent=2))
    else:
        print("未收到服务器响应")
    
    print("\n" + "="*60 + "\n")


def test_parameter_validation():
    """测试参数验证"""
    print("=== 测试参数验证 ===")
    
    # 1. 测试缺少必需参数的患者信息修改
    test_data1 = {
        "reset_patient_information": True,
        # 缺少 old_phone 参数
        "new_name": "测试患者"
    }
    
    print("1. 测试缺少old_phone参数:")
    print("发送的测试数据:")
    print(json.dumps(test_data1, ensure_ascii=False, indent=2))
    print()
    
    response1 = send_json_data('8.140.225.6', 55000, test_data1)
    if response1:
        print("服务器响应:")
        print(json.dumps(response1, ensure_ascii=False, indent=2))
    else:
        print("未收到服务器响应")
    
    print("\n" + "-"*50 + "\n")
    
    # 2. 测试缺少必需参数的医生信息修改
    test_data2 = {
        "reset_doctor_information": True,
        # 缺少 old_employee_id 参数
        "new_name": "测试医生"
    }
    
    print("2. 测试缺少old_employee_id参数:")
    print("发送的测试数据:")
    print(json.dumps(test_data2, ensure_ascii=False, indent=2))
    print()
    
    response2 = send_json_data('8.140.225.6', 55000, test_data2)
    if response2:
        print("服务器响应:")
        print(json.dumps(response2, ensure_ascii=False, indent=2))
    else:
        print("未收到服务器响应")
    
    print("\n" + "-"*50 + "\n")
    
    # 3. 测试只有识别参数没有更新字段
    test_data3 = {
        "reset_patient_information": True,
        "old_phone": "13800138000"
        # 没有任何new_字段
    }
    
    print("3. 测试没有任何更新字段:")
    print("发送的测试数据:")
    print(json.dumps(test_data3, ensure_ascii=False, indent=2))
    print()
    
    response3 = send_json_data('8.140.225.6', 55000, test_data3)
    if response3:
        print("服务器响应:")
        print(json.dumps(response3, ensure_ascii=False, indent=2))
    else:
        print("未收到服务器响应")
    
    print("\n" + "="*60 + "\n")


def query_updated_info():
    """查询修改后的信息进行验证"""
    print("=== 验证修改结果 ===")
    
    # 查询修改后的患者信息
    print("1. 查询修改后的患者信息:")
    patient_query = {
        "query_patient_info": True,
        "patient_name": "张三丰"  # 之前修改的名字
    }
    
    print("查询张三丰的信息:")
    response1 = send_json_data('8.140.225.6', 55000, patient_query)
    if response1:
        print("服务器响应:")
        print(json.dumps(response1, ensure_ascii=False, indent=2))
    else:
        print("未收到服务器响应")
    
    print("\n" + "-"*50 + "\n")
    
    # 查询修改后的医生信息
    print("2. 查询修改后的医生信息:")
    doctor_query = {
        "query_doctor_info": True,
        "doctor_name": "王主任医师"  # 之前修改的名字
    }
    
    print("查询王主任医师的信息:")
    response2 = send_json_data('8.140.225.6', 55000, doctor_query)
    if response2:
        print("服务器响应:")
        print(json.dumps(response2, ensure_ascii=False, indent=2))
    else:
        print("未收到服务器响应")
    
    print("\n" + "="*60 + "\n")


def main():
    """主测试函数"""
    print("开始测试修改个人信息功能...")
    print("注意：请确保服务器已经启动并监听在8.140.225.6:55000端口\n")
    
    try:
        # 测试修改患者信息
        test_update_patient_info()
        
        # 测试修改医生信息
        test_update_doctor_info()
        
        # 测试参数验证
        test_parameter_validation()
        
        # 查询验证修改结果
        query_updated_info()
        
        print("所有修改个人信息测试已完成！")
        
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"测试过程中出错: {e}")


if __name__ == "__main__":
    main()
