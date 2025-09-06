#include "messageclient.h"
#include <QHostAddress>

MessageClient::MessageClient(QObject *parent) : QObject(parent), socket(nullptr), loggedIn(false)
{
    socket = new QTcpSocket(this);

    connect(socket, &QTcpSocket::connected, this, &MessageClient::onConnected);
    connect(socket, &QTcpSocket::disconnected, this, &MessageClient::onDisconnected);
    connect(socket, &QTcpSocket::readyRead, this, &MessageClient::onReadyRead);
    connect(socket, &QTcpSocket::errorOccurred, this, &MessageClient::onErrorOccurred);
}

MessageClient::~MessageClient()
{
    disconnectFromServer();
}

void MessageClient::connectToServer(const QString &host, quint16 port)
{
    socket->connectToHost(host, port);
}

void MessageClient::disconnectFromServer()
{
    if (socket && socket->state() == QAbstractSocket::ConnectedState) {
        socket->disconnectFromHost();
    }
}

void MessageClient::login(const QString &userId)
{
    if (!socket->isOpen()) {
        emit loginResult(false, "Not connected to server");
        return;
    }

    currentUserId = userId;
    QString message = "LOGIN " + userId;
    socket->write(message.toUtf8());
}

void MessageClient::sendMessage(const QString &toUser, const QString &message)
{
    if (!loggedIn) {
        emit sendResult(false, "Not logged in");
        return;
    }

    QString cmd = "SEND " + toUser + " " + message;
    socket->write(cmd.toUtf8());
}

void MessageClient::getSenders()
{
    if (!loggedIn) {
        emit errorOccurred("Not logged in");
        return;
    }

    QString cmd = "GETSENDERS " + currentUserId;
    socket->write(cmd.toUtf8());
}

void MessageClient::getMessages(const QString &fromUser)
{
    if (!loggedIn) {
        emit errorOccurred("Not logged in");
        return;
    }

    QString cmd = "GETMESSAGES " + currentUserId + " " + fromUser;
    socket->write(cmd.toUtf8());
}

void MessageClient::replyMessage(const QString &toUser, const QString &message)
{
    if (!loggedIn) {
        emit replyResult(false, "Not logged in");
        return;
    }

    QString cmd = "REPLY " + toUser + " " + message;
    socket->write(cmd.toUtf8());
}

bool MessageClient::isConnected() const
{
    return socket && socket->state() == QAbstractSocket::ConnectedState;
}

QString MessageClient::getCurrentUserId() const
{
    return currentUserId;
}

void MessageClient::onConnected()
{
    loggedIn = false;
    emit connected();
}

void MessageClient::onDisconnected()
{
    loggedIn = false;
    emit disconnected();
}

void MessageClient::onReadyRead()
{
    QByteArray data = socket->readAll();
    QString response = QString::fromUtf8(data);

    if (response.startsWith("OK Login successful")) {
        loggedIn = true;
        emit loginResult(true, "Login successful");
    }
    else if (response.startsWith("ERROR")) {
        emit errorOccurred(response);
    }
    else if (response.startsWith("OK Message sent")) {
        emit sendResult(true, response);
    }
    else if (response.startsWith("OK Reply sent")) {
        emit replyResult(true, response);
    }
    else if (response.startsWith("SENDERS")) {
        QStringList parts = response.split(" ");
        parts.removeFirst(); // Remove "SENDERS"
        emit sendersReceived(parts);
    }
    else if (response.startsWith("MESSAGES")) {
        QString content = response.mid(9); // Remove "MESSAGES"
        QStringList messageParts = content.split("|", Qt::SkipEmptyParts);

        QStringList messages;
        QString fromUser;

        // 消息格式: |timestamp|from|content|
        for (int i = 0; i < messageParts.size(); i += 3) {
            if (i + 2 < messageParts.size()) {
                QString timestamp = messageParts[i].trimmed();
                fromUser = messageParts[i + 1].trimmed();
                QString content = messageParts[i + 2].trimmed();
                messages << timestamp + " - " + fromUser + ": " + content;
            }
        }

        emit messagesReceived(fromUser, messages);
    }
    else if (response == "NONE") {
        // Handle empty responses
        emit sendersReceived(QStringList());
    }
    else {
        emit errorOccurred("Unknown response: " + response);
    }
}

void MessageClient::onErrorOccurred(QAbstractSocket::SocketError error)
{
    emit errorOccurred(socket->errorString());
}

