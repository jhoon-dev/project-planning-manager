#include "persistence/ApplicationStorage.h"
#include "domain/Diagnostics.h"
#include "formatting/QtDiagnosticText.h"
#include "application/ProductIdentity.h"
#include "persistence/JsonRecoveryStore.h"
#include <QCoreApplication>
#include <QFileInfo>
#include <QDir>
#include <QStandardPaths>
#ifdef Q_OS_WIN
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include <appmodel.h>
#include <shlobj.h>
#include <vector>
#endif

namespace ppm {
namespace {
bool brandedApplication() {
    return QCoreApplication::organizationName() == storageOrganizationName &&
           QCoreApplication::applicationName() == productShortName;
}
} // namespace
ApplicationStorage applicationStorage() {
    ApplicationStorage storage;
#ifdef Q_OS_WIN
    UINT32 length = 0;
    const auto status = GetCurrentPackageFamilyName(&length, nullptr);
    if (status != APPMODEL_ERROR_NO_PACKAGE) {
        if (status != ERROR_INSUFFICIENT_BUFFER || length < 2 || length > 256)
            throw AppError(ErrorCode::FILE_OPERATION_FAILED, {"GetCurrentPackageFamilyName", std::to_string(status)});
        std::vector<wchar_t> family(length);
        const auto read = GetCurrentPackageFamilyName(&length, family.data());
        if (read != ERROR_SUCCESS)
            throw AppError(ErrorCode::FILE_OPERATION_FAILED, {"GetCurrentPackageFamilyName", std::to_string(read)});
        storage.packageFamilyName = QString::fromWCharArray(family.data());
        PWSTR local = nullptr;
        // The older SDK name is the same 0x10000 flag as KF_FLAG_NO_PACKAGE_REDIRECTION.
        const auto result =
            SHGetKnownFolderPath(FOLDERID_LocalAppData, KF_FLAG_NO_APPCONTAINER_REDIRECTION, nullptr, &local);
        if (FAILED(result))
            throw AppError(ErrorCode::FILE_OPERATION_FAILED, {"LocalAppData", std::to_string(result)});
        const auto root = QString::fromWCharArray(local);
        CoTaskMemFree(local);
        const auto packageRoot = QDir(root).filePath("Packages/" + storage.packageFamilyName + "/LocalState/ToolMoa");
        storage.stateDirectory = QDir(packageRoot).filePath("PPM");
        storage.legacyStateDirectory = QDir(packageRoot).filePath("JOBS");
        storage.recoveryDirectory = QDir(storage.stateDirectory).filePath("recovery");
        storage.settingsFile = QDir(storage.stateDirectory).filePath("settings.ini");
        return storage;
    }
#endif
    storage.stateDirectory = QStandardPaths::writableLocation(QStandardPaths::AppLocalDataLocation);
    // Locate legacy state for an explicit, non-destructive startup migration.
    if (brandedApplication())
        storage.legacyStateDirectory = QDir(QFileInfo(storage.stateDirectory).absolutePath()).filePath("JOBS");
    storage.recoveryDirectory = QDir(storage.stateDirectory).filePath("recovery");
    return storage;
}
QSettings applicationSettings() {
    const auto storage = applicationStorage();
    if (storage.packaged())
        return QSettings(storage.settingsFile, QSettings::IniFormat);
    if (brandedApplication())
        return QSettings("ToolMoa", "PPM");
    return QSettings();
}
void migrateApplicationSettings(QSettings &legacy, QSettings &current) {
    constexpr auto marker = "migration/ppmIdentifiersImported";
    if (current.value(marker, false).toBool())
        return;
    for (const auto &key : legacy.allKeys())
        if (!current.contains(key))
            current.setValue(key, legacy.value(key));
    if (legacy.status() != QSettings::NoError)
        throw AppError(ErrorCode::FILE_OPERATION_FAILED, {"legacy settings read"});
    current.setValue(marker, true);
    current.sync();
    if (current.status() != QSettings::NoError)
        throw AppError(ErrorCode::FILE_OPERATION_FAILED, {"PPM settings migration"});
}
QStringList migrateApplicationStorage() {
    const auto storage = applicationStorage();
    if (storage.legacyStateDirectory.isEmpty())
        return {};
    if (storage.packaged()) {
        QSettings legacy(QDir(storage.legacyStateDirectory).filePath("settings.ini"), QSettings::IniFormat);
        auto current = applicationSettings();
        migrateApplicationSettings(legacy, current);
    } else {
        QSettings legacy(storageOrganizationName, "JOBS");
        auto current = applicationSettings();
        migrateApplicationSettings(legacy, current);
    }
    const auto legacyRecovery = QDir(storage.legacyStateDirectory).filePath("recovery");
    try {
        return JsonRecoveryStore(legacyRecovery).migrateTo(storage.recoveryDirectory);
    } catch (const std::exception &error) {
        return {legacyRecovery + "\n" + qErrorText(error)};
    }
}
} // namespace ppm
