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
    class Board
    {
    public:
        QString name;
    };

    QString name;
    QString toolchainUrl;
    QList<Board> boards;
};

typedef QList<QkUtils::Target> TargetList;
typedef QList<QkUtils::Target::Board> TargetVariantList;

void setEmbeddedPath(const QString &path);
QMap<QString, Target> supportedTargets();

extern QString _infoPath;
QJsonDocument jsonFromFile(const QString &filePath);
bool validateJson(const QJsonDocument &doc);

}

#endif // QKUTILS_H
