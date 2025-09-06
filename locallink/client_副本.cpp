#include <iostream>
#include <fstream>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>

#define SERVER_IP "8.140.225.6"
#define PORT 55000

int main()
{
    int sock_fd;
    struct sockaddr_in server_addr{};

    // 1. 创建套接字
    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd == -1)
    {
        perror("socket");
        return -1;
    }

    // 2. 连接服务器
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr);

    if (connect(sock_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0)
    {
        perror("connect");
        close(sock_fd);
        return -1;
    }

    std::cout << "请输入要发送的JSON文件路径: ";
    std::string filepath;
    std::getline(std::cin, filepath);

    std::ifstream file(filepath, std::ios::binary | std::ios::ate);
    if (!file)
    {
        std::cerr << "无法打开文件" << std::endl;
        close(sock_fd);
        return -1;
    }

    // 获取文件大小
    std::streamsize filesize = file.tellg();
    file.seekg(0, std::ios::beg);

    // 发送文件名长度和文件名
    std::string filename = filepath.substr(filepath.find_last_of("/\\") + 1);
    uint32_t name_len = htonl(filename.size());
    send(sock_fd, &name_len, sizeof(name_len), 0);
    send(sock_fd, filename.c_str(), filename.size(), 0);

    // 发送文件大小
    uint32_t net_filesize = htonl(filesize);
    send(sock_fd, &net_filesize, sizeof(net_filesize), 0);

    // 发送文件内容
    char buffer[4096];
    while (!file.eof())
    {
        file.read(buffer, sizeof(buffer));
        std::streamsize bytes_read = file.gcount();
        if (bytes_read > 0)
        {
            send(sock_fd, buffer, bytes_read, 0);
        }
    }

    std::cout << "文件发送完成" << std::endl;

    file.close();
    close(sock_fd);
    return 0;
}