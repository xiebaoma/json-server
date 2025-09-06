#include "doctormainwindow.h"

PatientInfoWindow::PatientInfoWindow(QWidget *parent) : QMainWindow(parent)
{
    setWindowTitle("患者信息");
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
    QVBoxLayout *layout = new QVBoxLayout(centralWidget);
    layout->setContentsMargins(20, 20, 20, 20); // Increased margins for better padding
    layout->setSpacing(15); // Increased spacing for clarity

    QHBoxLayout *searchLayout = new QHBoxLayout();
    searchEdit = new QLineEdit();
    searchEdit->setPlaceholderText("输入患者信息");
    searchButton = new QPushButton("搜索");
    searchLayout->addWidget(searchEdit);
    searchLayout->addWidget(searchButton);

    patientTable = new QTableWidget();
    patientTable->setStyleSheet(
        "QTableWidget {"
        "    gridline-color: #ecf0f1;"
        "}"
        "QHeaderView::section {"
        "    background-color: #3498db;"
        "    color: white;"
        "    padding: 6px;"
        "    border: none;"
        "    font-weight: bold;"
        "}"
        );

    medicalRecordEdit = new QTextEdit();
    medicalRecordEdit->setMinimumHeight(100);
    prescriptionEdit = new QTextEdit();
    prescriptionEdit->setMinimumHeight(100);
    endVisitButton = new QPushButton("结束就诊");
    endVisitButton->setObjectName("returnButton");

    layout->addLayout(searchLayout);
    layout->addWidget(patientTable);
    layout->addWidget(new QLabel("病例记录:"));
    layout->addWidget(medicalRecordEdit);
    layout->addWidget(new QLabel("医嘱:"));
    layout->addWidget(prescriptionEdit);
    layout->addWidget(endVisitButton);
    layout->addStretch();


    QGraphicsDropShadowEffect *shadowEffect = new QGraphicsDropShadowEffect();
    shadowEffect->setBlurRadius(10);
    shadowEffect->setOffset(0, 2);
    shadowEffect->setColor(QColor(0, 0, 0, 50));
    centralWidget->setGraphicsEffect(shadowEffect);

    setCentralWidget(centralWidget);

    connect(searchButton, &QPushButton::clicked, this, &PatientInfoWindow::onSearchClicked);
    connect(endVisitButton, &QPushButton::clicked, this, &PatientInfoWindow::onEndVisitClicked);
}

void PatientInfoWindow::onSearchClicked()
{

}

void PatientInfoWindow::onEndVisitClicked()
{
    parentWidget()->show();
    this->hide();
}
