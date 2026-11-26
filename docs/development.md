# C++/Qt 초기 구현

검증 요약·회귀 입력·CI 산출물은 [검증 기록 보관 방식](validation/README.md)에 따라 분리한다.

2026-11-17: [MF-01~07 자재 제약 여유·임계](material-float.md)를 구현했다. 후보/전체 증인의 정확한 재고 검사·자재별 탐색 묶음·계획/잔여/공유 통합·새 기준선 엔진과 조건부84를 연결한다. 과거 승인 계산을 재현하며, 현재 상한84·미지원 미래85다.

2026-11-17: [SMAT-01~07 공유 통합 실제 자재](shared-material-actuals.md)를 구현했다. 구분된 원장/정정 연결·리비전 안정 정렬·동일 상태일 공급/잔여 수요·공유 부하·날짜별 잔여 공수/진척 정책·재고 근거와 원본/세대 보존을 연결한다. 저장 형식은 유지한다.

2026-11-17: [MAT-01~08 실제 자재 원장·잔여 자동 대기](actual-materials.md)를 구현했다. 추가 전용 거래/정정·보고 상태일별 재고·명시 확인/잔여 수량·미래 입고 잔량·네 계산 프로필/공수 곡선·채택/시나리오/복구·보고와 조건부83을 연결한다. [검증 기록](validation/actual-materials-2026-11-17/README.md).

2026-11-17: [MAD-01~07 입고 자동 대기](material-arrival-leveling.md)를 구현했다. 명시 옵션·직렬 예약/미래 소모 보호·시작/완료/균등/곡선·기존 세 계산 엔진과 공수 엔진·공유 투영·채택/결정 이력·조건부82를 연결한다. [검증 기록](validation/material-arrival-leveling-2026-11-17/README.md).

2026-11-17: [MINV-01~07 계획 자재 입고/재고](material-inventory.md)를 구현했다. 개시 시각·입고·작업 실행분 소모/누적 반올림·최초 부족·미정·단일/공유 평준화 검산·UI/출력·조건부81과 전체 사본/undo/복구를 연결한다. [검증 기록](validation/material-inventory-2026-11-17/README.md)을 따른다.

2026-11-16: [SPA-01~06 공유 가용기간](shared-resource-availability.md)을 구현했다. 열린/분 단위 기간·전체 경계·날짜 우선순위와 미정/0·공유 조회/부하 적분/평준화·편집·조건부 작업공간4·기존1~3/native80 보존을 연결한다. [검증 기록](validation/shared-resource-availability-2026-11-16/README.md)을 따른다.

2026-11-16: [SRA-01~06 공유 잔여 가용량](shared-remaining-availability.md)을 구현했다. 명시 연결·공유 공급 단일 적용·파일별 예측 상태일/누락 하한·세대 무효화·비동기 UI/취소·JSON/XLSX/PDF를 연결한다. [검증 기록](validation/shared-remaining-availability-2026-11-16/README.md)을 따른다. 파생 조회이며 native80과 기존 작업공간 schema를 유지한다.

2026-11-16: [RRA-01~06 잔여 가용량](remaining-resource-availability.md)을 구현했다. 자원 근무 달력·가용기간과 현재 일정 실행 수요를 시점별로 비교하며 조회 UI·두 외부 함수·계산 문맥 캐시·XML/XER/보고·schema80을 지원한다. [검증](validation/remaining-resource-availability-2026-11-16/README.md). 관련37/37·79.23초와 파서1,022개, 독립1,440분/7,200값·XML12값/XER9값·XLSX3행/PDF15쪽을 통과했다.

2026-11-16: [RAV-01~06 자원 가용기간](resource-availability.md)을 구현했다. native 경계/무기한·부분일 기간, 날짜 예외 우선순위·구간별 부하/평준화·계산식 캐시와 XML 정규화·schema79·편집/보고/복구를 연결한다. [검증 기록](validation/resource-availability-2026-11-16/README.md). 관련44/44·204.21초와 XER 일괄1/1·2.21초, 파서1,014개·독립 XML11,520분/MPXJ5,760분·XLSX/PDF12쪽을 확인했다.

2026-11-15: [XUF-01~06 Units·가용률 참조](xml-unit-fields.md)를 구현했다. 기본 배정률/자원 가용률과 명시 civil 날짜 조회, Null/0·요약·혼합 캐시·XML AvailabilityPeriods·schema78 및 편집/복구를 연결한다. [실행 검증](validation/xml-unit-fields-2026-11-15/README.md). 최종 회귀61/61·93.01초, 파서1,000개, 독립 XML48값/가용기간4개·XER/XLSX 각28값·PDF18쪽, MPXJ 배정4건/기간4건을 통과했다.

2026-11-15: [native 기준선 상세 시간분포](native-baseline-timephased.md)를 구현했다. 동결 실행 공수와 일별 원가/직접비·자재/경비의 다섯 범위 표준 출력, 부모 위치 재채택/병합과 조건부 schema77을 연결한다. 집중48/48·109.66초와 원가/Usage3/3·1.64초, 파서988개, 독립98블록/7,273분과 MPXJ 배정6건을 확인했다. [검증 기록](validation/native-baseline-timephased-2026-11-15/README.md).

2026-11-15: [기존 문서 XML 기준선 병합](xml-baseline-merge.md)을 구현했다. 번호별 전체 교체·명시 연결/제외·다른 번호의 출처/달력 보존·전후 불변 이력과 조건부 schema76을 연결한다. 집중 회귀47/47·53.34초, 파서976개, 독립 XML/JSON·XLSX/PDF와 현재 평준화 일정/관측 보존을 확인했다. [검증 기록](validation/xml-baseline-merge-2026-11-15/README.md).

2026-11-15: [외부 XML 기준선 채택·표준 내보내기](xml-baseline-exchange.md)를 구현했다. 번호별 새 사본 채택·표시/시간분포 보존·native 승인본 투영과 조건부 schema75·통화/ID/복구를 연결한다. 집중 회귀42/42·53.36초, 파서960개, 독립 XML/Decimal·XLSX/PDF와 MPXJ 공수/원가를 확인했다. MPXJ의 소수 초 제한과 실제 제품 왕복 미실행은 [검증 기록](validation/xml-baseline-exchange-2026-11-15/README.md)에 명시했다.

2026-11-15: [번호별 기준선](xml-numbered-baselines.md)·[요약 기간](xml-summary-durations.md)을 순차 구현했다. 새 전용 Release 빌드, 집중 회귀29/29·독립 근무시간129건·XML/XER·XLSX/PDF와 형식/구문 검사를 [검증 기록](validation/numbered-baselines-summary-2026-11-15/README.md)에 남긴다. 전체 CTest나 외부 제품 실행을 완료한 것으로 확대하지 않는다.

2026-11-15 후속: [XML SLN·SYD](xml-depreciation-functions.md)의 정액/연수합계 감가상각·소수 life/period·정확한 중간 계산·최종 반올림과 조건부 schema72를 구현했다. [검증](validation/xml-depreciation-2026-11-15/README.md). 최종 검증: 일반 CTest 230/230 통과·시간 초과 0건·703.60초, 대용량 단독1/1·156.69초로231개 테스트 확인(표준 시간 실패 없음), 집중 부분집합62/62·파서938개·형식565파일, 독립 유리수9032(overflow100)/Windows8714(정확8713·0.000001 차이1건)·직접 식25/공통 오류5·XML/XER20값·XLSX66행/PDF19쪽·schema72 실행 패키지를 확인했다.

2026-11-14 후속: [XML Partition](xml-partition-function.md)의 Text 구간·경계/반올림·Null·공백 보존과 조건부 schema71를 구현했다. [검증](validation/xml-partition-2026-11-14/README.md). 최종 검증: 일반 CTest 228/228 통과·시간 초과 0건·565.37초, 대용량 CTest180초 시간 초과/동일 실행 파일 직접1/1·160.24초로229개 테스트 확인(표준 시간 실패 1건 유지), 집중 부분집합60/60·파서934개·형식562파일, 독립 구간5332/Windows5332·직접 인수21/오류5·XML/XER22값·XLSX68행/PDF19쪽·schema71 실행 패키지를 확인했다.

2026-11-14 후속: [XML RGB·QBColor](xml-color-functions.md)의 Number 색상 코드·성분 제한·짝수 반올림·16색 팔레트와 조건부 schema70를 구현했다. [검증](validation/xml-colors-2026-11-14/README.md). 최종 검증: 일반 CTest 226/226 통과·시간 초과 0건·769.76초, 대용량 단독1/1·167.64초로227개 테스트 확인(표준 시간 실패 없음), 집중 부분집합58/58·파서930개·형식559파일, 독립 색상5609/Windows RGB5593·직접 식17/오류8·QBColor16·XML/XER20값·XLSX66행/PDF19쪽·schema70 실행 패키지를 확인했다.

2026-11-14 후속: [XNF-01~06 XML 숫자 표시3개](xml-numeric-display.md)의 FormatNumber/Percent/Currency·고정 en-US·정확한 십진 반올림·TriState·Null/오류와 네 범위·요약/전파·미리보기/교환/보고·조건부 schema69/전체 사본을 구현했다. Currency는 문서 통화와 별개의 고정 $ 표시다. [검증](validation/xml-numeric-display-2026-11-14/README.md). 최종 검증: 일반 CTest 224/224 통과·시간 초과 0건·658.42초, 대용량 단독1/1·168.89초로225개 테스트 확인(표준 시간 실패 없음), 집중 부분집합56/56·파서926개·형식556파일, 독립 십진16200/VBScript7128·직접 식28/오류8·XML/XER20값·XLSX66행/PDF19쪽·schema69 실행 패키지를 확인했다.

2026-11-14 후속: [XDT-01~06 XML FormatDateTime](xml-format-datetime.md)의 고정 en-US 표시0~4·기준일/자정·옵션 반올림·Null/오류와 네 범위·요약/전파·미리보기/교환/보고·조건부 schema68/전체 사본을 구현했다. 소수 초는 표시에서 버리며 원본 Date는 보존한다. [검증](validation/xml-date-display-2026-11-14/README.md). 최종 검증: 일반 CTest 222/222 통과·시간 초과 0건·664.49초, 대용량 단독1/1·174.28초로223개 테스트 확인(표준 시간 실패 없음), 집중 부분집합54/54·파서922개·형식553파일, 독립 표시7370/VBScript7370·직접 식19/오류4·XML/XER20값·XLSX66행/PDF19쪽·schema68 실행 패키지를 확인했다.

2026-11-14 후속: [XDN-01~06 XML MonthName·WeekdayName](xml-date-name-functions.md)의 고정 en-US 이름/약어·주 시작일·짝수 반올림·Null/오류와 네 범위·요약/전파·미리보기/교환/보고·조건부 schema67/전체 사본을 구현했다. [검증](validation/xml-date-names-2026-11-14/README.md). 최종 검증: 일반 CTest 220/220 통과·시간 초과 0건·697.84초, 대용량 단독1/1·152.60초로221개 테스트 확인(표준 시간 실패 없음), 집중 부분집합52/52·파서918개·형식550파일, 독립 이름5992/VBScript5992·직접 식26/오류8·XML/XER20값·XLSX66행/PDF19쪽·schema67 실행 패키지를 확인했다.

2026-11-14 후속: [XUC-01~06 XML AscW·ChrW](xml-unicode-functions.md)의 native/XML-safe BMP 코드 변환·부호/음수 별칭·짝수 반올림·Null/오류와 네 범위·요약/전파·미리보기/교환/보고·조건부 schema66/전체 사본을 구현했다. [검증](validation/xml-unicode-2026-11-14/README.md). 최종 검증: 일반 CTest 218/218 통과·시간 초과 0건·728.70초, 대용량 CTest180초 시간 초과/동일 실행 파일 직접1/1·273.18초로219개 테스트 확인(표준 시간 실패 1건 유지), 집중 부분집합50/50·파서914개·형식547파일, 독립 문자63456/VBScript63456·직접 식24·XML/XER20값·XLSX66행/PDF19쪽·schema66 실행 패키지를 확인했다.

2026-11-14 후속: [XLK-01~06 XML Like](xml-like-operator.md)를 구현했다. BMP 정확 비교·와일드카드/목록/범위/부정·전체 패턴 검증·유한 작업량/Null과 네 범위·요약/전파·미리보기/교환/보고·조건부 schema65/전체 사본을 연결한다. [검증](validation/xml-like-2026-11-14/README.md). 최종 검증: 일반 CTest 216/216 통과·시간 초과 0건·805.89초, 대용량 단독1/1·161.81초로217개 테스트 확인(표준 시간 실패 없음), 집중 부분집합48/48·파서910개·형식544파일, 독립 패턴8932/.NET8932·XML/XER20값·XLSX66행/PDF19쪽·schema65 실행 패키지를 확인했다.

2026-11-14 후속: [XLG-01~06 XML 논리 연산](xml-logical-operators.md)의 Eqv/Imp를 구현했다. Boolean/32비트·형식별 Null·새 식 우선순위/기존 문법 보존과 네 범위·요약/전파·미리보기/교환/보고·조건부 schema64/전체 사본을 연결한다. [검증](validation/xml-logical-2026-11-14/README.md). 최종 검증: 일반 CTest211/214 통과·시간 초과3건·637.02초, 동일 코드 순차 확장3/3 통과, 대용량 CTest180초 시간 초과/동일 실행 파일 직접1/1·224.57초로215개 기능 확인(표준 시간 실패4건 유지), 집중 부분집합46/46·파서906개·형식541파일, 독립 비트4096/진리표200·VBScript4296·XML/XER20값·XLSX66행/PDF19쪽·schema64 실행 패키지를 확인했다.

2026-11-14 후속: [XOP-01~06 XML 산술 연산](xml-arithmetic-operators.md)의 ^/정수 나눗셈을 구현했다. 새 식의 VBA 우선순위·과거 문법 보존·32비트 짝수 반올림·거듭제곱/범위/Null과 네 범위·요약/전파·미리보기/교환/보고·조건부 schema63/전체 사본을 연결한다. [검증](validation/xml-arithmetic-2026-11-14/README.md). 최종 검증: 일반212/212·487.22초, 대용량 CTest180초 시간 초과/동일 실행 파일 직접1/1·208.46초(표준 시간 실패1건 유지), 집중 부분집합44/44·파서902개·형식538파일, 독립 거듭제곱2048/정수 몫2048·VBScript4096·XML/XER20값·XLSX66행/PDF19쪽·schema63 실행 패키지를 확인했다.

2026-11-14 후속: [XBC-01~06 XML Baseline Cost](xml-baseline-cost.md)를 구현했다. 최초 native v1의 날짜별 동결 단가·공수·고정비·자재/경비와 네 범위·엄격 그룹/전파·미리보기/교환/보고·통화/이력·조건부 schema62를 연결한다. 번호별 외부 기준선 슬롯은 잔여다. [검증](validation/xml-baseline-cost-2026-11-14/README.md). 최종 검증: 일반210/210·452.48초, 대용량 CTest180초 시간 초과/동일 실행 파일 직접1/1·227.84초(표준 시간 실패1건 유지), 집중 부분집합42/42·파서898개·형식535파일, 독립128사례/1408값·XML/XER32값·XLSX45행/PDF24쪽·schema62 실행 패키지를 확인했다.

2026-11-14 후속: [XPC-01~06 XML Project 변환](xml-project-conversion-functions.md)을 구현했다. ProjDateValue/ProjDateConv/ProjDurConv의 ISO/NA·고정 영문 날짜/주차·분/근무/경과/추정·월 프로필·정수 반올림과 네 범위/미리보기/교환/보고·조건부 schema61/전체 사본을 지원한다. [검증](validation/xml-project-conversions-2026-11-14/README.md). 최종 검증: 일반208/208·335.90초, 대용량 단독1/1·152.38초로209/209, 집중 부분집합40/40·파서894개·형식532파일, 독립 날짜2816표시·기간10240표시/재파싱·직접20식·XML/XER26값·XLSX76행/PDF20쪽·schema61 실행 패키지를 확인했다.

2026-11-14 후속: [XCV-01~06 XML 형 변환](xml-conversion-functions.md)의 CDec/CSng/CVar를 구현했다. 고정 소수6자리·정확한 binary32 최근접 짝수/고정점 변환·형식/기간 보존·범위/Null과 네 범위/미리보기/교환/보고·조건부 schema60/전체 사본을 지원한다. [검증](validation/xml-conversions-2026-11-14/README.md). 최종 검증: 일반206/206·396.59초, 대용량 단독1/1·147.23초로207/207, 집중 부분집합38/38·파서890개·형식529파일, 독립 유리수2058건·.NET2058건·직접26식·XML/XER22값·XLSX72행/PDF19쪽·schema60 실행 패키지를 확인했다.

2026-11-14 후속: [XST-01~06 XML 문자열 함수](xml-string-functions.md)를 구현했다. Replace/InStrRev/StrReverse의 BMP·ASCII/제어 인수·치환/검색/반전·함수별 Null 구분과 네 범위/미리보기/교환/보고·조건부 schema59/전체 사본을 지원한다. [검증](validation/xml-string-functions-2026-11-14/README.md). 최종 검증: 일반204/204·299.23초, 대용량 단독1/1·167.80초로205/205, 집중 부분집합36/36·파서886개·형식526파일, 독립 문자열3072건·VBScript3072건·직접32식·XML/XER24값·XLSX74행/PDF20쪽·schema59 실행 패키지를 확인했다.

2026-11-13 후속: [XMH-01~06 XML 추가 수학 함수](xml-math-functions.md)를 구현했다. Atn/Cos/Exp/Log/Sin/Tan의 라디안·자연로그·부동소수 근사/소수6자리·정의역/범위·네 범위/미리보기/교환/보고와 조건부 schema58/전체 사본을 지원한다. [검증](validation/xml-math-functions-2026-11-13/README.md). 최종 검증: 일반202/202·309.14초, 대용량 단독1/1·146.42초로203/203, 집중 부분집합34/34·파서882개·형식523파일, 80자리 독립 수치6189건(정확한 반올림 일치6177건/최대 차이0.000001)·XML/XER24값·XLSX72행/PDF19쪽·schema58 실행 패키지를 확인했다.

2026-11-13 후속: [XML 숫자 문자열 XNT-01~06](xml-number-text.md)을 구현했다. Str/Val/Hex/Oct의 부호 공백·점 소수/지수·숫자 접두부/형식 접미사 지원 부분·정확한 소수6자리·32비트 진수를 지원한다. 네 범위/요약/전파·미리보기/교환/보고와 조건부 schema57/전체 사본/복구를 연결한다. [검증](validation/xml-number-text-2026-11-13/README.md). 최종 검증: 일반200/200·291.99초, 대용량 단독1/1·167.44초로201/201, 집중 부분집합32/32·파서878개·형식520파일, 독립 변환1024/고정점왕복1024/접두부1024·.NET4096·XML/XER22값·XLSX72행/PDF19쪽·schema57 실행 패키지를 확인했다.

2026-11-13 후속: [XML 시각 함수 XTM-01~06](xml-time-functions.md)을 구현했다. TimeSerial의 반올림/16비트/상대 넘침/음수 OLE와 TimeValue의 날짜 제거·명시24시간/영문 AM·PM/ISO·마이크로초를 지원한다. 기준일1899-12-30과 네 범위/요약/전파·미리보기/교환/보고·조건부 schema56/전체 사본/복구를 연결한다. [검증](validation/xml-time-functions-2026-11-13/README.md). 최종 검증: 일반198/198·300.17초, 대용량 단독1/1·159.40초로199/199, 집중 부분집합30/30·파서874개·형식517파일, 독립 생성1024/추출3072·VBScript4111·XML/XER22값·XLSX74행/PDF19쪽·schema56 실행 패키지를 확인했다.

2026-11-13 후속: [XML 날짜 함수 확장 XDT-01~06](xml-date-functions.md)을 구현했다. DatePart/Weekday, DateAdd/DateDiff의10간격·월말/윤년·정수 마이크로초·달력 경계/온전한 주·고정 주 규칙을 지원한다. 네 범위/요약/전파·미리보기/교환/보고와 조건부 schema55·레거시3인수 읽기·현재/전체 사본/복구를 연결한다. [검증](validation/xml-date-functions-2026-11-13/README.md). 최종 검증: 일반196/196·285.32초, 대용량 단독1/1·144.34초로197/197, 집중 부분집합28/28·파서870개·형식516파일, 독립 DatePart4608/DateAdd5120/DateDiff8192·.NET17920·XML/XER22값·XLSX70행/PDF19쪽·schema55 실행 패키지를 확인했다.

2026-11-13 후속: [XML 계산식 Format·StrConv XFS-01~06](xml-format-strconv.md)을 구현했다. 정확한 십진 표시·구간/Null·Gregorian 날짜/주 번호·Unicode16.0 대소문자/폭/가나와 명시 LCID1033/1041/1042를 지원한다. Format 기본은 고정 en-US, PPMFormat은 명시 로캘 확장이다. 네 범위/미리보기/교환/보고와 조건부 schema54/전체 사본/복구를 연결한다. 전체 VBA·호스트 지역 설정·코드페이지64/128과 실제 제품 왕복은 잔여다. [검증](validation/xml-format-strconv-2026-11-13/README.md). 최종 검증: 일반194/194·295.05초, 대용량 단독1/1·147.78초로195/195, 집중 부분집합26/26·파서866개·형식513파일, 독립 숫자2560/날짜1344/Unicode31158·XML/XER12칸·Windows25건과 NLS 차이1건·XLSX/PDF·schema54 실행 패키지를 확인했다.

2026-11-13 후속: [XML 계산식 시간대 변환 XTZ-01~06](xml-formula-timezones.md)을 구현했다. PPMTimeZone/Text/Offset·PPMParseUtc의 네 확장 함수로 명시 고정 오프셋과 버전 포함 IANA2026f·597이름을 지원한다. DST 누락/중복·음수/30분 전환·건너뛴 날짜·마이크로초·오프셋 문자열/UTC 왕복과 네 범위/요약/전파·typed 미리보기/교환/보고·조건부 schema53/전체 사본/복구를 연결한다. 원본 일정/실제는 자동 변환하지 않는다. [검증](validation/xml-timezone-conversion-2026-11-13/README.md). 최종 검증: 일반192/192·267.51초, 대용량 단독1/1·139.03초로193/193, 집중24/24·파서862개·형식510파일, 고정 TZif 전환92079/월별938484·XML36칸·XER34값·XLSX/PDF와 Windows schema53 실행 패키지/자료 라이선스를 확인했다.

2026-11-13 후속: [XML 계산식 추가 함수 XFN-01~06](xml-additional-functions.md)을 구현했다. 선택·문자열 검색/비교·정리/반복·ASCII 문자·형식 변환·날짜 추출·정수 제곱근13개를 지원한다. 네 범위·typed 결과·혼합/요약/전파·예시 삽입/비동기 미리보기·XML/XER·XLSX/PDF와 활성 조건부 schema52·전체 사본/복구를 연결한다. 과거 비활성 식은 기존 최소 버전에서 원본대로 읽고 자동 활성화하지 않는다. [검증](validation/xml-additional-functions-2026-11-13/README.md). 최종 검증: 일반 회귀190/190·388.55초, 대용량 단독 CTest180초 시간 초과 후 코드/실행 파일 변경 없이300초 한도 직접 재검증1/1·164.13초로191개 기능 확인(표준 시간 제한 실패1건 유지), 집중22/22, 파서850개·형식505파일, 독립512제곱근/22스칼라·XML53칸/정의21개·XER49값·XLSX48행/PDF16쪽과 Windows schema52 패키지 읽기를 통과했다.

2026-11-13 후속: [다일 실적 비례 배분 XPR-01~06](xml-multiday-proportional-actuals.md)을 구현했다. 명시 구간 전체 총량의 확인·경과분/달력 교집합 가중분·정수 최대 나머지법·0가중일 생략과 기존 값/누계/마감 검증을 연결한다. 미리보기 재생·원자 batch·동일 출처 재시도·후속 정정/척도별 추정 기원·검토 기록/Usage/감사/표준 XML 영수증을 지원한다. 기존 schema11·상한51을 유지한다. [검증](validation/xml-multiday-proportional-2026-11-13/README.md). 최종 검증: 전체188/188·296.93초와 대용량 교환 단독1/1·160.69초로189/189, 집중14/14, 파서838개·형식503파일, 독립 두 기준/16사례·총326u/배분5702센트·척도별 정정 기원·XLSX/PDF와 Windows schema11 패키지 읽기를 통과했다.

2026-11-13 후속: [공수 기반 작업 기간 병합 XWP-01~06](xml-work-driven-progress.md)을 구현했다. XML RemainingWork의 독립 오류/정확한 수량 검토·공수 기준 대상의 명시 잔여·현재 계획의 계산 기간 스냅샷과 batch 원장/예측을 연결한다. 기존 계획/실제 원장·날짜별 목표·정정/미래/중복·마감/취소·저장/복구를 보존하고 새 영속 형식 없이 기존 곡선 schema24·상한51을 사용한다. [검증](validation/xml-work-driven-progress-2026-11-13/README.md). 최종 검증: 전체1차186/187·411.81초(기존 대용량 교환 시간초과1)와 동일 코드 단독재검증1/1·159.95초로187개 확인, 집중12/12, 파서832개·형식495파일, 독립10사례·자원별569분·수신잔여123분/예측37분/공수3501u·원본실제123u·XLSX/PDF와 Windows schema24 패키지 읽기를 통과했다.

2026-11-13 후속: [표준 실적 XML 내보내기 XAE-01~06](xml-standard-actual-export.md)를 구현했다. 현재 상태일의 최신 관측·0/미보고·작업 진척/누계·배정/자원 보고 합계와 Type2/6 일별 버킷을 별도 writer 모드로 연결한다. 원래 계획/전체 이력·schema11/상한51·기본 계획 내보내기를 유지하고 전체 입력 해시/재생 대조·원자적 게시·취소/변경 검사를 제공한다. [검증](validation/xml-standard-actual-export-2026-11-13/README.md). 최종 검증: 전체185/185·298.87초, 집중10/10, 파서826개·형식493파일, 일별10값·공수26001u·배분4875/누계14000센트·독립 XML/native/MPXJ 및 Windows schema11 패키지 읽기를 통과했다.

2026-11-12 후속: [XML 일별 실적 여러 구간 XAF-01~05](xml-daily-actual-fragments.md)을 구현했다. source 배정·날짜·종류별 겹침 없는 범위 인덱스, 반열린 경계·정확한 정수 합계/한도·알려진 일자의 전체 오류 처리·검토 구간 수를 연결한다. 기존 native batch·schema11·보고서/복구와 작업/일별 XML 채택을 유지한다. 최종 [검증](validation/xml-daily-actual-fragments-2026-11-12/README.md): 전체183/183·272.33초, 집중8/8, 파서820개·형식489파일, 원본12구간/4종류별 그룹·정수 공수25501u·배분4775센트·독립 XML/native/XLSX/PDF와 Windows schema11 실행 패키지 읽기를 통과했다.

2026-11-12 후속: [XML 배정·일별 실제 공수/원가 XAP-01~06](xml-period-actual-adoption.md)을 추가했다. Type2/6·일별 명시 값과 단위/통화 후보, native 배정 연결·기존 값 보존·누계 AC 대사와 출처별 batch를 한 revision으로 반영한다. `PeriodActualBatchEdit`·기존 원장/잠금·Usage/보고서·schema11 저장/복구·ID/통화 이관을 연결한다. 미지원 구간은 날짜별 값으로 추정하지 않는다. 최종 [검증](validation/xml-period-actual-adoption-2026-11-12/README.md): 전체181/181·254.38초, 집중6/6, 파서814개·형식487파일, 정수 공수25501u·배분4775센트·누계14000센트·독립 XML/native/XLSX/PDF와 Windows schema11 실행 패키지 읽기를 통과했다.

2026-11-12 후속: [XML 진척 기존 문서 병합 XPM-01~06](xml-progress-merge.md)을 추가했다. `prepareXmlProgressMerge`의 원본 재검증·수동 연결·중복 대사와 `ProgressMergeEdit`/`Document::mergeProgress`의 단일 revision 원장 batch를 연결한다. UI의 현재/수신 비교·취소/변경 검사, native 저장/복구·ID 이관·감사 보고를 `xml_progress_merge_contract`/`xml_progress_merge_ui`와 독립 XML/JSON/XLSX/PDF 검사기로 검증한다. 기존 사본 채택과 지원 상한51은 유지한다. 최종 [검증](validation/xml-progress-merge-2026-11-12/README.md): 전체179/179·271.78초, 파서808개·형식482파일, 원장1→5→10건·독립 XML/JSON/XLSX/PDF와 Windows UI·schema48 실행 패키지 읽기를 통과했다.

2026-11-12 후속: [XPA-01~06 XML 작업 진척 채택](xml-progress-adoption.md)을 기존 새 사본 가져오기 흐름에 추가했다. 기본 미채택·선택 해제, UID→새 작업 연결·명시 상태일/작성자/사유·전체 원본 재검증·추가 전용 진척과 현재 선택/정정 보고서를 연결한다. 기존 schema9/48 등 최소 writer·복구/전체 이관 사본을 재사용하고 새 영속 구조를 추가하지 않는다. [검증 기록](validation/xml-progress-adoption-2026-11-12/README.md). 최종 [검증](validation/xml-progress-adoption-2026-11-12/README.md): 전체177/177·259.24초, 파서808개·형식481파일, 원장4건/48항목·수식/보고서36칸·정정5건·MPXJ와 Windows UI·기존 schema48 실행 패키지 읽기를 통과했다.

2026-11-12 후속: [XMLE-01~05 Early/Late 참조](xml-early-late-references.md)를 구현했다. 계획 배치·예측 잔여 재개/완료와 완료 제외, 검증된 논리/자원 순서 후진·미산정/오류의 격리, 두 계산 시계·이정표 경계, 그룹 요약·schema51/전체 사본·worker/출력을 `xml_early_late_contract`/`xml_early_late_ui`와 독립 분 단위 열거로 검사한다. [검증 기록](validation/xml-early-late-references-2026-11-12/README.md). 최종 [검증](validation/xml-early-late-references-2026-11-12/README.md): 전체175/175·259.48초, 파서800개·형식471파일, 독립 계획 XML60칸/XER48값·예측 보고서60칸·MPXJ와 Windows UI·실행 패키지 schema51 읽기를 통과했다.

2026-11-12 후속: [XMLB-01~05 최초 기준선 참조](xml-baseline-references.md)를 구현했다. 최초 native v1의 Start/Finish·실제 동결 기간·배정 공수와 네 범위/엄격한 그룹 요약·미설정/오류·schema50/전체 전후 사본·worker 미리보기/출력을 `xml_baseline_contract`/`xml_baseline_ui`와 독립 분 단위 검사기로 검증한다. [검증 기록](validation/xml-baseline-references-2026-11-12/README.md). 다음 순서는 Early/Late이며 외부 번호별 슬롯/Cost·제품 왕복과 다른 GAP 잔여는 유지한다. 최종 [검증](validation/xml-baseline-references-2026-11-12/README.md): 전체1차171/173·306.03초와 코드 변경 없는 제한 밖 서버 재검증2/2·47.70초로173개를 확인했다. 파서788개·형식467파일, 독립 XML/XER·XLSX/PDF·MPXJ와 Windows UI·실행 패키지 schema50 읽기를 통과했다.

2026-11-12 후속: [XMLR-01~05 잔여 기간·공수 참조](xml-remaining-references.md)를 추가했다. 상태일의 유효한 예측·공통 Usage 실행 구간과 작업 달력, 곡선/공수 역산/날짜 목표·선택 진척/잔여 평준화·schema49·편집/보고서/교환을 `xml_remaining_contract`/`xml_remaining_ui`와 독립 분 단위 검사기로 확인한다. 중단이 있는 곡선의 XML 기간 투영에서 중단을 생략한 달력 기준 전체 시간대 창을 보존하도록 보정했다.

XMLR 최종 [검증](validation/xml-remaining-references-2026-11-12/README.md): 전체171/171·280.92초, 파서774개·형식463파일, 독립 XML64칸/XER52값/보고서64칸·MPXJ strict reader와 Windows UI·291파일 실행 패키지의 schema49 파일 읽기를 통과했다. 다음 계산식 후보는 Baseline → Early/Late다.

2026-11-12 후속: [XML 실제 기간·보고 공수 참조](xml-actual-quantities.md)의 XMLQ-01~05를 추가했다. `xml_quantity_contract`/`xml_quantity_ui`로 상태일/정정·범위별 보고 공수·미보고/0·계획 계산 독립성·schema48/동결/복구와 보고서/교환을 검사한다. [검증 기록](validation/xml-actual-quantities-2026-11-12/README.md).

최종 전체169/169·254.72초, 파서762개·형식461파일, 독립 XML50칸/XER30값/보고서50칸·MPXJ strict reader·Windows800×700과291파일 실행 패키지의 독립 schema48 파일 읽기를 통과했다. 다음 계산식 후보는 Remaining → Baseline/Early/Late다.

2026-11-11 후속: [XML 실적 일정 참조](xml-actual-references.md)의 상태일 선택·정정/미설정·요약/배정·계획 계산 독립성·schema47과 UI/교환/원장 보존을 추가했다. [검증 기록](validation/xml-actual-references-2026-11-11/README.md).

2026-11-11 후속: [XML 근무 달력 함수](xml-calendar-functions.md)의 세 함수·초/소수 분·기본/명시 달력·프로젝트 달력 보존·schema46과 독립 대조를 추가했다. [검증 기록](validation/xml-calendar-functions-2026-11-11/README.md).

2026-11-11 후속: [계산된 일정 참조](xml-schedule-references.md)를 추가했다. XML 수식의 Start/Finish·범위별 참조, 활성 계획/예측과 XML 계획 기준, 요약 날짜·worker 미리보기·캐시/오래된 결과 격리·schema45를 검사한다. [검증 기록](validation/xml-schedule-references-2026-11-11/README.md).

2026-11-11 후속: [XML 외부 계산식](xml-external-formulas.md)의 bounded 실행기, 네 범위 형식별 결과·안정 바인딩·native 식/roll-up/down 연계·schema44를 구현했다. `xml_formula_contract`/`xml_formula_ui`, 독립 Decimal400·XML/XER·XLSX/PDF와 Windows 화면을 검사한다. [전체161/161·최종집중21/21·파서714개·형식448파일·독립 판독/Windows UI 검증](validation/xml-formulas-2026-11-11/README.md)을 통과했다.

2026-11-11 후속: [XML 요약 roll-up](xml-roll-up.md)의 8개 방식·형식별 정밀도/누락, WBS/루트와 작업·자원 그룹, 설정/미리보기·보고서·schema43 보존을 구현했다. 검사는 `xml_roll_up_contract`/`xml_roll_up_ui`와 독립 Decimal/XML/XLSX/PDF 판독을 따른다. [전체159/159·파서698개·형식441파일·독립 판독/Windows UI 검증](validation/xml-roll-up-2026-11-11/README.md)을 통과했다.

2026-11-11 후속: [XML 배정 roll-down](xml-roll-down.md)을 구현했다. `xml_roll_down_contract`/`xml_roll_down_ui` 및 독립 XML/XER/XLSX/PDF 판독으로 자동 연결·직접 값 우선·모든 스칼라/목록·schema42·통화/ID 이관과 저장/복구를 검사했다. [전체157/157·파서678개·형식435파일·독립 판독/Windows UI](validation/xml-roll-down-2026-11-11/README.md)를 통과했다.

2026-11-11 후속: [XML 코드 마스크·자동 생성](xml-code-masks.md)을 구현했다. `xml_code_mask_contract`/`xml_code_mask_ui`와 독립 XML·MPXJ·XLSX/PDF로 네 범위·공유 GUID·WBS 생성·schema41/전체 사본·원자 편집을 검증했다. [전체155/155·파서650개·형식429파일·독립 판독/Windows UI](validation/xml-code-masks-2026-11-11/README.md)를 통과했다.

2026-11-10 후속: [XML Start·Finish·Date 시각](xml-date-time-fields.md)을 구현했다. `xml_date_time_contract`/`xml_date_time_ui`와 독립 XML/날짜 산술·MPXJ/XLSX/PDF로 네 범위·일시·목록/GUID·schema40와 편집/복구를 검증했다. [전체153/153·파서630개·형식423파일·독립 판독/Windows UI](validation/xml-date-time-fields-2026-11-10/README.md)를 통과했다. 소수 초 원본의 MPXJ 판독 제한과 별도 정초 사본 검사를 구분한다.

2026-11-10 후속: [XML Flag·Cost·Duration](xml-additional-field-types.md)을 추가했다. `xml_field_types_contract`/`xml_field_types_ui`와 독립 XML/Decimal·MPXJ/XLSX/PDF로 형식·단위·네 범위·금액 전환과 저장/복구를 검증한다. [전체151/151 재실행·614개 파서 seed·421파일 형식 검사와 독립 판독/Windows UI](validation/xml-field-types-2026-11-10/README.md)를 통과했다.

2026-11-10 후속: [XML 값 목록·GUID 참조](xml-lookup-references.md)를 구현했다. `xml_lookup_contract`/`xml_lookup_ui`와 `scripts/verify-xml-lookups.py`로 단일/다중·계층·ID/GUID·네 범위와 저장/복구·편집·보고서 투영을 검증한다. 전체149/149·598개 파서 seed·419파일 형식 검사와 독립 XML/MPXJ/XLSX/PDF·Windows UI를 [통과했다](validation/xml-lookup-references-2026-11-10/README.md).

2026-11-10 [기업·배정 UDF/XML 프로젝트 필드](enterprise-assignment-udf.md)를 구현했다. `enterprise_udf_contract`/`enterprise_udf_ui`와 전체147개 회귀, 582개 파서 seed·418파일 형식 검사, 독립 XML/TSV·MPXJ/XLSX/PDF와 Windows 실제 UI를 [검증](validation/enterprise-assignment-udf-2026-11-10/README.md)했다. MPXJ16.10.0의 XML 기업 16진 값 판독 제한과 실제 제품 미실행을 구분한다.

2026-11-09 후속 [MPP 수동 계획 곡선 읽기](mpp-manual-curves.md)는 원본 정규 시간대 자료·총공수/0구간을 native 배정 구간에 연결한다. 실제/초과근무 제외와 분 경계·기간 창 투영을 명시하고 protocol2 bundle·기존 schema36·저장/복구/교환을 재사용한다. [전체 회귀·독립 분 단위 대조](validation/mpp-manual-curves-2026-11-09/README.md)를 따른다.

2026-11-09 [자원 생산성·외부 고유 곡선 교환](resource-productivity-curves.md)을 구현했다. 명시 물량→정수 공수·작업 유형별 유지값, 원본21값/시간대별 계획 투영·손실 진단, 취소 가능한 검산과 확인/undo, 조건부 schema36·이관/채택 사본/복구·보고서를 연결한다. [전체 회귀·독립 검산](validation/resource-productivity-curves-2026-11-09/README.md)을 따른다.

2026-11-08 [FixedWork/FixedUnits 날짜 고정 잔여 목표](dated-effort-targets.md)는 잔여 총공수에서 날짜 목표를 예약하고 미입력 날짜의 기존 곡선으로 나머지를 채워 완료를 역산한다. 기간 기준 FixedUnits는 잔여 기간을 유지한다. 같은 작업의 모든 자원 목표·정수 마지막 분·달력/중단·비단조 제약 교집합·논리/자원 여유와 증인을 검산하며 원래 계획/관측 원장을 유지한다. 새 의미는 schema35/`jobs-dated-effort-1.0`/`serial-dated-effort-v1`이며 기존1~34 경로를 유지한다. [전체 회귀·독립 분 단위/전수 여유·출력/Windows 검증](validation/dated-effort-2026-11-08/README.md)을 따른다.

2026-11-08 [프로젝트 전체 통화 전환](project-currency-conversion.md)은 정수 최소 단위의 명시 환율/정확·반올림 정책과 현재 단가/직접비·관측 원장·기준선/시나리오·기간 마감/외부 EVM·XER 재무 투영을 함께 환산한다. schema34에 전후 전체 원본을 보존하며 ID 이관과 교차 실행·저장/복구·새 사본을 지원한다. XER raw incoming과 과거 일정/ID 이관 원본은 그대로 유지하고 후속 원본 환산 단계를 별도 기록한다. worker 미리보기·확인·읽기 전용 이력 조회와 보고서 환산 근거를 제공한다. [전체 회귀·독립 수치/전체 필드·출력·Windows 검증](validation/project-currency-2026-11-08/README.md)을 따른다.

2026-11-08 [MPP 읽기](mpp-import.md)는 MPXJ16.10.0/Java21 별도 프로세스·기존 MSPDI 계획 검증과 실제 MPP8/9/12/14 공개 표본을 연결한다. 원본 바이트·진단/연결표·명시 사본 통화와 실적/원가/기준선 비생성, worker 취소/stale·새 폴더 게시·native 새 사본 열기 및 오프라인 runtime/대응 소스 배포를 지원한다. 전체139/139(219.71초), 파서478개·형식390파일, 직접 객체128개 대조·Windows 기본/800×600과 독립 실행/패키징28개를 통과했다. [검증 기록](validation/mpp-import-2026-11-08/README.md)을 따른다.

2026-11-08 [관측 원장 ID 이관](ledger-id-migration.md)은 작업/자원 명시 연결·새 ID/미관측 대상 합치기, 원장 수치/출처 보존, 기준선·시나리오·마감/외부 EVM·XER 참조 이관과 schema33 전후 문서 재실행 검증을 추가한다. 전체137/137(172.66초), 파서478개·형식384파일, 독립16,239개 필드/MPXJ strict·Windows 기본/800×600을 통과했다. [검증 기록](validation/ledger-id-migration-2026-11-08/README.md)을 따른다.

2026-11-08 [새 XER 일정·WBS·달력 채택](xer-schedule-adoption.md)은 작업의 기존 ID 연결/명시 신규 추가, 독립 범위 채택, native 원장·기준선·기간 마감 보존과 schema32 전후 계획 재실행 검증을 추가한다. worker 미리보기는 작업 날짜/관계·WBS 계층·요일/근무 구간/휴일을 표시한다. 전체136/136(184.47초), 파서458개·형식376파일, 독립133개 검사/16개 날짜·MPXJ strict와 Windows 기본/800×600을 통과했다. [실행 근거](validation/xer-schedule-adoption-2026-11-08/README.md)를 따른다.

2026-11-08 [XER 통화·자원 종류 전환](xer-source-conversion.md)은 새 원본/이전 집계의 명시 환율·종류별 공수 환산과 원본/전환값 미리보기·저장 이력 조회를 추가한다. schema31에 원본·환산비/기준일/근거를 보존하고 재열기 때 전환·연결·병합을 재실행한다. 현재 계획·원장·단가는 바뀌지 않는다. `xer_source_conversion_contract`를 포함한 전체135/135(160.15초), 파서424개·형식366파일, 독립760개 환산 사례/844개 검사·MPXJ strict·Windows 기본/800×600을 통과했다. 독립 Fraction/Decimal oracle 및 [전체 검증 기록](validation/xer-source-conversion-2026-11-08/README.md)을 따른다.

2026-11-08 [사용자 정의 기간·기간 마감](custom-financial-periods.md)은 조건부 schema30의 불변 정의/마감/재개방 이력과 작업별 native 경계 스냅샷을 사용한다. 기간 지정 PV/EV·native 누계·날짜배분 대사를 구분하고, 당시 지식 revision을 고정해 과거 보고를 출력한다. 원장의 상태일/실제 날짜 잠금과 최신 기간부터 재개방, worker 취소/stale/권한·저장 상태 검증을 적용한다. `custom_financial_period_contract/ui` 및 독립 raw 원장/Decimal·XLSX/PDF reader로 검증한다. 최종 전체134/134(163.78초), 집중29/29(36.66초), 파서390개·형식362파일, 독립340개 수치와 화면 XLSX170개 수치·Windows UI/1만 작업·PDF 구조/렌더 및 기존 native/XER reader를 통과했다. [실행 증거](validation/custom-financial-periods-2026-11-08/README.md)를 따른다.

2026-11-08 [외부 XER EV/PV native 채택](external-xer-evm-adoption.md)은 domain의 원본/revision·명시 개시/마감 검증과 불변 채택/철회 이력, worker 제출, 조건부 schema29를 사용한다. native 원가/기간 EVM·일반 보고가 같은 채택 인덱스를 사용하며 AC·물리 진척·원본은 바꾸지 않는다. `external_xer_evm_adoption_contract/ui`와 전체 회귀, `scripts/verify-external-xer-evm.py`의 독립 TSV/Decimal·원본/본문/투영 SHA256·원장/기간 참조 및 실제 XLSX/PDF 판독으로 검증한다. 전체132/132(167.06초), 집중27/27(34.64초), 파서348 seeds·형식350파일, 독립2,106개 수치·Windows UI·기존 native/XER reader를 통과했다. [실행 증거](validation/external-xer-evm-2026-11-08/README.md)를 따른다.

2026-11-08 [native 기간 EVM](native-period-evm.md)은 `PeriodEvm` 보고/범위·기간 경계와 기존 `Costs`의 동결 예산/EV 측정법을 공유하는 일괄 경계 계산을 사용한다. 비용/진척/Steps 보고는 작업·상태일 인덱스로 조회하고 예산은 작업당 한 번 생성한다. `native_period_evm_contract/ui`와 기존 원가/보고/기간 실적·XER/전체 회귀로 검증한다. `scripts/verify-native-period-evm.py`는 독립 civil-minute/Decimal·원장 ID/상태일 oracle와 실제 XLSX/PDF를 판독한다. 저장 schema는 추가하지 않는다. 전체130/130(167.66초), 집중21/21(26.85초), 파서326 seeds·형식336파일, 독립810개 수치·Windows UI와 A3/A4 PDF 판독/렌더를 통과했다. [실행 증거](validation/native-period-evm-2026-11-08/README.md)를 따른다.

2026-11-08 [새 XER 버전·삭제 ID 재연결](xer-source-relink.md)은 조건부 schema28과 `xer_source_relink_contract`로 검증한다. 비동기 파일/프로젝트 선택, 새 원본·이전 집계의 명시 ID 연결, 관측 없는 항목의 안전한 제외와 기존 재무 병합 검토를 연결한다. 원본/전체 native 입력·원장/AC를 보존하며 당시 연결표와 원장을 재구성해 검사한다. 전체128/128(161.21초), 집중15/15(20.79초), 파서326 seeds·형식327파일, Windows UI와 독립 SHA256/TSV/MPXJ·기존 교환/공개7개 표본을 통과했다. [실행 증거](validation/xer-relink-2026-11-08/README.md)를 따른다.

2026-11-07 [XER 원본·현재 원장 자동 병합](xer-ledger-merge.md)은 조건부 schema27과 `xer_financial_merge_contract`로 검증한다. native 날짜/원가 기록을 재작성하지 않고 현재 AC·모든 최신 원장 ID를 연결한다. 겹친 미배분 기간과 정규/초과근무 누계는 명시 선택하며, 병합 당시 참조의 최신성·완전성과 native AC를 검사한다. `scripts/verify-xer-merge.py`와 [전체 회귀 기록](validation/xer-merge-2026-11-07/README.md)을 따른다.

2026-11-07 [XER 집계 편집·날짜별 배분](xer-aggregate-editing.md)은 조건부 schema26 정정 이력과 `xer_financial_edit_allocation_contract`로 검증한다. 기존 보존 원본과 이전 원장 행을 유지하고 작업 AC·배정 누계·기간 집계·정수 날짜 비중을 한 worker 제출로 대사한다. `scripts/verify-xer-allocation.py`가 Decimal 배분 oracle/native SHA256/TSV/MPXJ를 독립 판독하며 [전체 회귀 기록](validation/xer-allocation-2026-11-07/README.md)을 남긴다.

2026-11-07 XER 재무기간·누계 스냅샷은 조건부 schema25와 `xer_financial_snapshot_contract`로 검증한다. 주/월 구간·정규/초과근무·기간 미지정 공수·외부 EV/PV를 현재 원장과 별도 보존하고 내용 지문이 일치할 때만 재내보낸다. native/복구·독립 사본/undo·검색 가능한 가상 표·기존 전체 회귀와 `scripts/verify-xer-financials.py`의 독립 TSV/Decimal/SHA256/MPXJ를 사용한다. [계약](xer-financial-snapshots.md)·[검증 기록](validation/xer-financials-2026-11-07/README.md).

2026-11-06 XER 실적·원가 상세 교환은 `xer_actual_cost_contract`와 확장 `primavera_xer_ui`, `parser_seed_replay` 및 전체 회귀로 검증한다. `scripts/verify-xer-actual-costs.py`는 독립 TSV/Decimal·native SHA256·MPXJ16.10.0으로 상태일·관측 날짜·누계/배분 원가·공수와 다중 참조를 대조한다. [기능 계약](xer-actual-cost-exchange.md)·[검증 기록](validation/xer-actual-cost-2026-11-06/README.md).

최종 전체124/124(158.52초)·집중8/8·파서272 seeds·형식298파일, Windows 기본 UI와 신규/기존 교환의 독립 reader를 통과했다. 공개 generated 표본1개의 미래 실제 시각 거절을 원본 해시 유지와 함께 기대 판정에 기록했다. 실제 P6 재계산/재저장은 미실행이다.

2026-11-06 FixedWork/FixedUnits 곡선 역산은 `work_contour_contract/ui`, 공통 실행·정확 기간 인증·비단조 후보·schema24/복구와 전체 회귀로 검증한다. `scripts/verify-work-contour-inverse.py`는 독립 Python civil-minute80종·native SHA256·숫자 XLSX/PDF를 대조한다. [기능 계약](work-contour-inverse.md)·[실행 증거](validation/work-contour-inverse-2026-11-06/README.md).

2026-11-06 후속: 날짜 고정 잔여 수요의 자원 여유·증인과 XML/XER UDF 스칼라 매핑을 추가했다. `dated_remaining_contract`의 독립 전수 oracle과 `udf_mapping_contract`, 기존 XML/XER UI/전체 회귀·252 parser seeds로 확인한다. `scripts/verify-dated-float-udf.py`는 기존 xer-reader-verification venv의 MPXJ16.10.0/JPype1.6.0으로 검증한다. [계약·실행 증거](validation/dated-float-udf-2026-11-06/README.md).

2026-11-06 자원 그룹/필터·저장 보기, 고정 기간 날짜별 잔여 공수, 숫자 계산식 필드를 순차 추가했다. CTest `resource_view_contract/ui`, `dated_remaining_contract/ui`, `formula_field_contract/ui`와 schema21~23 파서·기존 전체 회귀로 검증한다. `scripts/verify-professional-fields.py`는 openpyxl/pypdf·native SHA256·독립 civil-minute 적분과 Decimal 400건을 대조한다. [계약과 최종 실행 증거](validation/professional-fields-2026-11-06/README.md).

2026-11-03 기간별 실제 입력: `period_actual_contract` / `period_actual_ui`는 누계 포함 배분·불변 정정·과거/미래 대사·정밀도·schema 11/복구·원자적 worker 제출·취소/session 교체를 검증한다. native writer는 원장 있으면 11, 분류만 있으면 10, 둘 다 없으면 9다. 독립 출력 검사는 `scripts/verify-period-actual-exports.py`다.

2026-11-03 [시간축 Usage](timephased-usage.md) 조회 증분은 `ppm_usage_tests`/`timephased_usage_contract`, `ppm_usage_ui_tests`/`timephased_usage_ui`로 검증한다. `scripts/verify-usage-exports.py`는 openpyxl/pypdf로 직접 생성한 일별 명세와 실제 UI 버튼이 생성한 주별 XLSX를 대조한다. 파생 조회만 추가하므로 새 저장 schema나 영속 실적 모델은 추가하지 않는다.

2026-10-26 사용자 요청에 따른 구현 착수. PRD-01(초안 입력 일부), PRD-02(WBS·표·간트 일부), PRD-03(기본 FS CPM), PRD-04/05(기준선·실적·편차 일부), PRD-08,
DESK-01/03/04/05 및 FILE-01/02/03/05/06/07/09의 초기 수직 흐름이다.
전체 PRD나 FILE-T01~09의 완료 선언은 아니다.

## 구성

- `ppm_domain`: 표준 C++20 프로젝트·작업·WBS·기준선·실적 원장·자원/배정·불변 시나리오·날짜·revision 검증 및 계층 탐색. Qt 의존 없음.
- `ppm_calculation`: 표준 C++20 FS0 CPM, 달력, retained remaining 예측, 기준선 준비/검증, 계획/예측 비교, 자원 수요/가용량 및 비분할 직렬 평준화. Qt 의존 없음.
- `ppm_application`: 문서 세션, 생성/열기/편집/저장/사본, 추상 저장 포트.
- `ppm_persistence`: Qt Core JSON, checksum, 잠금, 외부 변경 감지, 원자적 교체.
- `JsonRecoveryStore`: 사용자 로컬 복구 세션/세대, 완료·해시 검증, 프로세스 잠금, 원본 상태/변경 미리보기. `AutoSaveController`가 입력 스냅샷을 백그라운드에서 기록한다.
- `ppm_reporting`: Qt Gui 기반 숫자/텍스트 표시·공통 추이, 공개 OOXML XLSX와 페이지를 나누는 PDF 출력. 외부 런타임/Office 라이브러리 없음.
- `ppm_ui`: Qt Widgets WBS·표·간트, 기준선/상태일/실적 대화상자, 자원 등록/배정·비동기 부하/시나리오 A/B 비교, 변경 상세, 미저장 변경 확인.

기간 미정(null)과 마일스톤(0분)을 구분한다. 기간·FS 선행·휴일을 입력하면 F9로
기간 중심 논리 일정을 계산한다. F9는 기본적으로 논리 일정을 계산하며 명시적 평준화 채택이 있으면 기록된 정책으로 재생한다. 자원 메뉴에서 별도로 배정·일별 부하와 평준화 시나리오를 비교한다.
기본 달력은 월~금 09–12/13–18이며 날짜는 시간대 없는 ISO civil date다.
WBS는 별도 그룹 트리로 편집하며 작업을 그룹에 배치한다. 간트에 최신 계산 결과·마일스톤·FS 연결선을 표시한다.
추적 메뉴에서 기준선을 새 버전으로 저장하고 상태일·실제 시작/완료·실제 소요/잔여 근무분을 입력한다.
기준선은 불변 입력·달력·결과 스냅샷, 실적은 정정 사유를 가진 append-only 보고 원장이다.
현재 계획과 상태일 이후 잔여 예측을 나누어 비교하며, 간트에서 선택 기준선을 회색으로 표시한다.
공수 중심 일정은 아래 공수·자원 달력·분할 계약을 따른다. 왼쪽 끝 resize/관계 생성 드래그는 후속 범위다. 간트 날짜/기간 드래그, 작업 제약·마감, FS·SS·FF·SF/lag와 작업별 달력, 일반 입력 실행 취소/다시 실행과 EVM용 물리 진척은 별도 구현 계약을 따른다.
[현재 계산 정책·수용시험·입력 예제](calculation-native-v1.md)를 참고한다.
[WBS·표·간트 사용법과 검증 계약](wbs-gantt.md)을 함께 따른다.
[기준선·실적·변경 비교 계약](baseline-progress.md)에 재현 예제와 예측 범위를 기록한다.
[자원·평준화 계약](resources-leveling.md)은 정률 배정·일별 최대 부하·별도 시나리오·재계산/출처와 후속 범위를 정의한다.

## 빌드와 실행

개발 기준: CMake 3.24+, C++20 컴파일러, Qt **6.8.3 Core/Widgets/Concurrent/PrintSupport/Network**.
Qt 패키지와 컴파일러 ABI를 맞춘다. Qt 6.8 이상을 CMake에서 허용하되 CI 기준 버전은 고정한다.

```powershell
cmake -S . -B build -DCMAKE_PREFIX_PATH=C:/Qt/6.8.3/msvc2022_64
cmake --build build --config Release --parallel
ctest --test-dir build -C Release --output-on-failure
& ./build/Release/PPM.exe
```

MinGW는 해당 Qt의 `bin`과 MinGW의 `bin`을 PATH에 추가한 뒤 Ninja를 사용한다.
이 작업 폴더에는 `.deps/Qt`에 개발 도구를 설치했으며 `./scripts/dev.ps1`로 빌드·검사·실행한다.
`./scripts/dev.ps1 -TestOnly`는 실행 창을 열지 않고 검사한다. 이 로컬 스크립트는 Python 3.14의
사용자 Scripts 경로를 사용한다. 다른 환경에서는 아래 일반 명령을 사용한다.

```powershell
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH=C:/Qt/6.8.3/mingw_64
cmake --build build --parallel
ctest --test-dir build --output-on-failure
& ./build/PPM.exe
```

macOS:

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH="$HOME/Qt/6.8.3/macos"
cmake --build build --parallel
ctest --test-dir build --output-on-failure
open build/PPM.app
```

개발 실행에는 Qt DLL/라이브러리 경로가 필요하다. Windows 배포는 [Microsoft Store MSIX](msix-store.md)만 사용하며 EXE/NSIS 배포는 폐기했다. `python scripts/package-msix.py`의 개발 MSIX는 `build/msix-development`에 생성되는 CI 검증 전용이다. `--mode store --identity <실제 identity JSON>`의 업로드 준비 파일은 `build/msix-store-upload`에 생성한다. 무서명 준비 파일을 사용자에게 배포하지 않는다. macOS는 별도 App Store 서명·업로드 절차를 따른다.
GitHub Actions는 Windows/macOS 빌드와 계산·파일·화면 테스트를 수행한다.
macOS는 `macos-15`와 Xcode 16.4를 고정한다. 최신 SDK에서 Qt 6.8.3의 AGL 링크 실패를 확인했다.

## `.ppm` 파일 형식과 호환성

UTF-8 JSON 한 파일에 `format`, `schemaVersion`, `payload`, `sha256`을 보존한다. 새로 저장하는 파일의 `format`은 `PPM`이며 이전 `JOBS` 파일도 읽는다. 현재 데스크톱은 schema 1~84를 읽으며 [코드의 읽기 상한](../src/domain/NativeSchema.h)을 따른다. 저장할 때는 schema 9부터 시작해 프로젝트 데이터에 필요한 최소 버전을 사용한다.
payload에는 documentId, derivedFrom, revision, name, startDate, calendar, tasks, holidays,
calculationProfile, wbsNodes, resources(rates·calendarId 포함), assignments, currency, costProfile, taskCosts, calendars, statusAt, baselines, progress, scenarios, costEntries가 들어간다. 각 작업은 UUID·이름·정수 근무분 또는 null·선행 ID 목록·wbsId를 갖는다. 계산 정책에 따라 관계 종류/지연(dependencyRules)·작업 달력(calendarId), 제약/마감, 작업 유형·입력 공수·공수 기준 여부·분할 중단을 함께 저장한다.
WBS 노드는 ID·이름·parentId를 가지며 빈 부모/소속 ID는 프로젝트 루트다. 순환·누락 부모·누락 소속을 거절한다.
schema 10은 선택적 `customFields`/`codeTypes` 사전, 작업 `attributes`, 현재 프로젝트 `savedTaskViews`를 추가한다. 새 배열/객체의 형식·필드·참조·개수·계층을 엄격히 검사한다. [분류 계약](task-classification.md)을 따르며 schema 9에 새 데이터를 추가해 저장하면 10이 되어 이전 앱에서는 미지원 버전으로 거절된다.
현재 계산 결과는 세션 cache이며 재열기 후 F9로 재계산한다. 기준선의 동결 결과는 파일에 보존한다.
기준선 입력과 결과는 열기/저장 시 고정 엔진으로 재검산한다. 실적은 source document/revision·상태일·UTC 기록시각·보고자·사유·이전 보고 ID를 보존한다.
checksum은 Qt의 compact JSON payload에 대한 SHA-256이며
보안 서명이 아닌 우발적 손상 검사다. 현재 최대 64 MiB이며 첨부/외부 링크는 포함하지 않는다. Project XML/XER 교환은 별도 변환·진단 패키지로 제공한다.
checksum과 구조·필드·날짜·ID 중복·revision을 검사한다. 미지원 schema/필드는 무음 삭제하지 않고 거절한다.

첫 저장은 새 프로젝트 ID를 유지한다. 저장된 문서의 다른 이름 저장은 새 documentId와
derivedFrom을 만들고 작업 ID를 유지한다. 기존 대상 파일 덮어쓰기는 초기 버전에서 거절한다.
현재 파일에 저장할 때는 SHA-256 fingerprint가 열린 시점과 같은지 쓰기 전·교체 직전에 확인한다.
실패하면 dirty 상태와 이전 문서 세션을 유지한다.

QSaveFile로 임시 파일을 쓰고 flush 후 commit한다. 직접 덮어쓰기 fallback은 비활성화한다.
QLockFile sidecar는 전달 파일이 아니며 단일 writer를 위한 협조적 잠금이다.
잠금 실패 시 읽기 전용 열기와 다른 이름 저장을 제공한다.
외부 비협조 writer의 검사 직후 변경, 네트워크/동기화 폴더 원자성, 정전 내구성은 보장하지 않는다.
schema 1~8은 ID·revision·기존 입력과 계산 정책을 유지하여 읽고 누락된 새 필드에 null/빈 목록/기본값을 적용한다.
schema 1~8 원본 덮어쓰기는 거절한다. 편집 후 저장하면 다른 이름 저장으로 데이터에 맞는 schema 9 이상 사본을 만들며
원본 bytes를 보존한다. 일반적인 다단계 이관·별도 백업 순환 정책은 아직 없다. 자동복구 체크포인트는 원본과 분리한 별도 레코드로 제공한다.
미지원 버전은 원본을 수정하지 않는다.

## 검증 범위

`ppm_file_tests`는 실제 임시 파일로 생성/편집/revision/재열기, Unicode 경로·데이터,
사본의 ID/계보·원본 bytes 보존, 중복 writer 잠금, 읽기 전용 사본, 외부 변경 거절,
JSON 손상/checksum/신버전/알 수 없는 필드/중복 ID, 열기·저장 실패 시 세션 보존,
단일 파일 복사, 계산 입력 왕복, revision/문서 ID가 다른 결과의 STALE 처리,
schema 1/2→5 사본 이관·WBS 계층/작업 소속 왕복·손상 계층 거절을 검사한다. 이는 FILE-T01/T02/T06/T08/T09 일부에 해당한다.

GUI 수동 점검: 새로 만들기→작업 목록 입력→저장→작업명 편집→열기/종료 시
저장·버리기·취소→다른 이름 저장→원본 재열기. 두 앱으로 같은 파일 열기와 읽기 전용 사본도 확인한다.
실제 OS 간 전달, 강제종료·디스크 부족·장치 제거, 접근성/IME/대용량 성능 시험은 미완료다.

`ppm_ui_tests`는 offscreen Qt Widgets 환경에서 새 프로젝트 대화상자·작업 목록 입력·표 편집·
저장 대화상자·종료 취소·종료 시 저장, 기간·선행·휴일 입력, 비동기 계산·계산 중 편집,
누락/순환/오래된 계산의 날짜 숨김과 재계산을 자동 검사한다. 네이티브 파일 대화상자와 실제 데스크톱
화면의 수동 검증을 대신하지 않는다.

`ppm_wbs_tests`는 F11 합계 변경·ID/그래프/날짜 보존, 중첩 그룹·이동·빈 삭제,
미정 기간·오래된 집계·부모 순환/누락·원자적 편집 거절·읽기 전용·깊이 2천 계층을 검사한다.
`ppm_wbs_gantt_ui_tests`는 필터와 프로젝트 행 번호, 필터된 편집, 작업/하위 WBS 이동,
추가/이름 변경/삭제, 간트 막대·마일스톤·FS 링크·상호 선택·배율·스크롤·오래된 막대 숨김을 검사한다.

`ppm_tracking_tests`는 F09의 +8h·기준선 불변/버전·계획/예측 분리, F08 잔여 논리, 완료 실제 고정,
상태일 조회·과거일 정정·잘못된 보고 거절·미보고/미정·읽기 전용을 검사한다.
`ppm_tracking_file_tests`는 기준선/실적 원장 왕복·사본의 원본 계보·달력 불변·기준선 재계산 무결성·잘못된 원장·schema 3→5 사본 저장을 검사한다.
`ppm_tracking_ui_tests`는 기준선/상태일/실적/비교 대화상자, +8h 표시·미보고 coverage·회색 기준선 선택,
모순 보고 오류·정정 이력·새 기준선 버전·저장/재열기를 검사한다.

## 구현 이력과 당시 실행 증거 · 2026-10-26 이후

아래 schema 번호와 테스트 개수는 각 증분 당시의 기록이다. 현재 파일 계약은 위의 [파일 형식과 호환성](#ppm-파일-형식과-호환성)과 기능별 계약을 따른다.

Windows x64, Qt 6.8.3, MinGW GCC 13.1.0, CMake 4.4.4, Ninja에서
첫 파일 구현은 `scripts/dev.ps1 -TestOnly`로 Release 빌드 및 2/2 테스트에 통과했다.
기본 계산 추가 후 `schedule_contract`, `file_lifecycle`, `ui_lifecycle` 3/3에 통과했다.
WBS·간트 추가 후 `wbs_contract`, `schedule_contract`, `file_lifecycle`, `ui_lifecycle`, `wbs_gantt_ui` 5/5에 통과했다.
WBS·간트 화면 테스트도 Windows 네이티브 플랫폼에서 통과했고 생성한 화면에서 트리·표·연결선·마일스톤을 확인했다.
기준선·실적·비교 추가 후 `tracking_contract`, `tracking_file`, `wbs_contract`, `schedule_contract`,
`file_lifecycle`, `ui_lifecycle`, `wbs_gantt_ui`, `tracking_ui` 8/8에 통과했다.
추적 화면 테스트를 Windows 네이티브 플랫폼에서도 실행해 통과했으며, 생성한 비교 화면에서
기준선/현재 계획/예측 +8h·보고 범위·기간 진척·변경 상세가 읽히는지 확인했다.
추가로 같은 화면 테스트를 Windows 네이티브 플랫폼(`-platform windows`)에서 실행하여 통과했고,
앱이 생성한 화면 이미지에서 한글·날짜·진단 표시를 확인했다. offscreen 테스트 이미지는
Windows의 폰트 로딩 차이로 글리프가 사각형으로 보이므로 시각 검토에 사용하지 않았다.
macOS 및 MSVC 검증은 GitHub Actions에서 별도 추적한다.

자원 증분은 `resource_contract_file`, `resource_ui`를 포함한 10개 테스트로 확장했다.
자원/배정·날짜 예외·불변 시나리오/기준선·schema 4→5 이관 및 분 단위 독립 수요 검산을 포함한다.

이번 증분에서 로컬 Release 전체 10/10 및 Windows 네이티브 자원 화면 테스트를 통과했다.
등록·A/B 일정 비교·원본 과부하·주 화면 이미지를 확인하고 다크 테마의 경고 행 글자 대비를 보정했다.

원가/EVM 증분은 유효일 단가·작업 고정비/성과 측정법·원가 보고 원장 및 비동기 분석/추이를 추가했다.
정의·통화/금액 한도·반올림·기준선 코호트·수용시험은 [원가·EVM 계약](costs-evm.md)을 따른다.
`cost_contract_file`, `cost_ui`를 포함한 전체 12개 테스트로 확장하며 F10·CPI 합계 비율·AC 불변·schema 5→6 이관을 검사한다.

원가/EVM 증분의 로컬 Release 전체 12/12와 Windows 네이티브 원가 화면 테스트를 통과했다.
단가·F10 EVM 표·PV/EV/AC 추이의 한글/금액 표시와 기존 자원 화면의 단가 보존을 확인했다.

보고서 증분은 `reports_export`, `reports_ui`를 더해 CTest 14개로 확장했다. `ppm_calculation`의 표준 C++ 보고서 스냅샷을 대시보드/표·두 출력기가 공유하며 설정은 `.ppm` 입력을 바꾸지 않는다. Qt Gui는 Widgets 의존 모듈이므로 별도 Qt 패키지 설치가 필요하지 않다.
[대시보드·보고서·출력 계약](reports-export.md)에 필터와 집계 범위·용지/글자 크기·한도·후속 범위를 기록한다.

로컬 Release 전체 14/14, Windows 네이티브 보고서 UI와 출력 시험을 통과했다. openpyxl/pypdf로 ZIP/숫자/미정/출처, PDF 크기·본문·긴 행 700구간과 마지막 표식을 독립 대조했다. 엑셀 14개 시트와 PDF 페이지를 렌더링해 한글/줄바꿈/정렬을 확인했다. 독립 재열기 검사 스크립트는 `scripts/verify-report-fixtures.py build`이며 Python 의존성은 개발/CI에만 사용한다. Windows/macOS CI에서도 CTest 뒤 같은 파일 검증을 실행한다.

자동 저장/복구·실행 취소 증분은 `undo_contract`, `recovery_crash_file`, `recovery_ui`를 더해 전체 17개로 확장했다. 실제 별도 프로세스 강제 종료와 flush 이후 commit 직전 강제 종료를 포함한다. 일반 입력은 새로운 revision으로 취소/재실행하고, 승인·제출 사실은 불변 이력 경계로 유지한다. 저장 입력과의 동일성(dirty)과 실제 저장된 revision을 구분해 보고서 출처도 보정했다.
[자동 저장·복구·편집 이력 계약](recovery-undo.md)에 저장 위치/간격·사본 복구·잠금/세대·중단·한도·후속 검증을 기록한다. 이 증분 당시 `.ppm`는 schema 6이었으며 복구 envelope는 별도 schema 1이다. 복구 envelope의 `projectSchema`는 안에 든 프로젝트 데이터의 버전을 기록한다. 현재 `.ppm`의 지원 범위는 [파일 형식과 호환성](#ppm-파일-형식과-호환성)을 따른다. 회귀 시험용 저장 단계 observer는 실제 flush/commit 사이에서 중단·경쟁을 재현하며 제품 UI에서는 설정하지 않는다.

후속 PDM/작업 달력 증분은 `.ppm` schema 7을 사용하며 schema 1~6 원본과 기존 기준선을 보존한다. 복구 envelope schema 1의 내부 projectSchema 6/7을 지원한다. `native-pdm-taskcal-v1`은 civil 분 좌표와 작업별 근무분을 구분하며 `jobs-pdm-1.0`으로 계산한다. 자원/원가는 같은 근무 구간을 사용한다. 기존 `native-fs0-workminutes-v1` / `jobs-cpm-0.2` 결과는 유지한다. [PDM·작업 달력 계약](pdm-calendars.md), `pdm_calendar_contract`/`pdm_calendar_ui`와 독립 reader를 추가해 CTest 19개로 확장했다.

제약·마감·간트 증분은 schema 8 / native-pdm-constraints-v1 / jobs-pdm-1.1을 사용하며 구 입력/기준선 정책을 보존한다. Constraints는 하드 충돌과 소프트 마감 경고를 구분하고, GanttEditing은 UI 미리보기 후 Document의 ID/revision guard와 단일 edit를 사용한다. [상세 계약](constraints-gantt.md), constraint_contract/constraint_gantt_ui로 CTest 21개와 독립 XLSX/PDF 검증을 제공한다.

공수·작업 유형·자원 달력·분할 증분은 schema 9 / native-effort-split-v1 / jobs-effort-1.0이다. TaskExecution의 달력 교집합/공수 적분·마지막 분 배분을 일정·부하·자원비·출력이 공유한다. [계산/편집/파일 계약](effort-calendars-splits.md), effort_work_calendar_split/effort_ui를 포함해 CTest 23개로 확장하고 새 공수 보고서의 19개 XLSX 시트와 PDF를 독립 reader로 검증한다. schema 1~8의 원본 보존 SaveAs와 이전 계산 엔진, projectSchema 6~9 복구를 유지한다.


성능·통합 검증 증분은 PRD PERF-01~04를 구현 전에 커밋하고 계산 진행/협력 취소, 요청/session 보호, 동일 스냅샷의 달력/공수 격자 공유와 화면 주변 간트를 추가했다. `calculation_cancellation`, `integrated_project_workflow`, `performance_cancellation_ui`로 CTest 26개를 구성한다. 로컬 26/26·Windows 네이티브 새 UI·독립 XLSX 5/PDF 6 검사를 통과했다. [측정 계약·원시 결과·한계](performance-integration.md)를 따르며 CI는 1천/1만 기본·공수 사례를 별도 프로세스에서 실행해 JSON/log artifact를 남긴다. 파일 schema/기존 계산 정책은 유지한다.


작업 편집 증분은 PRD EDIT-01~05를 먼저 정의한 뒤 `TaskEditing`의 Qt 독립 원자적 명령과 표 입력/TSV 공통 파서, ID 기반 검색/필터/정렬/선택을 구현했다. `task_editing_contract`, `task_editing_ui`로 CTest 28개이며 로컬 전체 28/28·네이티브 Windows UI·독립 XLSX/PDF 검사를 통과했다. [작업 편집 계약](task-editing.md)에 삭제 보호·복제 범위·붙여넣기 한도·완료 증거와 후속 범위를 기록한다.

Project XML 증분은 PRD XML-01~04를 먼저 커밋하고 `persistence/ProjectXml`의 제한 파서·계획 투영·원본 보존 교환 폴더와 `MainWindowXml` 미리보기를 추가한다. 기존 .ppm schema 9와 계산 코어는 유지한다. `project_xml_contract`, `project_xml_ui`를 포함해 CTest 30개다. 도메인 기대값/지원 부분 왕복/원본 바이트 및 승인·실적·원가 사본, XML 한도/오류, UI 취소/오래된 미리보기/읽기 전용 내보내기를 검사한다. `python scripts/verify-project-xml.py build`는 표준 XML reader의 독립 값 검사이며 실제 Microsoft Project 검증을 대체하지 않는다. `python scripts/capture-project-xml-ui.py build`는 네이티브 UI 동작과 미리보기 PNG를 기록한다. CI에서 기존 XLSX/PDF·1천/1만 성능 검증과 함께 실행한다. [지원 범위·손실·사용법](project-xml.md)을 따른다.

Primavera XER 증분은 PRD XER-01~04를 먼저 정의하고 `persistence/PrimaveraXer`의 제한된 탭/structured calendar 파서·기간 기반 계획 투영과 `MainWindowXer`의 인코딩/변환 미리보기를 추가했다. XML과 XER의 원자적 교환 폴더 게시를 `ExchangePackage`에서 공유한다. 파일 schema/계산 코어는 유지하며 `primavera_xer_contract`/`primavera_xer_ui`로 CTest 32개다. 소수 시간의 정수 분 변환/1분 오차·지연/24시간 달력·상속 휴일·가용량 미정/0·UTF-8/Windows-1252·승인/실적/원가 사본·오류/한도/취소/session 경계를 검사한다. 독립 검사는 Python 3.12+, `mpxj==16.10.0`, `JPype1==1.6.0`, Java 21을 설치하고 `python scripts/verify-primavera-xer.py build`로 실행한다. MPXJ의 공식 UniversalProjectReader proxy를 통해 BOM 인식과 strict read를 함께 적용하며 실제 파일을 수정하지 않는다. `python scripts/capture-primavera-xer-ui.py build`는 네이티브 UI 시험/미리보기 PNG를 기록한다. 앱 실행에는 Python/Java가 필요 없다. [형식·원본 보존·제한](primavera-xer.md)을 따른다.

작업 표 모델/비동기 편집 증분은 PRD MODEL-01·ASYNC-EDIT-01~03·MODEL-PERF-01을 구현 전에 커밋했다. TaskTableModel/TaskTableView는 14열과 ID 기반 보기/선택을 유지하며, AsyncEditController와 Document의 봉인된 준비/반영 API가 공수·실적·배정 계산을 격리한다. 새 prepared_edit_contract/task_table_model_contract/async_editing_ui로 CTest 37개다. 1만 공수 작업에서 실행 중/완료 직전 취소, 최신 요청·문서 재열기·저장/F9 순서, 대화상자 초안/재시도와 창 파괴를 검사한다. 네이티브 검사는 `python scripts/capture-model-async-ui.py build`이며 PNG와 관측 JSON을 남긴다. [모델·비동기 편집 계약과 검증](model-async-editing.md)을 따른다.

대규모 편집 응답성 증분은 PRD RESPONSIVE-01~04를 먼저 확정하고 내부 ProjectState의 owning read-only snapshot, worker의 정확한 dirty 준비와 일반 기간 단일 작업 delta, 연속 변경의 모델/WBS 증분 갱신을 추가했다. F9/공수 미리보기/기준선 준비/자동복구도 공유 입력을 캡처한다. responsive_document_contract/responsive_editing_ui를 포함해 CTest 39개를 구성하며, 상세 범위와 전후 원시 관측은 [대규모 편집 준비·dirty·화면 갱신](responsive-editing.md)을 따른다.


구조·복합 편집 증분은 PRD BULK-01~04를 먼저 확정하고 작업 추가/삽입·삭제·복제·모든 TSV 붙여넣기와 해당 복합 undo/redo의 해석/검증/표시 준비를 worker로 연결했다. 현재 계획만 검증하는 내부 경계와 준비된 BulkView, 기본 보기의 행 추가/삭제 및 변경 범위 신호, 공유 delta·선택 범위·기준선 캐시를 사용한다. `bulk_editing_contract_ui`를 포함해 CTest 40개다. [구조·복합 편집 계약과 측정](bulk-editing.md)을 따른다.


필터·정렬·WBS 대량 편집 증분은 PRD VIEWBULK-01~04를 선반영한 뒤 공통 TaskViewProjection/worker 준비와 ID 기반 모델 행·layout 갱신을 추가했다. 새 셀 초안은 반영 전에 확정하여 stale 결과가 덮지 않게 한다. projected_views_ui로 CTest 41개이며 [준비된 보기 계약·전후 관측](projected-task-views.md)을 따른다.

외부 파일 검증 증분은 PRD PARSER-SAFE-01~04를 먼저 확정하고 실제 native 메모리 decoder와 XML/XER import에 공유 harness를 추가했다. `parser_seed_replay`를 포함해 CTest 42개이며, 기본 빌드에서는 56개 정상/손상 seed를 재생한다. 별도 Linux/Clang CI는 선택적 ASan/UBSan 전체 회귀와 libFuzzer 세 타깃의 유한 실행을 수행한다. [명령·경계·검증 결과](parser-safety.md)를 따른다.

유지보수 증분은 PRD MAINT-01~04를 먼저 확정하고 편집 핵심의 점진 포맷, 전체 제품 src의 clang-tidy, private 편집 권한 가드를 도입했다. `document_edit_guards`를 포함해 CTest 43개다. 기본 빌드에는 formatter/analyzer가 필요하지 않으며 [도구 명령·가드 계약·검증](cpp-quality.md)을 따른다.

타입 증분은 PRD ENUM-01~04를 먼저 확정하고 DependencyType/ConstraintType/TaskType을 도메인·편집 API·계산·UI에 적용했다. writer schema9와 파일 문자열/기본값은 유지한다. `plan_enum_compatibility`를 더해 CTest 44개로 확장했으며 이전 writer 파일 13개, 중첩 이력, 엄격한 token/enum 검증과 사본 저장·복구를 검사한다. [변환표·기존 파일 호환·검증](plan-enums.md)을 따른다.

평준화 채택 증분은 `leveling_selection_contract`와 `leveling_selection_ui`를 추가한다. schema12 seed·기준선/원가/Usage·취소/session/복구와 offscreen 화면·출력을 검사하며 실제 결과는 [검증 기록](validation/leveling-adoption-2026-11-03/README.md)에 보존한다. [채택 계약](leveling-adoption.md).

## 일정표·간트 인쇄 (2026-11-03)

`ppm_reporting/SchedulePrint`는 새 전체 계산→표/막대/출처→가로 열/기간·세로 행 조각 페이지를 준비하며 72pt 좌표와 고정 줄바꿈을 모든 장치에 공용한다. `ppm_ui/SchedulePrintDialog`는 Qt PrintSupport의 네이티브 프린터 선택과 worker 출력, 단일 페이지 화면 렌더링을 연결한다. CMake는 Qt6 PrintSupport를 추가하며 Qt 자체 모듈 외 런타임은 요구하지 않는다. Windows payload 확인에 Qt6PrintSupport.dll을 포함하고 windeployqt/macdeployqt의 링크 의존성 추적을 사용한다.

`schedule_print_contract` / `schedule_print_ui`와 `scripts/verify-schedule-print.py build-forecast`가 다수 행/열·긴 한글 셀·기준선/실제·평준화·캡처된 필터/선택·페이지·300dpi 가상 프린터·범위/역순/복사·원본 불변·취소/session/파일 선택 변경을 검사한다. [계약](schedule-printing.md)과 [로컬 검증](validation/schedule-printing-2026-11-03/README.md)을 따른다.

## 네트워크 다이어그램 회귀

`network_diagram_contract` / `network_diagram_ui`는 전체 계산과 부분 표시 분리, 4종 관계/지연·임계/driving·실제 날짜, 평준화 자원 연결/계산 불가, SCC 순환, 생략/범위/묶음, 직접 관계 목록과 표/간트 선택, 읽기 전용·취소·revision/session을 검사한다. 1천/1만 작업 고정 입력의 순수 계산·query와 UI build/query/render 시간을 `build-forecast/network-qa/`에 기록한다. [계약](network-diagram.md)을 따른다.

네트워크 증분의 [Windows Release 전체 CTest 77개·독립 출력·소스 해시/포맷·규모/화면 증거](validation/network-diagram-2026-11-03/README.md)를 보존한다.

## 다중 프로젝트 XER 선택 회귀

`xer_project_selection_contract` / `xer_project_selection_ui`가 선택/소유·자원/달력 폐쇄·외부 관계·원본/게시·검색/취소/stale/session/한 번 읽기를 검사한다. 1천/1만 입력 작업의 500/5000개 선택 관측을 기록한다. `scripts/verify-xer-project-selection.py build-forecast`는 Python 표준 TSV와 MPXJ 16.10.0 / JPype1 1.6.0 / Java 21로 원본 목록/선택 ID·이름/관계·배정과 계획 투영 출력의 기간/자원을 독립 대조한다. Python 3.12 검증 venv를 사용했으며 앱 런타임 의존성은 아니다. [계약](xer-project-selection.md)을 따른다.

선택 증분의 [로컬 79개 CTest·9종 독립 검사·92 seeds·소스/시험/CI 해시·화면/worker 측정](validation/xer-project-selection-2026-11-03/README.md)을 보존한다. CI 설정 추가와 실제 CI 실행을 구분한다.

## 진척 정책 비교와 P6 준비

`progress_policy_contract` / `progress_policy_ui`는 4개 native 프로필·4종 관계/양음 lag·실제/완료·잔여 공수/분할/달력·제약/원본 오류 차단·비활성 관계·취소/session/읽기 전용·JSON 파일 선택 변경 보호와 1천/1만 관측을 검사한다. [정책 계약](progress-policy-comparison.md)과 [P6 왕복 절차](p6-roundtrip.md)를 따른다. 비교기의 `--self-test`는 합성 입력 시험이며 실제 P6 실행이 아니다.

[최종 로컬 검증](validation/progress-policy-2026-11-03/README.md)은 전체 CTest 81개·92 seeds·기존 독립 검사 9종·준비 P6 계획의 MPXJ strict 읽기/비교기 자체시험 6개를 포함한다. 실제 P6 실행은 미실행이다.

진척 정책 채택은 progress_policy_adoption_contract / progress_policy_adoption_ui를 추가한다. schema13·복구·undo/redo·조건부 writer·유효 단가 잔여 원가·plan/baseline 보존·stale/cancel/session·읽기 전용·UI 채택과 출력 연결을 검사한다. 독립 출력 확인: `.deps/report-verification/Scripts/python.exe scripts/verify-progress-policy-adoption.py build-forecast`. [계약](progress-policy-adoption.md).

진척 정책 채택의 [최종 Windows Release 검증](validation/progress-policy-adoption-2026-11-03/README.md)은 CTest 83개 전체, schema1..13의 104개 파서 seed, 형식 검사 132개 파일과 새/기존 독립 출력 판독을 포함한다. P6 실제 실행은 미설치로 미실행이다.

`progress_leveling_contract` / `progress_leveling_ui`는 선택 정책의 관계 마스크를 네 엔진의 평준화에 연결하고 schema14·시나리오/복구·변경/해제 이력·출력과 취소/stale를 검사한다. 독립 판독: `.deps/report-verification/Scripts/python.exe scripts/verify-progress-leveling.py build-forecast`. [계약](progress-policy-leveling.md).

조합 증분의 [최종 로컬 검증](validation/progress-leveling-2026-11-03/README.md)은 전체 CTest 85개, schema1..14의 114개 파서 seed, 형식 검사 136개 파일과 독립 출력 판독을 포함한다. 실제 P6는 미설치로 미실행이다.

`leveling_float_contract` / `leveling_float_ui`는 자원 흐름/병렬 용량/달력·가용량 감소/관계 순환/교차 분할 실행 창·이전1.1 미산정·A/B·기준선1.0/1.1/1.2와 표/자원 연결/출력을 검사한다. [정의·한도](leveling-float.md).

평준화 후 여유 증분의 [최종 로컬 검증](validation/leveling-float-2026-11-03/README.md)은 전체 CTest 87개(294.89초), schema1..14 파서 seed 114개, 형식 검사 141개 파일, 독립 판독·자체시험 14종과 1천/1만 파생 계산 관측을 포함한다. 실제 P6 실행은 미실행이다.

교차 분할은 같은 두 float 시험을 실행 창·3종 작업 유형·구간 작업량 재배분·다중 자원/용량·진척 실제일·기준선1.1/1.2·구간 인계 시각으로 확장한다. [최종 검증](validation/segment-leveling-float-2026-11-03/README.md)은 87개 대상의 최종 통과(전체86/87 후 시험 출력 충돌 정리·UI1/1 재검증), 파서 seed114개·형식142파일·독립 판독15종과 교차 한 쌍을 포함한 1천/1만 파생 계산 관측을 보존한다. 새 선택 계획 기준선 엔진1.2와 기존1.0/1.1 재현, schema9~14 조건부 writer를 유지한다.

`repartition_float_contract`와 확장한 `leveling_float_ui`는 창 소멸/재생성·작업별 가능한 총여유 증인/고정 날짜 자유여유·실제 합산 수요·활성 진척·미정/한도/취소·기존1.2/신규1.3 기준선과 표시를 검사한다. [최종 검증](validation/repartition-float-2026-11-03/README.md)은 전체88/88(278.39초), 최종 표 정책 전달 보완 UI2/2, 파서114개·형식145파일·독립 판독/자체시험16종과 Python 분 단위 전수 대조를 보존한다. source204개 해시와 전체 회귀 뒤 UI 한 줄 차이를 구분한다. 파일 schema는 추가하지 않는다.

2026-11-04 `scaled_repartition_float_contract`는 후보 제약 전파·고정 작업 분리·반복형 탐색과 이동 가능128개/고정 포함 큰 묶음, 4종 관계/합산 수요·129개 한도·취소/동일성·1.3 승인 기준선 재현과 현재1.4 전환을 검사한다. [전체89/89·독립17종·1,514증인 재구성](validation/scaled-repartition-float-2026-11-04/README.md), 파서114개·형식146파일을 통과했다. source204개와 빌드 식별값을 대조했다. 새 엔진은1.4지만 수학적 정책은 resource-repartition-float-v3이며 입력 schema는 유지한다.

이어 `leveling_witness_ui`는 구조화된 불변 증인·A/B별 작업 이름/날짜/선택 행·총/자유여유·필터·실적·0여유·미산정과 source 불일치를 검사한다. 문서 편집/교체·비교 조건 변경·재계산·채택 제출·부모 종료 시 창을 닫고 일반 저장은 유지한다. [전체90/90·독립18종·UI 화면·source206개 식별값](validation/leveling-witness-2026-11-04/README.md), 파서114개·형식149파일을 통과했다. 준비된1만 행 모델37.6173ms는 UI 생성/필터의 단회 관측이며 전체 일정 계산 성능이 아니다. 엔진/파일 schema는 추가하지 않는다.

`expanded_repartition_float_contract`는 엔진1.5의128개 고정 제한 제거·후보 결합 분해·큰 단위 반복 탐색·연결 우선 순서를 검증한다. 129/512 결합·이동 가능1,000개 분리·132개 교차 분할/논리 묶음, 삼중 합산 수요·129개 잔여 예측·4종 관계·예산/취소·기존1.4 기준선 재현·새1.5 native12·근거 창 전체 날짜와 큰 진단 미리보기/XLSX/PDF를 검사한다. [전체91/91·독립19종·2,641증인/280,785날짜 참조](validation/expanded-repartition-float-2026-11-04/README.md), 파서114개·형식151파일·source206개 식별값을 보존한다. 전체 작업/후보/판정/증인 예산을 유지하며 모든 대규모 입력의 성능 보장으로 보지 않는다.

`candidate_propagation_contract`는 [PROP-01~04 / 엔진1.6](candidate-propagation.md)의 안전한 생성 전 상한·조건부 후보 제외/복원·키 캐시·native 인증 공유를 검사한다. 같은 입력의1.5/1.6 각3회 교차 측정, 자원 순서 체인750개에서 기존 후보 한도 중단과 신규 완료, 비단조 용량·분기 실패/복원·원자성/취소·기존1.5/신규1.6 native12와 XLSX를 포함한다. `scripts/verify-candidate-propagation.py`는 전체 증인 재구성과 작은 용량 모델17,366개 허용 배치 전수 검산을 수행한다. [최종 회귀·측정·소스 식별값](validation/candidate-propagation-2026-11-04/README.md). 기존 확장 계약은1.5에 고정해 과거 기준선·진단을 재현하며, 당시 현재 출력을 읽는 세 여유 verifier는1.6 출처를 확인했다(현재1.8로 갱신). CI에 새 reader/artifact 보존 단계를 추가한다.

`nonmonotone_propagation_contract`는 [NPROP-01~04 / 엔진1.7](nonmonotone-propagation.md)의 점별 필수 부하·살아 있는 후보의 연쇄 지지/부하 전파와 가역 복원을 검사한다. 달력 공백 속2/32/96작업·151단위분 공수의 분수 마지막1분·수요 소멸·다일 용량·실제 시작 고정/잔여 공수·미정/취소·반복·기존1.6/신규1.7 기준선/native12와 XLSX를 포함한다. 작은 프로파일200개/9,600좌표를 원시 점별 합산과 대조하고, 새 독립 verifier는4/55/673/17,366개 허용 배치를 전수 검산한다. 기존 candidate 계약은1.6에 고정해 승인 결과/진단을 보존한다. 새 reader와 CI artifact를 추가하며 [최종 측정·전체 회귀·소스 식별값](validation/nonmonotone-propagation-2026-11-04/README.md)에 비용과 한계를 기록한다.

`propagation_cost_contract`는 [COST-01~03 / 현재1.8](propagation-cost.md)의 비용 경계·포화·실패 활성화/효과 피드백·재시도 경계와 분기 중 지연 마스크 생성/복원을 검사한다. 작은5사례 각5회와 큰96작업·관측 활성화·기존 분할3사례 각3회의1.7/1.8 순서 교차 관측, TaskSchedule 전체 일치·큰 후보11,136개 제거·미정/취소·구1.7/신규1.8 기준선과 native12/XLSX를 포함한다. 공통 fixture를 추출하고 기존 비단조 계약을1.7에 고정했다. 새 독립 reader는 기존 원시 oracle을 재사용해138증인/400날짜와4/55/673/17,366/64/32,768개 배치 및 분할155,761쌍을 대조한다. CI reader/artifact와 [최종 측정·전체 회귀·소스 식별값](validation/propagation-cost-2026-11-04/README.md)을 추가한다.

## 2026-11-05 결정 원장 검증

[평준화 결정 이력](leveling-decisions.md)의 `leveling_decision_contract`는 직접/worker 채택·교체·해제·자동 무효화·undo/redo·dirty, schema15·구 파일·사본·복구, stale/session/cancel/읽기 전용, 엄격 파싱과 10,000건 한도의 원자성 및 조회 화면을 검사한다. `python scripts/verify-leveling-decisions.py <build-dir>`는 native JSON을 독립 판독한다. 새 개발 순서는 [미개발 점검](planning/17-remaining-development.md)에 기록한다.

## 2026-11-05 프로젝트·자원 필드 검증

`object_fields_contract` / `object_fields_ui`는 네 형식·범위별 같은 ID·다중 자원 원자성·worker 취소/session·읽기 전용·undo/dirty·기준선/시나리오·schema16/구버전·사본/복구·평준화 무효화와 결정 원장을 검사한다. 실제 메뉴의 정의/입력/조회와 한국어 소형 화면을 포함한다. `python scripts/verify-object-fields.py <build-dir>`는 optional openpyxl/pypdf 환경에서 native/XLSX/PDF를 독립 판독한다. [계약](object-custom-fields.md).

기간별 계획 배정/곡선 검증은 `assignment_periods_contract`, `assignment_periods_ui` CTest와 `scripts/verify-assignment-periods.py <build>` 독립 native/XLSX/PDF reader를 사용한다. 출력·화면·1k/10k 수요 측정은 `<build>/assignment-periods-qa`에 생성한다. [계약](assignment-periods.md).

인쇄·네트워크 확장은 presentation_contract/presentation_ui CTest와 scripts/verify-print-network.py <build>로 검증한다. 독립 판독은 native schema18/checksum과 WBS/관계/PDF 쪽·출처, PDF/QPrinter 장치 DPI에 따른 실제 벡터 도형·글자 크기 일치를 확인한다. [계약](print-network-extension.md).

GAP-13/14 로컬 증분은 `governance_risk_automation_contract`, `governance_ui`를 추가하고 `PPM-Automation` CLI를 함께 빌드/설치합니다. [계약](organization-risk-automation.md)의 schema3/역할/확률 기대값/원자 batch와 `python scripts/verify-governance-risk.py build`를 검증합니다. 프로젝트 파일 schema는 유지합니다.

서버 후속 증분은 `ppm_collaboration`(Qt Network 인증/HTTP/재연결 feed), `ServerDialog`, 선택 Python/aiohttp/SQLite 서비스를 추가한다. [서버 계약](../server/README.md)과 `PPM_SERVER_TEST_PYTHON` 설정을 따르며, 설정 시 `server_native_realtime_ui` 및 `server_http_auth_sync_scheduler`를 전체 CTest에 추가한다. 기존 프로젝트/작업공간 schema는 바꾸지 않는다. Windows 패키지는 Qt6Network와 Schannel TLS backend를 포함하고 macOS outgoing network entitlement와 LAN 목적 문자열을 추가했다. 실제 Mac/Store 배포 검증은 별도다.
