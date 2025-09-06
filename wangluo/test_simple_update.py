#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版修改个人信息测试
"""

import json
import socket
import struct


def send_json_data(host, port, data):
    """发送JSON数据到服务器并接收响应"""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        json_bytes = json_str.encode('utf-8')
        
        filename = "simple_update.json"
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


def test_update_patient():
    """测试修改患者信息"""
    print("=== 修改患者信息测试 ===")
    
    # 修改张三的信息
    data = {
        "reset_patient_information": True,
        "old_phone": "13800138000",  # 张三原手机号
        "new_name": "张三丰",       # 新姓名
        "new_email": "zhangsan_updated@email.com"  # 新邮箱
    }
    
    print("修改张三的姓名和邮箱...")
    print(f"原手机号: {data['old_phone']}")
    print(f"新姓名: {data['new_name']}")
    print(f"新邮箱: {data['new_email']}")
    print()
    
    response = send_json_data('8.140.225.6', 55000, data)
    if response:
        if response.get('status') == 'success':
            result = response.get('result', '')
            print(f"✅ 修改成功: {result}")
        else:
            print(f"❌ 修改失败: {response}")
    else:
        print("❌ 服务器无响应")
    
    print("\n" + "="*50 + "\n")


def test_update_doctor():
    """测试修改医生信息"""
    print("=== 修改医生信息测试 ===")
    
    # 修改王医生的信息
    data = {
        "reset_doctor_information": True,
        "old_employee_id": "DOC001",  # 王医生原工号
        "new_name": "王主任",         # 新姓名
        "new_department": "心内科",   # 新科室
        "new_fee": 80.0              # 新收费
    }
    
    print("修改王医生的信息...")
    print(f"原工号: {data['old_employee_id']}")
    print(f"新姓名: {data['new_name']}")
    print(f"新科室: {data['new_department']}")
    print(f"新费用: {data['new_fee']}元")
    print()
    
    response = send_json_data('8.140.225.6', 55000, data)
    if response:
        if response.get('status') == 'success':
            result = response.get('result', '')
            print(f"✅ 修改成功: {result}")
        else:
            print(f"❌ 修改失败: {response}")
    else:
        print("❌ 服务器无响应")
    
    print("\n" + "="*50 + "\n")


def verify_updates():
    """验证修改结果"""
    print("=== 验证修改结果 ===")
    
    # 查询修改后的患者信息
    print("1. 查询修改后的患者信息:")
    patient_query = {
        "query_patient_info": True,
        "patient_name": "张三丰"
    }
    
    response1 = send_json_data('8.140.225.6', 55000, patient_query)
    if response1 and response1.get('status') == 'success':
        patient_info = response1['result']['patient_info']
        print(f"✅ 患者姓名: {patient_info['name']}")
        print(f"✅ 患者邮箱: {patient_info['email']}")
        print(f"✅ 患者手机: {patient_info['phone']}")
    else:
        print("❌ 查询患者信息失败")
    
    print()
    
    # 查询修改后的医生信息
    print("2. 查询修改后的医生信息:")
    doctor_query = {
        "query_doctor_info": True,
        "doctor_name": "王主任"
    }
    
    response2 = send_json_data('8.140.225.6', 55000, doctor_query)
    if response2 and response2.get('status') == 'success':
        doctor_info = response2['result']['doctor_info']
        print(f"✅ 医生姓名: {doctor_info['name']}")
        print(f"✅ 医生科室: {doctor_info['department']}")
        print(f"✅ 医生费用: {doctor_info['fee']}元")
        print(f"✅ 医生工号: {doctor_info['employee_id']}")
    else:
        print("❌ 查询医生信息失败")
    
    print("\n" + "="*50 + "\n")


def main():
    """主函数"""
    print("🔧 个人信息修改测试工具")
    print("📍 服务器地址: 8.140.225.6:55000")
    print("="*50)
    print()
    
    try:
        # 测试修改患者信息
        test_update_patient()
        
        # 测试修改医生信息
        test_update_doctor()
        
        # 验证修改结果
        verify_updates()
        
        print("🎉 所有测试完成！")
        
    except KeyboardInterrupt:
        print("\n⏹️  测试已中断")
    except Exception as e:
        print(f"❌ 测试出错: {e}")


if __name__ == "__main__":
    main()
