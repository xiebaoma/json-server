#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医生注册快速测试
简单快速的医生注册功能验证
"""

import sys
import os
import json
import hashlib
import time

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from network.communication import JSONProtocolClient


def hash_password(password):
    """哈希密码"""
    return hashlib.sha256(password.encode()).hexdigest()


def test_doctor_registration():
    """测试医生注册功能"""
    print("👨‍⚕️ 医生注册快速测试")
    print("=" * 40)
    
    client = JSONProtocolClient('8.140.225.6', 55000)
    
    # 生成唯一的测试数据
    timestamp = int(time.time())
    
    # 测试用例1: 正常注册
    print("\n1️⃣ 测试正常医生注册")
    print("-" * 30)
    
    doctor_data = {
        "register_doctor": True,
        "name": f"测试医生{timestamp}",
        "password_hash": hash_password("doctor123"),
        "employee_id": f"DOC{timestamp}",
        "department": "内科",
        "photo_path": f"/photos/doctor_{timestamp}.jpg"
    }
    
    print(f"注册信息:")
    print(f"  姓名: {doctor_data['name']}")
    print(f"  工号: {doctor_data['employee_id']}")
    print(f"  科室: {doctor_data['department']}")
    
    try:
        response = client.send_json_data(doctor_data)
        
        if response:
            result = response.get('result', '')
            if result == 'chenggongcharu':
                print("✅ 医生注册成功!")
                
                # 测试登录
                print("\n🔐 验证注册后登录...")
                login_data = {
                    "login": True,
                    "user_name": doctor_data['employee_id'],
                    "password": hash_password("doctor123")
                }
                
                time.sleep(0.5)
                login_response = client.send_json_data(login_data)
                
                if login_response and login_response.get('result') == 'verificationSuccess':
                    print("✅ 登录验证成功!")
                else:
                    print(f"❌ 登录验证失败: {login_response.get('result') if login_response else '无响应'}")
                
                # 测试查询医生信息
                print("\n🔍 验证医生信息查询...")
                query_data = {
                    "query_doctor_info": True,
                    "doctor_name": doctor_data['name']
                }
                
                time.sleep(0.5)
                query_response = client.send_json_data(query_data)
                
                if (query_response and 
                    query_response.get('result', {}).get('status') == 'success'):
                    doctor_info = query_response.get('result', {}).get('doctor_info', {})
                    print("✅ 医生信息查询成功!")
                    print(f"  查询到的姓名: {doctor_info.get('name')}")
                    print(f"  查询到的工号: {doctor_info.get('employee_id')}")
                    print(f"  查询到的科室: {doctor_info.get('department')}")
                else:
                    print("❌ 医生信息查询失败")
                
            else:
                print(f"❌ 医生注册失败: {result}")
        else:
            print("❌ 无服务器响应")
            
    except Exception as e:
        print(f"❌ 注册过程异常: {e}")
    
    # 测试用例2: 重复工号注册
    print("\n2️⃣ 测试重复工号注册")
    print("-" * 30)
    
    duplicate_data = {
        "register_doctor": True,
        "name": f"重复工号医生{timestamp}",
        "password_hash": hash_password("duplicate123"),
        "employee_id": f"DOC{timestamp}",  # 使用相同工号
        "department": "外科"
    }
    
    print(f"使用相同工号: {duplicate_data['employee_id']}")
    
    try:
        time.sleep(0.5)
        response = client.send_json_data(duplicate_data)
        
        if response:
            result = response.get('result', '')
            if 'gonghaoyicunzai' in result or 'yicunzai' in result:
                print("✅ 重复工号检测正常!")
                print(f"  返回结果: {result}")
            else:
                print(f"❌ 重复工号检测失败: {result}")
        else:
            print("❌ 无服务器响应")
            
    except Exception as e:
        print(f"❌ 重复工号测试异常: {e}")
    
    # 测试用例3: 无效数据注册
    print("\n3️⃣ 测试无效数据注册")
    print("-" * 30)
    
    invalid_data = {
        "register_doctor": True,
        "name": "",  # 空姓名
        "password_hash": hash_password("invalid123"),
        "employee_id": f"INVALID{timestamp}",
        "department": "测试科"
    }
    
    print("使用空姓名进行注册...")
    
    try:
        time.sleep(0.5)
        response = client.send_json_data(invalid_data)
        
        if response:
            result = response.get('result', '')
            if 'charuyichang' in result or 'error' in result.lower():
                print("✅ 无效数据检测正常!")
                print(f"  返回结果: {result}")
            else:
                print(f"❌ 无效数据检测失败: {result}")
        else:
            print("❌ 无服务器响应")
            
    except Exception as e:
        print(f"❌ 无效数据测试异常: {e}")


def main():
    """主函数"""
    print("🏥 医生注册快速测试工具")
    print("目标服务器: 8.140.225.6:55000")
    print()
    
    try:
        test_doctor_registration()
        
    except KeyboardInterrupt:
        print("\n⏹️ 测试被用户中断")
    except Exception as e:
        print(f"\n💥 测试过程中出现错误: {e}")
    
    print("\n" + "=" * 40)
    print("🏁 测试完成!")
    print("=" * 40)


if __name__ == "__main__":
    main()
