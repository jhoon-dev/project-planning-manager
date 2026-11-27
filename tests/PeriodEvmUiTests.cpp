#include "PeriodEvmFixture.h"
#include "ui/MainWindow.h"
#include "ui/ReportDialog.h"
#include <QAction>
#include <QApplication>
#include <QComboBox>
#include <QDateEdit>
#include <QDir>
#include <QFile>
#include <QFileDialog>
#include <QFontDatabase>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QTabWidget>
#include <QTableView>
#include <QTemporaryDir>
#include <QTest>
#include <QTimer>
#include <iostream>
using namespace ppm;
namespace {
void check(bool good, const char *m) {
    if (!good)
        throw std::runtime_error(m);
}
bool ready(ReportDialog &d, const QString &needle = {}) {
    for (int i = 0; i < 1000; ++i) {
        QTest::qWait(10);
        if (d.findChild<QPushButton *>("exportXlsx")->isEnabled() &&
            d.findChild<QLabel *>("reportMessage")->text().contains(needle))
            return true;
    }
    std::cerr << d.findChild<QLabel *>("reportMessage")->text().toStdString() << '\n';
    return false;
}
QString cell(ReportDialog &d, int r, int c) {
    auto *t = d.findChild<QTableView *>("periodEvm");
    check(t && t->model(), "missing virtual period table");
    return t->model()->index(r, c).data().toString();
}
void selectFile(const QString &path, bool cancel = false) {
    QTimer::singleShot(30, [path, cancel] {
        auto *chooser = qobject_cast<QFileDialog *>(QApplication::activeModalWidget());
        if (!chooser) {
            std::cerr << "file chooser missing\n";
            std::exit(2);
        }
        if (cancel)
            chooser->reject();
        else {
            chooser->findChild<QLineEdit *>("fileNameEdit")->setText(path);
            QMetaObject::invokeMethod(chooser, "accept");
        }
    });
}
} // namespace
int main(int argc, char **argv) {
    QApplication app(argc, argv);
#ifdef Q_OS_WIN
    const int font = QFontDatabase::addApplicationFont("C:/Windows/Fonts/malgun.ttf");
    if (font >= 0)
        app.setFont(QFont(QFontDatabase::applicationFontFamilies(font).front(), 9));
#endif
    QApplication::setAttribute(Qt::AA_DontUseNativeDialogs);
    QTimer watchdog;
    watchdog.setSingleShot(true);
    QObject::connect(&watchdog, &QTimer::timeout, [] {
        std::cerr << "native period EVM UI timeout\n";
        std::exit(2);
    });
    watchdog.start(90000);
    try {
        QTemporaryDir tmp;
        JsonProjectStore store;
        const auto path = (tmp.path() + "/source.ppm").toStdString();
        auto p = period_evm_fixture::make(store, path);
        Document d(store);
        d.open(path);
        const auto before = *d.project();
        QDir().mkpath("native-period-evm-ui-qa");
        MainWindow main(d);
        main.show();
        auto *action = main.findChild<QAction *>("nativePeriodEvm");
        check(action && action->isEnabled(), "menu unavailable");
        bool menuOpened = false;
        QTimer::singleShot(80, [&] {
            auto *dialog = dynamic_cast<ReportDialog *>(QApplication::activeModalWidget());
            if (!dialog || !dialog->property("nativePeriodEvm").toBool()) {
                std::cerr << "wrong EVM menu dialog\n";
                std::exit(2);
            }
            menuOpened = true;
            dialog->reject();
        });
        action->trigger();
        check(menuOpened, "menu not opened");
        ReportDialog dialog(d, {}, p.baselines.front().id, &main, true);
        dialog.resize(1100, 760);
        dialog.show();
        check(ready(dialog), "initial EVM calculation");
        auto *unit = dialog.findChild<QComboBox *>("periodEvmBucket");
        unit->setCurrentIndex(0);
        check(ready(dialog) && cell(dialog, 0, 8) == "20.00" && cell(dialog, 0, 11) == "19.00" &&
                  cell(dialog, 0, 14) == "18.00",
              "daily UI values");
        check(dialog.findChild<QTabWidget *>("reportTabs")->currentIndex() == 1, "period tab not selected");
        dialog.grab().save("native-period-evm-ui-qa/daily.png");
        dialog.resize(800, 600);
        QTest::qWait(40);
        dialog.grab().save("native-period-evm-ui-qa/daily-small.png");
        auto *close = dialog.findChild<QPushButton *>("exportXlsx");
        check(close->visibleRegion().boundingRect().height() > 0, "footer invisible");
        dialog.findChild<QDateEdit *>("reportTo")->setDate(QDate(2026, 11, 8));
        unit->setCurrentIndex(1);
        check(ready(dialog), "weekly UI");
        check(dialog.findChild<QTableView *>("periodEvm")->model()->rowCount() == 2, "week row count");
        unit->setCurrentIndex(2);
        check(ready(dialog), "monthly UI");
        check(dialog.findChild<QTableView *>("periodEvm")->model()->rowCount() == 2, "month row count");
        unit->setCurrentIndex(0);
        dialog.findChild<QDateEdit *>("reportTo")->setDate(QDate(2026, 10, 30));
        check(ready(dialog), "latest generation");
        dialog.findChild<QComboBox *>("reportScope")->setCurrentIndex(2);
        check(ready(dialog) && cell(dialog, 0, 5) == "10.00", "scope not applied");
        dialog.findChild<QComboBox *>("reportScope")->setCurrentIndex(0);
        check(ready(dialog), "scope restore");
        const auto out = QDir::currentPath() + "/native-period-evm-ui-qa/ui-report.xlsx";
        QFile::remove(out);
        selectFile(out);
        close->click();
        check(ready(dialog, "내보내기 완료") && QFile::exists(out), "UI XLSX output");
        const auto pdf = QDir::currentPath() + "/native-period-evm-ui-qa/ui-report.pdf";
        QFile::remove(pdf);
        selectFile(pdf);
        dialog.findChild<QPushButton *>("exportPdf")->click();
        check(ready(dialog, "내보내기 완료") && QFile::exists(pdf), "UI PDF output");
        auto cancelled = tmp.path() + "/cancel.xlsx";
        selectFile(cancelled, true);
        close->click();
        check(!QFile::exists(cancelled), "cancelled export");
        check(*d.project() == before && !d.dirty(), "query/export mutated native input");
        dialog.findChild<QPushButton *>("refreshReport")->click();
        dialog.findChild<QPushButton *>("cancelPeriodEvm")->click();
        QTest::qWait(100);
        check(!close->isEnabled() && !dialog.findChild<QTableView *>("periodEvm"), "cancelled result published");
        dialog.findChild<QPushButton *>("refreshReport")->click();
        check(ready(dialog), "refresh after cancellation");
        d.renameTask(0, "changed");
        check(QTest::qWaitFor(
                  [&] {
                      return !close->isEnabled() && !dialog.findChild<QPushButton *>("exportPdf")->isEnabled() &&
                             !dialog.findChild<QTableView *>("periodEvm");
                  },
                  2000),
              "stale result export enabled");
        dialog.findChild<QPushButton *>("refreshReport")->click();
        check(ready(dialog), "refresh stale");
        dialog.findChild<QPushButton *>("refreshReport")->click();
        d.setWriteAuthorization([] { return true; });
        QTest::qWait(150);
        check(!close->isEnabled() && !dialog.findChild<QTableView *>("periodEvm"),
              "same-revision session changed result published");
        dialog.reject();
        Document viewer(store);
        viewer.open(path, true);
        ReportDialog readOnly(viewer, {}, p.baselines.front().id, nullptr, true);
        readOnly.show();
        check(ready(readOnly), "readonly EVM unavailable");
        readOnly.reject();
        std::cout << "PASS: native period EVM menu/virtual tables, day/week/month/scope, XLSX/PDF, native equality, "
                     "cancel/stale/session/read-only, Windows responsive footer\n";
        return 0;
    } catch (const std::exception &e) {
        std::cerr << "FAIL: " << e.what() << '\n';
        return 1;
    }
}
