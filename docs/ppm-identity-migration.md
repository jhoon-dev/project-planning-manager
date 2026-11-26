# PPM 식별자 이관

코드 네임스페이스·CMake 프로젝트/타깃·검사 실행 파일·환경 변수·리소스 경로는 `PPM/ppm`을 사용한다.
예약 작업을 뜻하는 서버 `/jobs`, SQL 테이블과 GitHub Actions의 `jobs`는 제품 이름이 아니므로 유지한다.

## 저장 파일과 엔진

- 새 프로젝트와 작업공간은 `PPM`, `PPM-WORKSPACE` 형식 태그로 저장한다.
- 기존 `JOBS`, `JOBS-WORKSPACE` 파일도 읽는다. 원본 payload의 SHA-256을 먼저 검증하고,
  기준선의 `jobs-…` 엔진 ID를 같은 버전의 `ppm-…`로 이관한다. 사용자 이름·작업명·문서 ID·날짜·실적은 바꾸지 않는다.
- 엔진 버전의 숫자와 계산 정책은 그대로다. 이관된 과거 기준선은 이전과 같은 정책으로 재계산해 검증한다.
- 열기만 해서는 원본 파일을 다시 쓰지 않는다. 명시적으로 저장하면 새 태그와 엔진 ID가 기록된다.
  새 태그를 지원하지 않는 과거 앱으로 되돌아갈 때에는 이관 전 원본 사본을 사용해야 한다.
- XML/XER 교환 결과의 제품 계약 태그와 매핑 키는 `ppm-…`, `ppmId`, `ppmRecomputation`으로 출력한다.
  이전 XML 기준선 매핑의 `jobsId`는 입력 별칭으로 읽는다.

저장 데이터의 구조와 native schema 번호는 바꾸지 않는다. 과거 native-history fixture와 해시 목록은
옛 형식 읽기와 69개 기준선 재생을 검사하기 위해 원본 그대로 보존한다.

## 설정과 복구

일반 실행판의 설정은 `ToolMoa/PPM`, 상태·복구 경로의 앱 이름은 `PPM`으로 이동한다.
MSIX는 같은 package family의 `LocalState/ToolMoa/PPM`을 사용한다.
시작 시 `JOBS` 위치의 설정 중 새 설정에 없는 키만 복사하고 기존 설정은 덮어쓰지 않는다.

복구 세대는 원래 세션의 잠금을 확보한 뒤 검증하고, 새 `PPM-RECOVERY` 태그와 `.ppmrecovery` 확장자로
원자적으로 게시한다. 이전 `.jobrecovery`도 읽을 수 있다. 실행 중인 세션은 다음 시작으로 이관을 미룬다.
읽을 수 있는 손상 세대는 원래 내용을 옮겨 복구 목록에 손상으로 표시한다. 읽기에 실패하거나 크기 한도를 초과한 세대는
기존 위치에 보존하고 경로와 원인을 경고에 표시한 뒤 나머지 복구본을 이관한다. 복구 이관에 실패해도 앱을 시작할 수 있다.
완료한 세션 이관을 기록해, 사용자가 복구를 폐기한 뒤 다음 시작에 과거 복구가 되살아나지 않게 한다.
이전 설정·복구 원본은 삭제하지 않는다.

## Windows Store

기존 Store package identity와 publisher는 유지한다. 기본 실행 ID는 `PPM`으로 바꾼다.
Store 패키지에는 앱 진입점 하나만 포함하며 옛 실행 ID를 별도 앱으로 추가하지 않는다.
실행 ID 변경으로 기존 시작 화면 고정 위치가 달라질 수 있고, 기존 고정 바로가기는 새 앱으로 다시 고정해야 할 수 있다.
[Microsoft 실행 ID 안내](https://learn.microsoft.com/en-us/uwp/schemas/appxpackage/uapmanifestschema/element-f-application)와
[Store의 단일 앱 패키지 요건](https://learn.microsoft.com/en-us/uwp/schemas/appxpackage/uapmanifestschema/element-f-applications)을 따른다.
개발 MSIX identity와 probe 실행 파일도 `PPM/ppm` 이름을 사용한다.

남아 있는 옛 문자열은 입력·경로 이관 또는 과거 성능 기준 빌드에 필요한 호환 코드다.
새 출력과 현재 실행 이름에는 사용하지 않는다.
