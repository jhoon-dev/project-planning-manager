# PPM 서버 인증·실시간 동기화·HTTP API·주기 실행

선택적 Python 3.12+ / aiohttp 3.14.5 / SQLite 서버다. 기존 C++ `PPM-Automation`을 계산·편집 검증기로 사용한다. 서버 프로젝트는 한 데이터베이스의 native BLOB이 원본이며, 기존 로컬 파일을 공유 드라이브에서 동시에 수정하지 않는다. 서버 계정/역할은 로컬 작업공간의 구성원 선택과 독립적이다.

## 시작

현재 체크아웃에서 다음 명령을 실행한다. 기존 `build` 캐시에 이전 저장소 경로가 남아 있으면 새 `build-governance`를 사용한다. C++ Qt 6.8 Core/Network/Widgets/Concurrent/PrintSupport 빌드 환경은 기존 [개발 문서](../docs/development.md)를 따른다.

```powershell
python -m venv .deps/server
.deps/server/Scripts/python.exe -m pip install -r server/requirements-lock.txt
# Qt/MinGW 경로를 설정한 셸에서:
cmake -S . -B build-governance -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH=$pwd/.deps/Qt/6.8.3/mingw_64 -DCMAKE_CXX_COMPILER=$pwd/.deps/Qt/Tools/mingw1310_64/bin/c++.exe -DPPM_SERVER_TEST_PYTHON=$pwd/.deps/server/Scripts/python.exe
cmake --build build-governance --target PPM PPM-Automation --parallel 4
# 최초 관리자 생성: 비밀번호를 명령줄이나 파일에 쓰지 않고 프롬프트에서 입력
./scripts/server.ps1 -Action init -Username administrator
./scripts/server.ps1 -Action serve
```

브라우저의 `http://127.0.0.1:8765` 또는 PPM 작업공간 → **서버 인증·실시간 협업**을 연다. 관리자로 로그인해 native 프로젝트를 등록하고, 브라우저 관리 화면에서 계정과 프로젝트별 editor/viewer/reviewer 권한을 만든다. 데스크톱에서는 열린 로컬 프로젝트의 현재 스냅샷을 등록할 수 있다. 서버 등록은 schema 9부터 설치된 `PPM-Automation`의 읽기 상한까지 지원한다. 현재 소스의 상한은 [schema 84](../src/domain/NativeSchema.h)다. schema 1~8 파일은 데스크톱에서 이관 사본을 저장한 뒤 등록한다. 등록은 새 ID만 허용하며 기존 서버 원본을 native 업로드로 덮어쓰지 않는다. 내려받기는 명시적인 새 native 사본이고 로컬 원본을 자동 교체하지 않는다.

Python을 직접 실행하려면 작업 디렉터리를 `server`로 설정한다.

```text
python -m ppm_server --database /private/ppm/service.sqlite init --user administrator
python -m ppm_server --database /private/ppm/service.sqlite serve --engine /opt/ppm/PPM-Automation --host 127.0.0.1 --port 8765
```

원격 바인딩에는 TLS 인증서·키·정확한 공개 origin을 요구한다.

```powershell
./scripts/server.ps1 -Action serve -ListenHost 0.0.0.0 -Port 8765 -Certificate C:/private/ppm/server.crt -PrivateKey C:/private/ppm/server.key -PublicOrigin https://ppm.example.org:8765
```

실제 사용자는 신뢰할 수 있는 인증서를 발급/설치한다. 네이티브 클라이언트는 원격 평문 HTTP, 인증서 오류 무시, 리다이렉트에 따른 bearer 전달을 허용하지 않는다. loopback HTTP는 개발용이다. 서버는 전달된 proxy 헤더를 신뢰하지 않으며 비-loopback 평문 요청을 거부한다. 서버 DB·키·백업 폴더는 서비스 계정 전용 OS 권한으로 제한한다. POSIX의 새 DB/부모는 각각0600/0700으로 생성한다. Windows에서는 운영자가 폴더 ACL을 제한한다. DB는 로컬 디스크에 둔다.

## 구현 순서와 계약

1. **서버 인증:** 소금16바이트의 scrypt N=131072/r=8/p=1, verifier32바이트. 비밀번호12~256자, 기본 계정/기본 비밀번호 없음. hash 계산은 제한된 두 worker slot에서 수행한다. 로그인 실패는 계정+peer 15분5회, peer 30회로 제한한다. 사용자 열거를 피하도록 실패 응답을 통일한다. 세션은 임의256bit bearer이고 DB에는 SHA256만 저장한다. 절대8시간/유휴30분, 사용자당20개 제한이다. 로그아웃/비밀번호 재설정/계정 비활성화로 철회한다. 관리자 승격은 서버 운영자 초기화 경계다. reviewer/viewer는 조회 가능하고 쓰기는 editor 또는 서버 관리자만 가능하다. 서버는 actor를 요청에서 받지 않고 세션 신원을 기록한다.
2. **실시간 동기화:** 트랜잭션 안에서 전역 순번 이벤트를 추가한다. WebSocket은 연결 후 첫 JSON `{token,after}`로 인증하며 URL에 비밀을 넣지 않는다. 20초 heartbeat와 재연결 cursor를 사용한다. 동일 API의 HTTP long-poll은 after/wait0~25초이며 데스크톱은 이를 사용한다. 이벤트는 현재 권한으로 필터링하고 권한 철회 알림은 대상 사용자에게 전달한다. 세션 철회를 열린 stream에도 반영한다. 깨끗한 화면은 새 원본으로 갱신하고 작성 중인 표는 보존/충돌 표시한다. last-writer-wins나 자동 문자 병합을 수행하지 않는다.
3. **HTTP API:** [OpenAPI 3.1](openapi.json)을 제공한다. native 등록/조회/다운로드, 계정/권한, batch 미리보기/적용, 변경 feed, 영수증과 예약/이력을 지원한다. 원격 편집 필드는 현재 안정 작업 ID의 이름/기간이다. 기존 승인·실적·기준선 원장을 JSON으로 직접 덮어쓰지 않는다. 1MiB 요청, native64MiB, 엄격 키/중복 JSON 키/유한 숫자/Unicode, 타임아웃을 검사한다. 미리보기는 사용자·프로젝트·서버 버전·정규화 요청 SHA256에 묶여 10분 유효하다. 적용은 현재 인증/권한과 버전을 다시 확인한다. 동일 사용자/project/requestId와 내용의 재요청은 저장된 영수증을 반환하고 내용이 다르면409다. 영수증 조회 API는 티켓이 정리된 뒤에도 결과를 확인할 수 있게 한다.
4. **주기 실행:** 닫힌 native batch만 실행하는 고정 간격 worker다. 간격60초~30일과 UTC Unix 시작 시각을 저장한다. UI의 현지 시각은 Unix UTC로 변환한다. 예약 검증 시와 매 실행 commit 시 소유자의 현재 권한을 검사한다. 작업/실행 키·120초 lease·결과/다음 시각이 영속적이다. 중단 후 lease가 만료되면 같은 실행 키로 재시도하며, 결과 native BLOB/receipt/event/run/다음 예약을 같은 DB 트랜잭션에 commit한다. 여러 worker가 같은 시각을 중복 commit하지 않는다. 서버 중단 동안 놓친 횟수는 한 번으로 합치고 다음을 현재 시각+간격으로 설정한다. 외부 수정/권한 철회/native 실패는 예약을 멈추고 이력을 남긴다. 취소는 아직 commit하지 않은 실행도 차단한다. 실패/충돌 뒤에는 원본을 다시 검토해 새 예약을 만든다.

서버 버전은 수락한 batch마다 증가하고 native revision은 실제 입력 변경이 있을 때 증가한다. 따라서 no-op 반복도 실행 이력과 별도 서버 버전을 가진다. 클라이언트는 두 값을 혼동하지 않는다. 개별 HTTP 미리보기/적용에는 source server version과 native revision을 모두 요구한다. 다른 클라이언트의 변경이 있으면409이며 자동 재기반하지 않는다. 요청 전후 SHA256은 같은 정규화 바이트를 사용한다.

## 호출 예

```json
POST /api/v1/projects/{project}/preview
{
  "expectedVersion": 3,
  "request": {
    "format": "PPM-AUTOMATION-1",
    "documentId": "project-id",
    "revision": 8,
    "requestId": "request-001",
    "operations": [{"taskId": "task-id", "name": "검토 완료", "durationMinutes": 960}]
  }
}
```

로그인에서 받은 token을 `Authorization: Bearer ...`로 보낸다. 미리보기 결과의 변경 전후를 검토하고 `POST /api/v1/projects/{project}/apply {"previewId":"..."}`를 보낸다. 성공 영수증에는 serverVersion/actor/committedAt이 추가된다. 저장된 영수증은 `GET /api/v1/projects/{project}/receipts/{request_id}`에서 본인 실행에 한해 조회한다.

예약은 `POST /api/v1/jobs`에 위 request/expectedVersion과 projectId/intervalSeconds/startAt을 보낸다. `GET /api/v1/jobs`, `GET /api/v1/runs`, `DELETE /api/v1/jobs/{id}`로 조회/취소한다. 서버가 실행 중일 때 실행되며 OS 알람이나 Codex 자동화에 등록하지 않는다. 임의 셸/Python/외부 URL 실행은 지원하지 않는다.

사용자당 활성 예약은 100건까지 만들 수 있다. 취소 또는 실패한 예약은 이력에 남고 활성 예약 자리는 다시 사용할 수 있다.

## 운영·복구

```powershell
./scripts/server.ps1 -Action backup -BackupOutput C:/private/ppm/backup-2026-11-05.sqlite
./scripts/server.ps1 -Action reset-password -Username editor
```

백업은 SQLite online backup API이며 WAL 파일을 수동 복사하지 않는다. 기존 백업 파일을 덮어쓰지 않는다. 복구는 서버를 중지하고 백업 DB를 새 경로에 둔 뒤 그 경로로 시작한다. 복구 후 모든 클라이언트에서 로그아웃/재로그인하여 백업 시점의 원본과 변경 cursor로 새 세션을 시작한다. 비밀도 포함되므로 백업의 OS 권한을 유지한다. 세션 철회가 필요하면 비밀번호 재설정으로 정리한다. DB schema1, SQLite WAL/synchronous FULL/BEGIN IMMEDIATE를 사용한다. 이벤트·영수증·작업 이력은 임의 삭제하지 않는다. 운영자는 용량/백업/접근 로그 정책을 별도로 정한다. [systemd 예제](deployment/ppm.service)는 경로·서비스 계정·인증서를 설치 환경에 맞게 바꿔 사용하며 이번 개발에서 등록/배포하지 않았다.

데스크톱은 Qt Network를 추가 사용하며 Windows 패키지에 Qt6Network와 TLS backend를 포함한다. macOS 앱의 outgoing network entitlement와 local-network 목적 문자열을 추가했다. 실제 macOS/스토어 설치본의 네트워크 승인 동작과 외부 서버 운영 배포는 해당 환경의 수용 검증이다. 기존 `.ppm`와 `.ppmworkspace` schema는 바꾸지 않는다.

## 검증

```powershell
cmake -S . -B build-governance -DPPM_SERVER_TEST_PYTHON=$pwd/.deps/server/Scripts/python.exe
cmake --build build-governance --parallel 4
ctest --test-dir build-governance --output-on-failure
```

선택 Python 경로를 지정하면 server_http_auth_sync_scheduler(실제 native CLI를 사용하는 Python 통합 검사)와 server_native_realtime_ui(두 네이티브 클라이언트·Qt 화면·TLS 인증서 거부)를 기존 전체 CTest에 더한다. CI는 고정 server requirements를 설치하고 두 검사도 실행한다. 브라우저의 로그인/수정/초안 보존/예약 실행·취소와 Windows 화면도 별도로 확인한다. [검증 기록](../docs/validation/server-collaboration-2026-11-05/README.md).

테스트 전용 공개 인증서/키와 계정은 tests fixture에서만 사용한다. production launcher가 이들을 자동 선택하지 않는다. 서비스의 독립 보안 감사, MFA/SSO·비밀번호 복구 메일, 임의 필드 동시 병합, cron/달력 스케줄, 여러 서버의 HA/부하 운영은 이번 구현의 완료 주장에 포함하지 않는다.

구현 근거: [OWASP scrypt 매개변수](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html), [SQLite transaction](https://sqlite.org/lang_transaction.html), [Qt NetworkAccessManager](https://doc.qt.io/qt-6/qnetworkaccessmanager.html), [Apple network.client](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.security.network.client), [Apple local network privacy](https://developer.apple.com/documentation/technotes/tn3179-understanding-local-network-privacy).
