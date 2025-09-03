#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医生注册功能测试
测试目标服务器: 8.140.225.6:55000
"""

import sys
import os
import json
import time
import hashlib
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from network.communication import JSONProtocolClient


class DoctorRegistrationTester:
    def __init__(self, host='8.140.225.6', port=55000):
        self.host = host
        self.port = port
        self.client = JSONProtocolClient(host, port)
        self.test_results = []
    
    def hash_password(self, password):
        """哈希密码"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def log_test(self, test_name, success, response=None, error=None, test_data=None):
        """记录测试结果"""
        result = {
            'test_name': test_name,
            'timestamp': datetime.now().isoformat(),
            'success': success,
            'response': response,
            'error': str(error) if error else None,
            'test_data': test_data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        
        if test_data:
            print(f"   测试数据: 工号={test_data.get('employee_id')}, 姓名={test_data.get('name')}")
        
        if success and response:
            result_msg = response.get('result', 'N/A')
            print(f"   响应结果: {result_msg}")
        
        if error:
            print(f"   错误信息: {error}")
        
        print()
    
    def test_connection(self):
        """测试服务器连接"""
        print("🔗 测试服务器连接...")
        try:
            test_data = {"test": "connection"}
            response = self.client.send_json_data(test_data)
            
            if response:
                self.log_test("服务器连接测试", True, response)
                return True
            else:
                self.log_test("服务器连接测试", False, error="无响应")
                return False
                
        except Exception as e:
            self.log_test("服务器连接测试", False, error=e)
            return False
    
    def test_valid_doctor_registration(self):
        """测试有效医生注册"""
        print("👨‍⚕️ 测试有效医生注册...")
        
        # 生成唯一的测试数据
        timestamp = int(time.time())
        
        test_doctors = [
            {
                "name": f"测试医生{timestamp}",
                "employee_id": f"DOC{timestamp}",
                "password": "test123456",
                "department": "内科",
                "photo_path": f"/photos/doctor_{timestamp}.jpg"
            },
            {
                "name": f"李医师{timestamp}",
                "employee_id": f"DOC{timestamp + 1}",
                "password": "secure_password",
                "department": "外科",
                "photo_path": f"/photos/doctor_{timestamp + 1}.jpg"
            },
            {
                "name": f"张主任{timestamp}",
                "employee_id": f"DOC{timestamp + 2}",
                "password": "doctor_pass",
                "department": "儿科",
                "photo_path": None  # 测试可选字段
            }
        ]
        
        for i, doctor in enumerate(test_doctors, 1):
            register_data = {
                "register_doctor": True,
                "name": doctor["name"],
                "password_hash": self.hash_password(doctor["password"]),
                "employee_id": doctor["employee_id"],
                "department": doctor["department"]
            }
            
            # 添加可选字段
            if doctor["photo_path"]:
                register_data["photo_path"] = doctor["photo_path"]
            
            try:
                response = self.client.send_json_data(register_data)
                
                if response and response.get('result') == 'chenggongcharu':
                    self.log_test(f"有效医生注册 - 测试{i}", True, response, test_data=doctor)
                    
                    # 验证注册后能否登录
                    self.verify_doctor_login(doctor["employee_id"], doctor["password"])
                    
                else:
                    self.log_test(f"有效医生注册 - 测试{i}", False, response, test_data=doctor)
                    
            except Exception as e:
                self.log_test(f"有效医生注册 - 测试{i}", False, error=e, test_data=doctor)
            
            # 请求间隔
            time.sleep(0.5)
    
    def test_duplicate_employee_id(self):
        """测试重复工号注册"""
        print("🔄 测试重复工号注册...")
        
        timestamp = int(time.time())
        duplicate_employee_id = f"DUP{timestamp}"
        
        # 第一次注册
        first_doctor = {
            "register_doctor": True,
            "name": f"第一个医生{timestamp}",
            "password_hash": self.hash_password("password1"),
            "employee_id": duplicate_employee_id,
            "department": "内科"
        }
        
        try:
            response1 = self.client.send_json_data(first_doctor)
            if response1 and response1.get('result') == 'chenggongcharu':
                print("   ✓ 第一次注册成功")
                
                # 第二次注册相同工号
                second_doctor = {
                    "register_doctor": True,
                    "name": f"第二个医生{timestamp}",
                    "password_hash": self.hash_password("password2"),
                    "employee_id": duplicate_employee_id,  # 相同工号
                    "department": "外科"
                }
                
                time.sleep(0.5)
                response2 = self.client.send_json_data(second_doctor)
                
                if response2 and 'gonghaoyicunzai' in str(response2.get('result', '')):
                    self.log_test("重复工号检测", True, response2, test_data={"employee_id": duplicate_employee_id})
                else:
                    self.log_test("重复工号检测", False, response2, 
                                error="应该返回工号已存在错误", test_data={"employee_id": duplicate_employee_id})
            else:
                self.log_test("重复工号检测 - 前置注册", False, response1, 
                            error="第一次注册失败", test_data={"employee_id": duplicate_employee_id})
                
        except Exception as e:
            self.log_test("重复工号检测", False, error=e, test_data={"employee_id": duplicate_employee_id})
    
    def test_invalid_registration_data(self):
        """测试无效注册数据"""
        print("⚠️ 测试无效注册数据...")
        
        invalid_test_cases = [
            {
                "name": "缺少姓名字段",
                "data": {
                    "register_doctor": True,
                    # "name": "缺少姓名",  # 故意缺少
                    "password_hash": self.hash_password("test123"),
                    "employee_id": f"INVALID1_{int(time.time())}",
                    "department": "内科"
                }
            },
            {
                "name": "缺少密码字段",
                "data": {
                    "register_doctor": True,
                    "name": "测试医生",
                    # "password_hash": "缺少密码",  # 故意缺少
                    "employee_id": f"INVALID2_{int(time.time())}",
                    "department": "外科"
                }
            },
            {
                "name": "缺少工号字段",
                "data": {
                    "register_doctor": True,
                    "name": "测试医生",
                    "password_hash": self.hash_password("test123"),
                    # "employee_id": "缺少工号",  # 故意缺少
                    "department": "儿科"
                }
            },
            {
                "name": "空姓名字段",
                "data": {
                    "register_doctor": True,
                    "name": "",  # 空值
                    "password_hash": self.hash_password("test123"),
                    "employee_id": f"INVALID3_{int(time.time())}",
                    "department": "内科"
                }
            },
            {
                "name": "空工号字段",
                "data": {
                    "register_doctor": True,
                    "name": "测试医生",
                    "password_hash": self.hash_password("test123"),
                    "employee_id": "",  # 空值
                    "department": "外科"
                }
            }
        ]
        
        for test_case in invalid_test_cases:
            try:
                response = self.client.send_json_data(test_case["data"])
                
                # 期望返回错误
                if response and 'charuyichang' in str(response.get('result', '')):
                    self.log_test(f"无效数据检测 - {test_case['name']}", True, response)
                else:
                    self.log_test(f"无效数据检测 - {test_case['name']}", False, response, 
                                error="应该返回注册异常错误")
                    
            except Exception as e:
                self.log_test(f"无效数据检测 - {test_case['name']}", False, error=e)
            
            time.sleep(0.3)
    
    def verify_doctor_login(self, employee_id, password):
        """验证医生注册后能否登录"""
        try:
            login_data = {
                "login": True,
                "user_name": employee_id,
                "password": self.hash_password(password)
            }
            
            time.sleep(0.5)
            response = self.client.send_json_data(login_data)
            
            if response and response.get('result') == 'verificationSuccess':
                self.log_test(f"注册后登录验证 - {employee_id}", True, response)
            else:
                self.log_test(f"注册后登录验证 - {employee_id}", False, response, 
                            error="注册成功但无法登录")
                
        except Exception as e:
            self.log_test(f"注册后登录验证 - {employee_id}", False, error=e)
    
    def test_doctor_info_query_after_registration(self):
        """测试注册后查询医生信息"""
        print("🔍 测试注册后查询医生信息...")
        
        timestamp = int(time.time())
        doctor_name = f"查询测试医生{timestamp}"
        employee_id = f"QUERY{timestamp}"
        
        # 先注册医生
        register_data = {
            "register_doctor": True,
            "name": doctor_name,
            "password_hash": self.hash_password("query_test"),
            "employee_id": employee_id,
            "department": "测试科"
        }
        
        try:
            register_response = self.client.send_json_data(register_data)
            
            if register_response and register_response.get('result') == 'chenggongcharu':
                print(f"   ✓ 医生 {doctor_name} 注册成功")
                
                # 等待一下再查询
                time.sleep(1)
                
                # 查询医生信息
                query_data = {
                    "query_doctor_info": True,
                    "doctor_name": doctor_name
                }
                
                query_response = self.client.send_json_data(query_data)
                
                if (query_response and 
                    query_response.get('result', {}).get('status') == 'success'):
                    
                    doctor_info = query_response.get('result', {}).get('doctor_info', {})
                    
                    # 验证查询到的信息是否正确
                    if (doctor_info.get('name') == doctor_name and 
                        doctor_info.get('employee_id') == employee_id):
                        self.log_test("注册后信息查询", True, query_response, 
                                    test_data={"name": doctor_name, "employee_id": employee_id})
                    else:
                        self.log_test("注册后信息查询", False, query_response, 
                                    error="查询到的信息不匹配", 
                                    test_data={"name": doctor_name, "employee_id": employee_id})
                else:
                    self.log_test("注册后信息查询", False, query_response, 
                                error="查询失败", test_data={"name": doctor_name})
            else:
                self.log_test("注册后信息查询 - 前置注册", False, register_response, 
                            error="注册失败，无法进行查询测试", test_data={"name": doctor_name})
                
        except Exception as e:
            self.log_test("注册后信息查询", False, error=e, test_data={"name": doctor_name})
    
    def test_batch_doctor_registration(self):
        """测试批量医生注册"""
        print("📊 测试批量医生注册...")
        
        timestamp = int(time.time())
        departments = ["内科", "外科", "儿科", "妇产科", "眼科", "耳鼻喉科", "皮肤科", "神经科"]
        
        batch_doctors = []
        for i in range(8):
            doctor = {
                "name": f"批量医生{i+1}_{timestamp}",
                "employee_id": f"BATCH{i+1}_{timestamp}",
                "password": f"batch_pass_{i+1}",
                "department": departments[i],
                "photo_path": f"/photos/batch_{i+1}_{timestamp}.jpg"
            }
            batch_doctors.append(doctor)
        
        successful_registrations = 0
        failed_registrations = 0
        
        print(f"   开始批量注册 {len(batch_doctors)} 个医生...")
        
        for i, doctor in enumerate(batch_doctors, 1):
            register_data = {
                "register_doctor": True,
                "name": doctor["name"],
                "password_hash": self.hash_password(doctor["password"]),
                "employee_id": doctor["employee_id"],
                "department": doctor["department"],
                "photo_path": doctor["photo_path"]
            }
            
            try:
                response = self.client.send_json_data(register_data)
                
                if response and response.get('result') == 'chenggongcharu':
                    successful_registrations += 1
                    print(f"   ✓ {i}/8 - {doctor['name']} 注册成功")
                else:
                    failed_registrations += 1
                    print(f"   ✗ {i}/8 - {doctor['name']} 注册失败: {response.get('result') if response else '无响应'}")
                
                # 批量注册间隔
                time.sleep(0.2)
                
            except Exception as e:
                failed_registrations += 1
                print(f"   ✗ {i}/8 - {doctor['name']} 注册异常: {e}")
        
        success_rate = successful_registrations / len(batch_doctors) * 100
        
        if success_rate >= 80:  # 80%成功率认为通过
            self.log_test(f"批量医生注册 ({successful_registrations}/{len(batch_doctors)})", 
                         True, {"success_rate": f"{success_rate:.1f}%"})
        else:
            self.log_test(f"批量医生注册 ({successful_registrations}/{len(batch_doctors)})", 
                         False, error=f"成功率仅{success_rate:.1f}%")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始医生注册功能测试")
        print(f"目标服务器: {self.host}:{self.port}")
        print("=" * 60)
        
        # 基础连接测试
        if not self.test_connection():
            print("❌ 服务器连接失败，终止测试")
            return
        
        # 功能测试
        self.test_valid_doctor_registration()
        self.test_duplicate_employee_id()
        self.test_invalid_registration_data()
        self.test_doctor_info_query_after_registration()
        self.test_batch_doctor_registration()
        
        # 生成测试报告
        self.generate_report()
    
    def generate_report(self):
        """生成测试报告"""
        print("=" * 60)
        print("📊 医生注册测试报告")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"总测试数: {total_tests}")
        print(f"通过: {passed_tests} ✅")
        print(f"失败: {failed_tests} ❌")
        print(f"成功率: {passed_tests/total_tests*100:.1f}%")
        print()
        
        # 分类统计
        categories = {}
        for result in self.test_results:
            category = result['test_name'].split(' - ')[0]
            if category not in categories:
                categories[category] = {'total': 0, 'passed': 0}
            categories[category]['total'] += 1
            if result['success']:
                categories[category]['passed'] += 1
        
        print("📈 分类测试结果:")
        for category, stats in categories.items():
            success_rate = stats['passed'] / stats['total'] * 100
            print(f"  {category}: {stats['passed']}/{stats['total']} ({success_rate:.1f}%)")
        print()
        
        if failed_tests > 0:
            print("❌ 失败的测试:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  • {result['test_name']}: {result['error']}")
            print()
        
        # 保存详细报告到文件
        report_file = f"doctor_registration_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'server': f"{self.host}:{self.port}",
                'test_time': datetime.now().isoformat(),
                'summary': {
                    'total_tests': total_tests,
                    'passed_tests': passed_tests,
                    'failed_tests': failed_tests,
                    'success_rate': f"{passed_tests/total_tests*100:.1f}%",
                    'categories': categories
                },
                'detailed_results': self.test_results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"📄 详细报告已保存到: {report_file}")


def main():
    """主函数"""
    print("👨‍⚕️ 医生注册功能测试工具")
    print("目标服务器: 8.140.225.6:55000")
    print()
    
    # 创建测试器实例
    tester = DoctorRegistrationTester()
    
    try:
        # 运行所有测试
        tester.run_all_tests()
        
    except KeyboardInterrupt:
        print("\n⏹️ 测试被用户中断")
    except Exception as e:
        print(f"\n💥 测试过程中发生错误: {e}")
    
    print(f"\n🏁 测试完成！- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()


