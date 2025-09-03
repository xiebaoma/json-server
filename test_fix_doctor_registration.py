#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试医生注册数据类型修复
验证修复后的医生注册功能是否正常工作
"""

import sys
import os
import json
import time

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from network.communication import JSONProtocolClient


def test_problematic_data():
    """测试之前出现问题的数据格式"""
    print("🔧 测试修复后的医生注册功能")
    print("=" * 50)
    
    client = JSONProtocolClient('8.140.225.6', 55000)
    
    # 使用与错误日志中相似的数据格式
    timestamp = int(time.time())
    
    print("📋 测试用例1: 模拟原始问题数据")
    print("-" * 40)
    
    # 模拟原始问题数据（字符串类型的register_doctor）
    problem_data = {
        'department': '内科',
        'employee_id': f'fix_test_{timestamp}',
        'name': '修复测试医生',
        'password_hash': 'test_hash_123',
        'photo_path': 'F:/CODE/SmallTerm/JigsawMaster/images/boat.jpg',
        'register_doctor': '1'  # 字符串类型，模拟前端可能发送的格式
    }
    
    print(f"发送数据: {json.dumps(problem_data, ensure_ascii=False, indent=2)}")
    
    try:
        response = client.send_json_data(problem_data)
        
        if response:
            result = response.get('result', '')
            print(f"响应结果: {result}")
            
            if result == 'chenggongcharu':
                print("✅ 修复成功！数据类型问题已解决")
                
                # 验证注册后能否登录
                print("\n🔐 验证登录功能...")
                login_data = {
                    "login": True,
                    "user_name": problem_data['employee_id'],
                    "password": problem_data['password_hash']
                }
                
                time.sleep(0.5)
                login_response = client.send_json_data(login_data)
                
                if login_response and login_response.get('result') == 'verificationSuccess':
                    print("✅ 登录验证成功")
                else:
                    print(f"❌ 登录验证失败: {login_response.get('result') if login_response else '无响应'}")
                
                # 验证查询医生信息
                print("\n🔍 验证医生信息查询...")
                query_data = {
                    "query_doctor_info": True,
                    "doctor_name": problem_data['name']
                }
                
                time.sleep(0.5)
                query_response = client.send_json_data(query_data)
                
                if (query_response and 
                    query_response.get('result', {}).get('status') == 'success'):
                    doctor_info = query_response.get('result', {}).get('doctor_info', {})
                    print("✅ 医生信息查询成功")
                    print(f"   姓名: {doctor_info.get('name')}")
                    print(f"   工号: {doctor_info.get('employee_id')}")
                    print(f"   科室: {doctor_info.get('department')}")
                else:
                    print("❌ 医生信息查询失败")
                    
            elif result == 'gonghaoyicunzai':
                print("⚠️ 工号已存在（这是正常的，说明之前的测试数据还在）")
            else:
                print(f"❌ 注册失败: {result}")
        else:
            print("❌ 无服务器响应")
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")


def test_various_data_types():
    """测试各种数据类型的处理"""
    print("\n📊 测试各种数据类型处理")
    print("=" * 50)
    
    client = JSONProtocolClient('8.140.225.6', 55000)
    timestamp = int(time.time())
    
    test_cases = [
        {
            "name": "字符串类型字段",
            "data": {
                'register_doctor': True,
                'name': '字符串测试医生',
                'employee_id': f'STR_{timestamp}',
                'password_hash': 'string_hash',
                'department': '内科',
                'photo_path': '/path/to/photo.jpg'
            }
        },
        {
            "name": "数字类型字段（应转为字符串）",
            "data": {
                'register_doctor': True,
                'name': 123,  # 数字
                'employee_id': 456,  # 数字
                'password_hash': 'num_hash',
                'department': 789,  # 数字
                'photo_path': None
            }
        },
        {
            "name": "空字段处理",
            "data": {
                'register_doctor': True,
                'name': '',  # 空字符串
                'employee_id': f'EMPTY_{timestamp}',
                'password_hash': 'empty_hash',
                'department': '',
                'photo_path': ''
            }
        },
        {
            "name": "None值处理",
            "data": {
                'register_doctor': True,
                'name': '空值测试医生',
                'employee_id': f'NULL_{timestamp}',
                'password_hash': 'null_hash',
                'department': None,
                'photo_path': None
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 30)
        
        try:
            response = client.send_json_data(test_case['data'])
            
            if response:
                result = response.get('result', '')
                
                if result == 'chenggongcharu':
                    print("✅ 注册成功")
                elif result == 'charuyichang':
                    print("⚠️ 注册异常（预期的验证错误）")
                elif result == 'gonghaoyicunzai':
                    print("⚠️ 工号已存在")
                else:
                    print(f"❓ 未知结果: {result}")
            else:
                print("❌ 无响应")
                
        except Exception as e:
            print(f"❌ 测试异常: {e}")
        
        time.sleep(0.3)


def test_edge_cases():
    """测试边界情况"""
    print("\n🎯 测试边界情况")
    print("=" * 50)
    
    client = JSONProtocolClient('8.140.225.6', 55000)
    timestamp = int(time.time())
    
    edge_cases = [
        {
            "name": "超长字段",
            "data": {
                'register_doctor': True,
                'name': '超长姓名' * 50,  # 超长姓名
                'employee_id': f'LONG_{timestamp}',
                'password_hash': 'long_hash',
                'department': '超长科室名称' * 20,
                'photo_path': '/very/long/path/' + 'subdir/' * 50 + 'photo.jpg'
            }
        },
        {
            "name": "特殊字符",
            "data": {
                'register_doctor': True,
                'name': '特殊字符医生@#$%^&*()',
                'employee_id': f'SPEC_{timestamp}',
                'password_hash': 'special_hash!@#',
                'department': '特殊科室<>&"\'',
                'photo_path': '/path/with spaces/and-symbols.jpg'
            }
        },
        {
            "name": "Unicode字符",
            "data": {
                'register_doctor': True,
                'name': '张医生👨‍⚕️',
                'employee_id': f'UNI_{timestamp}',
                'password_hash': 'unicode_hash_密码',
                'department': '心内科💗',
                'photo_path': '/照片/医生.jpg'
            }
        }
    ]
    
    for i, test_case in enumerate(edge_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 30)
        
        try:
            response = client.send_json_data(test_case['data'])
            
            if response:
                result = response.get('result', '')
                print(f"结果: {result}")
                
                if result == 'chenggongcharu':
                    print("✅ 边界情况处理正常")
                else:
                    print("⚠️ 边界情况被拒绝（可能是预期的）")
            else:
                print("❌ 无响应")
                
        except Exception as e:
            print(f"❌ 边界测试异常: {e}")
        
        time.sleep(0.3)


def main():
    """主函数"""
    print("🔧 医生注册数据类型修复验证测试")
    print("目标服务器: 8.140.225.6:55000")
    print()
    
    try:
        # 测试修复效果
        test_problematic_data()
        
        # 测试各种数据类型
        test_various_data_types()
        
        # 测试边界情况
        test_edge_cases()
        
        print("\n" + "=" * 50)
        print("🎉 修复验证测试完成!")
        print("=" * 50)
        print("\n💡 修复要点:")
        print("   • 添加了数据类型转换和验证")
        print("   • 确保字段不为空的检查")
        print("   • 正确处理可选字段的None值")
        print("   • 明确指定数据库字段的数据类型")
        
    except KeyboardInterrupt:
        print("\n⏹️ 测试被用户中断")
    except Exception as e:
        print(f"\n💥 测试过程中出现错误: {e}")


if __name__ == "__main__":
    main()
