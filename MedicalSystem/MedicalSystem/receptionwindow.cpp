#include "doctormainwindow.h"

ReceptionWindow::ReceptionWindow(QWidget *parent) : QMainWindow(parent)
{
    setWindowTitle("接诊");
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
    QVBoxLayout *layout = new QVBoxLayout(centralWidget);
    layout->setContentsMargins(20, 20, 20, 20);
    layout->setSpacing(15);

    patientInfoLabel = new QLabel("患者信息");
    patientInfoLabel->setStyleSheet("font-size: 16px; font-weight: bold;");
    medicalRecordEdit = new QTextEdit();
    medicalRecordEdit->setMinimumHeight(100);
    prescriptionEdit = new QTextEdit();
    prescriptionEdit->setMinimumHeight(100);
    adviceEdit = new QTextEdit();
    adviceEdit->setMinimumHeight(100);

    QHBoxLayout *searchLayout = new QHBoxLayout();
    searchPatientEdit = new QLineEdit();
    searchPatientEdit->setPlaceholderText("输入患者信息");
    searchPatientButton = new QPushButton("查询患者");
    searchLayout->addWidget(searchPatientEdit);
    searchLayout->addWidget(searchPatientButton);

    nextPatientButton = new QPushButton("下一个患者");
    returnButton = new QPushButton("返回");
    returnButton->setObjectName("returnButton");

    layout->addWidget(patientInfoLabel);
    layout->addWidget(new QLabel("病例:"));
    layout->addWidget(medicalRecordEdit);
    layout->addWidget(new QLabel("医嘱:"));
    layout->addWidget(adviceEdit);
    layout->addWidget(new QLabel("处方:"));
    layout->addWidget(prescriptionEdit);
    layout->addLayout(searchLayout);
    layout->addWidget(nextPatientButton);
    layout->addWidget(returnButton);
    layout->addStretch();

    QGraphicsDropShadowEffect *shadowEffect = new QGraphicsDropShadowEffect();
    shadowEffect->setBlurRadius(10);
    shadowEffect->setOffset(0, 2);
    shadowEffect->setColor(QColor(0, 0, 0, 50));
    centralWidget->setGraphicsEffect(shadowEffect);

    setCentralWidget(centralWidget);

    connect(nextPatientButton, &QPushButton::clicked, this, &ReceptionWindow::onNextPatientClicked);
    connect(searchPatientButton, &QPushButton::clicked, this, &ReceptionWindow::onSearchPatientClicked);
    connect(returnButton, &QPushButton::clicked, this, &ReceptionWindow::returnMainWindow);
}

void ReceptionWindow::onNextPatientClicked()
{

}

void ReceptionWindow::onSearchPatientClicked()
{

}

void ReceptionWindow::returnMainWindow()
{
    parentWidget()->show();
    this->hide();
}
