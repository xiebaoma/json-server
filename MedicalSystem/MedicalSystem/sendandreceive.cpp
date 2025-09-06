#include "sendAndReceive.h"


bool sendJsonData(const QString &serverAddress, quint16 port, const QByteArray &jsonData, const QString &fileName)
{
    // 创建 TCP socket
    QTcpSocket socket;

    qDebug() << "正在连接到服务器" << serverAddress << ":" << port;
    socket.connectToHost(serverAddress, port);

    // 等待连接建立
    if (!socket.waitForConnected(5000))
    {
        qDebug() << "连接失败:" << socket.errorString();
        return false;
    }

    qDebug() << "已连接到服务器";

    // 获取文件名
    QByteArray fileNameData = fileName.toUtf8();

    qDebug() << "文件名:" << fileName;
    qDebug() << "数据大小:" << jsonData.size() << "字节";

    // 按照test_client.py的协议发送数据
    // 1. 发送文件名长度（4字节，网络字节序）
    quint32 fileNameLength = static_cast<quint32>(fileNameData.size());
    QByteArray fileNameLengthBytes;
    QDataStream fileNameLengthStream(&fileNameLengthBytes, QIODevice::WriteOnly);
    fileNameLengthStream.setByteOrder(QDataStream::BigEndian);
    fileNameLengthStream << fileNameLength;
    
    qint64 sent1 = socket.write(fileNameLengthBytes);
    qDebug() << "发送文件名长度:" << fileNameLength << "字节数:" << sent1;

    // 2. 发送文件名
    qint64 sent2 = socket.write(fileNameData);
    qDebug() << "发送文件名:" << fileName << "字节数:" << sent2;

    // 3. 发送JSON数据长度（4字节，网络字节序）  
    quint32 jsonDataLength = static_cast<quint32>(jsonData.size());
    QByteArray jsonDataLengthBytes;
    QDataStream jsonDataLengthStream(&jsonDataLengthBytes, QIODevice::WriteOnly);
    jsonDataLengthStream.setByteOrder(QDataStream::BigEndian);
    jsonDataLengthStream << jsonDataLength;
    
    qint64 sent3 = socket.write(jsonDataLengthBytes);
    qDebug() << "发送JSON数据长度:" << jsonDataLength << "字节数:" << sent3;

    // 4. 发送JSON数据内容
    qint64 sent4 = socket.write(jsonData);
    qDebug() << "发送JSON数据内容，字节数:" << sent4;

    // 检查是否所有数据都发送成功
    if (sent1 <= 0 || sent2 <= 0 || sent3 <= 0 || sent4 <= 0)
    {
        qDebug() << "数据发送失败！";
        return false;
    }

    qDebug() << "JSON 数据发送完成";
    qDebug() << "发送的 JSON 内容:";
    qDebug().noquote() << QString::fromUtf8(jsonData);

    // 等待数据发送完成
    socket.waitForBytesWritten(3000);
    socket.disconnectFromHost();

    if (socket.state() != QAbstractSocket::UnconnectedState)
    {
        socket.waitForDisconnected(3000);
    }

    qDebug() << "已断开连接";
    return true;
}
