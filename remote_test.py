#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
远程医疗系统服务器测试模块
测试目标服务器: 8.140.225.6:55000
"""

import sys
import os
import json
import time
import threading
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from network.communication import JSONProtocolClient


class RemoteMedicalServerTester:
    def __init__(self, host='8.140.225.6', port=55000):
        self.host = host
        self.port = port
        self.client = JSONProtocolClient(host, port)
        self.test_results = []
        
    def log_test(self, test_name, success, response=None, error=None):
        """记录测试结果"""
        result = {
            'test_name': test_name,
            'timestamp': datetime.now().isoformat(),
            'success': success,
            'response': response,
            'error': str(error) if error else None
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if error:
            print(f"   错误: {error}")
        if response and success:
            print(f"   响应: {response.get('result', 'N/A')}")
        print()
    
    def test_connection(self):
        """测试基本连接"""
        print("🔗 测试服务器连接...")
        try:
            # 发送一个简单的测试请求
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
    
    def test_user_login(self):
        """测试用户登录功能"""
        print("👤 测试用户登录...")
        
        # 测试有效登录
        login_data = {
            "login": True,
            "user_name": "13800138000",
            "password_hash": "hash_patient1"
        }
        
        try:
            response = self.client.send_json_data(login_data)
            if response and response.get('result') == 'verificationSuccess':
                self.log_test("用户登录 - 有效凭据", True, response)
            else:
                self.log_test("用户登录 - 有效凭据", False, response)
        except Exception as e:
            self.log_test("用户登录 - 有效凭据", False, error=e)
        
        # 测试无效登录
        invalid_login_data = {
            "login": True,
            "user_name": "invalid_user",
            "password_hash": "wrong_password"
        }
        
        try:
            response = self.client.send_json_data(invalid_login_data)
            if response and 'verificationFalse' in str(response.get('result', '')):
                self.log_test("用户登录 - 无效凭据", True, response)
            else:
                self.log_test("用户登录 - 无效凭据", False, response)
        except Exception as e:
            self.log_test("用户登录 - 无效凭据", False, error=e)
    
    def test_patient_registration(self):
        """测试患者注册功能"""
        print("📝 测试患者注册...")
        
        # 生成唯一的测试数据
        timestamp = int(time.time())
        phone = f"138{timestamp % 100000000:08d}"
        
        register_data = {
            "register_patient": True,
            "name": f"测试患者{timestamp}",
            "password_hash": "test_hash_123",
            "phone": phone,
            "birth_date": "1990-01-01",
            "id_card": f"11010119900101{timestamp % 10000:04d}",
            "email": f"test{timestamp}@example.com"
        }
        
        try:
            response = self.client.send_json_data(register_data)
            if response and response.get('result') == 'chenggongcharu':
                self.log_test("患者注册", True, response)
            else:
                self.log_test("患者注册", False, response)
        except Exception as e:
            self.log_test("患者注册", False, error=e)
    
    def test_doctor_query(self):
        """测试医生信息查询"""
        print("👨‍⚕️ 测试医生信息查询...")
        
        query_data = {
            "query_doctor_info": True,
            "doctor_name": "王医生"
        }
        
        try:
            response = self.client.send_json_data(query_data)
            if response and response.get('result', {}).get('status') == 'success':
                self.log_test("医生信息查询", True, response)
            else:
                self.log_test("医生信息查询", False, response)
        except Exception as e:
            self.log_test("医生信息查询", False, error=e)
    
    def test_appointment_creation(self):
        """测试预约创建"""
        print("📅 测试预约创建...")
        
        # 使用已知的患者和医生数据
        appointment_data = {
            "create_appointment": True,
            "patient_phone": "13800138000",
            "doctor_name": "王医生",
            "appointment_time": "2024-03-15 10:00:00",
            "fee_paid": 1
        }
        
        try:
            response = self.client.send_json_data(appointment_data)
            result = response.get('result', {}) if response else {}
            if result.get('status') == 'success':
                self.log_test("预约创建", True, response)
                return result.get('appointment_info', {}).get('appointment_id')
            else:
                self.log_test("预约创建", False, response)
                return None
        except Exception as e:
            self.log_test("预约创建", False, error=e)
            return None
    
    def test_appointment_query(self):
        """测试预约查询"""
        print("🔍 测试预约查询...")
        
        query_data = {
            "query_appointments": True,
            "patient_phone": "13800138000"
        }
        
        try:
            response = self.client.send_json_data(query_data)
            result = response.get('result', {}) if response else {}
            if result.get('status') == 'success':
                self.log_test("预约查询", True, response)
                return result.get('appointments', [])
            else:
                self.log_test("预约查询", False, response)
                return []
        except Exception as e:
            self.log_test("预约查询", False, error=e)
            return []
    
    def test_sql_query(self):
        """测试SQL查询功能"""
        print("🗄️ 测试SQL查询...")
        
        sql_data = {
            "sql_query": "SELECT COUNT(*) as user_count FROM users"
        }
        
        try:
            response = self.client.send_json_data(sql_data)
            result = response.get('result', {}) if response else {}
            if 'columns' in result and 'data' in result:
                self.log_test("SQL查询", True, response)
            else:
                self.log_test("SQL查询", False, response)
        except Exception as e:
            self.log_test("SQL查询", False, error=e)
    
    def test_concurrent_connections(self, num_threads=5):
        """测试并发连接"""
        print(f"🔄 测试并发连接 ({num_threads}个线程)...")
        
        results = []
        threads = []
        
        def concurrent_test(thread_id):
            try:
                client = JSONProtocolClient(self.host, self.port)
                test_data = {
                    "sql_query": f"SELECT 'Thread-{thread_id}' as thread_id, datetime('now') as timestamp"
                }
                response = client.send_json_data(test_data)
                results.append({
                    'thread_id': thread_id,
                    'success': response is not None,
                    'response': response
                })
            except Exception as e:
                results.append({
                    'thread_id': thread_id,
                    'success': False,
                    'error': str(e)
                })
        
        # 启动并发线程
        for i in range(num_threads):
            thread = threading.Thread(target=concurrent_test, args=(i,))
            threads.append(thread)
            thread.start()
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
        
        # 统计结果
        success_count = sum(1 for r in results if r['success'])
        success_rate = success_count / num_threads * 100
        
        if success_rate >= 80:  # 80%成功率认为通过
            self.log_test(f"并发连接测试 ({success_count}/{num_threads})", True, 
                         {'success_rate': f'{success_rate:.1f}%'})
        else:
            self.log_test(f"并发连接测试 ({success_count}/{num_threads})", False,
                         error=f'成功率仅{success_rate:.1f}%')
    
    def test_error_handling(self):
        """测试错误处理"""
        print("⚠️ 测试错误处理...")
        
        # 测试无效JSON结构
        invalid_data = {
            "invalid_operation": True,
            "random_field": "test"
        }
        
        try:
            response = self.client.send_json_data(invalid_data)
            if response:
                self.log_test("错误处理 - 无效操作", True, response)
            else:
                self.log_test("错误处理 - 无效操作", False, error="无响应")
        except Exception as e:
            self.log_test("错误处理 - 无效操作", False, error=e)
    
    def run_performance_test(self, num_requests=10):
        """性能测试"""
        print(f"⚡ 性能测试 ({num_requests}次请求)...")
        
        start_time = time.time()
        success_count = 0
        response_times = []
        
        for i in range(num_requests):
            request_start = time.time()
            try:
                test_data = {
                    "sql_query": f"SELECT {i} as request_id, datetime('now') as timestamp"
                }
                response = self.client.send_json_data(test_data)
                request_end = time.time()
                
                if response:
                    success_count += 1
                    response_times.append(request_end - request_start)
                    
            except Exception as e:
                print(f"   请求 {i+1} 失败: {e}")
        
        total_time = time.time() - start_time
        
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
            
            performance_result = {
                'total_requests': num_requests,
                'successful_requests': success_count,
                'success_rate': f'{success_count/num_requests*100:.1f}%',
                'total_time': f'{total_time:.2f}s',
                'avg_response_time': f'{avg_response_time*1000:.1f}ms',
                'min_response_time': f'{min_response_time*1000:.1f}ms',
                'max_response_time': f'{max_response_time*1000:.1f}ms',
                'requests_per_second': f'{success_count/total_time:.1f}'
            }
            
            self.log_test("性能测试", True, performance_result)
        else:
            self.log_test("性能测试", False, error="所有请求都失败")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始远程医疗系统服务器测试")
        print(f"目标服务器: {self.host}:{self.port}")
        print("=" * 60)
        
        # 基础连接测试
        if not self.test_connection():
            print("❌ 服务器连接失败，终止测试")
            return
        
        # 功能测试
        self.test_user_login()
        self.test_patient_registration()
        self.test_doctor_query()
        
        appointment_id = self.test_appointment_creation()
        appointments = self.test_appointment_query()
        
        self.test_sql_query()
        self.test_error_handling()
        
        # 性能和并发测试
        self.test_concurrent_connections()
        self.run_performance_test()
        
        # 生成测试报告
        self.generate_report()
    
    def generate_report(self):
        """生成测试报告"""
        print("=" * 60)
        print("📊 测试报告")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"总测试数: {total_tests}")
        print(f"通过: {passed_tests} ✅")
        print(f"失败: {failed_tests} ❌")
        print(f"成功率: {passed_tests/total_tests*100:.1f}%")
        print()
        
        if failed_tests > 0:
            print("失败的测试:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  ❌ {result['test_name']}: {result['error']}")
            print()
        
        # 保存详细报告到文件
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'server': f"{self.host}:{self.port}",
                'test_time': datetime.now().isoformat(),
                'summary': {
                    'total_tests': total_tests,
                    'passed_tests': passed_tests,
                    'failed_tests': failed_tests,
                    'success_rate': f"{passed_tests/total_tests*100:.1f}%"
                },
                'detailed_results': self.test_results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"详细报告已保存到: {report_file}")


def main():
    """主函数"""
    print("医疗系统远程服务器测试工具")
    print("目标服务器: 8.140.225.6:55000")
    print()
    
    # 创建测试器实例
    tester = RemoteMedicalServerTester()
    
    try:
        # 运行所有测试
        tester.run_all_tests()
        
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"\n测试过程中发生错误: {e}")
    
    print("\n测试完成！")


if __name__ == "__main__":
    main()
