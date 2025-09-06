/********************************************************************************
** Form generated from reading UI file 'chatinitwindow.ui'
**
** Created by: Qt User Interface Compiler version 6.9.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_CHATINITWINDOW_H
#define UI_CHATINITWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_ChatInitWindow
{
public:
    QVBoxLayout *verticalLayout;
    QLabel *titleLabel;
    QLabel *userIdLabel;
    QLineEdit *userIdEdit;
    QPushButton *loginButton;
    QLabel *statusLabel;

    void setupUi(QWidget *ChatInitWindow)
    {
        if (ChatInitWindow->objectName().isEmpty())
            ChatInitWindow->setObjectName("ChatInitWindow");
        ChatInitWindow->resize(300, 200);
        verticalLayout = new QVBoxLayout(ChatInitWindow);
        verticalLayout->setObjectName("verticalLayout");
        titleLabel = new QLabel(ChatInitWindow);
        titleLabel->setObjectName("titleLabel");
        titleLabel->setAlignment(Qt::AlignCenter);
        QFont font;
        font.setPointSize(16);
        font.setBold(true);
        titleLabel->setFont(font);

        verticalLayout->addWidget(titleLabel);

        userIdLabel = new QLabel(ChatInitWindow);
        userIdLabel->setObjectName("userIdLabel");

        verticalLayout->addWidget(userIdLabel);

        userIdEdit = new QLineEdit(ChatInitWindow);
        userIdEdit->setObjectName("userIdEdit");

        verticalLayout->addWidget(userIdEdit);

        loginButton = new QPushButton(ChatInitWindow);
        loginButton->setObjectName("loginButton");

        verticalLayout->addWidget(loginButton);

        statusLabel = new QLabel(ChatInitWindow);
        statusLabel->setObjectName("statusLabel");
        statusLabel->setAlignment(Qt::AlignCenter);

        verticalLayout->addWidget(statusLabel);


        retranslateUi(ChatInitWindow);

        QMetaObject::connectSlotsByName(ChatInitWindow);
    } // setupUi

    void retranslateUi(QWidget *ChatInitWindow)
    {
        ChatInitWindow->setWindowTitle(QCoreApplication::translate("ChatInitWindow", "\346\266\210\346\201\257\347\263\273\347\273\237 - \347\231\273\345\275\225", nullptr));
        titleLabel->setText(QCoreApplication::translate("ChatInitWindow", "\346\266\210\346\201\257\347\263\273\347\273\237", nullptr));
        userIdLabel->setText(QCoreApplication::translate("ChatInitWindow", "\347\224\250\346\210\267ID:", nullptr));
        userIdEdit->setPlaceholderText(QCoreApplication::translate("ChatInitWindow", "\350\257\267\350\276\223\345\205\245\346\202\250\347\232\204\347\224\250\346\210\267ID", nullptr));
        loginButton->setText(QCoreApplication::translate("ChatInitWindow", "\347\231\273\345\275\225", nullptr));
        statusLabel->setText(QCoreApplication::translate("ChatInitWindow", "\345\207\206\345\244\207\345\260\261\347\273\252", nullptr));
    } // retranslateUi

};

namespace Ui {
    class ChatInitWindow: public Ui_ChatInitWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_CHATINITWINDOW_H
