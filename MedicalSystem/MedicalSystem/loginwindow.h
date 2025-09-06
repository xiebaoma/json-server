#ifndef LOGINWINDOW_H
#define LOGINWINDOW_H

#include <QMainWindow>
#include <QLineEdit>
#include <QPushButton>
#include <QLabel>
#include <QVBoxLayout>
#include <QComboBox>
#include <QStackedWidget>
#include <QFileDialog>
#include <QtNetwork/QTcpSocket>

#include <QWidget>
#include <QMessageBox>
#include <QFormLayout>
#include <QFile>
#include <QTextStream>
#include <QHostAddress>
#include <QJsonDocument>
#include <QJsonObject>
#include <QDebug>


class LoginWindow : public QMainWindow
{
    Q_OBJECT

public:
    LoginWindow(QWidget *parent = nullptr);
    ~LoginWindow();
    QString account;

private slots:
    void onLoginClicked();
    void onRegisterClicked();
    void onResetPasswordClicked();
    //医患沟通测试
    void onChatClicked();

    // 角色切换槽函数
    void onRoleChanged(const QString &role);
    void jumpToDoctorWindow(); //跳转到医生界面
    void jumpToPatientWindow(); //跳转到患者界面


    void onSocketConnected();
    void onSocketDisconnected();
    void onSocketError(QAbstractSocket::SocketError socketError);
    void onSocketReadyRead();

private:
    QLabel *titleLabel;
    QComboBox *roleCombo; // 角色选择
    QLineEdit *accountEdit; // 账号（患者：手机号，医生：工号）
    QLineEdit *passwordEdit;
    QPushButton *loginButton;
    QPushButton *registerButton;
    QPushButton *resetPasswordButton;
    QPushButton *chatButton;

    QLabel *accountLabel; // 动态更新标签（手机号/工号）
    QTcpSocket* tcpSocket;
};



class RegisterWindow : public QMainWindow
{
    Q_OBJECT
public:
    RegisterWindow(QWidget *parent = nullptr);
    ~RegisterWindow();
private slots:
    void onSubmitClicked();
    void onBackToLoginClicked();
    void onRoleChanged(const QString &role); // 角色切换槽函数
    void onSelectPhoto(); // 选择照片

private:
    QComboBox *roleCombo; // 角色选择
    QStackedWidget *stackedWidget; // 动态切换患者/医生输入区域

    // 患者注册字段
    QLabel *patientNameLabel;
    QLineEdit *patientNameEdit;
    QLabel *patientUsernameLabel;
    QLineEdit *patientUsernameEdit;
    QLabel *patientPasswordLabel;
    QLineEdit *patientPasswordEdit;
    QLabel *patientConfirmPasswordLabel;
    QLineEdit *patientConfirmPasswordEdit;
    QLabel *patientBirthdateLabel;
    QLineEdit *patientBirthdateEdit;
    QLabel *patientIdCardLabel;
    QLineEdit *patientIdCardEdit;
    QLabel *patientPhoneLabel;
    QLineEdit *patientPhoneEdit;
    QLabel *patientEmailLabel;
    QLineEdit *patientEmailEdit;

    // 医生注册字段
    QLabel *doctorNameLabel;
    QLineEdit *doctorNameEdit;
    QLabel *doctorUsernameLabel;
    QLineEdit *doctorUsernameEdit;
    QLabel *doctorPasswordLabel;
    QLineEdit *doctorPasswordEdit;
    QLabel *doctorConfirmPasswordLabel;
    QLineEdit *doctorConfirmPasswordEdit;
    QLabel *doctorEmployeeIdLabel;
    QLineEdit *doctorEmployeeIdEdit;
    QLabel *doctorDepartmentLabel;
    QComboBox *doctorDepartmentCombo;
    QLabel *doctorPhotoLabel;
    QLineEdit *doctorPhotoEdit;
    QPushButton *photoButton;
    QPushButton *submitButton;
    QPushButton *returnLoginButton;
};



class ResetPasswordWindow : public QMainWindow
{
    Q_OBJECT

public:
    ResetPasswordWindow(QWidget *parent = nullptr);
    ~ResetPasswordWindow();

private slots:
    void onSubmitClicked();
    void onBackToLoginClicked();
    void onRoleChanged(const QString &role);
    // 角色切换槽函数

private:
    QComboBox *roleCombo; // 角色选择
    QStackedWidget *stackedWidget; // 动态切换患者/医生输入区域

    // 患者重置字段
    QLabel *patientNameLabel;
    QLineEdit *patientNameEdit;
    QLabel *patientIdCardLabel;
    QLineEdit *patientIdCardEdit;
    QLabel *patientPhoneLabel;
    QLineEdit *patientPhoneEdit;
    QLabel *patientBirthdateLabel;
    QLineEdit *patientBirthdateEdit;
    QLabel *patientNewPasswordLabel;
    QLineEdit *patientNewPasswordEdit;
    QLabel *patientOldPasswordLabel;
    QLineEdit *patientOldPasswordEdit;

    // 医生重置字段
    QLabel *doctorNameLabel;
    QLineEdit *doctorNameEdit;
    QLabel *doctorEmployeeIdLabel;
    QLineEdit *doctorEmployeeIdEdit;
    QLabel *doctorDepartmentLabel;
    QComboBox *doctorDepartmentCombo;
    QLabel *doctorAdminCodeLabel;
    QLineEdit *doctorAdminCodeEdit;
    QLabel *doctorNewPasswordLabel;
    QLineEdit *doctorNewPasswordEdit;
    QLabel *doctorOldPasswordLabel;
    QLineEdit *doctorOldPasswordEdit;

    QPushButton *submitButton;
    QPushButton *returnLoginButton;
};


#endif // LOGINWINDOW_H
