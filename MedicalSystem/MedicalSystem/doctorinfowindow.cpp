#include "doctormainwindow.h"

DoctorInfoWindow::DoctorInfoWindow(QWidget *parent) : QMainWindow(parent)
{
    setWindowTitle("个人信息");
    resize(450, 600);
    setStyleSheet(
        "QMainWindow {"
        "    background-color: #e6ecf2;"
        "    font-family: 'Segoe UI', Arial, sans-serif;"
        "}"
        "QLabel {"
        "    font-size: 14px;"
        "    color: #2c3e50;"
        "    font-weight: 500;"
        "}"
        "QTableWidget {"
        "    background-color: #ffffff;"
        "    border: 1px solid #bdc3c7;"
        "    border-radius: 6px;"
        "    font-size: 13px;"
        "}"
        "QTableWidget::item {"
        "    padding: 8px;"
        "}"
        "QTableWidget::item:selected {"
        "    background-color: #3498db;"
        "    color: white;"
        "}"
        "QTextEdit, QLineEdit {"
        "    padding: 8px;"
        "    font-size: 14px;"
        "    border: 1px solid #bdc3c7;"
        "    border-radius: 6px;"
        "    background-color: #ffffff;"
        "}"
        "QTextEdit:focus, QLineEdit:focus {"
        "    border: 1px solid #3498db;"
        "    background-color: #f8fcff;"
        "}"
        "QPushButton {"
        "    background-color: #3498db;"
        "    color: white;"
        "    font-size: 14px;"
        "    font-weight: bold;"
        "    padding: 10px 20px;"
        "    border: none;"
        "    border-radius: 6px;"
        "    min-width: 100px;"
        "}"
        "QPushButton:hover {"
        "    background-color: #2980b9;"
        "}"
        "QPushButton:pressed {"
        "    background-color: #20638f;"
        "}"
        "QPushButton#returnButton {"
        "    background-color: #7f8c8d;"
        "}"
        "QPushButton#returnButton:hover {"
        "    background-color: #6d7676;"
        "}"
        "QPushButton#returnButton:pressed {"
        "    background-color: #596060;"
        "}"
        );

    QWidget *centralWidget = new QWidget(this);
    QVBoxLayout *vlayout = new QVBoxLayout(centralWidget);
    vlayout->setContentsMargins(20, 20, 20, 20);
    vlayout->setSpacing(15);

    QFormLayout *mainLayout = new QFormLayout(centralWidget);

    employeeIDLabel = new QLabel("工号:", centralWidget);
    employeeIDLabel->setStyleSheet("font: 14px 'Arial'; color: #333;");
    employeeIDEdit = new QLineEdit(centralWidget);
    employeeIDEdit->setPlaceholderText("请输入新工号");
    employeeIDEdit->setStyleSheet("QLineEdit { border: 1px solid #ccc; border-radius: 5px; padding: 5px; }");
    mainLayout->addRow(employeeIDLabel, employeeIDEdit);

    departmentLabel = new QLabel("科室:", centralWidget);
    departmentLabel->setStyleSheet("font: 14px 'Arial'; color: #333;");
    departmentEdit = new QLineEdit(centralWidget);
    departmentEdit->setPlaceholderText("请输入新科室");
    departmentEdit->setStyleSheet("QLineEdit { border: 1px solid #ccc; border-radius: 5px; padding: 5px; }");
    mainLayout->addRow(departmentLabel, departmentEdit);


    workTimeLabel = new QLabel("上班时间:", centralWidget);
    workTimeLabel->setStyleSheet("font: 14px 'Arial'; color: #333;");
    workTimeEdit = new QLineEdit(centralWidget);
    workTimeEdit->setPlaceholderText("请输入上班时间");
    workTimeEdit->setStyleSheet("QLineEdit { border: 1px solid #ccc; border-radius: 5px; padding: 5px; }");
    mainLayout->addRow(workTimeLabel, workTimeEdit);

    registeredFeeLabel = new QLabel("挂号费用:", centralWidget);
    registeredFeeLabel->setStyleSheet("font: 14px 'Arial'; color: #333;");
    registeredFeeEdit = new QLineEdit(centralWidget);
    registeredFeeEdit->setPlaceholderText("挂号费用");
    registeredFeeEdit->setStyleSheet("QLineEdit { border: 1px solid #ccc; border-radius: 5px; padding: 5px; }");
    mainLayout->addRow(registeredFeeLabel, registeredFeeEdit);

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
    mainLayout->addRow(doctorPhotoLabel, photoLayout);

    submitButton = new QPushButton("选择", centralWidget);
    submitButton->setStyleSheet(
        "QPushButton { background-color: #6c757d; color: white; border-radius: 5px; padding: 8px; font: 14px 'Arial'; }"
        "QPushButton:hover { background-color: #5a6268; }"
        "QPushButton:pressed { background-color: #4b545c; }");
    mainLayout->addRow(submitButton);

    returnButton = new QPushButton("返回", centralWidget);
    mainLayout->addRow(returnButton);

    vlayout->addStretch();
    vlayout->addLayout(mainLayout);
    vlayout->addStretch();

    setCentralWidget(centralWidget);

    connect(returnButton,&QPushButton::clicked,this,&DoctorInfoWindow::returnMainWindow);

}

void DoctorInfoWindow::returnMainWindow()
{
    parentWidget()->show();
    this->hide();
};
