#ifndef DATABASEMANAGER_H
#define DATABASEMANAGER_H
#include<QSqlDatabase>
#include<QDebug>
#include<QVariant>
#include<QVariantMap>
#include<QSqlQuery>
#include<QSqlError>
#include<QString>
#include<string>
#include<QSqlRecord>
#include<QMap>
#include<QFile>
#include<QJsonObject>
#include<QJsonDocument>
class databaseManager{
    QSqlDatabase m_database;
public:
    bool openDatabase(const QString dbname);
    bool insertData(const QString tableName, const QMap<QString, QVariant> &data);
    QString QueryFromtable(QString tablename,QString id,QString key);
    QMap<QString,QVariant> makeQmapbytxt (const QString &filename);
    QMap<QString,QVariant>makeQmapbyJson(const QString &filename);
    QMap<QString,QVariant> makeQmap(const QString &filepath);
#endif // DATABASEMANAGER_H
};
