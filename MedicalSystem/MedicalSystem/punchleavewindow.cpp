#include "doctormainwindow.h"

PunchLeaveWindow::PunchLeaveWindow(QWidget *parent) : QMainWindow(parent)
{
    setWindowTitle("打卡与请假");
    resize(450, 500);
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
        "QCheckBox {"
        "    font-size: 14px;"
        "    color: #2c3e50;"
        "    padding: 8px;"
        "}"
        "QCheckBox::indicator {"
        "    width: 20px;"
        "    height: 20px;"
        "}"
        "QCheckBox::indicator:checked {"
        "    background-color: #3498db;"
        "    border: 1px solid #2980b9;"
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

    punchCheckBox = new QCheckBox("今日打卡");
    punchHistoryTable = new QTableWidget();
    punchHistoryTable->setStyleSheet(
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
    refreshHistoryButton = new QPushButton("刷新记录");
    returnButton = new QPushButton("返回");
    returnButton->setObjectName("returnButton");
    layout->addWidget(punchCheckBox);
    layout->addWidget(punchHistoryTable);
    layout->addWidget(refreshHistoryButton);
    layout->addWidget(returnButton);
    layout->addStretch();

    QGraphicsDropShadowEffect *shadowEffect = new QGraphicsDropShadowEffect();
    shadowEffect->setBlurRadius(10);
    shadowEffect->setOffset(0, 2);
    shadowEffect->setColor(QColor(0, 0, 0, 50));
    centralWidget->setGraphicsEffect(shadowEffect);

    setCentralWidget(centralWidget);

    connect(punchCheckBox, &QCheckBox::toggled, this, &PunchLeaveWindow::onPunchCheckBoxToggled);
    connect(returnButton, &QPushButton::clicked, this, &PunchLeaveWindow::returnMainWindow);
}

void PunchLeaveWindow::onPunchCheckBoxToggled(bool checked)
{

}

void PunchLeaveWindow::returnMainWindow()
{
    parentWidget()->show();
    this->hide();
}
