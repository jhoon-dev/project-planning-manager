#pragma once
#include <QSettings>
#include <QString>
#include <QStringList>

namespace ppm {
struct ApplicationStorage {
    QString packageFamilyName;
    QString stateDirectory;
    QString recoveryDirectory;
    QString settingsFile;
    QString legacyStateDirectory;
    bool packaged() const {
        return !packageFamilyName.isEmpty();
    }
};
// No directory creation, settings migration or fallback to another package's state.
ApplicationStorage applicationStorage();
QSettings applicationSettings();
// Copies missing settings and recovery generations once. Returns recovery warnings for startup.
QStringList migrateApplicationStorage();
void migrateApplicationSettings(QSettings &legacy, QSettings &current);
} // namespace ppm
