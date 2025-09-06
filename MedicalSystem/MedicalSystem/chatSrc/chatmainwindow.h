#ifndef CHATMAINWINDOW_H
#define CHATMAINWINDOW_H
#include <QMainWindow>
#include <QListWidget>
#include <QTextEdit>
#include <QLineEdit>
#include <QPushButton>
#include <QLabel>
#include <QSplitter>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QMessageBox>
#include "messageclient.h"
#include <QWidget>

namespace Ui {
class ChatMainWindow;
}

class ChatMainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit ChatMainWindow(const QString &userId, MessageClient *client, QWidget *parent = nullptr);
    ~ChatMainWindow();

private slots:
    void onSendClicked();
    void onSendersReceived(const QStringList &senders);
    void onMessagesReceived(const QString &fromUser, const QStringList &messages);
    void onSendResult(bool success, const QString &message);
    void onReplyResult(bool success, const QString &message);
    void onErrorOccurred(const QString &error);
    void onSendersItemClicked(QListWidgetItem *item);
    void onRefreshSenders();
    void onReplyClicked();

private:
    Ui::ChatMainWindow *ui;
    QString currentUserId;
    MessageClient *client;
    QString currentSender;

    void loadSenders();
};

#endif // CHATMAINWINDOW_H
