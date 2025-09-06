import socket
import struct
import os
import sys

def send_json_file(server_address, port, file_path):
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误: 文件不存在 {file_path}")
        return False

    # 读取文件内容
    with open(file_path, "rb") as f:
        file_data = f.read()

    file_name = os.path.basename(file_path)
    file_name_bytes = file_name.encode("utf-8")

    print(f"正在连接到服务器 {server_address}:{port}")
    try:
        # 创建 TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 连接超时 5 秒
        sock.connect((server_address, port))
    except Exception as e:
        print(f"连接失败: {e}")
        return False

    print("已连接到服务器")
    print(f"文件名: {file_name}")
    print(f"文件大小: {len(file_data)} 字节")

    try:
        # 发送 文件名长度 (4字节, 大端)
        sock.sendall(struct.pack(">I", len(file_name_bytes)))
        # 发送 文件名
        sock.sendall(file_name_bytes)

        # 发送 文件大小 (4字节, 大端)
        sock.sendall(struct.pack(">I", len(file_data)))
        # 发送 文件内容
        sock.sendall(file_data)

        print("JSON文件发送完成")
        print("发送的JSON内容:")
        try:
            print(file_data.decode("utf-8"))
        except UnicodeDecodeError:
            print("（文件内容不是有效的UTF-8编码，无法打印）")

        sock.shutdown(socket.SHUT_WR)  # 通知对端发送完成
    except Exception as e:
        print(f"发送失败: {e}")
        sock.close()
        return False

    sock.close()
    print("已断开连接")
    return True


if __name__ == "__main__":
    # 获取 JSON 文件路径
    if len(sys.argv) > 1:
        json_file_path = sys.argv[1]
    else:
        json_file_path = "hello.json"

    print(f"正在发送JSON文件: {json_file_path}")
    print("目标服务器: 8.140.225.6:55000")

    success = send_json_file("8.140.225.6", 55000, json_file_path)

    if success:
        print("JSON文件发送成功!")
    else:
        print("JSON文件发送失败!")
        sys.exit(1)
