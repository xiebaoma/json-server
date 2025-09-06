#include "chatmainwindow.h"
#include "ui_chatmainwindow.h"

ChatMainWindow::ChatMainWindow(const QString &userId, MessageClient *client, QWidget *parent)
    : QMainWindow(parent), ui(new Ui::ChatMainWindow), currentUserId(userId), client(client), currentSender("")
{
    qDebug() << "Creating ChatMainWindow for user:" << userId;
    ui->setupUi(this);
    setFixedSize(716,415);
    setWindowTitle("消息系统 - " + userId);
    //setAttribute(Qt::WA_DeleteOnClose);
    // 连接信号槽
    connect(ui->sendButton, &QPushButton::clicked, this, &ChatMainWindow::onSendClicked);
    connect(ui->replyButton, &QPushButton::clicked, this, &ChatMainWindow::onReplyClicked);
    connect(ui->refreshButton, &QPushButton::clicked, this, &ChatMainWindow::onRefreshSenders);
    connect(ui->sendersList, &QListWidget::itemClicked, this, &ChatMainWindow::onSendersItemClicked);
    connect(client, &MessageClient::sendersReceived, this, &ChatMainWindow::onSendersReceived);
    connect(client, &MessageClient::messagesReceived, this, &ChatMainWindow::onMessagesReceived);
    connect(client, &MessageClient::sendResult, this, &ChatMainWindow::onSendResult);
    connect(client, &MessageClient::replyResult, this, &ChatMainWindow::onReplyResult);
    connect(client, &MessageClient::errorOccurred, this, &ChatMainWindow::onErrorOccurred);

    // 加载发送者列表
    loadSenders();
}

ChatMainWindow::~ChatMainWindow()
{
    delete ui;
}

void ChatMainWindow::onSendClicked()
{
    QString toUser = ui->toUserEdit->text().trimmed();
    QString message = ui->messageEdit->toPlainText().trimmed();

    if (toUser.isEmpty() || message.isEmpty()) {
        QMessageBox::warning(this, "错误", "请输入接收用户ID和消息内容");
        return;
    }

    client->sendMessage(toUser, message);
    ui->messageEdit->clear();
}

void ChatMainWindow::onReplyClicked()
{
    if (currentSender.isEmpty()) {
        QMessageBox::warning(this, "错误", "请先选择一个发送者");
        return;
    }

    QString message = ui->replyEdit->toPlainText().trimmed();
    if (message.isEmpty()) {
        QMessageBox::warning(this, "错误", "请输入回复内容");
        return;
    }

    client->replyMessage(currentSender, message);
    ui->replyEdit->clear();
}

void ChatMainWindow::onRefreshSenders()
{
    loadSenders();
}

void ChatMainWindow::onSendersItemClicked(QListWidgetItem *item)
{
    currentSender = item->text();
    client->getMessages(currentSender);
}

void ChatMainWindow::onSendersReceived(const QStringList &senders)
{
    ui->sendersList->clear();
    if (senders.isEmpty()) {
        ui->sendersList->addItem("暂无消息");
    } else {
        ui->sendersList->addItems(senders);
    }
}

void ChatMainWindow::onMessagesReceived(const QString &fromUser, const QStringList &messages)
{
    ui->messagesText->clear();
    ui->messagesText->append("来自 " + fromUser + " 的消息:");
    ui->messagesText->append("");

    for (const QString &message : messages) {
        ui->messagesText->append(message);
        ui->messagesText->append("");
    }
}

void ChatMainWindow::onSendResult(bool success, const QString &message)
{
    if (success) {
        ui->statusLabel->setText("消息发送成功");
        QMessageBox::information(this, "成功", "消息发送成功");
    } else {
        QMessageBox::warning(this, "发送失败", message);
    }
}

void ChatMainWindow::onReplyResult(bool success, const QString &message)
{
    if (success) {
        ui->statusLabel->setText("回复发送成功");
        QMessageBox::information(this, "成功", "回复发送成功");
    } else {
        QMessageBox::warning(this, "回复失败", message);
    }
}

void ChatMainWindow::onErrorOccurred(const QString &error)
{
    QMessageBox::critical(this, "错误", error);
}

void ChatMainWindow::loadSenders()
{
    client->getSenders();
}
