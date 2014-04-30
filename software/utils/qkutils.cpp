#include "qkutils.h"

#include <QDebug>
#include <QFile>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>


namespace QkUtils
{
QString _embeddedPath = QString("embeddedPath");
}

using namespace QkUtils;

void QkUtils::setEmbeddedPath(const QString &path)
{
    _embeddedPath = path;
}

QMap<QString, Target> QkUtils::supportedTargets()
{
    QMap<QString, Target>  targets;

    QString filePath = _embeddedPath + "/target/targets.json";
    QJsonDocument doc = jsonFromFile(filePath);


    QVariantMap jsonTargets = doc.object().toVariantMap();

    foreach(QString targetName, jsonTargets.keys())
    {
        Target target;

        target.name = targetName;
        QVariantMap jsonTargetInfo = jsonTargets[targetName].toMap();

        target.toolchainUrl = jsonTargetInfo["toolchainUrl"].toString();

        QVariantList jsonTargetVariants = jsonTargetInfo["variants"].toList();
        TargetVariantList targetVariants;

        qDebug() << jsonTargetInfo;

        foreach(QVariant jsonVariant, jsonTargetVariants)
        {
            QMap<QString, QVariant> variant = jsonVariant.toMap();
            Target::Board targetVariant;

            targetVariant.name = variant["name"].toString();

            targetVariants.append(targetVariant);
        }
        target.boards.append(targetVariants);
        targets.insert(targetName, target);
    }

    return targets;
}

QJsonDocument QkUtils::jsonFromFile(const QString &filePath)
{
    QString jsonFilePath = filePath;
    QJsonDocument doc;

    QFile file(jsonFilePath);
    if(!file.open(QFile::ReadOnly | QFile::Text))
    {
        qDebug() << "failed to open file" << jsonFilePath;
    }
    else
    {
        QString jsonStr = QString(file.readAll());
        jsonStr.remove('\t');
        jsonStr.remove(' ');

        QJsonParseError parseError;
        doc = QJsonDocument::fromJson(jsonStr.toUtf8(), &parseError);

        if(parseError.error != QJsonParseError::NoError)
            qDebug() << "json parse error:" << parseError.errorString();
    }

    return doc;
}


