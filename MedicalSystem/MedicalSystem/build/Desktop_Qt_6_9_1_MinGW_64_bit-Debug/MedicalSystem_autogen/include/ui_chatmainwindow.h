/********************************************************************************
** Form generated from reading UI file 'chatmainwindow.ui'
**
** Created by: Qt User Interface Compiler version 6.9.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_CHATMAINWINDOW_H
#define UI_CHATMAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QFrame>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QListWidget>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSplitter>
#include <QtWidgets/QTextEdit>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_ChatMainWindow
{
public:
    QSplitter *splitter;
    QWidget *leftWidget;
    QVBoxLayout *verticalLayout_2;
    QLabel *label;
    QListWidget *sendersList;
    QPushButton *refreshButton;
    QVBoxLayout *verticalLayout;
    QFrame *line;
    QHBoxLayout *horizontalLayout;
    QLabel *label_4;
    QLineEdit *toUserEdit;
    QLabel *label_5;
    QTextEdit *messageEdit;
    QPushButton *sendButton;
    QLabel *statusLabel;
    QWidget *rightWidget;
    QVBoxLayout *verticalLayout_3;
    QLabel *label_2;
    QTextEdit *messagesText;
    QLabel *label_3;
    QTextEdit *replyEdit;
    QPushButton *replyButton;

    void setupUi(QWidget *ChatMainWindow)
    {
        if (ChatMainWindow->objectName().isEmpty())
            ChatMainWindow->setObjectName("ChatMainWindow");
        ChatMainWindow->resize(716, 415);
        splitter = new QSplitter(ChatMainWindow);
        splitter->setObjectName("splitter");
        splitter->setGeometry(QRect(20, 20, 671, 371));
        splitter->setOrientation(Qt::Orientation::Horizontal);
        leftWidget = new QWidget(splitter);
        leftWidget->setObjectName("leftWidget");
        verticalLayout_2 = new QVBoxLayout(leftWidget);
        verticalLayout_2->setObjectName("verticalLayout_2");
        verticalLayout_2->setContentsMargins(0, 0, 0, 0);
        label = new QLabel(leftWidget);
        label->setObjectName("label");

        verticalLayout_2->addWidget(label);

        sendersList = new QListWidget(leftWidget);
        sendersList->setObjectName("sendersList");

        verticalLayout_2->addWidget(sendersList);

        refreshButton = new QPushButton(leftWidget);
        refreshButton->setObjectName("refreshButton");

        verticalLayout_2->addWidget(refreshButton);

        verticalLayout = new QVBoxLayout();
        verticalLayout->setObjectName("verticalLayout");
        line = new QFrame(leftWidget);
        line->setObjectName("line");
        line->setFrameShape(QFrame::Shape::HLine);
        line->setFrameShadow(QFrame::Shadow::Sunken);

        verticalLayout->addWidget(line);

        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setObjectName("horizontalLayout");
        label_4 = new QLabel(leftWidget);
        label_4->setObjectName("label_4");

        horizontalLayout->addWidget(label_4);

        toUserEdit = new QLineEdit(leftWidget);
        toUserEdit->setObjectName("toUserEdit");

        horizontalLayout->addWidget(toUserEdit);


        verticalLayout->addLayout(horizontalLayout);

        label_5 = new QLabel(leftWidget);
        label_5->setObjectName("label_5");

        verticalLayout->addWidget(label_5);

        messageEdit = new QTextEdit(leftWidget);
        messageEdit->setObjectName("messageEdit");

        verticalLayout->addWidget(messageEdit);

        sendButton = new QPushButton(leftWidget);
        sendButton->setObjectName("sendButton");

        verticalLayout->addWidget(sendButton);

        statusLabel = new QLabel(leftWidget);
        statusLabel->setObjectName("statusLabel");

        verticalLayout->addWidget(statusLabel);


        verticalLayout_2->addLayout(verticalLayout);

        splitter->addWidget(leftWidget);
        rightWidget = new QWidget(splitter);
        rightWidget->setObjectName("rightWidget");
        verticalLayout_3 = new QVBoxLayout(rightWidget);
        verticalLayout_3->setObjectName("verticalLayout_3");
        verticalLayout_3->setContentsMargins(0, 0, 0, 0);
        label_2 = new QLabel(rightWidget);
        label_2->setObjectName("label_2");

        verticalLayout_3->addWidget(label_2);

        messagesText = new QTextEdit(rightWidget);
        messagesText->setObjectName("messagesText");

        verticalLayout_3->addWidget(messagesText);

        label_3 = new QLabel(rightWidget);
        label_3->setObjectName("label_3");

        verticalLayout_3->addWidget(label_3);

        replyEdit = new QTextEdit(rightWidget);
        replyEdit->setObjectName("replyEdit");
        replyEdit->setEnabled(true);

        verticalLayout_3->addWidget(replyEdit);

        replyButton = new QPushButton(rightWidget);
        replyButton->setObjectName("replyButton");

        verticalLayout_3->addWidget(replyButton);

        splitter->addWidget(rightWidget);

        retranslateUi(ChatMainWindow);

        QMetaObject::connectSlotsByName(ChatMainWindow);
    } // setupUi

    void retranslateUi(QWidget *ChatMainWindow)
    {
        ChatMainWindow->setWindowTitle(QCoreApplication::translate("ChatMainWindow", "\346\266\210\346\201\257\347\263\273\347\273\237", nullptr));
        label->setText(QCoreApplication::translate("ChatMainWindow", "\347\273\231\346\210\221\345\217\221\350\277\207\346\266\210\346\201\257\347\232\204\347\224\250\346\210\267:", nullptr));
        refreshButton->setText(QCoreApplication::translate("ChatMainWindow", "\345\210\267\346\226\260\345\210\227\350\241\250", nullptr));
        label_4->setText(QCoreApplication::translate("ChatMainWindow", "\345\217\221\351\200\201\347\273\231:", nullptr));
        toUserEdit->setPlaceholderText(QCoreApplication::translate("ChatMainWindow", "\350\276\223\345\205\245\347\224\250\346\210\267ID", nullptr));
        label_5->setText(QCoreApplication::translate("ChatMainWindow", "\346\266\210\346\201\257\345\206\205\345\256\271:", nullptr));
        sendButton->setText(QCoreApplication::translate("ChatMainWindow", "\345\217\221\351\200\201\346\266\210\346\201\257", nullptr));
        statusLabel->setText(QCoreApplication::translate("ChatMainWindow", "\345\260\261\347\273\252", nullptr));
        label_2->setText(QCoreApplication::translate("ChatMainWindow", "\346\266\210\346\201\257\345\206\205\345\256\271:", nullptr));
        label_3->setText(QCoreApplication::translate("ChatMainWindow", "\345\233\236\345\244\215:", nullptr));
        replyButton->setText(QCoreApplication::translate("ChatMainWindow", "\345\217\221\351\200\201\345\233\236\345\244\215", nullptr));
    } // retranslateUi

};

namespace Ui {
    class ChatMainWindow: public Ui_ChatMainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_CHATMAINWINDOW_H
