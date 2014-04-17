#ifndef QKUTILS_H
#define QKUTILS_H

#include <QString>
#include <QList>
#include <QJsonDocument>
#include <QMap>

namespace QkUtils
{

class Target
{
public:
    class Variant
    {
    public:
        QString name;
    };

    QString name;
    QString toolchainUrl;
    QList<Variant> variants;
};

typedef QList<QkUtils::Target> TargetList;
typedef QList<QkUtils::Target::Variant> TargetVariantList;

void setInfoPath(const QString &path);
QMap<QString, Target> supportedTargets();

extern QString _infoPath;
QJsonDocument jsonFromFile(const QString &filePath);
bool validateJson(const QJsonDocument &doc);

}

#endif // QKUTILS_H
