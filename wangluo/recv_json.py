import os
import socket
import struct
import logging
import daemon  # pip install python-daemon

PORT = 55000
SAVE_DIR = "/xiebaoma/json"
LOG_FILE = "/xiebaoma/server.log"

# 确保日志目录存在
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# 配置日志（用全局 logger）
logger = logging.getLogger("server")
logger.setLevel(logging.INFO)

# 文件 handler
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
logger.addHandler(file_handler)

def log_message(msg: str):
    logger.info(msg)

def run_server():
    # 确保保存目录存在
    os.makedirs(SAVE_DIR, exist_ok=True)

    # 创建 TCP socket
    server_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 绑定端口
    server_fd.bind(("0.0.0.0", PORT))
    server_fd.listen(5)

    log_message("服务器已启动，等待连接...")

    while True:
        client_fd, addr = server_fd.accept()
        log_message(f"客户端已连接: {addr}")

        try:
            # 接收文件名长度
            raw_len = client_fd.recv(4)
            if not raw_len:
                client_fd.close()
                continue
            name_len = struct.unpack("!I", raw_len)[0]

            # 接收文件名
            filename = client_fd.recv(name_len).decode("utf-8")

            # 接收文件大小
            raw_size = client_fd.recv(4)
            if not raw_size:
                client_fd.close()
                continue
            filesize = struct.unpack("!I", raw_size)[0]

            # 保存文件
            save_path = os.path.join(SAVE_DIR, filename)
            received = 0
            with open(save_path, "wb") as f:
                while received < filesize:
                    chunk = client_fd.recv(min(4096, filesize - received))
                    if not chunk:
                        break
                    f.write(chunk)
                    received += len(chunk)

            log_message(f"文件已保存到: {save_path}")

        except Exception as e:
            log_message(f"错误: {e}")
        finally:
            client_fd.close()

def main():
    # 保留日志文件句柄，避免被 DaemonContext 关闭
    with daemon.DaemonContext(files_preserve=[file_handler.stream]):
        run_server()

if __name__ == "__main__":
    main()