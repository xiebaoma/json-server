#include "loginwindow.h"
#include "sendandreceive.h"
#include <QMessageBox>
#include <QFormLayout>
#include <QVBoxLayout>
#include <QRegularExpression>
#include <QFile>
#include <QTextStream>

RegisterWindow::RegisterWindow(QWidget *parent)
    : QMainWindow(parent)
{
    // 设置窗口标题和大小
    setWindowTitle("用户注册");
    resize(400, 400);

    // 设置窗口背景样式
    setStyleSheet("QMainWindow { background-color: #f0f4f8; }");

    // 创建中心部件和主垂直布局
    QWidget *centralWidget = new QWidget(this);
    QVBoxLayout *mainLayout = new QVBoxLayout(centralWidget);
    mainLayout->setContentsMargins(20, 20, 20, 20);
    mainLayout->setSpacing(10);

    // 角色选择
    roleCombo = new QComboBox(centralWidget);
    roleCombo->addItems({"患者", "医生"});
    roleCombo->setStyleSheet("QComboBox { border: 1px solid #ccc; border-radius: 5px; padding: 5px; }");
    mainLayout->addWidget(new QLabel("角色:", centralWidget));
    mainLayout->addWidget(roleCombo);

    // 创建堆叠窗口
    stackedWidget = new QStackedWidget(centralWidget);

    // 患者注册页面
    QWidget *patientWidget = new QWidget(centralWidget);
    QFormLayout *patientLayout = new QFormLayout(patientWidget);
    patientLayout->setSpacing(10);

    patientNameLabel = new QLabel("姓名:", centralWidget);
    patientNameLabel->setStyleSheet("font: 14px 'Arial'; color: #333;");
    patientNameEdit = new QLineEdit(centralWidget);
    patientNameEdit->setPlaceholderText("请输入姓名");
    patientNameEdit->setStyleSheet("QLineEdit { border: 1px solid #ccc; border-radius: 5px; padding: 5px; }");
    patientLayout->addRow(patientNameLabel, patientNameEdit);

    patientPasswordLabel = new QLabel("密码:", centralWidget);
    patientPasswordLabel->setStyleSheet("font: 14px 'Arial'; color: #333;");
    patientPasswordEdit = new QLineEdit(centralWidget);
    patientPasswordEdit->setEchoMode(QLineEdit::Password);
    patientPasswordEdit->setPlaceholderText("请输入密码");
    patientPasswordEdit->setStyleSheet("QLineEdit { border: 1px solid #ccc; border-radius: 5px; padding: 5px; }");
    patientLayout->addRow(patientPasswordLabel, patientPasswordEdit);

    patientConfirmPasswordLabel = new QLabel("确认密码:", centralWidget);
    patientConfirmPasswordLabel->setStyleSheet("font: 14px 'Arial'; color: #333;");
    patientConfirmPasswordEdit = new QLineEdit(centralWidget);
    patientConfirmPasswordEdit->setEchoMode(QLineEdit::Password);
    patientConfirmPasswordEdit->setPlaceholderText("请再次输入密码");
    patientConfirmPasswordEdit->setStyleSheet("QLineEdit { border: 1px solid #ccc; border-radius: 5px; padding: 5px; }");
    patientLayout->addRow(patientConfirmPasswordLabel, patientConfirmPasswordEdit);

    patientBirthdateLabel = new QLabel("出生日期:", centralWidget);
    patientBirthdateLabel->setStyleSheet("font: 14px 'Arial'; color: #333;");
    patientBirthdateEdit = new QLineEdit(centralWidget);
    patientBirthdateEdit->setPlaceholderText("格式：YYYY-MM-DD");
    patientBirthdateEdit->setStyleSheet("QLineEdit { border: 1px solid #ccc; border-radius: 5px; padding: 5px; }");
    patientLayout->addRow(patientBirthdateLabel, patientBirthdateEdit);

    patientIdCardLabel = new QLabel("身份证号:", centralWidget);
    patientIdCardLabel->setStyleSheet("font: 14px 'Arial'; color: #333;");
    patientIdCardEdit = new QLineEdit(centralWidget);
    patientIdCardEdit->setPlaceholderText("请输入18位身份证号");
    patientIdCardEdit->setStyleSheet("QLineEdit { border: 1px solid #ccc; border-radius: 5px; padding: 5px; }");
    patientLayout->addRow(patientIdCardLabel, patientIdCardEdit);

    patientPhoneLabel = new QLabel("手机号:", centralWidget);
    patientPhoneLabel->setStyleSheet("font: 14px 'Arial'; color: #333;");
    patientPhoneEdit = new QLineEdit(centralWidget);
    patientPhoneEdit->setPlaceholderText("请输入11位手机号");
    patientPhoneEdit->setStyleSheet("QLineEdit { border: 1px solid #ccc; border-radius: 5px; padding: 5px; }");
    patientLayout->addRow(patientPhoneLabel, patientPhoneEdit);

    patientEmailLabel = new QLabel("邮箱:", centralWidget);
    patientEmailLabel->setStyleSheet("font: 14px 'Arial'; color: #333;");
    patientEmailEdit = new QLineEdit(centralWidget);
    patientEmailEdit->setPlaceholderText("请输入邮箱");
    patientEmailEdit->setStyleSheet("QLineEdit { border: 1px solid #ccc; border-radius: 5px; padding: 5px; }");
    patientLayout->addRow(patientEmailLabel, patientEmailEdit);

    stackedWidget->addWidget(patientWidget);

    // 医生注册页面
    QWidget *doctorWidget = new QWidget(centralWidget);
    QFormLayout *doctorLayout = new QFormLayout(doctorWidget);
    doctorLayout->setSpacing(10);

    doctorNameLabel = new QLabel("姓名:", centralWidget);
    doctorNameLabel->setStyleSheet("font: 14px 'Arial'; color: #333;");
    doctorNameEdit = new QLineEdit(centralWidget);
    doctorNameEdit->setPlaceholderText("请输入姓名");
    doctorNameEdit->setStyleSheet("QLineEdit { border: 1px solid #ccc; border-radius: 5px; padding: 5px; }");
    doctorLayout->addRow(doctorNameLabel, doctorNameEdit);

    doctorPasswordLabel = new QLabel("密码:", centralWidget);
    doctorPasswordLabel->setStyleSheet("font: 14px 'Arial'; color: #333;");
    doctorPasswordEdit = new QLineEdit(centralWidget);
    doctorPasswordEdit->setEchoMode(QLineEdit::Password);
    doctorPasswordEdit->setPlaceholderText("请输入密码");
    doctorPasswordEdit->setStyleSheet("QLineEdit { border: 1px solid #ccc; border-radius: 5px; padding: 5px; }");
    doctorLayout->addRow(doctorPasswordLabel, doctorPasswordEdit);

    doctorConfirmPasswordLabel = new QLabel("确认密码:", centralWidget);
    doctorConfirmPasswordLabel->setStyleSheet("font: 14px 'Arial'; color: #333;");
    doctorConfirmPasswordEdit = new QLineEdit(centralWidget);
    doctorConfirmPasswordEdit->setEchoMode(QLineEdit::Password);
    doctorConfirmPasswordEdit->setPlaceholderText("请再次输入密码");
    doctorConfirmPasswordEdit->setStyleSheet("QLineEdit { border: 1px solid #ccc; border-radius: 5px; padding: 5px; }");
    doctorLayout->addRow(doctorConfirmPasswordLabel, doctorConfirmPasswordEdit);

    doctorEmployeeIdLabel = new QLabel("工号:", centralWidget);
    doctorEmployeeIdLabel->setStyleSheet("font: 14px 'Arial'; color: #333;");
    doctorEmployeeIdEdit = new QLineEdit(centralWidget);
    doctorEmployeeIdEdit->setPlaceholderText("请输入工号");
    doctorEmployeeIdEdit->setStyleSheet("QLineEdit { border: 1px solid #ccc; border-radius: 5px; padding: 5px; }");
    doctorLayout->addRow(doctorEmployeeIdLabel, doctorEmployeeIdEdit);

    doctorDepartmentLabel = new QLabel("科室:", centralWidget);
    doctorDepartmentLabel->setStyleSheet("font: 14px 'Arial'; color: #333;");
    doctorDepartmentCombo = new QComboBox(centralWidget);
    doctorDepartmentCombo->addItems({"内科", "外科", "儿科", "急诊"});
    doctorDepartmentCombo->setStyleSheet("QComboBox { border: 1px solid #ccc; border-radius: 5px; padding: 5px; }");
    doctorLayout->addRow(doctorDepartmentLabel, doctorDepartmentCombo);

    doctorPhotoLabel = new QLabel("照片:", centralWidget);
    doctorPhotoLabel->setStyleSheet("font: 14px 'Arial'; color: #333;");
    doctorPhotoEdit = new QLineEdit(centralWidget);
    doctorPhotoEdit->setPlaceholderText("选择照片文件");
    doctorPhotoEdit->setStyleSheet("QLineEdit { border: 1px solid #ccc; border-radius: 5px; padding: 5px; }");
    photoButton = new QPushButton("选择", centralWidget);
    photoButton->setStyleSheet(
        "QPushButton { background-color: #6c757d; color: white; border-radius: 5px; padding: 8px; font: 14px 'Arial'; }"
        "QPushButton:hover { background-color: #5a6268; }"
        "QPushButton:pressed { background-color: #4b545c; }");
    QHBoxLayout *photoLayout = new QHBoxLayout();
    photoLayout->addWidget(doctorPhotoEdit);
    photoLayout->addWidget(photoButton);
    doctorLayout->addRow(doctorPhotoLabel, photoLayout);

    stackedWidget->addWidget(doctorWidget);

    // 添加堆叠窗口到主布局
    mainLayout->addWidget(stackedWidget);

    // 提交按钮
    submitButton = new QPushButton("提交", centralWidget);
    submitButton->setStyleSheet(
        "QPushButton { background-color: #007bff; color: white; border-radius: 5px; padding: 8px; font: 14px 'Arial'; }"
        "QPushButton:hover { background-color: #0056b3; }"
        "QPushButton:pressed { background-color: #003d80; }");
    mainLayout->addWidget(submitButton);

    // 返回登录按钮
    returnLoginButton = new QPushButton("返回登录", centralWidget);
    returnLoginButton->setStyleSheet(
        "QPushButton { background-color: #6c757d; color: white; border-radius: 5px; padding: 8px; font: 14px 'Arial'; }"
        "QPushButton:hover { background-color: #5a6268; }"
        "QPushButton:pressed { background-color: #4b545c; }");
    mainLayout->addWidget(returnLoginButton);

    // 居中布局
    mainLayout->addStretch();

    // 设置中心部件
    setCentralWidget(centralWidget);

    // 连接信号和槽
    connect(roleCombo, &QComboBox::currentTextChanged, this, &RegisterWindow::onRoleChanged);
    connect(submitButton, &QPushButton::clicked, this, &RegisterWindow::onSubmitClicked);
    connect(returnLoginButton, &QPushButton::clicked, this, &RegisterWindow::onBackToLoginClicked);
    connect(photoButton, &QPushButton::clicked, this, &RegisterWindow::onSelectPhoto);
}

RegisterWindow::~RegisterWindow()
{
}

void RegisterWindow::onRoleChanged(const QString &role)
{
    stackedWidget->setCurrentIndex(role == "患者" ? 0 : 1);
}

void RegisterWindow::onSelectPhoto()
{
    QString fileName = QFileDialog::getOpenFileName(this, "选择照片", "", "Images (*.jpg *.png)");
    if (!fileName.isEmpty()) {
        doctorPhotoEdit->setText(fileName);
    }
}

void RegisterWindow::onSubmitClicked()
{
    QString role = roleCombo->currentText();
    QMap<QString, QString> parameters;

    if (role == "患者") {
        QString name = patientNameEdit->text();
        QString password = patientPasswordEdit->text();
        QString confirmPassword = patientConfirmPasswordEdit->text();
        QString birthdate = patientBirthdateEdit->text();
        QString idcard = patientIdCardEdit->text();
        QString phone = patientPhoneEdit->text();
        QString email = patientEmailEdit->text();

        // 验证空输入
        if (name.isEmpty()  || password.isEmpty() || confirmPassword.isEmpty() ||
            birthdate.isEmpty() || idcard.isEmpty() || phone.isEmpty() || email.isEmpty()) {
            QMessageBox::warning(this, "输入错误", "所有字段均为必填项！");
            return;
        }

        // 验证密码一致性
        if (password != confirmPassword) {
            QMessageBox::warning(this, "密码错误", "两次输入的密码不一致！");
            return;
        }

        // 格式验证
        QRegularExpression birthdateRx("^\\d{4}-\\d{2}-\\d{2}$");
        QRegularExpression phoneRx("^\\d{11}$");
        QRegularExpression emailRx("^[^@]+@[^@]+\\.[^@]+$");
        if (!birthdateRx.match(birthdate).hasMatch()) {
            QMessageBox::warning(this, "格式错误", "出生日期格式应为 YYYY-MM-DD！");
            return;
        }
        if (idcard.length() != 18) {
            QMessageBox::warning(this, "格式错误", "身份证号应为18位！");
            return;
        }
        if (!phoneRx.match(phone).hasMatch()) {
            QMessageBox::warning(this, "格式错误", "手机号应为11位数字！");
            return;
        }
        if (!emailRx.match(email).hasMatch()) {
            QMessageBox::warning(this, "格式错误", "请输入有效的邮箱地址！");
            return;
        }

        // 收集参数
        parameters["table_name"]= "register";
        parameters["name"] = name;
        parameters["password"] = password;
        parameters["birth_date"] = birthdate;
        parameters["id_card"] = idcard;
        parameters["phone"] = phone;
        parameters["email"] = email;

    } else {
        QString name = doctorNameEdit->text();
        QString password = doctorPasswordEdit->text();
        QString confirmPassword = doctorConfirmPasswordEdit->text();
        QString employeeId = doctorEmployeeIdEdit->text();
        QString department = doctorDepartmentCombo->currentText();
        QString photoPath = doctorPhotoEdit->text();

        // 验证空输入
        if (name.isEmpty()  || password.isEmpty() || confirmPassword.isEmpty() ||
            employeeId.isEmpty() || department.isEmpty()) {
            QMessageBox::warning(this, "输入错误", "除照片外，所有字段均为必填项！");
            return;
        }

        // 验证密码一致性
        if (password != confirmPassword) {
            QMessageBox::warning(this, "密码错误", "两次输入的密码不一致！");
            return;
        }

        // 收集参数
        parameters["table_name"] = "register";
        parameters["name"] = name;
        parameters["password"] = password;
        parameters["employee_id"] = employeeId;
        parameters["department"] = department;
        if (!photoPath.isEmpty()) {
            parameters["photo_path"] = photoPath;
        }

    }
    //文件格式转换与数据库连接

    // 将用户输入数据组织成 QMap
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

    QMessageBox::information(this,"注册成功","恭喜，已注册");
}

void RegisterWindow::onBackToLoginClicked()
{
    parentWidget()->show();
    this->close();
}
