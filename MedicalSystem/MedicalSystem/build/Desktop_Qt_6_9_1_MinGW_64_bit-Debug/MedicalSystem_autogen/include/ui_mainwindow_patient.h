/********************************************************************************
** Form generated from reading UI file 'mainwindow_patient.ui'
**
** Created by: Qt User Interface Compiler version 6.9.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_PATIENT_H
#define UI_MAINWINDOW_PATIENT_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QFrame>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QScrollArea>
#include <QtWidgets/QStackedWidget>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTableWidget>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow_patient
{
public:
    QWidget *centralwidget;
    QFrame *frame_2;
    QHBoxLayout *horizontalLayout_2;
    QFrame *frame;
    QFrame *frame_4;
    QVBoxLayout *verticalLayout;
    QPushButton *home_btn;
    QPushButton *info_btn;
    QPushButton *regist_btn;
    QPushButton *history_btn;
    QPushButton *advice_btn;
    QPushButton *presciption_btn;
    QPushButton *com_btn;
    QFrame *frame_3;
    QStackedWidget *stackedWidget;
    QWidget *page_home;
    QLabel *label_home;
    QWidget *page_info;
    QScrollArea *scrollArea;
    QWidget *scrollAreaWidgetContents;
    QLabel *label_info;
    QTableWidget *tableWidget_info;
    QFrame *frame_5;
    QVBoxLayout *verticalLayout_2;
    QPushButton *pushButton_info_edit;
    QPushButton *pushButton_info_confirm;
    QPushButton *pushButton_info_back;
    QFrame *frame_6;
    QVBoxLayout *verticalLayout_3;
    QLabel *label_pname;
    QLabel *label_pgender;
    QLabel *label_pbirthdate;
    QLabel *label_pid;
    QLabel *label_pphone;
    QLabel *label_pemail;
    QFrame *frame_7;
    QVBoxLayout *verticalLayout_4;
    QLineEdit *lineEdit_pname;
    QLineEdit *lineEdit_pgender;
    QLineEdit *lineEdit_pbirthdate;
    QLineEdit *lineEdit_pid;
    QLineEdit *lineEdit_pphone;
    QLineEdit *lineEdit_pemail;
    QWidget *page_reg;
    QFrame *frame_8;
    QVBoxLayout *verticalLayout_5;
    QPushButton *pushButton_reg_appoint;
    QPushButton *pushButton_reg_window;
    QPushButton *pushButton_reg_doctor;
    QPushButton *pushButton_reg_back;
    QWidget *page_reg_doctor;
    QScrollArea *scrollArea_2;
    QWidget *scrollAreaWidgetContents_2;
    QLabel *label_reg_doctor;
    QFrame *frame_9;
    QLabel *label_daoctor_pic;
    QFrame *frame_10;
    QLabel *label_doctor_office;
    QLabel *label_doctor_name;
    QLabel *label_doctor_office_2;
    QLabel *label_doctor_name_2;
    QPushButton *pushButton_docdetail;
    QPushButton *pushButton_regdoctor_back;
    QWidget *page_reg_docdetail;
    QLabel *label_docdetail;
    QFrame *frame_11;
    QLabel *label_docdetail_pic;
    QFrame *frame_12;
    QVBoxLayout *verticalLayout_6;
    QLabel *label_docdetail_office;
    QLabel *label_docdetail_id;
    QLabel *label_docdetail_name;
    QLabel *label_docdetail_worktime;
    QLabel *label_docdetail_cost;
    QLabel *label_docdetail_maxpatient;
    QFrame *frame_13;
    QVBoxLayout *verticalLayout_7;
    QLabel *label_docdetail_office_2;
    QLabel *label_docdetail_id_2;
    QLabel *label_docdetail_name_2;
    QLabel *label_docdetail_worktime_2;
    QLabel *label_docdetail_cost_2;
    QLabel *label_docdetail_maxpatient_2;
    QPushButton *pushButton_doctor_close;
    QWidget *page_reg_window;
    QLabel *label_window;
    QTableWidget *tableWidget_window;
    QLabel *label_window_office;
    QLabel *label_window_dname;
    QLineEdit *lineEdit_window_office;
    QLineEdit *lineEdit_window_dname;
    QPushButton *pushButton_window_confirm;
    QPushButton *pushButton_window_back;
    QLabel *label_window_cost;
    QLineEdit *lineEdit_window_cost;
    QWidget *page_reg_appoint;
    QLabel *label_reg_appoint;
    QWidget *page_history;
    QLabel *label_history;
    QTableWidget *tableWidget_history;
    QPushButton *pushButton_history_back;
    QWidget *page_advice;
    QLabel *label_advice;
    QTableWidget *tableWidget_advice;
    QLabel *label_prescription_content;
    QLineEdit *lineEdit_prescription_content;
    QLabel *label_advicedetail;
    QLineEdit *lineEdit_advicedetail;
    QPushButton *pushButton_advicedetail;
    QPushButton *pushButton_advice_back;
    QWidget *page_prescription;
    QLabel *label_prescription_info;
    QTableWidget *tableWidget_prescription;
    QLabel *label_prescription_id;
    QLabel *label_pre_doctor;
    QLineEdit *lineEdit_prescription_id;
    QLineEdit *lineEdit_prescription_doctor;
    QLabel *label_predetail;
    QLineEdit *lineEdit_predetail;
    QPushButton *pushButton_prescription_detail;
    QPushButton *pushButton_prescription_back;
    QWidget *page_com;
    QLabel *label_com;
    QTableWidget *tableWidget_com;
    QLabel *label_office;
    QLabel *label_dname;
    QLineEdit *lineEdit_office;
    QLineEdit *lineEdit_dname;
    QLabel *label_dsuggest;
    QLineEdit *lineEdit_dsuggest;
    QLabel *label_psuggest;
    QLineEdit *lineEdit_psuggest;
    QPushButton *pushButton_send;
    QPushButton *pushButton_com_back;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *MainWindow_patient)
    {
        if (MainWindow_patient->objectName().isEmpty())
            MainWindow_patient->setObjectName("MainWindow_patient");
        MainWindow_patient->resize(1109, 691);
        centralwidget = new QWidget(MainWindow_patient);
        centralwidget->setObjectName("centralwidget");
        frame_2 = new QFrame(centralwidget);
        frame_2->setObjectName("frame_2");
        frame_2->setGeometry(QRect(10, 10, 1071, 651));
        QSizePolicy sizePolicy(QSizePolicy::Policy::Expanding, QSizePolicy::Policy::Expanding);
        sizePolicy.setHorizontalStretch(4);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(frame_2->sizePolicy().hasHeightForWidth());
        frame_2->setSizePolicy(sizePolicy);
        frame_2->setFrameShape(QFrame::Shape::StyledPanel);
        frame_2->setFrameShadow(QFrame::Shadow::Raised);
        horizontalLayout_2 = new QHBoxLayout(frame_2);
        horizontalLayout_2->setObjectName("horizontalLayout_2");
        frame = new QFrame(frame_2);
        frame->setObjectName("frame");
        QSizePolicy sizePolicy1(QSizePolicy::Policy::Expanding, QSizePolicy::Policy::Expanding);
        sizePolicy1.setHorizontalStretch(1);
        sizePolicy1.setVerticalStretch(0);
        sizePolicy1.setHeightForWidth(frame->sizePolicy().hasHeightForWidth());
        frame->setSizePolicy(sizePolicy1);
        frame->setFrameShape(QFrame::Shape::StyledPanel);
        frame->setFrameShadow(QFrame::Shadow::Raised);
        frame_4 = new QFrame(frame);
        frame_4->setObjectName("frame_4");
        frame_4->setGeometry(QRect(10, 9, 181, 611));
        frame_4->setFrameShape(QFrame::Shape::StyledPanel);
        frame_4->setFrameShadow(QFrame::Shadow::Raised);
        verticalLayout = new QVBoxLayout(frame_4);
        verticalLayout->setObjectName("verticalLayout");
        home_btn = new QPushButton(frame_4);
        home_btn->setObjectName("home_btn");

        verticalLayout->addWidget(home_btn);

        info_btn = new QPushButton(frame_4);
        info_btn->setObjectName("info_btn");

        verticalLayout->addWidget(info_btn);

        regist_btn = new QPushButton(frame_4);
        regist_btn->setObjectName("regist_btn");

        verticalLayout->addWidget(regist_btn);

        history_btn = new QPushButton(frame_4);
        history_btn->setObjectName("history_btn");

        verticalLayout->addWidget(history_btn);

        advice_btn = new QPushButton(frame_4);
        advice_btn->setObjectName("advice_btn");

        verticalLayout->addWidget(advice_btn);

        presciption_btn = new QPushButton(frame_4);
        presciption_btn->setObjectName("presciption_btn");

        verticalLayout->addWidget(presciption_btn);

        com_btn = new QPushButton(frame_4);
        com_btn->setObjectName("com_btn");

        verticalLayout->addWidget(com_btn);


        horizontalLayout_2->addWidget(frame);

        frame_3 = new QFrame(frame_2);
        frame_3->setObjectName("frame_3");
        sizePolicy.setHeightForWidth(frame_3->sizePolicy().hasHeightForWidth());
        frame_3->setSizePolicy(sizePolicy);
        frame_3->setFrameShape(QFrame::Shape::StyledPanel);
        frame_3->setFrameShadow(QFrame::Shadow::Raised);
        stackedWidget = new QStackedWidget(frame_3);
        stackedWidget->setObjectName("stackedWidget");
        stackedWidget->setGeometry(QRect(10, 0, 811, 611));
        page_home = new QWidget();
        page_home->setObjectName("page_home");
        label_home = new QLabel(page_home);
        label_home->setObjectName("label_home");
        label_home->setGeometry(QRect(118, 138, 561, 181));
        stackedWidget->addWidget(page_home);
        page_info = new QWidget();
        page_info->setObjectName("page_info");
        scrollArea = new QScrollArea(page_info);
        scrollArea->setObjectName("scrollArea");
        scrollArea->setGeometry(QRect(0, 9, 801, 1991));
        scrollArea->setMinimumSize(QSize(0, 0));
        scrollArea->setWidgetResizable(true);
        scrollAreaWidgetContents = new QWidget();
        scrollAreaWidgetContents->setObjectName("scrollAreaWidgetContents");
        scrollAreaWidgetContents->setGeometry(QRect(0, 0, 782, 2300));
        scrollAreaWidgetContents->setMinimumSize(QSize(0, 2300));
        label_info = new QLabel(scrollAreaWidgetContents);
        label_info->setObjectName("label_info");
        label_info->setGeometry(QRect(20, 10, 141, 51));
        tableWidget_info = new QTableWidget(scrollAreaWidgetContents);
        if (tableWidget_info->columnCount() < 6)
            tableWidget_info->setColumnCount(6);
        QTableWidgetItem *__qtablewidgetitem = new QTableWidgetItem();
        tableWidget_info->setHorizontalHeaderItem(0, __qtablewidgetitem);
        QTableWidgetItem *__qtablewidgetitem1 = new QTableWidgetItem();
        tableWidget_info->setHorizontalHeaderItem(1, __qtablewidgetitem1);
        QTableWidgetItem *__qtablewidgetitem2 = new QTableWidgetItem();
        tableWidget_info->setHorizontalHeaderItem(2, __qtablewidgetitem2);
        QTableWidgetItem *__qtablewidgetitem3 = new QTableWidgetItem();
        tableWidget_info->setHorizontalHeaderItem(3, __qtablewidgetitem3);
        QTableWidgetItem *__qtablewidgetitem4 = new QTableWidgetItem();
        tableWidget_info->setHorizontalHeaderItem(4, __qtablewidgetitem4);
        QTableWidgetItem *__qtablewidgetitem5 = new QTableWidgetItem();
        tableWidget_info->setHorizontalHeaderItem(5, __qtablewidgetitem5);
        tableWidget_info->setObjectName("tableWidget_info");
        tableWidget_info->setGeometry(QRect(10, 60, 771, 421));
        frame_5 = new QFrame(scrollAreaWidgetContents);
        frame_5->setObjectName("frame_5");
        frame_5->setGeometry(QRect(660, 740, 117, 122));
        frame_5->setFrameShape(QFrame::Shape::StyledPanel);
        frame_5->setFrameShadow(QFrame::Shadow::Raised);
        verticalLayout_2 = new QVBoxLayout(frame_5);
        verticalLayout_2->setObjectName("verticalLayout_2");
        pushButton_info_edit = new QPushButton(frame_5);
        pushButton_info_edit->setObjectName("pushButton_info_edit");

        verticalLayout_2->addWidget(pushButton_info_edit);

        pushButton_info_confirm = new QPushButton(frame_5);
        pushButton_info_confirm->setObjectName("pushButton_info_confirm");

        verticalLayout_2->addWidget(pushButton_info_confirm);

        pushButton_info_back = new QPushButton(frame_5);
        pushButton_info_back->setObjectName("pushButton_info_back");

        verticalLayout_2->addWidget(pushButton_info_back);

        frame_6 = new QFrame(scrollAreaWidgetContents);
        frame_6->setObjectName("frame_6");
        frame_6->setGeometry(QRect(20, 490, 111, 361));
        frame_6->setFrameShape(QFrame::Shape::StyledPanel);
        frame_6->setFrameShadow(QFrame::Shadow::Raised);
        verticalLayout_3 = new QVBoxLayout(frame_6);
        verticalLayout_3->setObjectName("verticalLayout_3");
        label_pname = new QLabel(frame_6);
        label_pname->setObjectName("label_pname");

        verticalLayout_3->addWidget(label_pname);

        label_pgender = new QLabel(frame_6);
        label_pgender->setObjectName("label_pgender");

        verticalLayout_3->addWidget(label_pgender);

        label_pbirthdate = new QLabel(frame_6);
        label_pbirthdate->setObjectName("label_pbirthdate");

        verticalLayout_3->addWidget(label_pbirthdate);

        label_pid = new QLabel(frame_6);
        label_pid->setObjectName("label_pid");

        verticalLayout_3->addWidget(label_pid);

        label_pphone = new QLabel(frame_6);
        label_pphone->setObjectName("label_pphone");

        verticalLayout_3->addWidget(label_pphone);

        label_pemail = new QLabel(frame_6);
        label_pemail->setObjectName("label_pemail");

        verticalLayout_3->addWidget(label_pemail);

        frame_7 = new QFrame(scrollAreaWidgetContents);
        frame_7->setObjectName("frame_7");
        frame_7->setGeometry(QRect(130, 480, 421, 391));
        frame_7->setFrameShape(QFrame::Shape::StyledPanel);
        frame_7->setFrameShadow(QFrame::Shadow::Raised);
        verticalLayout_4 = new QVBoxLayout(frame_7);
        verticalLayout_4->setObjectName("verticalLayout_4");
        lineEdit_pname = new QLineEdit(frame_7);
        lineEdit_pname->setObjectName("lineEdit_pname");
        lineEdit_pname->setMinimumSize(QSize(0, 0));

        verticalLayout_4->addWidget(lineEdit_pname);

        lineEdit_pgender = new QLineEdit(frame_7);
        lineEdit_pgender->setObjectName("lineEdit_pgender");

        verticalLayout_4->addWidget(lineEdit_pgender);

        lineEdit_pbirthdate = new QLineEdit(frame_7);
        lineEdit_pbirthdate->setObjectName("lineEdit_pbirthdate");

        verticalLayout_4->addWidget(lineEdit_pbirthdate);

        lineEdit_pid = new QLineEdit(frame_7);
        lineEdit_pid->setObjectName("lineEdit_pid");

        verticalLayout_4->addWidget(lineEdit_pid);

        lineEdit_pphone = new QLineEdit(frame_7);
        lineEdit_pphone->setObjectName("lineEdit_pphone");

        verticalLayout_4->addWidget(lineEdit_pphone);

        lineEdit_pemail = new QLineEdit(frame_7);
        lineEdit_pemail->setObjectName("lineEdit_pemail");

        verticalLayout_4->addWidget(lineEdit_pemail);

        scrollArea->setWidget(scrollAreaWidgetContents);
        stackedWidget->addWidget(page_info);
        page_reg = new QWidget();
        page_reg->setObjectName("page_reg");
        frame_8 = new QFrame(page_reg);
        frame_8->setObjectName("frame_8");
        frame_8->setGeometry(QRect(10, 0, 791, 561));
        frame_8->setFrameShape(QFrame::Shape::StyledPanel);
        frame_8->setFrameShadow(QFrame::Shadow::Raised);
        verticalLayout_5 = new QVBoxLayout(frame_8);
        verticalLayout_5->setObjectName("verticalLayout_5");
        pushButton_reg_appoint = new QPushButton(frame_8);
        pushButton_reg_appoint->setObjectName("pushButton_reg_appoint");
        pushButton_reg_appoint->setMinimumSize(QSize(0, 40));

        verticalLayout_5->addWidget(pushButton_reg_appoint);

        pushButton_reg_window = new QPushButton(frame_8);
        pushButton_reg_window->setObjectName("pushButton_reg_window");
        pushButton_reg_window->setMinimumSize(QSize(0, 40));

        verticalLayout_5->addWidget(pushButton_reg_window);

        pushButton_reg_doctor = new QPushButton(frame_8);
        pushButton_reg_doctor->setObjectName("pushButton_reg_doctor");
        pushButton_reg_doctor->setMinimumSize(QSize(0, 40));

        verticalLayout_5->addWidget(pushButton_reg_doctor);

        pushButton_reg_back = new QPushButton(frame_8);
        pushButton_reg_back->setObjectName("pushButton_reg_back");
        pushButton_reg_back->setMinimumSize(QSize(0, 40));

        verticalLayout_5->addWidget(pushButton_reg_back);

        stackedWidget->addWidget(page_reg);
        page_reg_doctor = new QWidget();
        page_reg_doctor->setObjectName("page_reg_doctor");
        scrollArea_2 = new QScrollArea(page_reg_doctor);
        scrollArea_2->setObjectName("scrollArea_2");
        scrollArea_2->setGeometry(QRect(-11, -1, 821, 611));
        scrollArea_2->setWidgetResizable(true);
        scrollAreaWidgetContents_2 = new QWidget();
        scrollAreaWidgetContents_2->setObjectName("scrollAreaWidgetContents_2");
        scrollAreaWidgetContents_2->setGeometry(QRect(0, 0, 819, 609));
        label_reg_doctor = new QLabel(scrollAreaWidgetContents_2);
        label_reg_doctor->setObjectName("label_reg_doctor");
        label_reg_doctor->setGeometry(QRect(10, 0, 121, 61));
        frame_9 = new QFrame(scrollAreaWidgetContents_2);
        frame_9->setObjectName("frame_9");
        frame_9->setGeometry(QRect(9, 59, 771, 551));
        frame_9->setFrameShape(QFrame::Shape::StyledPanel);
        frame_9->setFrameShadow(QFrame::Shadow::Raised);
        label_daoctor_pic = new QLabel(frame_9);
        label_daoctor_pic->setObjectName("label_daoctor_pic");
        label_daoctor_pic->setGeometry(QRect(10, 0, 141, 181));
        frame_10 = new QFrame(frame_9);
        frame_10->setObjectName("frame_10");
        frame_10->setGeometry(QRect(170, 20, 241, 161));
        frame_10->setFrameShape(QFrame::Shape::StyledPanel);
        frame_10->setFrameShadow(QFrame::Shadow::Raised);
        label_doctor_office = new QLabel(frame_10);
        label_doctor_office->setObjectName("label_doctor_office");
        label_doctor_office->setGeometry(QRect(20, 20, 69, 19));
        label_doctor_name = new QLabel(frame_10);
        label_doctor_name->setObjectName("label_doctor_name");
        label_doctor_name->setGeometry(QRect(20, 70, 69, 19));
        label_doctor_office_2 = new QLabel(frame_10);
        label_doctor_office_2->setObjectName("label_doctor_office_2");
        label_doctor_office_2->setGeometry(QRect(140, 20, 69, 19));
        label_doctor_name_2 = new QLabel(frame_10);
        label_doctor_name_2->setObjectName("label_doctor_name_2");
        label_doctor_name_2->setGeometry(QRect(140, 70, 69, 19));
        pushButton_docdetail = new QPushButton(frame_10);
        pushButton_docdetail->setObjectName("pushButton_docdetail");
        pushButton_docdetail->setGeometry(QRect(130, 120, 93, 28));
        pushButton_regdoctor_back = new QPushButton(scrollAreaWidgetContents_2);
        pushButton_regdoctor_back->setObjectName("pushButton_regdoctor_back");
        pushButton_regdoctor_back->setGeometry(QRect(690, 20, 93, 28));
        scrollArea_2->setWidget(scrollAreaWidgetContents_2);
        stackedWidget->addWidget(page_reg_doctor);
        page_reg_docdetail = new QWidget();
        page_reg_docdetail->setObjectName("page_reg_docdetail");
        label_docdetail = new QLabel(page_reg_docdetail);
        label_docdetail->setObjectName("label_docdetail");
        label_docdetail->setGeometry(QRect(10, 10, 191, 41));
        frame_11 = new QFrame(page_reg_docdetail);
        frame_11->setObjectName("frame_11");
        frame_11->setGeometry(QRect(10, 60, 791, 541));
        frame_11->setFrameShape(QFrame::Shape::StyledPanel);
        frame_11->setFrameShadow(QFrame::Shadow::Raised);
        label_docdetail_pic = new QLabel(frame_11);
        label_docdetail_pic->setObjectName("label_docdetail_pic");
        label_docdetail_pic->setGeometry(QRect(20, 20, 141, 171));
        frame_12 = new QFrame(frame_11);
        frame_12->setObjectName("frame_12");
        frame_12->setGeometry(QRect(20, 210, 121, 321));
        frame_12->setFrameShape(QFrame::Shape::StyledPanel);
        frame_12->setFrameShadow(QFrame::Shadow::Raised);
        verticalLayout_6 = new QVBoxLayout(frame_12);
        verticalLayout_6->setObjectName("verticalLayout_6");
        label_docdetail_office = new QLabel(frame_12);
        label_docdetail_office->setObjectName("label_docdetail_office");

        verticalLayout_6->addWidget(label_docdetail_office);

        label_docdetail_id = new QLabel(frame_12);
        label_docdetail_id->setObjectName("label_docdetail_id");

        verticalLayout_6->addWidget(label_docdetail_id);

        label_docdetail_name = new QLabel(frame_12);
        label_docdetail_name->setObjectName("label_docdetail_name");

        verticalLayout_6->addWidget(label_docdetail_name);

        label_docdetail_worktime = new QLabel(frame_12);
        label_docdetail_worktime->setObjectName("label_docdetail_worktime");

        verticalLayout_6->addWidget(label_docdetail_worktime);

        label_docdetail_cost = new QLabel(frame_12);
        label_docdetail_cost->setObjectName("label_docdetail_cost");

        verticalLayout_6->addWidget(label_docdetail_cost);

        label_docdetail_maxpatient = new QLabel(frame_12);
        label_docdetail_maxpatient->setObjectName("label_docdetail_maxpatient");

        verticalLayout_6->addWidget(label_docdetail_maxpatient);

        frame_13 = new QFrame(frame_11);
        frame_13->setObjectName("frame_13");
        frame_13->setGeometry(QRect(170, 210, 281, 321));
        frame_13->setFrameShape(QFrame::Shape::StyledPanel);
        frame_13->setFrameShadow(QFrame::Shadow::Raised);
        verticalLayout_7 = new QVBoxLayout(frame_13);
        verticalLayout_7->setObjectName("verticalLayout_7");
        label_docdetail_office_2 = new QLabel(frame_13);
        label_docdetail_office_2->setObjectName("label_docdetail_office_2");

        verticalLayout_7->addWidget(label_docdetail_office_2);

        label_docdetail_id_2 = new QLabel(frame_13);
        label_docdetail_id_2->setObjectName("label_docdetail_id_2");

        verticalLayout_7->addWidget(label_docdetail_id_2);

        label_docdetail_name_2 = new QLabel(frame_13);
        label_docdetail_name_2->setObjectName("label_docdetail_name_2");

        verticalLayout_7->addWidget(label_docdetail_name_2);

        label_docdetail_worktime_2 = new QLabel(frame_13);
        label_docdetail_worktime_2->setObjectName("label_docdetail_worktime_2");

        verticalLayout_7->addWidget(label_docdetail_worktime_2);

        label_docdetail_cost_2 = new QLabel(frame_13);
        label_docdetail_cost_2->setObjectName("label_docdetail_cost_2");

        verticalLayout_7->addWidget(label_docdetail_cost_2);

        label_docdetail_maxpatient_2 = new QLabel(frame_13);
        label_docdetail_maxpatient_2->setObjectName("label_docdetail_maxpatient_2");

        verticalLayout_7->addWidget(label_docdetail_maxpatient_2);

        pushButton_doctor_close = new QPushButton(page_reg_docdetail);
        pushButton_doctor_close->setObjectName("pushButton_doctor_close");
        pushButton_doctor_close->setGeometry(QRect(732, 10, 31, 28));
        stackedWidget->addWidget(page_reg_docdetail);
        page_reg_window = new QWidget();
        page_reg_window->setObjectName("page_reg_window");
        label_window = new QLabel(page_reg_window);
        label_window->setObjectName("label_window");
        label_window->setGeometry(QRect(10, 10, 121, 51));
        tableWidget_window = new QTableWidget(page_reg_window);
        if (tableWidget_window->columnCount() < 9)
            tableWidget_window->setColumnCount(9);
        QTableWidgetItem *__qtablewidgetitem6 = new QTableWidgetItem();
        tableWidget_window->setHorizontalHeaderItem(0, __qtablewidgetitem6);
        QTableWidgetItem *__qtablewidgetitem7 = new QTableWidgetItem();
        tableWidget_window->setHorizontalHeaderItem(1, __qtablewidgetitem7);
        QTableWidgetItem *__qtablewidgetitem8 = new QTableWidgetItem();
        tableWidget_window->setHorizontalHeaderItem(2, __qtablewidgetitem8);
        QTableWidgetItem *__qtablewidgetitem9 = new QTableWidgetItem();
        tableWidget_window->setHorizontalHeaderItem(3, __qtablewidgetitem9);
        QTableWidgetItem *__qtablewidgetitem10 = new QTableWidgetItem();
        tableWidget_window->setHorizontalHeaderItem(4, __qtablewidgetitem10);
        QTableWidgetItem *__qtablewidgetitem11 = new QTableWidgetItem();
        tableWidget_window->setHorizontalHeaderItem(5, __qtablewidgetitem11);
        QTableWidgetItem *__qtablewidgetitem12 = new QTableWidgetItem();
        tableWidget_window->setHorizontalHeaderItem(6, __qtablewidgetitem12);
        QTableWidgetItem *__qtablewidgetitem13 = new QTableWidgetItem();
        tableWidget_window->setHorizontalHeaderItem(7, __qtablewidgetitem13);
        QTableWidgetItem *__qtablewidgetitem14 = new QTableWidgetItem();
        tableWidget_window->setHorizontalHeaderItem(8, __qtablewidgetitem14);
        tableWidget_window->setObjectName("tableWidget_window");
        tableWidget_window->setGeometry(QRect(10, 60, 791, 401));
        label_window_office = new QLabel(page_reg_window);
        label_window_office->setObjectName("label_window_office");
        label_window_office->setGeometry(QRect(30, 480, 69, 19));
        label_window_dname = new QLabel(page_reg_window);
        label_window_dname->setObjectName("label_window_dname");
        label_window_dname->setGeometry(QRect(30, 520, 69, 19));
        lineEdit_window_office = new QLineEdit(page_reg_window);
        lineEdit_window_office->setObjectName("lineEdit_window_office");
        lineEdit_window_office->setGeometry(QRect(110, 480, 113, 25));
        lineEdit_window_dname = new QLineEdit(page_reg_window);
        lineEdit_window_dname->setObjectName("lineEdit_window_dname");
        lineEdit_window_dname->setGeometry(QRect(110, 520, 113, 25));
        pushButton_window_confirm = new QPushButton(page_reg_window);
        pushButton_window_confirm->setObjectName("pushButton_window_confirm");
        pushButton_window_confirm->setGeometry(QRect(580, 550, 93, 28));
        pushButton_window_back = new QPushButton(page_reg_window);
        pushButton_window_back->setObjectName("pushButton_window_back");
        pushButton_window_back->setGeometry(QRect(710, 550, 93, 28));
        label_window_cost = new QLabel(page_reg_window);
        label_window_cost->setObjectName("label_window_cost");
        label_window_cost->setGeometry(QRect(30, 560, 69, 19));
        lineEdit_window_cost = new QLineEdit(page_reg_window);
        lineEdit_window_cost->setObjectName("lineEdit_window_cost");
        lineEdit_window_cost->setGeometry(QRect(110, 560, 113, 25));
        stackedWidget->addWidget(page_reg_window);
        page_reg_appoint = new QWidget();
        page_reg_appoint->setObjectName("page_reg_appoint");
        label_reg_appoint = new QLabel(page_reg_appoint);
        label_reg_appoint->setObjectName("label_reg_appoint");
        label_reg_appoint->setGeometry(QRect(240, 280, 69, 19));
        stackedWidget->addWidget(page_reg_appoint);
        page_history = new QWidget();
        page_history->setObjectName("page_history");
        label_history = new QLabel(page_history);
        label_history->setObjectName("label_history");
        label_history->setGeometry(QRect(10, 10, 131, 51));
        tableWidget_history = new QTableWidget(page_history);
        if (tableWidget_history->columnCount() < 5)
            tableWidget_history->setColumnCount(5);
        QTableWidgetItem *__qtablewidgetitem15 = new QTableWidgetItem();
        tableWidget_history->setHorizontalHeaderItem(0, __qtablewidgetitem15);
        QTableWidgetItem *__qtablewidgetitem16 = new QTableWidgetItem();
        tableWidget_history->setHorizontalHeaderItem(1, __qtablewidgetitem16);
        QTableWidgetItem *__qtablewidgetitem17 = new QTableWidgetItem();
        tableWidget_history->setHorizontalHeaderItem(2, __qtablewidgetitem17);
        QTableWidgetItem *__qtablewidgetitem18 = new QTableWidgetItem();
        tableWidget_history->setHorizontalHeaderItem(3, __qtablewidgetitem18);
        QTableWidgetItem *__qtablewidgetitem19 = new QTableWidgetItem();
        tableWidget_history->setHorizontalHeaderItem(4, __qtablewidgetitem19);
        tableWidget_history->setObjectName("tableWidget_history");
        tableWidget_history->setGeometry(QRect(0, 60, 811, 461));
        pushButton_history_back = new QPushButton(page_history);
        pushButton_history_back->setObjectName("pushButton_history_back");
        pushButton_history_back->setGeometry(QRect(680, 540, 93, 28));
        stackedWidget->addWidget(page_history);
        page_advice = new QWidget();
        page_advice->setObjectName("page_advice");
        label_advice = new QLabel(page_advice);
        label_advice->setObjectName("label_advice");
        label_advice->setGeometry(QRect(10, 10, 131, 41));
        tableWidget_advice = new QTableWidget(page_advice);
        if (tableWidget_advice->columnCount() < 5)
            tableWidget_advice->setColumnCount(5);
        QTableWidgetItem *__qtablewidgetitem20 = new QTableWidgetItem();
        tableWidget_advice->setHorizontalHeaderItem(0, __qtablewidgetitem20);
        QTableWidgetItem *__qtablewidgetitem21 = new QTableWidgetItem();
        tableWidget_advice->setHorizontalHeaderItem(1, __qtablewidgetitem21);
        QTableWidgetItem *__qtablewidgetitem22 = new QTableWidgetItem();
        tableWidget_advice->setHorizontalHeaderItem(2, __qtablewidgetitem22);
        QTableWidgetItem *__qtablewidgetitem23 = new QTableWidgetItem();
        tableWidget_advice->setHorizontalHeaderItem(3, __qtablewidgetitem23);
        QTableWidgetItem *__qtablewidgetitem24 = new QTableWidgetItem();
        tableWidget_advice->setHorizontalHeaderItem(4, __qtablewidgetitem24);
        tableWidget_advice->setObjectName("tableWidget_advice");
        tableWidget_advice->setGeometry(QRect(10, 60, 801, 271));
        label_prescription_content = new QLabel(page_advice);
        label_prescription_content->setObjectName("label_prescription_content");
        label_prescription_content->setGeometry(QRect(40, 370, 81, 41));
        lineEdit_prescription_content = new QLineEdit(page_advice);
        lineEdit_prescription_content->setObjectName("lineEdit_prescription_content");
        lineEdit_prescription_content->setGeometry(QRect(140, 380, 341, 25));
        label_advicedetail = new QLabel(page_advice);
        label_advicedetail->setObjectName("label_advicedetail");
        label_advicedetail->setGeometry(QRect(40, 450, 91, 41));
        lineEdit_advicedetail = new QLineEdit(page_advice);
        lineEdit_advicedetail->setObjectName("lineEdit_advicedetail");
        lineEdit_advicedetail->setGeometry(QRect(140, 460, 341, 151));
        pushButton_advicedetail = new QPushButton(page_advice);
        pushButton_advicedetail->setObjectName("pushButton_advicedetail");
        pushButton_advicedetail->setGeometry(QRect(682, 457, 111, 61));
        pushButton_advice_back = new QPushButton(page_advice);
        pushButton_advice_back->setObjectName("pushButton_advice_back");
        pushButton_advice_back->setGeometry(QRect(682, 540, 111, 28));
        stackedWidget->addWidget(page_advice);
        page_prescription = new QWidget();
        page_prescription->setObjectName("page_prescription");
        label_prescription_info = new QLabel(page_prescription);
        label_prescription_info->setObjectName("label_prescription_info");
        label_prescription_info->setGeometry(QRect(20, 20, 131, 41));
        tableWidget_prescription = new QTableWidget(page_prescription);
        if (tableWidget_prescription->columnCount() < 4)
            tableWidget_prescription->setColumnCount(4);
        QTableWidgetItem *__qtablewidgetitem25 = new QTableWidgetItem();
        tableWidget_prescription->setHorizontalHeaderItem(0, __qtablewidgetitem25);
        QTableWidgetItem *__qtablewidgetitem26 = new QTableWidgetItem();
        tableWidget_prescription->setHorizontalHeaderItem(1, __qtablewidgetitem26);
        QTableWidgetItem *__qtablewidgetitem27 = new QTableWidgetItem();
        tableWidget_prescription->setHorizontalHeaderItem(2, __qtablewidgetitem27);
        QTableWidgetItem *__qtablewidgetitem28 = new QTableWidgetItem();
        tableWidget_prescription->setHorizontalHeaderItem(3, __qtablewidgetitem28);
        tableWidget_prescription->setObjectName("tableWidget_prescription");
        tableWidget_prescription->setGeometry(QRect(10, 60, 801, 391));
        label_prescription_id = new QLabel(page_prescription);
        label_prescription_id->setObjectName("label_prescription_id");
        label_prescription_id->setGeometry(QRect(20, 480, 91, 31));
        label_pre_doctor = new QLabel(page_prescription);
        label_pre_doctor->setObjectName("label_pre_doctor");
        label_pre_doctor->setGeometry(QRect(20, 520, 81, 41));
        lineEdit_prescription_id = new QLineEdit(page_prescription);
        lineEdit_prescription_id->setObjectName("lineEdit_prescription_id");
        lineEdit_prescription_id->setGeometry(QRect(110, 480, 113, 25));
        lineEdit_prescription_doctor = new QLineEdit(page_prescription);
        lineEdit_prescription_doctor->setObjectName("lineEdit_prescription_doctor");
        lineEdit_prescription_doctor->setGeometry(QRect(110, 530, 113, 25));
        label_predetail = new QLabel(page_prescription);
        label_predetail->setObjectName("label_predetail");
        label_predetail->setGeometry(QRect(280, 480, 91, 31));
        lineEdit_predetail = new QLineEdit(page_prescription);
        lineEdit_predetail->setObjectName("lineEdit_predetail");
        lineEdit_predetail->setGeometry(QRect(380, 480, 231, 81));
        pushButton_prescription_detail = new QPushButton(page_prescription);
        pushButton_prescription_detail->setObjectName("pushButton_prescription_detail");
        pushButton_prescription_detail->setGeometry(QRect(680, 490, 93, 28));
        pushButton_prescription_back = new QPushButton(page_prescription);
        pushButton_prescription_back->setObjectName("pushButton_prescription_back");
        pushButton_prescription_back->setGeometry(QRect(680, 540, 93, 28));
        stackedWidget->addWidget(page_prescription);
        page_com = new QWidget();
        page_com->setObjectName("page_com");
        label_com = new QLabel(page_com);
        label_com->setObjectName("label_com");
        label_com->setGeometry(QRect(20, 10, 131, 41));
        tableWidget_com = new QTableWidget(page_com);
        if (tableWidget_com->columnCount() < 3)
            tableWidget_com->setColumnCount(3);
        QTableWidgetItem *__qtablewidgetitem29 = new QTableWidgetItem();
        tableWidget_com->setHorizontalHeaderItem(0, __qtablewidgetitem29);
        QTableWidgetItem *__qtablewidgetitem30 = new QTableWidgetItem();
        tableWidget_com->setHorizontalHeaderItem(1, __qtablewidgetitem30);
        QTableWidgetItem *__qtablewidgetitem31 = new QTableWidgetItem();
        tableWidget_com->setHorizontalHeaderItem(2, __qtablewidgetitem31);
        tableWidget_com->setObjectName("tableWidget_com");
        tableWidget_com->setGeometry(QRect(10, 70, 721, 281));
        label_office = new QLabel(page_com);
        label_office->setObjectName("label_office");
        label_office->setGeometry(QRect(30, 380, 69, 41));
        label_dname = new QLabel(page_com);
        label_dname->setObjectName("label_dname");
        label_dname->setGeometry(QRect(20, 430, 101, 61));
        lineEdit_office = new QLineEdit(page_com);
        lineEdit_office->setObjectName("lineEdit_office");
        lineEdit_office->setGeometry(QRect(130, 390, 113, 25));
        lineEdit_dname = new QLineEdit(page_com);
        lineEdit_dname->setObjectName("lineEdit_dname");
        lineEdit_dname->setGeometry(QRect(130, 450, 113, 25));
        label_dsuggest = new QLabel(page_com);
        label_dsuggest->setObjectName("label_dsuggest");
        label_dsuggest->setGeometry(QRect(300, 380, 81, 41));
        lineEdit_dsuggest = new QLineEdit(page_com);
        lineEdit_dsuggest->setObjectName("lineEdit_dsuggest");
        lineEdit_dsuggest->setGeometry(QRect(410, 390, 401, 71));
        label_psuggest = new QLabel(page_com);
        label_psuggest->setObjectName("label_psuggest");
        label_psuggest->setGeometry(QRect(300, 470, 91, 41));
        lineEdit_psuggest = new QLineEdit(page_com);
        lineEdit_psuggest->setObjectName("lineEdit_psuggest");
        lineEdit_psuggest->setGeometry(QRect(410, 470, 401, 91));
        pushButton_send = new QPushButton(page_com);
        pushButton_send->setObjectName("pushButton_send");
        pushButton_send->setGeometry(QRect(550, 570, 93, 28));
        pushButton_com_back = new QPushButton(page_com);
        pushButton_com_back->setObjectName("pushButton_com_back");
        pushButton_com_back->setGeometry(QRect(690, 570, 93, 28));
        stackedWidget->addWidget(page_com);

        horizontalLayout_2->addWidget(frame_3);

        MainWindow_patient->setCentralWidget(centralwidget);
        statusbar = new QStatusBar(MainWindow_patient);
        statusbar->setObjectName("statusbar");
        MainWindow_patient->setStatusBar(statusbar);

        retranslateUi(MainWindow_patient);

        stackedWidget->setCurrentIndex(5);


        QMetaObject::connectSlotsByName(MainWindow_patient);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow_patient)
    {
        MainWindow_patient->setWindowTitle(QCoreApplication::translate("MainWindow_patient", "MainWindow", nullptr));
        home_btn->setText(QCoreApplication::translate("MainWindow_patient", "\344\270\273\351\241\265", nullptr));
        info_btn->setText(QCoreApplication::translate("MainWindow_patient", "\344\270\252\344\272\272\344\277\241\346\201\257", nullptr));
        regist_btn->setText(QCoreApplication::translate("MainWindow_patient", "\346\214\202\345\217\267\344\277\241\346\201\257", nullptr));
        history_btn->setText(QCoreApplication::translate("MainWindow_patient", "\347\227\205\345\216\206\344\277\241\346\201\257", nullptr));
        advice_btn->setText(QCoreApplication::translate("MainWindow_patient", "\345\214\273\345\230\261\344\277\241\346\201\257", nullptr));
        presciption_btn->setText(QCoreApplication::translate("MainWindow_patient", "\345\244\204\346\226\271\344\277\241\346\201\257", nullptr));
        com_btn->setText(QCoreApplication::translate("MainWindow_patient", "\345\214\273\346\202\243\346\262\237\351\200\232", nullptr));
        label_home->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:36pt;\">\347\224\250\346\210\267\346\202\250\345\245\275</span></p></body></html>", nullptr));
        label_info->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:18pt;\">\344\270\252\344\272\272\344\277\241\346\201\257</span></p></body></html>", nullptr));
        QTableWidgetItem *___qtablewidgetitem = tableWidget_info->horizontalHeaderItem(0);
        ___qtablewidgetitem->setText(QCoreApplication::translate("MainWindow_patient", "\345\247\223\345\220\215", nullptr));
        QTableWidgetItem *___qtablewidgetitem1 = tableWidget_info->horizontalHeaderItem(1);
        ___qtablewidgetitem1->setText(QCoreApplication::translate("MainWindow_patient", "\346\200\247\345\210\253", nullptr));
        QTableWidgetItem *___qtablewidgetitem2 = tableWidget_info->horizontalHeaderItem(2);
        ___qtablewidgetitem2->setText(QCoreApplication::translate("MainWindow_patient", "\345\207\272\347\224\237\346\227\245\346\234\237", nullptr));
        QTableWidgetItem *___qtablewidgetitem3 = tableWidget_info->horizontalHeaderItem(3);
        ___qtablewidgetitem3->setText(QCoreApplication::translate("MainWindow_patient", "\350\272\253\344\273\275\350\257\201\345\217\267", nullptr));
        QTableWidgetItem *___qtablewidgetitem4 = tableWidget_info->horizontalHeaderItem(4);
        ___qtablewidgetitem4->setText(QCoreApplication::translate("MainWindow_patient", "\346\211\213\346\234\272\345\217\267", nullptr));
        QTableWidgetItem *___qtablewidgetitem5 = tableWidget_info->horizontalHeaderItem(5);
        ___qtablewidgetitem5->setText(QCoreApplication::translate("MainWindow_patient", "\351\202\256\347\256\261", nullptr));
        pushButton_info_edit->setText(QCoreApplication::translate("MainWindow_patient", "\347\274\226\350\276\221", nullptr));
        pushButton_info_confirm->setText(QCoreApplication::translate("MainWindow_patient", "\347\241\256\350\256\244", nullptr));
        pushButton_info_back->setText(QCoreApplication::translate("MainWindow_patient", "\350\277\224\345\233\236", nullptr));
        label_pname->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:12pt;\">\345\247\223\345\220\215</span></p></body></html>", nullptr));
        label_pgender->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:12pt;\">\346\200\247\345\210\253</span></p></body></html>", nullptr));
        label_pbirthdate->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:12pt;\">\345\207\272\347\224\237\346\227\245\346\234\237</span></p></body></html>", nullptr));
        label_pid->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:12pt;\">\350\272\253\344\273\275\350\257\201\345\217\267</span></p></body></html>", nullptr));
        label_pphone->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:12pt;\">\346\211\213\346\234\272\345\217\267</span></p></body></html>", nullptr));
        label_pemail->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:12pt;\">\351\202\256\347\256\261</span></p></body></html>", nullptr));
        pushButton_reg_appoint->setText(QCoreApplication::translate("MainWindow_patient", "\351\242\204\347\272\246\346\214\202\345\217\267", nullptr));
        pushButton_reg_window->setText(QCoreApplication::translate("MainWindow_patient", "\347\252\227\345\217\243\346\214\202\345\217\267", nullptr));
        pushButton_reg_doctor->setText(QCoreApplication::translate("MainWindow_patient", "\346\237\245\347\234\213\345\214\273\347\224\237\344\277\241\346\201\257", nullptr));
        pushButton_reg_back->setText(QCoreApplication::translate("MainWindow_patient", "\350\277\224\345\233\236", nullptr));
        label_reg_doctor->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:18pt;\">\345\214\273\347\224\237\344\277\241\346\201\257</span></p></body></html>", nullptr));
        label_daoctor_pic->setText(QCoreApplication::translate("MainWindow_patient", "\347\205\247\347\211\207", nullptr));
        label_doctor_office->setText(QCoreApplication::translate("MainWindow_patient", "\347\247\221\345\256\244", nullptr));
        label_doctor_name->setText(QCoreApplication::translate("MainWindow_patient", "\345\247\223\345\220\215", nullptr));
        label_doctor_office_2->setText(QCoreApplication::translate("MainWindow_patient", "TextLabel", nullptr));
        label_doctor_name_2->setText(QCoreApplication::translate("MainWindow_patient", "TextLabel", nullptr));
        pushButton_docdetail->setText(QCoreApplication::translate("MainWindow_patient", "\350\257\246\346\203\205\344\277\241\346\201\257", nullptr));
        pushButton_regdoctor_back->setText(QCoreApplication::translate("MainWindow_patient", "\350\277\224\345\233\236", nullptr));
        label_docdetail->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:18pt;\">\345\214\273\347\224\237\350\257\246\346\203\205\344\277\241\346\201\257</span></p></body></html>", nullptr));
        label_docdetail_pic->setText(QCoreApplication::translate("MainWindow_patient", "\347\205\247\347\211\207", nullptr));
        label_docdetail_office->setText(QCoreApplication::translate("MainWindow_patient", "\347\247\221\345\256\244", nullptr));
        label_docdetail_id->setText(QCoreApplication::translate("MainWindow_patient", "\345\267\245\345\217\267", nullptr));
        label_docdetail_name->setText(QCoreApplication::translate("MainWindow_patient", "\345\247\223\345\220\215", nullptr));
        label_docdetail_worktime->setText(QCoreApplication::translate("MainWindow_patient", "\344\270\212\347\217\255\346\227\266\351\227\264", nullptr));
        label_docdetail_cost->setText(QCoreApplication::translate("MainWindow_patient", "\346\214\202\345\217\267\350\264\271\347\224\250", nullptr));
        label_docdetail_maxpatient->setText(QCoreApplication::translate("MainWindow_patient", "\345\215\225\346\227\245\346\202\243\350\200\205\344\270\212\351\231\220", nullptr));
        label_docdetail_office_2->setText(QCoreApplication::translate("MainWindow_patient", "TextLabel", nullptr));
        label_docdetail_id_2->setText(QCoreApplication::translate("MainWindow_patient", "TextLabel", nullptr));
        label_docdetail_name_2->setText(QCoreApplication::translate("MainWindow_patient", "TextLabel", nullptr));
        label_docdetail_worktime_2->setText(QCoreApplication::translate("MainWindow_patient", "TextLabel", nullptr));
        label_docdetail_cost_2->setText(QCoreApplication::translate("MainWindow_patient", "TextLabel", nullptr));
        label_docdetail_maxpatient_2->setText(QCoreApplication::translate("MainWindow_patient", "TextLabel", nullptr));
        pushButton_doctor_close->setText(QCoreApplication::translate("MainWindow_patient", "\303\227", nullptr));
        label_window->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:18pt;\">\347\252\227\345\217\243\346\214\202\345\217\267</span></p></body></html>", nullptr));
        QTableWidgetItem *___qtablewidgetitem6 = tableWidget_window->horizontalHeaderItem(0);
        ___qtablewidgetitem6->setText(QCoreApplication::translate("MainWindow_patient", "\347\247\221\345\256\244", nullptr));
        QTableWidgetItem *___qtablewidgetitem7 = tableWidget_window->horizontalHeaderItem(1);
        ___qtablewidgetitem7->setText(QCoreApplication::translate("MainWindow_patient", "\345\214\273\347\224\237\347\274\226\345\217\267", nullptr));
        QTableWidgetItem *___qtablewidgetitem8 = tableWidget_window->horizontalHeaderItem(2);
        ___qtablewidgetitem8->setText(QCoreApplication::translate("MainWindow_patient", "\345\267\245\345\217\267", nullptr));
        QTableWidgetItem *___qtablewidgetitem9 = tableWidget_window->horizontalHeaderItem(3);
        ___qtablewidgetitem9->setText(QCoreApplication::translate("MainWindow_patient", "\345\214\273\347\224\237\345\247\223\345\220\215", nullptr));
        QTableWidgetItem *___qtablewidgetitem10 = tableWidget_window->horizontalHeaderItem(4);
        ___qtablewidgetitem10->setText(QCoreApplication::translate("MainWindow_patient", "\344\270\212\347\217\255\346\227\266\351\227\264", nullptr));
        QTableWidgetItem *___qtablewidgetitem11 = tableWidget_window->horizontalHeaderItem(5);
        ___qtablewidgetitem11->setText(QCoreApplication::translate("MainWindow_patient", "\346\214\202\345\217\267\350\264\271\347\224\250", nullptr));
        QTableWidgetItem *___qtablewidgetitem12 = tableWidget_window->horizontalHeaderItem(6);
        ___qtablewidgetitem12->setText(QCoreApplication::translate("MainWindow_patient", "\345\215\225\346\227\245\346\202\243\350\200\205\344\270\212\351\231\220", nullptr));
        QTableWidgetItem *___qtablewidgetitem13 = tableWidget_window->horizontalHeaderItem(7);
        ___qtablewidgetitem13->setText(QCoreApplication::translate("MainWindow_patient", "\345\267\262\351\242\204\347\272\246\344\272\272\346\225\260", nullptr));
        QTableWidgetItem *___qtablewidgetitem14 = tableWidget_window->horizontalHeaderItem(8);
        ___qtablewidgetitem14->setText(QCoreApplication::translate("MainWindow_patient", "\345\211\251\344\275\231\351\242\204\347\272\246\344\272\272\346\225\260", nullptr));
        label_window_office->setText(QCoreApplication::translate("MainWindow_patient", "\347\247\221\345\256\244", nullptr));
        label_window_dname->setText(QCoreApplication::translate("MainWindow_patient", "\345\214\273\347\224\237\345\247\223\345\220\215", nullptr));
        pushButton_window_confirm->setText(QCoreApplication::translate("MainWindow_patient", "\347\241\256\350\256\244\346\214\202\345\217\267", nullptr));
        pushButton_window_back->setText(QCoreApplication::translate("MainWindow_patient", "\350\277\224\345\233\236", nullptr));
        label_window_cost->setText(QCoreApplication::translate("MainWindow_patient", "\346\214\202\345\217\267\350\264\271\347\224\250", nullptr));
        label_reg_appoint->setText(QCoreApplication::translate("MainWindow_patient", "\351\242\204\347\272\246\346\214\202\345\217\267", nullptr));
        label_history->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:18pt;\">\347\227\205\345\216\206\344\277\241\346\201\257</span></p></body></html>", nullptr));
        QTableWidgetItem *___qtablewidgetitem15 = tableWidget_history->horizontalHeaderItem(0);
        ___qtablewidgetitem15->setText(QCoreApplication::translate("MainWindow_patient", "\347\227\205\345\216\206\345\272\217\345\217\267", nullptr));
        QTableWidgetItem *___qtablewidgetitem16 = tableWidget_history->horizontalHeaderItem(1);
        ___qtablewidgetitem16->setText(QCoreApplication::translate("MainWindow_patient", "\347\227\205\345\216\206\345\273\272\347\253\213\346\227\245\346\234\237", nullptr));
        QTableWidgetItem *___qtablewidgetitem17 = tableWidget_history->horizontalHeaderItem(2);
        ___qtablewidgetitem17->setText(QCoreApplication::translate("MainWindow_patient", "\347\247\221\345\256\244", nullptr));
        QTableWidgetItem *___qtablewidgetitem18 = tableWidget_history->horizontalHeaderItem(3);
        ___qtablewidgetitem18->setText(QCoreApplication::translate("MainWindow_patient", "\344\270\273\346\262\273\345\214\273\347\224\237", nullptr));
        QTableWidgetItem *___qtablewidgetitem19 = tableWidget_history->horizontalHeaderItem(4);
        ___qtablewidgetitem19->setText(QCoreApplication::translate("MainWindow_patient", "\350\257\212\346\226\255\347\273\223\346\236\234", nullptr));
        pushButton_history_back->setText(QCoreApplication::translate("MainWindow_patient", "\350\277\224\345\233\236", nullptr));
        label_advice->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:18pt;\">\345\214\273\345\230\261\344\277\241\346\201\257</span></p></body></html>", nullptr));
        QTableWidgetItem *___qtablewidgetitem20 = tableWidget_advice->horizontalHeaderItem(0);
        ___qtablewidgetitem20->setText(QCoreApplication::translate("MainWindow_patient", "\345\214\273\345\230\261\345\272\217\345\217\267", nullptr));
        QTableWidgetItem *___qtablewidgetitem21 = tableWidget_advice->horizontalHeaderItem(1);
        ___qtablewidgetitem21->setText(QCoreApplication::translate("MainWindow_patient", "\346\227\245\346\234\237", nullptr));
        QTableWidgetItem *___qtablewidgetitem22 = tableWidget_advice->horizontalHeaderItem(2);
        ___qtablewidgetitem22->setText(QCoreApplication::translate("MainWindow_patient", "\347\247\221\345\256\244", nullptr));
        QTableWidgetItem *___qtablewidgetitem23 = tableWidget_advice->horizontalHeaderItem(3);
        ___qtablewidgetitem23->setText(QCoreApplication::translate("MainWindow_patient", "\344\270\273\346\262\273\345\214\273\347\224\237", nullptr));
        QTableWidgetItem *___qtablewidgetitem24 = tableWidget_advice->horizontalHeaderItem(4);
        ___qtablewidgetitem24->setText(QCoreApplication::translate("MainWindow_patient", "\345\244\204\346\226\271\345\206\205\345\256\271", nullptr));
        label_prescription_content->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:12pt;\">\345\244\204\346\226\271\345\206\205\345\256\271</span></p></body></html>", nullptr));
        label_advicedetail->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:12pt;\">\345\214\273\345\230\261\350\257\246\346\203\205</span></p></body></html>", nullptr));
        pushButton_advicedetail->setText(QCoreApplication::translate("MainWindow_patient", "\346\237\245\347\234\213\350\257\246\346\203\205\344\277\241\346\201\257", nullptr));
        pushButton_advice_back->setText(QCoreApplication::translate("MainWindow_patient", "\350\277\224\345\233\236", nullptr));
        label_prescription_info->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:18pt;\">\345\244\204\346\226\271\344\277\241\346\201\257</span></p></body></html>", nullptr));
        QTableWidgetItem *___qtablewidgetitem25 = tableWidget_prescription->horizontalHeaderItem(0);
        ___qtablewidgetitem25->setText(QCoreApplication::translate("MainWindow_patient", "\345\244\204\346\226\271\345\272\217\345\217\267", nullptr));
        QTableWidgetItem *___qtablewidgetitem26 = tableWidget_prescription->horizontalHeaderItem(1);
        ___qtablewidgetitem26->setText(QCoreApplication::translate("MainWindow_patient", "\346\227\245\346\234\237", nullptr));
        QTableWidgetItem *___qtablewidgetitem27 = tableWidget_prescription->horizontalHeaderItem(2);
        ___qtablewidgetitem27->setText(QCoreApplication::translate("MainWindow_patient", "\347\247\221\345\256\244", nullptr));
        QTableWidgetItem *___qtablewidgetitem28 = tableWidget_prescription->horizontalHeaderItem(3);
        ___qtablewidgetitem28->setText(QCoreApplication::translate("MainWindow_patient", "\344\270\273\346\262\273\345\214\273\347\224\237", nullptr));
        label_prescription_id->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:12pt;\">\345\244\204\346\226\271\345\272\217\345\217\267</span></p></body></html>", nullptr));
        label_pre_doctor->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:12pt;\">\344\270\273\346\262\273\345\214\273\347\224\237</span></p></body></html>", nullptr));
        label_predetail->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:12pt;\">\345\244\204\346\226\271\350\257\246\346\203\205</span></p></body></html>", nullptr));
        pushButton_prescription_detail->setText(QCoreApplication::translate("MainWindow_patient", "\346\237\245\347\234\213\350\257\246\346\203\205", nullptr));
        pushButton_prescription_back->setText(QCoreApplication::translate("MainWindow_patient", "\350\277\224\345\233\236", nullptr));
        label_com->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:18pt;\">\345\214\273\346\202\243\346\262\237\351\200\232</span></p></body></html>", nullptr));
        QTableWidgetItem *___qtablewidgetitem29 = tableWidget_com->horizontalHeaderItem(0);
        ___qtablewidgetitem29->setText(QCoreApplication::translate("MainWindow_patient", "\347\247\221\345\256\244", nullptr));
        QTableWidgetItem *___qtablewidgetitem30 = tableWidget_com->horizontalHeaderItem(1);
        ___qtablewidgetitem30->setText(QCoreApplication::translate("MainWindow_patient", "\345\267\245\345\217\267", nullptr));
        QTableWidgetItem *___qtablewidgetitem31 = tableWidget_com->horizontalHeaderItem(2);
        ___qtablewidgetitem31->setText(QCoreApplication::translate("MainWindow_patient", "\345\214\273\347\224\237\345\247\223\345\220\215", nullptr));
        label_office->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:12pt;\">\347\247\221\345\256\244</span></p></body></html>", nullptr));
        label_dname->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:12pt;\">\345\214\273\347\224\237\345\247\223\345\220\215</span></p></body></html>", nullptr));
        label_dsuggest->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:12pt;\">\345\214\273\347\224\237\345\273\272\350\256\256</span></p></body></html>", nullptr));
        label_psuggest->setText(QCoreApplication::translate("MainWindow_patient", "<html><head/><body><p><span style=\" font-size:12pt;\">\346\202\243\350\200\205\345\273\272\350\256\256</span></p></body></html>", nullptr));
        pushButton_send->setText(QCoreApplication::translate("MainWindow_patient", "\345\217\221\351\200\201", nullptr));
        pushButton_com_back->setText(QCoreApplication::translate("MainWindow_patient", "\350\277\224\345\233\236", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow_patient: public Ui_MainWindow_patient {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_PATIENT_H
