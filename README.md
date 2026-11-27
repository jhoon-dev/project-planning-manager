# Project Planning Manager (PPM)

설비·자동화 구축 프로젝트의 PM 겸 공정 담당자를 위한 일정 관리 데스크톱 앱입니다.
여러 담당자의 이번 주 실적과 남은 일을 반영하고, 완료일 변화와 인력 중복 배정을 확인해
다음 주 조정안과 회의 자료를 준비하는 흐름에 집중하고 있습니다.

Windows/macOS · C++20 / Qt 6.8 · 개발 중. 기본 작업은 계정·서버 없이 프로젝트별 `.ppm` 파일로 수행합니다.

## 주간 갱신 흐름

1. 작업·기간·선후관계·근무달력·자원을 입력하고 최초 계획과 기준선을 확정합니다.
2. **주간 갱신**에서 상태일과 실제·잔여 기간을 보고합니다. 미보고는 착수 여부 미확인으로 구분합니다.
3. **결과 비교**에서 기준선·현재 계획·실적 반영 예측의 완료일과 지연 근거를 확인합니다.
4. 인력 과부하와 자원 조정 후보를 비교하고, 선택한 조정안을 사유와 함께 적용합니다.
5. 회의용 PDF를 출력하고 프로젝트를 저장해 다음 주에 이어 씁니다. 파일 저장과 일정 계산은 각각 실행합니다.

[주간 갱신 사용법](docs/weekly-update.md) · [첫 사용자와 과업 범위](docs/planning/20-first-user-weekly-update.md) ·
[빌드·실행 안내](docs/development.md)

코드·저장 식별자와 이전 파일·설정 호환성은 [PPM 식별자 이관](docs/ppm-identity-migration.md)을 참고하세요.

현재는 합성 사례의 자동 검사와 전문가 화면 점검을 마쳤으며, **실제 PM 사용자 시험은 아직 진행하지 않았습니다.**
준비된 [30개 작업 사례와 시험 계획](docs/planning/22-weekly-pm-pilot.md)은 주간 갱신부터 저장·재개까지를 대상으로 합니다.
최초 계획 작성·기준선 생성의 실제 사용자 사용성과 Microsoft Project/Primavera 대체 가능성은 별도 검증이 필요합니다.

## 지원 기능과 개발 상태

작업 표·WBS·간트, 기준선과 실적 이력, 잔여 예측, 자원 배정·과부하·조정 후보 비교,
일정 인쇄와 XLSX/PDF 출력, 자동 복구를 제공합니다. 상세 지원 범위와 제약은 각 사용 안내를 따릅니다.

장기 비전은 Microsoft Project·Primavera를 대체할 수준의 전문 PM 도구이며, 현재 우선순위는 위 주간 업무의 실제 사용자 검증입니다.

## 사용·개발 안내

- [기준선·실적·비교](docs/baseline-progress.md) · [자원·부하·조정안](docs/resources-leveling.md)
- [회의용 일정 출력](docs/schedule-printing.md) · [자동 저장·복구](docs/recovery-undo.md)
- [Project XML](docs/project-xml.md) · [MPP 읽기](docs/mpp-import.md) · [Primavera XER](docs/primavera-xer.md)
- [빌드·실행·검증](docs/development.md) · [제품 PRD](docs/planning/01-product-prd.md) · [현재 로드맵](docs/planning/06-roadmap.md)
- [상세 기능·파일 형식·배포·구현 기록](docs/implementation-overview.md)

개발자 **jhoon-dev** · 브랜드 **Toolmoa** · App ID **`app.toolmoa.ppm`**.
Windows는 [Microsoft Store](https://apps.microsoft.com/detail/9N0PRBD80X6B)에서 배포합니다. macOS는 TestFlight 내부 테스트 빌드를 제공하며, 정식 Mac App Store 심사는 아직 제출하지 않았습니다. [Mac 배포·검증 절차](docs/store/mac-app-store.md)를 참고하세요.
