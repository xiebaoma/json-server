#include "doctormainwindow.h"

RegistrationInfoWindow::RegistrationInfoWindow(QWidget *parent) : QMainWindow(parent)
{
    setWindowTitle("挂号信息");
    resize(450, 500); // Slightly larger for better spacing
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

    registrationTable = new QTableWidget();
    registrationTable->setStyleSheet(
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
    layout->addWidget(registrationTable);

    refreshButton = new QPushButton("刷新");
    returnButton = new QPushButton("返回");
    returnButton->setObjectName("returnButton"); // For distinct styling
    layout->addWidget(refreshButton);
    layout->addWidget(returnButton);
    layout->addStretch();

    // Add a subtle shadow effect to central widget
    QGraphicsDropShadowEffect *shadowEffect = new QGraphicsDropShadowEffect();
    shadowEffect->setBlurRadius(10);
    shadowEffect->setOffset(0, 2);
    shadowEffect->setColor(QColor(0, 0, 0, 50));
    centralWidget->setGraphicsEffect(shadowEffect);

    setCentralWidget(centralWidget);

    connect(registrationTable, &QTableWidget::cellDoubleClicked, this, &RegistrationInfoWindow::onViewDetailsClicked);
    connect(returnButton, &QPushButton::clicked, this, &RegistrationInfoWindow::returnMainWindow);
}

void RegistrationInfoWindow::onViewDetailsClicked(int row)
{
    // Placeholder: Handle viewing patient details
}

void RegistrationInfoWindow::returnMainWindow()
{
    parentWidget()->show();
    this->hide();
}
