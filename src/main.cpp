#include "ui/SandboxAccess.h"
#include "persistence/JsonProjectStore.h"
#include "ui/MainWindow.h"
#include "ui/ApplicationIcon.h"
#include "ui/UiTranslations.h"
#include "ui/DesktopWorkspace.h"
#include "persistence/ApplicationStorage.h"
#include "persistence/JsonRecoveryStore.h"
#include "updates/UpdateController.h"
#include "application/ProductIdentity.h"
#include <QApplication>
#include <QMessageBox>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    ppm::installUiTranslations(app);
    QCoreApplication::setApplicationName(ppm::productShortName);
    QGuiApplication::setApplicationDisplayName(ppm::productDisplayName);
    QCoreApplication::setApplicationVersion(ppm::appVersion());
    QCoreApplication::setOrganizationName(ppm::storageOrganizationName);
    QGuiApplication::setDesktopFileName(ppm::productAppId);
    QApplication::setWindowIcon(ppm::applicationIcon());
    QStringList recoveryWarnings;
    try {
        recoveryWarnings = ppm::migrateApplicationStorage();
    } catch (const std::exception &error) {
        QMessageBox::warning(nullptr, "PPM 데이터 이관", QString::fromUtf8(error.what()));
        return 1;
    }
    ppm::restoreSandboxFolders();
    auto store = std::make_shared<ppm::JsonProjectStore>();
    auto recovery = std::make_shared<ppm::JsonRecoveryStore>(ppm::JsonRecoveryStore::defaultDirectory());
    ppm::UpdateController updates(ppm::updateConfig());
    ppm::DesktopWorkspace workspace(store, recovery);
    workspace.setUpdates(&updates);
    auto *window = workspace.newWindow();
    if (!recoveryWarnings.isEmpty()) {
        auto *warning = new QMessageBox(QMessageBox::Warning, "이전 복구본 이관",
                                        "이전 복구본을 이관하는 중 문제가 발생했습니다. 원본은 보존했습니다.",
                                        QMessageBox::Ok, window);
        warning->setModal(false);
        warning->setAttribute(Qt::WA_DeleteOnClose);
        warning->setDetailedText(recoveryWarnings.join("\n\n"));
        warning->show();
    }
    return app.exec();
}
