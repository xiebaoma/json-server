#ifndef CHATSYSTEMINIT_H
#define CHATSYSTEMINIT_H
#include "chatinitwindow.h"
#include <QApplication>
#include <QMessageBox>

class ChatSystemInit : public QObject
{
public:
    ChatSystemInit(QString loginID, QString loginRole, QObject *parent = nullptr);

private:
    ChatInitWindow *chatinit;
};

#endif // CHATSYSTEMINIT_H
