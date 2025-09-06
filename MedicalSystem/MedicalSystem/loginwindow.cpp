#include "loginwindow.h"
#include "doctormainwindow.h"
#include "mainwindow_patient.h"
#include "./chatSrc/chatsysteminit.h"
#include "sendandreceive.h"
#include <QWidget>
#include <QMessageBox>
#include <QFormLayout>
#include <QVBoxLayout>
#include <QFile>
#include <QTextStream>
#include <QHostAddress>
#include <QJsonDocument>
#include <QJsonObject>
#include <QDebug>

LoginWindow::LoginWindow(QWidget *parent)
    : QMainWindow(parent)
{
    // 设置窗口标题和大小、样式
    setWindowTitle("北京理工大学第二医院");
    resize(400, 400);
    setStyleSheet("QMainWindow { background-color: white; }");

    // 创建中心部件和主垂直布局
    QWidget *centralWidget = new QWidget(this);
    QVBoxLayout *mainLayout = new QVBoxLayout(centralWidget);
    mainLayout->setContentsMargins(20, 20, 20, 20);
    mainLayout->setSpacing(15);

    // 创建表单布局
    QFormLayout *formLayout = new QFormLayout();
    formLayout->setSpacing(15);


    titleLabel = new QLabel("账号登录", centralWidget);
    titleLabel->setAlignment(Qt::AlignCenter);
    titleLabel->setStyleSheet("QLabel { "
                              "font-size: 26px; "
                              "font-weight: bold;"
                              "font-family: FangSong; "
                              "color: black; "
                              "margin: 20px 0px; "
                              "}");
    formLayout->addRow(titleLabel);
    // 角色选择
    roleCombo = new QComboBox(centralWidget);
    roleCombo->addItems({"患者", "医生"});
    roleCombo->setStyleSheet(
        "QComboBox { border: 1px solid #ccc; border-radius: 5px; padding: 5px; color: #808080;}");
    QLabel *roleLabel = new QLabel("角色:", centralWidget);
    roleLabel->setStyleSheet("QLabel { color: black; }");
    formLayout->addRow(roleLabel, roleCombo);

    // 账号输入框
    accountLabel = new QLabel("手机号:", centralWidget);
    accountLabel->setStyleSheet("font: 14px 'Arial'; color: black;");
    accountEdit = new QLineEdit(centralWidget);
    accountEdit->setPlaceholderText("请输入手机号");
    accountEdit->setStyleSheet("font:color:black;");
    accountEdit->setStyleSheet(
        "QLineEdit { border: 1px solid #ccc; border-radius: 5px; padding: 5px; color: black;}"
        "QLineEdit:focus { border-color: #007bff; }");
    formLayout->addRow(accountLabel, accountEdit);

    // 密码输入框
    QLabel *passwordLabel = new QLabel("密码:", centralWidget);
    passwordLabel->setStyleSheet("font: 14px 'Arial'; color: black;");
    passwordEdit = new QLineEdit(centralWidget);
    passwordEdit->setEchoMode(QLineEdit::Password);
    passwordEdit->setPlaceholderText("请输入密码");
    passwordEdit->setStyleSheet(
        "QLineEdit { border: 1px solid #ccc; border-radius: 5px; padding: 5px;}"
        "QLineEdit:focus { border-color: #007bff; }");
    formLayout->addRow(passwordLabel, passwordEdit);

    // 登录按钮
    loginButton = new QPushButton("登录", centralWidget);
    loginButton->setStyleSheet(
        "QPushButton { background-color: #FF6200; color: white; border-radius: 5px; padding: 8px; font: 14px 'Arial'; }"
        "QPushButton:hover { background-color: #FF9800; }"
        "QPushButton:pressed { background-color: #FF8C00; }");
    formLayout->addRow(loginButton);

    // 注册按钮
    registerButton = new QPushButton("注册", centralWidget);
    registerButton->setStyleSheet(
        "QPushButton { background-color: #28a745; color: white; border-radius: 5px; padding: 8px; font: 14px 'Arial'; }"
        "QPushButton:hover { background-color: #218838; }"
        "QPushButton:pressed { background-color: #1e7e34; }");
    formLayout->addRow(registerButton);

    // 重置密码按钮
    resetPasswordButton = new QPushButton("重置密码", centralWidget);
    resetPasswordButton->setStyleSheet(
        "QPushButton { background-color: #9E9E9E; color: white; border-radius: 5px; padding: 8px; font: 14px 'Arial'; }"
        "QPushButton:hover { background-color: #4A4A4A; }"
        "QPushButton:pressed { background-color: #808080; }");
    formLayout->addRow(resetPasswordButton);

    // 医患沟通按钮（测试用）
    chatButton = new QPushButton("医患沟通", centralWidget);
    chatButton->setStyleSheet(
        "QPushButton { background-color: #9E9E9E; color: white; border-radius: 5px; padding: 8px; font: 14px 'Arial'; }"
        "QPushButton:hover { background-color: #4A4A4A; }"
        "QPushButton:pressed { background-color: #808080; }");
    formLayout->addRow(chatButton);

    // 居中布局、设置中心部件
    mainLayout->addStretch(1);
    mainLayout->addLayout(formLayout);
    mainLayout->addStretch(3);
    setCentralWidget(centralWidget);

    // 连接信号和槽
    connect(loginButton, &QPushButton::clicked, this, &LoginWindow::onLoginClicked);
    connect(registerButton, &QPushButton::clicked, this, &LoginWindow::onRegisterClicked);
    connect(resetPasswordButton, &QPushButton::clicked, this, &LoginWindow::onResetPasswordClicked);
    connect(roleCombo, &QComboBox::currentTextChanged, this, &LoginWindow::onRoleChanged);


    //医患沟通按钮测试
    connect(chatButton, &QPushButton::clicked, this, &LoginWindow::onChatClicked);

    //数据库连接槽函数
    tcpSocket = new QTcpSocket(this);
    connect(tcpSocket, &QTcpSocket::connected, this, &LoginWindow::onSocketConnected);
    connect(tcpSocket, &QTcpSocket::disconnected, this, &LoginWindow::onSocketDisconnected);
    connect(tcpSocket, &QTcpSocket::errorOccurred, this, &LoginWindow::onSocketError);
    connect(tcpSocket, &QTcpSocket::readyRead, this, &LoginWindow::onSocketReadyRead);
}

LoginWindow::~LoginWindow()
{
}

void LoginWindow::onChatClicked(){
    qDebug() << "clicked";
    // 使用 new 创建对象，确保生命周期
    ChatSystemInit *chatinit = new ChatSystemInit("QiDianban", "Doctor", this);
    qDebug() << "after";
}

void LoginWindow::onRoleChanged(const QString &role)
{
    // 动态更新账号标签和占位符
    if (role == "患者") {
        accountLabel->setText("手机号:");
        accountEdit->setPlaceholderText("请输入手机号");
    } else {
        accountLabel->setText("工号:   "); //这里的三个空格是为了切换角色时对话框相对位置不发生改变，这是最简单的方法了，虽然不优雅
        accountEdit->setPlaceholderText("请输入工号");
    }
}

void LoginWindow::onLoginClicked()
{
    QString role = roleCombo->currentText();
    account = accountEdit->text();
    QString password = passwordEdit->text();

    //格式验证逻辑，后续账号改成手机号和工号的验证
    if (account.isEmpty() || password.isEmpty()) {
        QMessageBox::warning(this, "输入错误", "账号或密码不能为空！");
        return;
    }

    /*
    //格式验证
    if(account.length()<3){
        QMessageBox::warning(this,"输入格式错误","账号长度不能小于3位");
    }
    if(password.length()<6){
        QMessageBox::warning(this,"输入格式错误","密码长度不能小于6位");
    }
    */

    //文件格式转换与数据库连接

    // 将用户输入数据组织成 QMap
    QMap<QString, QString> parameters;
    parameters["table_name"] = "login";
    parameters["user_name"] = account;
    parameters["password"] = password;
    QMap<QString, QVariant> variantMap;
    for (auto it = parameters.constBegin(); it != parameters.constEnd(); ++it) {
        variantMap.insert(it.key(), QVariant(it.value()));
    }

    // 将 QMap 转换为 JSON 格式的 QByteArray
    QJsonObject jsonObject = QJsonObject::fromVariantMap(variantMap);
    QJsonDocument jsonDocument(jsonObject);
    QByteArray dataToSend = jsonDocument.toJson(QJsonDocument::Compact);


    // 发送 JSON 数据到服务器
    QString serverAddress = "8.140.225.6"; // 服务器地址
    quint16 port = 55000; // 服务器端口
    if (sendJsonData(serverAddress, port, dataToSend, "doctor.json")) {
        qDebug() << "JSON 数据发送成功";
    } else {
        qDebug() << "JSON 数据发送失败";
    }


}

void LoginWindow::onRegisterClicked()
{
    RegisterWindow *registerWindow = new RegisterWindow(this);
    registerWindow->show();
    this->hide();
}

void LoginWindow::onResetPasswordClicked()
{
    ResetPasswordWindow *resetPasswordWindow = new ResetPasswordWindow(this);
    resetPasswordWindow->show();
    this->hide();
}

void LoginWindow::jumpToDoctorWindow()
{
    DoctorMainWindow *doctorwindow = new DoctorMainWindow(this);
    doctorwindow->show();
    this->hide();

}

void LoginWindow::jumpToPatientWindow()
{
    MainWindow_patient *mainwindow_patient = new MainWindow_patient(this);
    mainwindow_patient->show();
    this->hide();
}
void LoginWindow::onSocketConnected()
{
    qDebug() << "Successfully connected to the server.";
    // 可以在这里做一些界面提示，比如状态栏信息
}

void LoginWindow::onSocketDisconnected()
{
    qDebug() << "Disconnected from the server.";
}

void LoginWindow::onSocketError(QAbstractSocket::SocketError socketError)
{
    Q_UNUSED(socketError);
    QMessageBox::critical(this, "网络错误", "发生套接字错误：" + tcpSocket->errorString());
    qDebug() << "Socket error:" << tcpSocket->errorString();
}

void LoginWindow::onSocketReadyRead()
{
    // 从服务器接收数据
    QByteArray responseData = tcpSocket->readAll();
    qDebug() << "Server response:" << responseData;

    // 解析服务器返回的 JSON 数据
    QJsonDocument jsonResponse = QJsonDocument::fromJson(responseData);
    if (jsonResponse.isNull() || !jsonResponse.isObject()) {
        QMessageBox::critical(this, "服务器响应错误", "服务器返回了无效数据。");
        return;
    }

    QJsonObject responseObject = jsonResponse.object();
    bool success = responseObject.value("success").toBool();
    QString message = responseObject.value("message").toString();

    // 根据服务器返回的 success 字段判断登录是否成功
    if (success) {
        QMessageBox::information(this, "登录成功", "欢迎！进入主页面（角色：" + roleCombo->currentText() + "）");
        if(roleCombo->currentText() == "医生"){
            jumpToDoctorWindow();
        } else {
            jumpToPatientWindow();
        }
        this->hide();
    } else {
        QMessageBox::warning(this, "登录失败", message);
    }
}
