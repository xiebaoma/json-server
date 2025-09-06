#include "doctormainwindow.h"
#include "loginwindow.h"
#include <QFontDatabase>
#include <QDebug>

DoctorMainWindow::DoctorMainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    setWindowTitle("Doctor");
    resize(500, 600);
    setStyleSheet("QMainWindow { background-color: #f0f4f8; }");

    // 加载字体
    int regattiaFontId = QFontDatabase::addApplicationFont("://fonts/fonts/Regattia-Bold.otf");
    if (regattiaFontId == -1) {
        qWarning() << "Failed to load Regattia-Bold font";
    }
    int ziKuFontId = QFontDatabase::addApplicationFont("://fonts/fonts/庞门正道粗书体.ttf");
    if (ziKuFontId == -1) {
        qWarning() << "Failed to load ZiKuTangHuangZiYuanKaiTi font";
    }

    DoctorMainWindow::returnAccount();

    //创建中心容器，总体垂直堆叠，从上到下依次为：标题、横幅、按钮标题、按钮
    QWidget *centralWidget = new QWidget(this);
    QVBoxLayout *vLayout = new QVBoxLayout(centralWidget);
    vLayout->setContentsMargins(0, 10, 0, 20);
    vLayout->setSpacing(0);
    vLayout->setAlignment(Qt::AlignTop);

    // 创建标题容器，标题总体垂直布局（虽然只包含一个部件）
    QWidget *titleWidget = new QWidget(centralWidget);
    QVBoxLayout *titleLayout = new QVBoxLayout(titleWidget);
    titleLayout->setContentsMargins(10, 0, 20, 0); // 标题左右外边距 20px
    titleLayout->setSpacing(0);

    // 标题文字水平布局（Doctor + Page）
    QHBoxLayout *titleHHLayout = new QHBoxLayout();
    titleHHLayout->setSpacing(0); // Doctor 和 Page 无间距
    titleHHLayout->setContentsMargins(0, 0, 0, 0);

    // Doctor 标签（花体）
    QLabel *doctorLabel = new QLabel("Doctor", titleWidget);
    doctorLabel->setStyleSheet("QLabel { "
                               "font-size: 26px; "
                               "font-weight: bold; "
                               "font-family: 'Regattia', 'Mistral', Arial; "
                               "color: black; "
                               "padding: 0px; "
                               "margin: 0px; "
                               "letter-spacing: -1px; "
                               "}");
    // Page 标签（普通字体）
    QLabel *pageLabel = new QLabel("Page", titleWidget);
    pageLabel->setStyleSheet("QLabel { "
                             "font-size: 26px; "
                             "font-weight: normal;"
                             "font-family: Arial; "
                             "color: black; "
                             "padding: 5px; "
                             "margin: 0px; "
                             "letter-spacing: -1px; "
                             "}");
    titleHHLayout->addWidget(doctorLabel);
    titleHHLayout->addWidget(pageLabel);
    titleHHLayout->addStretch();

    titleLayout->addLayout(titleHHLayout);

    // 横幅
    banner = new QWidget(centralWidget);
    banner->setFixedHeight(26);
    banner->setStyleSheet("QWidget { background-color: #2b82d1; "
                          "margin-left: -20px; margin-right: -20px; }");
    banner->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);

    // 创建按钮标题容器，总体垂直布局（文字和横线），按钮文字水平布局
    QWidget *buttonTitleWidget = new QWidget(centralWidget);
    QVBoxLayout *buttonTitleLayout = new QVBoxLayout(buttonTitleWidget);
    buttonTitleLayout->setContentsMargins(20, 0, 20, 0); // 按钮标题左右外边距 20px
    buttonTitleLayout->setSpacing(5);

    // 按钮标题文字布局
    QHBoxLayout *titleHLayout = new QHBoxLayout();
    titleHLayout->setSpacing(5); // 装饰块与标题间距 5px
    QWidget *decorationBlock = new QWidget(buttonTitleWidget);
    decorationBlock->setFixedSize(14, 43);
    decorationBlock->setStyleSheet("QWidget { background-color: #2b82d1; }");
    buttonTitleLabel = new QLabel("功能", buttonTitleWidget);
    buttonTitleLabel->setStyleSheet("QLabel { "
                                    "font-size: 26px; "
                                    "font-weight: bold; "
                                    "font-family: FangSong, Microsoft YaHei, sans-serif; "
                                    "color: black; "
                                    "}");
    titleHLayout->addWidget(decorationBlock);
    titleHLayout->addWidget(buttonTitleLabel);
    titleHLayout->addStretch(); // 标题靠左，右侧留空

    // 横线
    QFrame *hline = new QFrame(buttonTitleWidget);
    hline->setFrameShape(QFrame::HLine);
    hline->setFrameShadow(QFrame::Sunken);
    hline->setStyleSheet("QFrame { color: black; }");

    // 按钮标题布局
    buttonTitleLayout->addLayout(titleHLayout);
    buttonTitleLayout->addWidget(hline);

    // 创建按钮容器，总体垂直布局
    QWidget *buttonWidget = new QWidget(centralWidget);
    QVBoxLayout *buttonLayout = new QVBoxLayout(buttonWidget);
    buttonLayout->setContentsMargins(20, 0, 20, 0); // 按钮左右外边距 20px
    buttonLayout->setSpacing(0);

    // 按钮用表单布局
    QFormLayout *formLayout = new QFormLayout(); // 修复：移除 this
    formLayout->setSpacing(10);
    formLayout->setFormAlignment(Qt::AlignHCenter);

    // 按钮部件
    admissionStatusButton = new QPushButton("接诊状态", buttonWidget);
    formLayout->addRow(admissionStatusButton);
    admissionStatusButton->setFixedSize(334, 64);
    admissionStatusButton->setStyleSheet(
        "QPushButton { background-color: #5f9cd3; color: white; border-radius: 5px; padding: 8px; font: 20px '庞门正道粗书体'; }"
        "QPushButton:hover { background-color: #339af0; }"
        "QPushButton:pressed { background-color: #228be6; }");

    registerInformationButton = new QPushButton("挂号信息", buttonWidget);
    formLayout->addRow(registerInformationButton);
    registerInformationButton->setFixedSize(334, 64);
    registerInformationButton->setStyleSheet(
        "QPushButton { background-color: #5f9cd3; color: white; border-radius: 5px; padding: 8px; font: 20px '庞门正道粗书体'; }"
        "QPushButton:hover { background-color: #339af0; }"
        "QPushButton:pressed { background-color: #228be6; }");

    patientInformationButton = new QPushButton("患者信息", buttonWidget);
    formLayout->addRow(patientInformationButton);
    patientInformationButton->setFixedSize(334, 64);
    patientInformationButton->setStyleSheet(
        "QPushButton { background-color: #5f9cd3; color: white; border-radius: 5px; padding: 8px; font: 20px '庞门正道粗书体'; }"
        "QPushButton:hover { background-color: #339af0; }"
        "QPushButton:pressed { background-color: #228be6; }");

    doctorInformationButton = new QPushButton("个人信息修改", buttonWidget);
    formLayout->addRow(doctorInformationButton);
    doctorInformationButton->setFixedSize(334, 64);
    doctorInformationButton->setStyleSheet(
        "QPushButton { background-color: #5f9cd3; color: white; border-radius: 5px; padding: 8px; font: 20px '庞门正道粗书体'; }"
        "QPushButton:hover { background-color: #339af0; }"
        "QPushButton:pressed { background-color: #228be6; }");

    punchAndAskForLeaveButton = new QPushButton("打卡与请假", buttonWidget);
    formLayout->addRow(punchAndAskForLeaveButton);
    punchAndAskForLeaveButton->setFixedSize(334, 64);
    punchAndAskForLeaveButton->setStyleSheet(
        "QPushButton { background-color: #5f9cd3; color: white; border-radius: 5px; padding: 8px; font: 20px '庞门正道粗书体'; }"
        "QPushButton:hover { background-color: #339af0; }"
        "QPushButton:pressed { background-color: #228be6; }");

    receptionButton = new QPushButton("接诊", buttonWidget);
    formLayout->addRow(receptionButton);
    receptionButton->setFixedSize(334, 64);
    receptionButton->setStyleSheet(
        "QPushButton { background-color: #5f9cd3; color: white; border-radius: 5px; padding: 8px; font: 20px '庞门正道粗书体'; }"
        "QPushButton:hover { background-color: #339af0; }"
        "QPushButton:pressed { background-color: #228be6; }");

    chatButton = new QPushButton("医患交流", buttonWidget);
    formLayout->addRow(chatButton);
    chatButton->setFixedSize(334, 64);
    chatButton->setStyleSheet(
        "QPushButton { background-color: #5f9cd3; color: white; border-radius: 5px; padding: 8px; font: 20px '庞门正道粗书体'; }"
        "QPushButton:hover { background-color: #339af0; }"
        "QPushButton:pressed { background-color: #228be6; }");

    buttonLayout->addLayout(formLayout);

    vLayout->addWidget(titleWidget);
    vLayout->addSpacing(25);
    vLayout->addWidget(banner);
    vLayout->addSpacing(20);
    vLayout->addWidget(buttonTitleWidget);
    vLayout->addSpacing(30);
    vLayout->addWidget(buttonWidget);

    setCentralWidget(centralWidget);

    connect(admissionStatusButton, &QPushButton::clicked, this, &DoctorMainWindow::onAdmissionStatusClicked);
    connect(registerInformationButton, &QPushButton::clicked, this, &DoctorMainWindow::onRegisterInformationClicked);
    connect(patientInformationButton, &QPushButton::clicked, this, &DoctorMainWindow::onPatientInformationClicked);
    connect(doctorInformationButton, &QPushButton::clicked, this, &DoctorMainWindow::onDoctorInformationClicked);
    connect(punchAndAskForLeaveButton, &QPushButton::clicked, this, &DoctorMainWindow::onPunchAndAskForLeaveClicked);
    connect(receptionButton, &QPushButton::clicked, this, &DoctorMainWindow::onReceptionClicked);
}

DoctorMainWindow::~DoctorMainWindow() {}

void DoctorMainWindow::onAdmissionStatusClicked()
{
    AdmissionStatusWindow *window = new AdmissionStatusWindow(this);
    window->show();
    this->hide();
}

void DoctorMainWindow::onRegisterInformationClicked()
{
    RegistrationInfoWindow *window = new RegistrationInfoWindow(this);
    window->show();
    this->hide();
}

void DoctorMainWindow::onPatientInformationClicked()
{
    PatientInfoWindow *window = new PatientInfoWindow(this);
    window->show();
    this->hide();
}

void DoctorMainWindow::onDoctorInformationClicked()
{
    DoctorInfoWindow *window = new DoctorInfoWindow(this);
    window->show();
    this->hide();
}

void DoctorMainWindow::onPunchAndAskForLeaveClicked()
{
    PunchLeaveWindow *window = new PunchLeaveWindow(this);
    window->show();
    this->hide();
}

void DoctorMainWindow::onReceptionClicked()
{
    ReceptionWindow *window = new ReceptionWindow(this);
    window->show();
    this->hide();
}

QString DoctorMainWindow::returnAccount()
{
    //returnAccount 是一个普通的成员函数，不是构造函数，无法直接访问构造函数的 parent 参数,所以用parent(),可以动态调用
    LoginWindow *loginWindow = qobject_cast<LoginWindow *>(parent());
    QString doctorAccount = loginWindow->account;
    //qDebug() << "测试信息："<< doctorAccount;
    return doctorAccount;
}
