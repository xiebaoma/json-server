#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医疗系统服务器启动脚本
提供命令行接口和服务管理功能
"""

import sys
import os
import argparse
import time

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.medical_server import MedicalServer
from utils.server_manager import ServerManager


def start_server(args):
    """启动服务器"""
    # 创建服务器管理器来检查状态
    server_manager = ServerManager(args.pid_file, args.log_file)
    
    # 检查服务器是否已经在运行
    if server_manager.is_server_running():
        existing_pid = server_manager.get_server_pid()
        print(f"服务器已在运行 (PID: {existing_pid})")
        return False
    
    print("启动医疗系统JSON数据库服务器...")
    
    if args.daemon:
        print("以守护进程模式启动...")
    
    # 创建服务器实例
    server = MedicalServer(
        host=args.host, 
        port=args.port, 
        db_path=args.db_path,
        log_file=args.log_file,
        pid_file=args.pid_file
    )
    
    try:
        # 启动服务器
        success = server.start_server(daemon=args.daemon)
        if not success:
            return False
    except KeyboardInterrupt:
        if not args.daemon:
            print("\n收到中断信号，正在关闭服务器...")
        server.stop_server()
    except Exception as e:
        print(f"服务器运行时出错: {e}")
        return False
    
    if not args.daemon:
        print("服务器已关闭")
    
    return True


def stop_server(args):
    """停止服务器"""
    server_manager = ServerManager(args.pid_file, args.log_file)
    return server_manager.stop_server()


def restart_server(args):
    """重启服务器"""
    print("重启服务器...")
    server_manager = ServerManager(args.pid_file, args.log_file)
    server_manager.stop_server()
    time.sleep(2)  # 等待2秒确保完全停止
    return start_server(args)


def status_server(args):
    """查看服务器状态"""
    server_manager = ServerManager(args.pid_file, args.log_file)
    pid = server_manager.get_server_pid()
    
    if pid:
        print(f"服务器正在运行 (PID: {pid})")
        print(f"配置信息:")
        print(f"  监听地址: {args.host}:{args.port}")
        print(f"  数据库文件: {args.db_path}")
        print(f"  日志文件: {args.log_file}")
        print(f"  PID文件: {args.pid_file}")
        return True
    else:
        print("服务器未在运行")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='医疗系统JSON数据库服务器')
    parser.add_argument('action', choices=['start', 'stop', 'restart', 'status'], 
                       help='操作: start(启动), stop(停止), restart(重启), status(状态)')
    parser.add_argument('--host', default='0.0.0.0', help='监听地址 (默认: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=55000, help='监听端口 (默认: 55000)')
    parser.add_argument('--db-path', default='/medical/MedicalSystem.db', help='数据库文件路径')
    parser.add_argument('--log-file', default='/medical/server.log', help='日志文件路径')
    parser.add_argument('--pid-file', default='/medical/server.pid', help='PID文件路径')
    parser.add_argument('--daemon', action='store_true', help='以守护进程模式运行')
    parser.add_argument('--foreground', action='store_true', help='前台运行（覆盖--daemon）')
    
    args = parser.parse_args()
    
    # 如果指定了--foreground，覆盖--daemon设置
    if args.foreground:
        args.daemon = False
    elif args.action == 'start' and not args.foreground:
        # 默认以守护进程模式启动
        args.daemon = True
    
    # 执行相应操作
    actions = {
        'start': start_server,
        'stop': stop_server,
        'restart': restart_server,
        'status': status_server
    }
    
    action_func = actions[args.action]
    success = action_func(args)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
