#ifndef SEND_AND_RECEIVE_H
#define SEND_AND_RECEIVE_H

#include <QCoreApplication>
#include <QtNetwork/QTcpSocket>
#include <QFile>
#include <QFileInfo>
#include <QDataStream>
#include <QDebug>
#include <QEventLoop>
#include <QUuid>
#include <QString>
#include <QByteArray>
#include <QJsonDocument>
#include <QJsonObject>

// 发送JSON数据并接收响应
QJsonObject sendJsonDataAndReceive(const QString &serverAddress, quint16 port, const QByteArray &jsonData, const QString &fileName = "data.json");

// 兼容性函数：只发送不接收（保持向后兼容）
bool sendJsonData(const QString &serverAddress, quint16 port, const QByteArray &jsonData, const QString &fileName);

#endif // SEND_AND_RECEIVE_H
