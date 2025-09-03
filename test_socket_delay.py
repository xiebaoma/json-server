#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Socket延迟功能
验证socket连接在断开前是否有适当的延迟
"""

import sys
import os
import time
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from network.communication import JSONProtocolClient


def test_socket_delay():
    """测试socket延迟功能"""
    print("🔗 测试Socket延迟功能")
    print("=" * 50)
    
    client = JSONProtocolClient('8.140.225.6', 55000)
    
    # 测试数据
    test_requests = [
        {
            "name": "用户登录测试",
            "data": {
                "login": True,
                "user_name": "13800138000",
                "password": "hash_patient1"
            }
        },
        {
            "name": "SQL查询测试",
            "data": {
                "sql_query": "SELECT COUNT(*) as total_users FROM users"
            }
        },
        {
            "name": "医生信息查询测试",
            "data": {
                "query_doctor_info": True,
                "doctor_name": "王医生"
            }
        }
    ]
    
    for i, test in enumerate(test_requests, 1):
        print(f"\n{i}. {test['name']}")
        print("-" * 30)
        
        start_time = time.time()
        
        try:
            response = client.send_json_data(test['data'])
            end_time = time.time()
            
            if response:
                print(f"✅ 请求成功")
                print(f"⏱️  总耗时: {end_time - start_time:.3f} 秒")
                print(f"📊 响应状态: {response.get('status', 'unknown')}")
                
                # 显示简化的响应结果
                result = response.get('result')
                if isinstance(result, dict):
                    print(f"📝 响应摘要: {len(str(result))} 字符的详细数据")
                else:
                    print(f"📝 响应结果: {result}")
            else:
                print(f"❌ 请求失败")
                print(f"⏱️  总耗时: {end_time - start_time:.3f} 秒")
                
        except Exception as e:
            end_time = time.time()
            print(f"❌ 请求异常: {e}")
            print(f"⏱️  总耗时: {end_time - start_time:.3f} 秒")
        
        # 请求间隔
        if i < len(test_requests):
            print("⏳ 等待1秒后继续下一个测试...")
            time.sleep(1)
    
    print("\n" + "=" * 50)
    print("🎉 Socket延迟测试完成!")
    print("\n💡 延迟说明:")
    print("   • 服务器端: 响应发送后延迟1秒再关闭连接")
    print("   • 客户端: 接收响应后延迟0.1秒再关闭连接")
    print("   • 这样可以确保数据传输的完整性和稳定性")


def test_concurrent_connections():
    """测试并发连接的延迟处理"""
    print("\n🔄 测试并发连接延迟处理")
    print("=" * 50)
    
    import threading
    import concurrent.futures
    
    def single_request(request_id):
        """单个请求测试"""
        client = JSONProtocolClient('8.140.225.6', 55000)
        test_data = {
            "sql_query": f"SELECT {request_id} as request_id, datetime('now') as timestamp"
        }
        
        start_time = time.time()
        try:
            response = client.send_json_data(test_data)
            end_time = time.time()
            
            return {
                'request_id': request_id,
                'success': response is not None,
                'duration': end_time - start_time,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            end_time = time.time()
            return {
                'request_id': request_id,
                'success': False,
                'duration': end_time - start_time,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    # 并发测试
    num_requests = 5
    print(f"📊 启动 {num_requests} 个并发请求...")
    
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(single_request, i) for i in range(num_requests)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    end_time = time.time()
    
    # 分析结果
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    durations = [r['duration'] for r in results if r['success']]
    avg_duration = sum(durations) / len(durations) if durations else 0
    
    print(f"\n📈 并发测试结果:")
    print(f"   • 总请求数: {num_requests}")
    print(f"   • 成功请求: {successful}")
    print(f"   • 失败请求: {failed}")
    print(f"   • 总耗时: {end_time - start_time:.3f} 秒")
    print(f"   • 平均单请求耗时: {avg_duration:.3f} 秒")
    print(f"   • 成功率: {successful/num_requests*100:.1f}%")
    
    if failed > 0:
        print(f"\n❌ 失败请求详情:")
        for result in results:
            if not result['success']:
                print(f"   • 请求 {result['request_id']}: {result.get('error', '未知错误')}")


def main():
    """主函数"""
    print("🧪 Socket延迟功能测试工具")
    print("目标服务器: 8.140.225.6:55000")
    print("=" * 50)
    
    try:
        # 基本延迟测试
        test_socket_delay()
        
        # 并发延迟测试
        test_concurrent_connections()
        
    except KeyboardInterrupt:
        print("\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n💥 测试过程中出现错误: {e}")
    
    print(f"\n🏁 测试完成! - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()


