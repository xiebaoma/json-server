#!/bin/bash

# JSON数据库服务器控制脚本

SERVER_SCRIPT="$(dirname "$0")/integrated_server.py"
PYTHON_CMD="python3"

# 检查Python脚本是否存在
if [ ! -f "$SERVER_SCRIPT" ]; then
    echo "错误: 找不到服务器脚本 $SERVER_SCRIPT"
    exit 1
fi

# 显示帮助信息
show_help() {
    echo "用法: $0 {start|stop|restart|status|logs|foreground}"
    echo ""
    echo "命令:"
    echo "  start      - 启动服务器（后台运行）"
    echo "  stop       - 停止服务器"
    echo "  restart    - 重启服务器"
    echo "  status     - 查看服务器状态"
    echo "  logs       - 查看服务器日志"
    echo "  foreground - 前台启动服务器（用于调试）"
    echo ""
    echo "示例:"
    echo "  $0 start              # 后台启动服务器"
    echo "  $0 foreground         # 前台启动服务器"
    echo "  $0 status             # 查看状态"
    echo "  $0 logs               # 查看日志"
}

# 启动服务器
start_server() {
    echo "启动JSON数据库服务器..."
    $PYTHON_CMD "$SERVER_SCRIPT" start --daemon
}

# 停止服务器
stop_server() {
    echo "停止JSON数据库服务器..."
    $PYTHON_CMD "$SERVER_SCRIPT" stop
}

# 重启服务器
restart_server() {
    echo "重启JSON数据库服务器..."
    $PYTHON_CMD "$SERVER_SCRIPT" restart
}

# 查看状态
status_server() {
    $PYTHON_CMD "$SERVER_SCRIPT" status
}

# 前台启动
foreground_server() {
    echo "前台启动JSON数据库服务器..."
    echo "按 Ctrl+C 停止服务器"
    $PYTHON_CMD "$SERVER_SCRIPT" start --foreground
}

# 查看日志
show_logs() {
    LOG_FILE="/medical/server.log"
    if [ -f "$LOG_FILE" ]; then
        echo "显示服务器日志 ($LOG_FILE):"
        echo "按 Ctrl+C 退出日志查看"
        tail -f "$LOG_FILE"
    else
        echo "日志文件不存在: $LOG_FILE"
        exit 1
    fi
}

# 主函数
case "$1" in
    start)
        start_server
        ;;
    stop)
        stop_server
        ;;
    restart)
        restart_server
        ;;
    status)
        status_server
        ;;
    logs)
        show_logs
        ;;
    foreground)
        foreground_server
        ;;
    *)
        show_help
        exit 1
        ;;
esac

exit $?
