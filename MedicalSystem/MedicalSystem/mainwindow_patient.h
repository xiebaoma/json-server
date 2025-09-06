#ifndef MAINWINDOW_PATIENT_H
#define MAINWINDOW_PATIENT_H

#include <QMainWindow>
#include <QStackedWidget>
#include <QTableWidget>
#include <QLineEdit>
#include <QPushButton>
#include <QLabel>
#include <QFrame>

namespace Ui {
class MainWindow_patient;
}

class MainWindow_patient : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow_patient(QWidget *parent = nullptr);
    ~MainWindow_patient();

private slots:
    // 侧边栏按钮点击事件
    void on_home_btn_clicked();
    void on_info_btn_clicked();
    void on_regist_btn_clicked();
    void on_history_btn_clicked();
    void on_advice_btn_clicked();
    void on_presciption_btn_clicked();
    void on_com_btn_clicked();

    // 个人信息页面
    void on_pushButton_info_edit_clicked();
    void on_pushButton_info_confirm_clicked();
    void on_pushButton_info_back_clicked();

    // 挂号信息页面
    void on_pushButton_reg_appoint_clicked();
    void on_pushButton_reg_window_clicked();
    void on_pushButton_reg_doctor_clicked();
    void on_pushButton_reg_back_clicked();

    // 医生信息页面
    void on_pushButton_docdetail_clicked();
    void on_pushButton_regdoctor_back_clicked();

    // 医生详情页面
    void on_pushButton_doctor_close_clicked();

    // 窗口挂号页面
    void on_pushButton_window_confirm_clicked();
    void on_pushButton_window_back_clicked();

    // 病历信息页面
    void on_pushButton_history_back_clicked();

    // 医嘱信息页面
    void on_pushButton_advicedetail_clicked();
    void on_pushButton_advice_back_clicked();

    // 处方信息页面
    void on_pushButton_prescription_detail_clicked();
    void on_pushButton_prescription_back_clicked();

    // 医患沟通页面
    void on_pushButton_send_clicked();
    void on_pushButton_com_back_clicked();

private:
    Ui::MainWindow_patient *ui;

    // 初始化函数
    void initUI();
    void setupConnections();
};

#endif // MAINWINDOW_PATIENT_H
