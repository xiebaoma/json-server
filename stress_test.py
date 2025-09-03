#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医疗系统服务器压力测试
目标服务器: 8.140.225.6:55000
"""

import sys
import os
import json
import time
import threading
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from network.communication import JSONProtocolClient


class StressTester:
    def __init__(self, host='8.140.225.6', port=55000):
        self.host = host
        self.port = port
        self.results = []
        self.lock = threading.Lock()
    
    def single_request_test(self, request_id, test_data):
        """单个请求测试"""
        start_time = time.time()
        try:
            client = JSONProtocolClient(self.host, self.port)
            response = client.send_json_data(test_data)
            end_time = time.time()
            
            result = {
                'request_id': request_id,
                'success': response is not None,
                'response_time': end_time - start_time,
                'timestamp': datetime.now().isoformat(),
                'response': response
            }
            
            with self.lock:
                self.results.append(result)
            
            return result
            
        except Exception as e:
            end_time = time.time()
            result = {
                'request_id': request_id,
                'success': False,
                'response_time': end_time - start_time,
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
            
            with self.lock:
                self.results.append(result)
            
            return result
    
    def concurrent_test(self, num_threads=10, requests_per_thread=10):
        """并发测试"""
        print(f"🔄 开始并发测试: {num_threads}个线程，每线程{requests_per_thread}个请求")
        print(f"总请求数: {num_threads * requests_per_thread}")
        
        self.results = []
        
        # 准备测试数据
        test_cases = [
            {"sql_query": "SELECT COUNT(*) FROM users"},
            {"query_doctor_info": True, "doctor_name": "王医生"},
            {"login": True, "user_name": "13800138000", "password": "hash_patient1"},
            {"query_appointments": True, "patient_phone": "13800138000"}
        ]
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            
            for thread_id in range(num_threads):
                for req_id in range(requests_per_thread):
                    request_id = thread_id * requests_per_thread + req_id
                    test_data = test_cases[request_id % len(test_cases)]
                    
                    future = executor.submit(self.single_request_test, request_id, test_data)
                    futures.append(future)
            
            # 等待所有请求完成
            completed = 0
            for future in as_completed(futures):
                completed += 1
                if completed % 10 == 0:
                    print(f"已完成: {completed}/{len(futures)}")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # 分析结果
        self.analyze_results(total_time)
    
    def sequential_test(self, num_requests=50):
        """顺序测试"""
        print(f"📈 开始顺序测试: {num_requests}个请求")
        
        self.results = []
        
        test_data = {"sql_query": "SELECT datetime('now') as current_time"}
        
        start_time = time.time()
        
        for i in range(num_requests):
            if i % 10 == 0:
                print(f"进度: {i}/{num_requests}")
            
            self.single_request_test(i, test_data)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # 分析结果
        self.analyze_results(total_time)
    
    def analyze_results(self, total_time):
        """分析测试结果"""
        if not self.results:
            print("❌ 没有测试结果")
            return
        
        # 基本统计
        total_requests = len(self.results)
        successful_requests = sum(1 for r in self.results if r['success'])
        failed_requests = total_requests - successful_requests
        success_rate = (successful_requests / total_requests) * 100
        
        # 响应时间统计
        response_times = [r['response_time'] for r in self.results if r['success']]
        
        if response_times:
            avg_response_time = statistics.mean(response_times)
            median_response_time = statistics.median(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            
            # 计算百分位数
            response_times_sorted = sorted(response_times)
            p95_response_time = response_times_sorted[int(0.95 * len(response_times_sorted))]
            p99_response_time = response_times_sorted[int(0.99 * len(response_times_sorted))]
        else:
            avg_response_time = median_response_time = min_response_time = max_response_time = 0
            p95_response_time = p99_response_time = 0
        
        # 吞吐量
        throughput = successful_requests / total_time if total_time > 0 else 0
        
        # 打印结果
        print("\n" + "=" * 60)
        print("📊 压力测试结果")
        print("=" * 60)
        print(f"测试时间: {total_time:.2f} 秒")
        print(f"总请求数: {total_requests}")
        print(f"成功请求: {successful_requests}")
        print(f"失败请求: {failed_requests}")
        print(f"成功率: {success_rate:.2f}%")
        print(f"吞吐量: {throughput:.2f} 请求/秒")
        print()
        print("响应时间统计 (毫秒):")
        print(f"  平均: {avg_response_time * 1000:.1f} ms")
        print(f"  中位数: {median_response_time * 1000:.1f} ms")
        print(f"  最小: {min_response_time * 1000:.1f} ms")
        print(f"  最大: {max_response_time * 1000:.1f} ms")
        print(f"  95%: {p95_response_time * 1000:.1f} ms")
        print(f"  99%: {p99_response_time * 1000:.1f} ms")
        
        # 错误分析
        if failed_requests > 0:
            print(f"\n❌ 错误分析 ({failed_requests} 个失败):")
            error_counts = {}
            for result in self.results:
                if not result['success']:
                    error = result.get('error', 'Unknown error')
                    error_counts[error] = error_counts.get(error, 0) + 1
            
            for error, count in error_counts.items():
                print(f"  {error}: {count} 次")
        
        # 保存详细结果
        self.save_results(total_time, {
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'failed_requests': failed_requests,
            'success_rate': success_rate,
            'throughput': throughput,
            'avg_response_time': avg_response_time,
            'median_response_time': median_response_time,
            'min_response_time': min_response_time,
            'max_response_time': max_response_time,
            'p95_response_time': p95_response_time,
            'p99_response_time': p99_response_time
        })
    
    def save_results(self, total_time, summary):
        """保存测试结果到文件"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"stress_test_result_{timestamp}.json"
        
        report = {
            'server': f"{self.host}:{self.port}",
            'test_time': datetime.now().isoformat(),
            'total_duration': total_time,
            'summary': summary,
            'detailed_results': self.results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 详细结果已保存到: {filename}")
    
    def connection_test(self):
        """连接测试"""
        print("🔗 测试服务器连接...")
        
        test_data = {"test": "connection"}
        result = self.single_request_test(0, test_data)
        
        if result['success']:
            print(f"✅ 连接成功 (响应时间: {result['response_time']*1000:.1f} ms)")
            return True
        else:
            print(f"❌ 连接失败: {result.get('error', '未知错误')}")
            return False


def main():
    """主函数"""
    print("🚀 医疗系统服务器压力测试工具")
    print("目标服务器: 8.140.225.6:55000")
    print("=" * 60)
    
    tester = StressTester()
    
    # 连接测试
    if not tester.connection_test():
        print("无法连接到服务器，测试终止")
        return
    
    print("\n请选择测试类型:")
    print("1. 轻量测试 (10个并发，每个5次请求)")
    print("2. 中等测试 (20个并发，每个10次请求)")
    print("3. 重度测试 (50个并发，每个20次请求)")
    print("4. 顺序测试 (100个顺序请求)")
    print("5. 自定义测试")
    
    try:
        choice = input("\n请输入选择 (1-5): ").strip()
        
        if choice == '1':
            tester.concurrent_test(num_threads=10, requests_per_thread=5)
        elif choice == '2':
            tester.concurrent_test(num_threads=20, requests_per_thread=10)
        elif choice == '3':
            tester.concurrent_test(num_threads=50, requests_per_thread=20)
        elif choice == '4':
            tester.sequential_test(num_requests=100)
        elif choice == '5':
            threads = int(input("并发线程数: "))
            requests = int(input("每线程请求数: "))
            tester.concurrent_test(num_threads=threads, requests_per_thread=requests)
        else:
            print("无效选择，执行默认轻量测试")
            tester.concurrent_test(num_threads=10, requests_per_thread=5)
            
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"\n测试过程中发生错误: {e}")
    
    print("\n压力测试完成！")


if __name__ == "__main__":
    main()
