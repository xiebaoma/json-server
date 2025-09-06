#include <QCoreApplication>
#include <QTcpSocket>
#include <QFile>
#include <QFileInfo>
#include <QDataStream>
#include <QDebug>
#include <QEventLoop>
#include <iostream>

//8.140.225.6
//55000
bool sendJsonFile(const QString &serverAddress, quint16 port, const QString &filePath)
{
    // 检查文件是否存在
    QFile file(filePath);
    if (!file.exists()) {
        qDebug() << "错误: 文件不存在" << filePath;
        return false;
    }
    
    // 创建TCP socket
    QTcpSocket socket;
    
    qDebug() << "正在连接到服务器" << serverAddress << ":" << port;
    socket.connectToHost(serverAddress, port);
    
    // 等待连接建立
    if (!socket.waitForConnected(5000)) {
        qDebug() << "连接失败:" << socket.errorString();
        return false;
    }
    
    qDebug() << "已连接到服务器";
    
    // 打开并读取文件
    if (!file.open(QIODevice::ReadOnly)) {
        qDebug() << "错误: 无法打开文件" << filePath;
        return false;
    }
    
    QByteArray fileData = file.readAll();
    file.close();
    
    // 获取文件名
    QFileInfo fileInfo(filePath);
    QString fileName = fileInfo.fileName();
    QByteArray fileNameData = fileName.toUtf8();
    
    qDebug() << "文件名:" << fileName;
    qDebug() << "文件大小:" << fileData.size() << "字节";
    
    // 创建数据流来发送数据（网络字节序）
    QDataStream stream(&socket);
    stream.setByteOrder(QDataStream::BigEndian);
    
    // 发送文件名长度和文件名
    stream << static_cast<quint32>(fileNameData.size());
    socket.write(fileNameData);
    
    // 发送文件大小
    stream << static_cast<quint32>(fileData.size());
    
    // 发送文件内容
    socket.write(fileData);
    
    qDebug() << "JSON文件发送完成";
    qDebug() << "发送的JSON内容:";
    qDebug().noquote() << QString::fromUtf8(fileData);
    
    // 等待数据发送完成
    socket.waitForBytesWritten(3000);
    socket.disconnectFromHost();
    
    if (socket.state() != QAbstractSocket::UnconnectedState) {
        socket.waitForDisconnected(3000);
    }
    
    qDebug() << "已断开连接";
    return true;
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    
    // 获取JSON文件路径
    QString jsonFilePath;
    if (argc > 1) {
        jsonFilePath = QString::fromLocal8Bit(argv[1]);
    } else {
        // 默认使用hello.json
        jsonFilePath = "hello.json";
    }
    
    std::cout << "正在发送JSON文件: " << jsonFilePath.toStdString() << std::endl;
    std::cout << "目标服务器: 8.140.225.6:55000" << std::endl;
    
    // 发送JSON文件
    bool success = sendJsonFile("8.140.225.6", 55000, jsonFilePath);
    
    if (success) {
        std::cout << "JSON文件发送成功!" << std::endl;
    } else {
        std::cout << "JSON文件发送失败!" << std::endl;
        return 1;
    }
    
    return 0;
}
