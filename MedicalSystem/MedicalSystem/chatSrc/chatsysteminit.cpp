#include "chatsysteminit.h"
#include "chatinitwindow.h"
#include "chatmainwindow.h"
#include <QApplication>
#include <QMessageBox>
#include <QDebug>
#include <QObject>
//聊天界面初始化类
ChatSystemInit::ChatSystemInit(QString loginID, QString loginRole, QObject *parent)
    : QObject(parent)
{
    chatinit = new ChatInitWindow(nullptr, loginID, loginRole);
    chatinit->show();

    QObject::connect(chatinit, &ChatInitWindow::loginSuccess, [=](const QString &userId) {
        qDebug() << "Login success, user ID:" << userId;
        ChatMainWindow *mainWindow = new ChatMainWindow(userId, chatinit->getClient());
        mainWindow->show();
        chatinit->hide();

        QObject::connect(mainWindow, &ChatMainWindow::destroyed, [=]() {
            chatinit->show();
            mainWindow->deleteLater();
        });
    });

    // 确保 ChatSystemInit 对象不被立即销毁
    this->setParent(parent);
}
