#ifndef CHATINITWINDOW_H
#define CHATINITWINDOW_H

#include <QWidget>
#include <QLineEdit>
#include <QPushButton>
#include <QLabel>
#include <QVBoxLayout>
#include <QMessageBox>
#include "MessageClient.h"

namespace Ui {
class ChatInitWindow;
}

class ChatInitWindow : public QWidget
{
    Q_OBJECT

public:
    explicit ChatInitWindow(QWidget *parent = nullptr,
                            QString loginID = "",
                            QString loginRole = "");
    ~ChatInitWindow();

    MessageClient* getClient() const { return client; }

signals:
    void loginSuccess(const QString &userId);

private slots:
    void onLoginClicked();
    void onLoginResult(bool success, const QString &message);
    void onConnected();
    void onErrorOccurred(const QString &error);

private:
    MessageClient *client;
    Ui::ChatInitWindow *ui;
    QString loginID;
    QString loginRole;
    void inputInfo();
};

#endif // CHATINITWINDOW_H
