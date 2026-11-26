#include "application/Document.h"
#include "calculation/Tracking.h"
#include "persistence/JsonProjectStore.h"
#include "persistence/JsonRecoveryStore.h"
#include <QCoreApplication>
#include <QCryptographicHash>
#include <QDir>
#include <QFile>
#include <QFileInfo>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QTemporaryDir>
#include <iostream>
#include <stdexcept>

namespace {
void check(bool value, const char *message) {
    if (!value)
        throw std::runtime_error(message);
}
QByteArray read(const QString &path) {
    QFile file(path);
    check(file.open(QIODevice::ReadOnly), "read migration fixture");
    return file.readAll();
}
void write(const QString &path, const QByteArray &bytes) {
    QFile file(path);
    check(file.open(QIODevice::WriteOnly) && file.write(bytes) == bytes.size(), "write migration fixture");
}
QByteArray signedFile(QJsonObject root) {
    root["sha256"] = QString::fromLatin1(
        QCryptographicHash::hash(QJsonDocument(root["payload"].toObject()).toJson(QJsonDocument::Compact),
                                 QCryptographicHash::Sha256)
            .toHex());
    return QJsonDocument(root).toJson();
}
} // namespace

int main(int argc, char **argv) {
    QCoreApplication app(argc, argv);
    try {
        QTemporaryDir folder;
        ppm::JsonProjectStore files;
        ppm::Document document(files);
        document.create("JOBS in a user title is not an identifier", "2026-11-09", {"jobs-order user task"});
        document.setDuration(0, 480);
        document.captureBaseline("approved", "PM", "reason", "2026-11-09T00:00:00Z");
        const auto expected = *document.project();
        const auto path = folder.filePath("project.ppm");
        document.saveAs(path.toStdString());
        auto legacy = QJsonDocument::fromJson(read(path)).object();
        check(legacy["format"] == "PPM", "new project did not use PPM format");
        legacy["format"] = "JOBS";
        auto payload = legacy["payload"].toObject();
        auto baselines = payload["baselines"].toArray();
        auto baseline = baselines[0].toObject();
        baseline["engineVersion"] = "jobs-cpm-0.2";
        baselines[0] = baseline;
        payload["baselines"] = baselines;
        legacy["payload"] = payload;
        const auto original = signedFile(legacy);
        write(path, original);
        const auto loaded = files.load(path.toStdString());
        check(loaded.project == expected && read(path) == original, "migration changed user data or old bytes");
        ppm::verifyBaseline(loaded.project.baselines[0]);
        const auto output = folder.filePath("saved-ppm.ppm");
        files.save(output.toStdString(), loaded.project, {});
        const auto migrated = QJsonDocument::fromJson(read(output)).object();
        check(migrated["format"] == "PPM" &&
                  migrated["payload"].toObject()["baselines"].toArray()[0].toObject()["engineVersion"] == "ppm-cpm-0.2",
              "new identifiers were not saved");
        auto corrupt = QJsonDocument::fromJson(original).object();
        corrupt["payload"] = migrated["payload"];
        write(path, QJsonDocument(corrupt).toJson());
        bool rejected = false;
        try {
            files.load(path.toStdString());
        } catch (const std::exception &) {
            rejected = true;
        }
        check(rejected, "legacy checksum must be verified before alias normalization");

        const auto oldRoot = folder.filePath("legacy-recovery"), newRoot = folder.filePath("ppm-recovery");
        document.renameTask(0, "edited jobs-order user task");
        const auto recoveryExpected = *document.project();
        ppm::JsonRecoveryStore oldStore(oldRoot), newStore(newRoot);
        auto session = oldStore.newSession();
        const auto id = session->id();
        session->checkpoint(document.recoverySnapshot("2026-11-09T01:00:00Z"));
        oldStore.migrateTo(newRoot);
        check(newStore.scan().candidates.empty(), "active legacy session was copied");
        session->checkpoint(document.recoverySnapshot("2026-11-09T01:05:00Z"));
        session.reset();

        const auto oversizedCheckpoint = QDir(oldRoot).filePath(id + "/checkpoint-000000001.jobrecovery");
        check(QFile::rename(QDir(oldRoot).filePath(id + "/checkpoint-000000001.ppmrecovery"), oversizedCheckpoint),
              "rename owned checkpoint for oversized legacy fixture");
        constexpr qint64 oversizedBytes = 64 * 1024 * 1024 + 1;
        QFile oversizedFile(oversizedCheckpoint);
        check(oversizedFile.open(QIODevice::ReadWrite) && oversizedFile.resize(oversizedBytes),
              "create oversized legacy fixture");
        oversizedFile.close();

        const auto currentCheckpoint = QDir(oldRoot).filePath(id + "/checkpoint-000000002.ppmrecovery");
        auto record = QJsonDocument::fromJson(read(currentCheckpoint)).object();
        record["format"] = "JOBS-RECOVERY";
        auto recoveryPayload = record["payload"].toObject();
        auto oldProject = recoveryPayload["project"].toObject();
        auto oldBaselines = oldProject["baselines"].toArray();
        auto oldBaseline = oldBaselines[0].toObject();
        oldBaseline["engineVersion"] = "jobs-cpm-0.2";
        oldBaselines[0] = oldBaseline;
        oldProject["baselines"] = oldBaselines;
        recoveryPayload["project"] = oldProject;
        record["payload"] = recoveryPayload;
        const auto oldCheckpoint = QDir(oldRoot).filePath(id + "/checkpoint-000000002.jobrecovery");
        const auto oldBytes = signedFile(record);
        write(oldCheckpoint, oldBytes);
        check(QFile::remove(currentCheckpoint), "remove owned generated checkpoint");
        const auto corruptCheckpoint = QDir(oldRoot).filePath(id + "/checkpoint-000000003.jobrecovery");
        write(corruptCheckpoint, "corrupt generation");
        const auto warnings = oldStore.migrateTo(newRoot);
        check(warnings.size() == 1 && warnings.front().contains(oversizedCheckpoint) &&
                  QFileInfo(oversizedCheckpoint).size() == oversizedBytes,
              "oversized legacy checkpoint was not reported and preserved");
        const auto scan = newStore.scan();
        check(scan.candidates.size() == 2 && scan.candidates[0].valid && scan.candidates[0].sequence == 2 &&
                  !scan.candidates[1].valid && scan.candidates[1].sequence == 3 &&
                  read(oldCheckpoint) == oldBytes,
              "legacy checkpoint was lost or changed");
        check(read(QDir(newRoot).filePath(id + "/checkpoint-000000003.ppmrecovery")) == "corrupt generation",
              "corrupt recovery generation was silently changed or discarded");
        const auto migratedCheckpoint = QDir(newRoot).filePath(id + "/checkpoint-000000002.ppmrecovery");
        check(QJsonDocument::fromJson(read(migratedCheckpoint)).object()["format"] == "PPM-RECOVERY",
              "recovery envelope was not migrated");
        const auto marker = QDir(newRoot).filePath("brand-migration.json");
        check(QFile::remove(marker), "simulate interruption before migration marker");
        check(oldStore.migrateTo(newRoot) == warnings, "resume lost the oversized checkpoint warning");
        const auto migratedBytes = read(migratedCheckpoint);
        check(QFile::remove(marker), "remove owned marker for conflict test");
        write(migratedCheckpoint, "unrelated current state");
        bool conflictRejected = false;
        try {
            oldStore.migrateTo(newRoot);
        } catch (const std::exception &) {
            conflictRejected = true;
        }
        check(conflictRejected && read(migratedCheckpoint) == "unrelated current state",
              "migration overwrote conflicting current state");
        write(migratedCheckpoint, migratedBytes);
        oldStore.migrateTo(newRoot);
        auto claim = newStore.claim(scan.candidates[0]);
        check(claim->snapshot.project == recoveryExpected, "recovery migration changed project inputs");
        claim.reset();
        newStore.discardSession(id);
        check(oldStore.migrateTo(newRoot).isEmpty(), "completed migration reported a previously skipped checkpoint");
        check(newStore.scan().candidates.empty(), "discarded migrated recovery resurrected on the next launch");
        std::cout << "PASS: legacy hash-first load, PPM save, immutable baseline/user text, active leases, recovery "
                     "migration past oversized generation and no resurrection\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
