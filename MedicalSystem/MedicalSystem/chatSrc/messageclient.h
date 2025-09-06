#ifndef MESSAGECLIENT_H
#define MESSAGECLIENT_H

#include <QObject>
#include <QTcpSocket>
#include <QString>

class MessageClient : public QObject
{
    Q_OBJECT

public:
    explicit MessageClient(QObject *parent = nullptr);
    ~MessageClient();

    void connectToServer(const QString &host, quint16 port);
    void login(const QString &userId);
    void sendMessage(const QString &toUser, const QString &message);
    void getSenders();
    void getMessages(const QString &fromUser);
    void replyMessage(const QString &toUser, const QString &message);
    void disconnectFromServer();

    bool isConnected() const;
    QString getCurrentUserId() const;

signals:
    void connected();
    void disconnected();
    void loginResult(bool success, const QString &message);
    void sendResult(bool success, const QString &message);
    void sendersReceived(const QStringList &senders);
    void messagesReceived(const QString &fromUser, const QStringList &messages);
    void replyResult(bool success, const QString &message);
    void errorOccurred(const QString &error);

private slots:
    void onConnected();
    void onDisconnected();
    void onReadyRead();
    void onErrorOccurred(QAbstractSocket::SocketError error);

private:
    QTcpSocket *socket;
    QString currentUserId;
    bool loggedIn;
};

#endif // MESSAGECLIENT_H
