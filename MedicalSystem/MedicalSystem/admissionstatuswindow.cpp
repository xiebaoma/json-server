#include "doctormainwindow.h"

AdmissionStatusWindow::AdmissionStatusWindow(QWidget *parent) : QMainWindow(parent)
{
    //五个子页面的设置大同小异，所以仅在此处注释

    setWindowTitle("接诊状态设置");
    resize(450, 500);

    //对各个部件进行一个通用设置
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
        "QSpinBox {"
        "    padding: 8px;"
        "    font-size: 14px;"
        "    border: 1px solid #bdc3c7;"
        "    border-radius: 6px;"
        "    background-color: #ffffff;"
        "    min-width: 100px;"
        "}"
        "QSpinBox:focus {"
        "    border: 1px solid #3498db;"
        "    background-color: #f8fcff;"
        "}"
        "QCheckBox {"
        "    font-size: 14px;"
        "    color: #2c3e50;"
        "    padding: 8px;"
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

    //中心部件和总体垂直布局
    QWidget *centralWidget = new QWidget(this);
    QVBoxLayout *vLayout = new QVBoxLayout(centralWidget);
    vLayout->setContentsMargins(20, 20, 20, 20);
    vLayout->setSpacing(15);

    //三个小部件采用表单布局
    QFormLayout *formLayout = new QFormLayout();
    formLayout->setLabelAlignment(Qt::AlignRight | Qt::AlignVCenter);
    formLayout->setSpacing(12);


    //最大预约人数
    maxAppointmentsSpinBox = new QSpinBox();
    maxAppointmentsSpinBox->setRange(0, 100);
    maxAppointmentsSpinBox->setStyleSheet(
        "QSpinBox::up-button, QSpinBox::down-button {"
        "    width: 20px;"
        "    background-color: #ecf0f1;"
        "}"
        "QSpinBox::up-button:hover, QSpinBox::down-button:hover {"
        "    background-color: #dfe6e9;"
        "}"
        );
    formLayout->addRow("每日最大预约人数:", maxAppointmentsSpinBox);

    //接诊状态
    receptionStatusCheckBox = new QCheckBox("接诊状态 (开启/关闭)");
    receptionStatusCheckBox->setStyleSheet(
        "QCheckBox::indicator {"
        "    width: 20px;"
        "    height: 20px;"
        "}"
        "QCheckBox::indicator:checked {"
        "    background-color: #3498db;"
        "    border: 1px solid #2980b9;"
        "}"
        );
    formLayout->addRow(receptionStatusCheckBox);

    //两按钮
    saveButton = new QPushButton("保存");
    formLayout->addRow(saveButton);
    returnButton = new QPushButton("返回");
    returnButton->setObjectName("returnButton");
    formLayout->addRow(returnButton);

    vLayout->addLayout(formLayout);
    vLayout->addStretch();

    //阴影效果
    QGraphicsDropShadowEffect *shadowEffect = new QGraphicsDropShadowEffect();
    shadowEffect->setBlurRadius(10);
    shadowEffect->setOffset(0, 2);
    shadowEffect->setColor(QColor(0, 0, 0, 50));
    centralWidget->setGraphicsEffect(shadowEffect);

    setCentralWidget(centralWidget);

    connect(returnButton, &QPushButton::clicked, this, &AdmissionStatusWindow::returnMainWindow);
}

void AdmissionStatusWindow::returnMainWindow()
{
    parentWidget()->show();
    this->hide();
}
