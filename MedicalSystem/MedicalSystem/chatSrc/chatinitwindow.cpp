#include "chatinitwindow.h"
#include "ui_chatinitwindow.h"

ChatInitWindow::ChatInitWindow(QWidget *parent,QString ID,QString Role)
    : QWidget(parent)
    , ui(new Ui::ChatInitWindow)
    , loginID(ID)
    , loginRole(Role)
{
    ui->setupUi(this);
    setWindowTitle("消息系统 - 登录");

    client = new MessageClient(this);

    qDebug() << "Client pointer:" << client;
    qDebug() << "Client is valid:" << (client != nullptr);

    connect(ui->loginButton, &QPushButton::clicked, this, &ChatInitWindow::onLoginClicked);
    connect(client, &MessageClient::loginResult, this, &ChatInitWindow::onLoginResult);
    connect(client, &MessageClient::connected, this, &ChatInitWindow::onConnected);
    connect(client, &MessageClient::errorOccurred, this, &ChatInitWindow::onErrorOccurred);
    //连接到本地服务器
    client->connectToServer("119.3.255.213", 8080);
    qDebug() << "client connect";
    loginID=ID;
    loginRole=Role;
    //认证信息自动输入
    inputInfo();
}

ChatInitWindow::~ChatInitWindow()
{
    delete ui;
}

//自动输入认证信息
void ChatInitWindow::inputInfo(){
    ui->userIdEdit->setText(loginID);
}

void ChatInitWindow::onLoginClicked()
{
    QString userId = ui->userIdEdit->text().trimmed();
    if (userId.isEmpty()) {
        QMessageBox::warning(this, "错误", "请输入用户ID");
        return;
    }

    ui->loginButton->setEnabled(false);
    ui->statusLabel->setText("正在登录...");

    client->login(userId);
}

void ChatInitWindow::onLoginResult(bool success, const QString &message)
{
    ui->loginButton->setEnabled(true);

    if (success) {
        ui->statusLabel->setText("登录成功");
        emit loginSuccess(ui->userIdEdit->text());
    } else {
        ui->statusLabel->setText("登录失败: " + message);
        QMessageBox::warning(this, "登录失败", message);
    }
}

void ChatInitWindow::onConnected()
{
    ui->statusLabel->setText("已连接到服务器");
}

void ChatInitWindow::onErrorOccurred(const QString &error)
{
    ui->statusLabel->setText("错误: " + error);
    QMessageBox::critical(this, "错误", error);
}
