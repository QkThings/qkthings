#ifndef QKUTILS_H
#define QKUTILS_H

#include <QString>
#include <QList>
#include <QJsonDocument>
#include <QMap>
#include <stdint.h>

#define MASK(bit, shift) (((1<<bit)-1) << shift)
#define FLAG_SET(val, mask) (val |= mask)
#define FLAG_CLR(val, mask) (val &= ~mask)
#define FLAG(val, mask)     ((val & mask) ? true : false)

namespace QkUtils
{
class Version
{
public:
    enum StringFormat
    {
        sfDec,
        sfHex
    };
    Version(int major = 0, int minor = 0, int patch = 0)
    {
        m_major = major;
        m_minor = minor;
        m_patch = patch;
    }
    QString toString(StringFormat sf)
    {
        switch(sf)
        {
        case sfDec: return QString().sprintf("%d.%d.%02d", m_major, m_minor, m_patch);
        case sfHex: return QString().sprintf("%1X%1X%02X", m_major, m_minor, m_patch);
        }
    }
private:
    int m_major, m_minor, m_patch;
};

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

QMap<QString, Target> supportedTargets(const QString &embPath);

extern QString _infoPath;
QJsonDocument jsonFromFile(const QString &filePath);
bool validateJson(const QJsonDocument &doc);

union IntFloatConverter {
    float f_value;
    int i_value;
    uint8_t bytes[4];
};
void fillValue(int value, int count, int *idx, QByteArray &data);
void fillString(const QString &str, int count, int *idx, QByteArray &data);
void fillString(const QString &str, int *idx, QByteArray &data);
int getValue(int count, int *idx, const QByteArray &data, bool sigExt = false);
QString getString(int *idx, const QByteArray &data);
QString getString(int count, int *idx, const QByteArray &data);
float floatFromBytes(int value);
int bytesFromFloat(float value);
}

#endif // QKUTILS_H
