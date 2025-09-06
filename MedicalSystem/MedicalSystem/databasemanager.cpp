#include"databasemanager.h"
#include<qvariant.h>
bool databaseManager::openDatabase(const QString dbname){
    m_database = QSqlDatabase::addDatabase("QSQLITE");
    m_database.setDatabaseName(dbname);
    if(!m_database.open()){
        qDebug()<<"open failure";
        return false;
    }
    qDebug()<<"open success, ready to execute sql query";
    return true;
}
bool databaseManager::insertData(const QString tableName, const QMap<QString, QVariant> &data)
{
    // 检查数据是否为空
    if (data.isEmpty()) {
        qWarning() << "插入数据为空!";
        return false;
    }

    // 准备SQL语句
    QString fields;
    QString placeholders;

    for (auto it = data.constBegin(); it != data.constEnd(); ++it) {
        if (!fields.isEmpty()) {
            fields += ", ";
            placeholders += ", ";
        }
        fields += it.key();
        placeholders += ":" + it.key();
    }

    QString queryStr = QString("INSERT INTO %1 (%2) VALUES (%3)")
                           .arg(tableName, fields, placeholders);

    // 执行插入操作
    QSqlQuery query;
    query.prepare(queryStr);

    // 绑定值
    for (auto it = data.constBegin(); it != data.constEnd(); ++it) {
        query.bindValue(":" + it.key(), it.value());
    }

    if (!query.exec()) {
        qCritical() << "插入数据失败:" << query.lastError().text();
        qCritical() << "SQL语句:" << queryStr;
        return false;
    }

    qDebug() << "数据插入成功,影响行数:" << query.numRowsAffected();
    return true;
}
QString databaseManager::QueryFromtable(QString tabelname,QString id,QString key){
    QSqlQuery query;
    QString sql = QString("select * from %1 where %2 = %3").arg(tabelname).arg(key).arg(id);
    qDebug()<<"test";
    //qDebug()<<query.exec("INSERT INTO student(id,age) VALUES(2,357);");
    qDebug()<<query.exec(sql);
    qDebug()<<query.lastError().text();
    /*while(query.next()){
        int id= query.value(0).toInt();
        int age = query.value(1).toInt();
        qDebug()<<id<<"id"<<age<<"age";
    }*/
    QStringList allRows;
    while (query.next()) {
        // 获取一条记录的所有字段
        QSqlRecord record = query.record();
        QStringList fieldValues;
        for (int i = 0; i < record.count(); ++i) {
            fieldValues.append(record.value(i).toString());
        }
        // 将当前行的字段用"|"连接
        allRows.append(fieldValues.join("|"));
    }

    if (allRows.isEmpty()) {
        qWarning() << "No records found for" << key << "=" << id;
        return QString();
    }

    // 将所有行用":"连接
    return allRows.join(":");

}
QMap<QString,QVariant> databaseManager::makeQmap(const QString &filepath){
    QMap<QString,QVariant> resultmap;
    QFile file(filepath);
    //打开文件，无法打开就报错
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        qWarning() << "无法打开文件:" << filepath;
        return resultmap;
    }
    QTextStream in(&file);
    QString line;

    // 逐行读取文件
    while (!in.atEnd()) {
        line = in.readLine().trimmed();

        // 跳过空行和注释行
        if (line.isEmpty() || line.startsWith("----")) {
            continue;
        }

        // 查找分隔符":"
        int separatorIndex = line.indexOf(":");
        if (separatorIndex == -1) {
            qWarning() << "行格式错误，缺少分隔符':':" << line;
            continue;
        }

        // 提取键和值
        QString key = line.left(separatorIndex).trimmed();
        QString value = line.mid(separatorIndex + 1).trimmed();

        // 将值存储到Map中
        resultmap[key] = QVariant(value);
    }


    file.close();
    return resultmap;
}

QMap<QString,QVariant> databaseManager::makeQmapbyJson(const QString &filename){
    QMap<QString, QVariant> resultMap;

    // 打开文件
    QFile file(filename);
    if (!file.open(QIODevice::ReadOnly)) {
        qWarning() << "无法打开文件:" << filename;
        return resultMap;
    }

    // 读取文件内容
    QByteArray jsonData = file.readAll();
    file.close();

    // 解析JSON
    QJsonParseError parseError;
    QJsonDocument jsonDoc = QJsonDocument::fromJson(jsonData, &parseError);

    if (parseError.error != QJsonParseError::NoError) {
        qWarning() << "JSON解析错误:" << parseError.errorString();
        return resultMap;
    }

    // 检查JSON是否为对象
    if (!jsonDoc.isObject()) {
        qWarning() << "JSON文件不包含对象";
        return resultMap;
    }

    // 获取JSON对象
    QJsonObject jsonObject = jsonDoc.object();

    // 遍历JSON对象的所有键
    QStringList keys = jsonObject.keys();
    for (const QString &key : keys) {
        QJsonValue value = jsonObject.value(key);

        // 只处理简单值类型
        if (value.isString()) {
            resultMap[key] = value.toString();
        } else if (value.isDouble()) {
            // 检查是否为整数
            double dValue = value.toDouble();
            if (dValue == static_cast<int>(dValue)) {
                resultMap[key] = static_cast<int>(dValue);
            } else {
                resultMap[key] = dValue;
            }
        } else if (value.isBool()) {
            resultMap[key] = value.toBool();
        } else if (value.isNull()) {
            resultMap[key] = NULL; // 空值
        } else {
            qWarning() << "跳过复杂类型键:" << key;
        }
    }

    return resultMap;
}

