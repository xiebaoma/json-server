#include "mainwindow_patient.h"
#include "ui_mainwindow_patient.h"

MainWindow_patient::MainWindow_patient(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow_patient)
{
    ui->setupUi(this);
    initUI();
    setupConnections();
}

MainWindow_patient::~MainWindow_patient()
{
    delete ui;
}

void MainWindow_patient::initUI()
{
    // 设置窗口标题
    setWindowTitle("患者主界面");

    // 设置初始页面为主页
    ui->stackedWidget->setCurrentIndex(0);
}

void MainWindow_patient::setupConnections()
{
    // 连接侧边栏按钮
    connect(ui->home_btn, &QPushButton::clicked, this, &MainWindow_patient::on_home_btn_clicked);
    connect(ui->info_btn, &QPushButton::clicked, this, &MainWindow_patient::on_info_btn_clicked);
    connect(ui->regist_btn, &QPushButton::clicked, this, &MainWindow_patient::on_regist_btn_clicked);
    connect(ui->history_btn, &QPushButton::clicked, this, &MainWindow_patient::on_history_btn_clicked);
    connect(ui->advice_btn, &QPushButton::clicked, this, &MainWindow_patient::on_advice_btn_clicked);
    connect(ui->presciption_btn, &QPushButton::clicked, this, &MainWindow_patient::on_presciption_btn_clicked);
    connect(ui->com_btn, &QPushButton::clicked, this, &MainWindow_patient::on_com_btn_clicked);

    // 连接个人信息页面按钮
    connect(ui->pushButton_info_edit, &QPushButton::clicked, this, &MainWindow_patient::on_pushButton_info_edit_clicked);
    connect(ui->pushButton_info_confirm, &QPushButton::clicked, this, &MainWindow_patient::on_pushButton_info_confirm_clicked);
    connect(ui->pushButton_info_back, &QPushButton::clicked, this, &MainWindow_patient::on_pushButton_info_back_clicked);

    // 连接挂号信息页面按钮
    connect(ui->pushButton_reg_appoint, &QPushButton::clicked, this, &MainWindow_patient::on_pushButton_reg_appoint_clicked);
    connect(ui->pushButton_reg_window, &QPushButton::clicked, this, &MainWindow_patient::on_pushButton_reg_window_clicked);
    connect(ui->pushButton_reg_doctor, &QPushButton::clicked, this, &MainWindow_patient::on_pushButton_reg_doctor_clicked);
    connect(ui->pushButton_reg_back, &QPushButton::clicked, this, &MainWindow_patient::on_pushButton_reg_back_clicked);

    // 连接医生信息页面按钮
    connect(ui->pushButton_docdetail, &QPushButton::clicked, this, &MainWindow_patient::on_pushButton_docdetail_clicked);
    connect(ui->pushButton_regdoctor_back, &QPushButton::clicked, this, &MainWindow_patient::on_pushButton_regdoctor_back_clicked);

    // 连接医生详情页面按钮
    connect(ui->pushButton_doctor_close, &QPushButton::clicked, this, &MainWindow_patient::on_pushButton_doctor_close_clicked);

    // 连接窗口挂号页面按钮
    connect(ui->pushButton_window_confirm, &QPushButton::clicked, this, &MainWindow_patient::on_pushButton_window_confirm_clicked);
    connect(ui->pushButton_window_back, &QPushButton::clicked, this, &MainWindow_patient::on_pushButton_window_back_clicked);

    // 连接病历信息页面按钮
    connect(ui->pushButton_history_back, &QPushButton::clicked, this, &MainWindow_patient::on_pushButton_history_back_clicked);

    // 连接医嘱信息页面按钮
    connect(ui->pushButton_advicedetail, &QPushButton::clicked, this, &MainWindow_patient::on_pushButton_advicedetail_clicked);
    connect(ui->pushButton_advice_back, &QPushButton::clicked, this, &MainWindow_patient::on_pushButton_advice_back_clicked);

    // 连接处方信息页面按钮
    connect(ui->pushButton_prescription_detail, &QPushButton::clicked, this, &MainWindow_patient::on_pushButton_prescription_detail_clicked);
    connect(ui->pushButton_prescription_back, &QPushButton::clicked, this, &MainWindow_patient::on_pushButton_prescription_back_clicked);

    // 连接医患沟通页面按钮
    connect(ui->pushButton_send, &QPushButton::clicked, this, &MainWindow_patient::on_pushButton_send_clicked);
    connect(ui->pushButton_com_back, &QPushButton::clicked, this, &MainWindow_patient::on_pushButton_com_back_clicked);
}

// 侧边栏按钮点击事件实现
void MainWindow_patient::on_home_btn_clicked() { ui->stackedWidget->setCurrentIndex(0); }
void MainWindow_patient::on_info_btn_clicked() { ui->stackedWidget->setCurrentIndex(1); }
void MainWindow_patient::on_regist_btn_clicked() { ui->stackedWidget->setCurrentIndex(2); }
void MainWindow_patient::on_history_btn_clicked() { ui->stackedWidget->setCurrentIndex(7); }
void MainWindow_patient::on_advice_btn_clicked() { ui->stackedWidget->setCurrentIndex(8); }
void MainWindow_patient::on_presciption_btn_clicked() { ui->stackedWidget->setCurrentIndex(9); }
void MainWindow_patient::on_com_btn_clicked() { ui->stackedWidget->setCurrentIndex(10); }

// 个人信息页面
void MainWindow_patient::on_pushButton_info_edit_clicked()
{
    // 启用编辑功能
    ui->lineEdit_pname->setEnabled(true);
    ui->lineEdit_pgender->setEnabled(true);
    ui->lineEdit_pbirthdate->setEnabled(true);
    ui->lineEdit_pid->setEnabled(true);
    ui->lineEdit_pphone->setEnabled(true);
    ui->lineEdit_pemail->setEnabled(true);
}

void MainWindow_patient::on_pushButton_info_confirm_clicked()
{
    // 保存修改并禁用编辑
    ui->lineEdit_pname->setEnabled(false);
    ui->lineEdit_pgender->setEnabled(false);
    ui->lineEdit_pbirthdate->setEnabled(false);
    ui->lineEdit_pid->setEnabled(false);
    ui->lineEdit_pphone->setEnabled(false);
    ui->lineEdit_pemail->setEnabled(false);

    // TODO: 保存数据到数据库
}

void MainWindow_patient::on_pushButton_info_back_clicked()
{
    ui->stackedWidget->setCurrentIndex(0); // 返回主页
}

// 挂号信息页面
void MainWindow_patient::on_pushButton_reg_appoint_clicked()
{
    ui->stackedWidget->setCurrentIndex(6); // 切换到预约挂号页面
}

void MainWindow_patient::on_pushButton_reg_window_clicked()
{
    ui->stackedWidget->setCurrentIndex(5); // 切换到窗口挂号页面
}

void MainWindow_patient::on_pushButton_reg_doctor_clicked()
{
    ui->stackedWidget->setCurrentIndex(3); // 切换到医生信息页面
}

void MainWindow_patient::on_pushButton_reg_back_clicked()
{
    ui->stackedWidget->setCurrentIndex(0); // 返回主页
}

// 医生信息页面
void MainWindow_patient::on_pushButton_docdetail_clicked()
{
    ui->stackedWidget->setCurrentIndex(4); // 切换到医生详情页面
}

void MainWindow_patient::on_pushButton_regdoctor_back_clicked()
{
    ui->stackedWidget->setCurrentIndex(2); // 返回挂号信息页面
}

// 医生详情页面
void MainWindow_patient::on_pushButton_doctor_close_clicked()
{
    ui->stackedWidget->setCurrentIndex(3); // 返回医生信息页面
}

// 窗口挂号页面
void MainWindow_patient::on_pushButton_window_confirm_clicked()
{
    // TODO: 实现窗口挂号确认逻辑
    QString office = ui->lineEdit_window_office->text();
    QString doctorName = ui->lineEdit_window_dname->text();
    QString cost = ui->lineEdit_window_cost->text();

    // 挂号逻辑...
}

void MainWindow_patient::on_pushButton_window_back_clicked()
{
    ui->stackedWidget->setCurrentIndex(2); // 返回挂号信息页面
}

// 其他页面的返回按钮实现
void MainWindow_patient::on_pushButton_history_back_clicked() { ui->stackedWidget->setCurrentIndex(0); }
void MainWindow_patient::on_pushButton_advice_back_clicked() { ui->stackedWidget->setCurrentIndex(0); }
void MainWindow_patient::on_pushButton_prescription_back_clicked() { ui->stackedWidget->setCurrentIndex(0); }
void MainWindow_patient::on_pushButton_com_back_clicked() { ui->stackedWidget->setCurrentIndex(0); }

// 其他功能按钮的占位实现
void MainWindow_patient::on_pushButton_advicedetail_clicked()
{
    // TODO: 实现查看医嘱详情
}

void MainWindow_patient::on_pushButton_prescription_detail_clicked()
{
    // TODO: 实现查看处方详情
}

void MainWindow_patient::on_pushButton_send_clicked()
{
    // TODO: 实现发送消息功能
    QString suggestion = ui->lineEdit_psuggest->text();
    // 发送逻辑...
}
