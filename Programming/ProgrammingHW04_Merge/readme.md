
# 1. Log Merge

## 1.1. 파일 설명

a.csv ~ c.csv 파일에는 각각 다른 데이터가 있으며, 각 파일들 안에는 low limit, high limit, header, data가 있다.

- [a.csv](a.csv)
- [b.csv](b.csv)
- [c.csv](c.csv)

## 1.2. 문제

a.csv, b.csv, c.csv 파일은 각각 다른 공정에서 생성된 테스트 로그입니다.  
각각의 파일에서 중복된 바코드를 제거하고, a, b, c 모든 로그에 존재하는 바코드에 대해 모듈 별 데이터를 하나의 row에 Merge하고, 스팩을 체크하여 양품 여부를 판별하세요.

## 1.3. 주의사항

출력 파일은 아래와 같이 나오도록 작성하시오.

- low limit, high limit 행 삭제
- 모든 데이터를 Merge하여 출력하고 마지막 열에는 Spec Out인 모든 항목들을 ' '로 구분하여 출력 (Spec In인 경우 'PASS'라고 출력)
- 재검으로 인해 바코드가 중복되는 경우 마지막으로(최근에) 테스트 된  바코드의 데이터만 남기도록 함

[mg.csv](mg.csv)

## 1.4. 참고

중복 바코드 제거 시 pandas.DataFrame.drop_duplicates 함수를 사용하면 편리합니다.
