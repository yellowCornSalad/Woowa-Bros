# 데이터 추출 도구 사용법

이 폴더는 배달의민족 비정형 데이터를 추출하고 분석하는 도구들을 포함합니다.

## 📁 파일 구조

```
data_extraction/
├── requirements.txt          # 필요한 패키지 목록
├── data_extractor.py        # 메인 데이터 추출 클래스
├── text_analyzer.py         # 텍스트 분석 도구
├── run_extraction.py        # 실행 스크립트
└── README.md               # 이 파일
```

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 가상환경 생성 (Windows)
python -m venv delivery_env
delivery_env\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. 데이터 추출 실행

```bash
# 기본 실행 (모든 분석 포함)
python run_extraction.py

# 텍스트 분석 건너뛰기
python run_extraction.py --skip-text-analysis

# 로그 분석 건너뛰기
python run_extraction.py --skip-log-analysis

# Redis 설정 변경
python run_extraction.py --redis-host localhost --redis-port 6379
```

## 📊 주요 기능

### DataExtractor 클래스

- **CSV 데이터 추출**: `extract_csv_data()`
- **JSON 데이터 추출**: `extract_json_data()`
- **XML 데이터 추출**: `extract_xml_data()`
- **로그 데이터 추출**: `extract_log_data()`
- **Pickle 데이터 추출**: `extract_pickle_data()`
- **Redis 저장**: `save_to_redis()`
- **데이터베이스 저장**: `save_to_database()`

### TextAnalyzer 클래스

- **텍스트 전처리**: `preprocess_text()`
- **토큰화**: `tokenize_text()`
- **감정 분석**: `analyze_sentiment()`
- **키워드 추출**: `extract_keywords()`
- **메시지 패턴 분석**: `analyze_message_patterns()`
- **워드클라우드 생성**: `generate_wordcloud()`
- **개체명 추출**: `extract_entities()`

## 📈 출력 결과

실행 후 다음 폴더들이 생성됩니다:

```
extracted_data/           # 추출된 데이터
├── extracted_*.json     # 각 파일별 추출 결과
└── extraction_summary.json

reports/                 # 분석 리포트
├── text_analysis.json
├── text_analysis_report.txt
├── log_analysis.json
├── final_report.json
└── final_report.txt

visualizations/          # 시각화 결과
└── wordcloud.png       # 워드클라우드
```

## 🔧 사용 예시

### 기본 데이터 추출

```python
from data_extractor import DataExtractor

# 초기화
extractor = DataExtractor()

# Redis 연결
extractor.setup_redis()

# 모든 데이터 추출
results = extractor.extract_all_data()

# 결과 확인
for filename, result in results.items():
    print(f"{filename}: {result['type']}")
```

### 텍스트 분석

```python
from text_analyzer import TextAnalyzer

# 초기화
analyzer = TextAnalyzer(language='korean')

# 텍스트 리스트
texts = ["맛있는 치킨 배달해주세요!", "피자 주문했는데 늦게 왔어요"]

# 키워드 추출
keywords = analyzer.extract_keywords(texts, top_n=10)
print("주요 키워드:", keywords)

# 감정 분석
for text in texts:
    sentiment = analyzer.analyze_sentiment(text)
    print(f"'{text}': {sentiment['polarity']:.3f}")
```

## ⚙️ 설정 옵션

### Redis 설정

```python
extractor = DataExtractor()
extractor.setup_redis(host='localhost', port=6379, db=0)
```

### 데이터베이스 설정

```python
extractor.setup_database("postgresql://user:password@localhost/dbname")
```

### 언어 설정

```python
# 한국어
analyzer = TextAnalyzer(language='korean')

# 영어
analyzer = TextAnalyzer(language='english')
```

## 🐛 문제 해결

### 1. Redis 연결 실패

```bash
# Redis 서버 시작 (Windows)
redis-server

# 또는 Docker 사용
docker run -d -p 6379:6379 redis:latest
```

### 2. 폰트 문제 (워드클라우드)

Windows에서 한국어 워드클라우드 생성 시 폰트 경로를 수정하세요:

```python
# text_analyzer.py의 generate_wordcloud 메서드에서
font_path = 'C:/Windows/Fonts/malgun.ttf'  # Windows
```

### 3. 메모리 부족

대용량 파일 처리 시 메모리 부족이 발생할 수 있습니다:

```python
# 청크 단위로 처리
def process_large_file(filename):
    chunk_size = 1000
    for chunk in pd.read_csv(filename, chunksize=chunk_size):
        # 청크별 처리
        process_chunk(chunk)
```

## 📋 지원 파일 형식

- **CSV**: `.csv` 파일
- **JSON**: `.json` 파일
- **XML**: `.xml` 파일
- **로그**: `.log` 파일
- **Pickle**: `.pickle` 파일

## 🔍 분석 기능

### 텍스트 분석
- 키워드 추출 및 빈도 분석
- 감정 분석 (긍정/부정)
- 메시지 패턴 분석
- 워드클라우드 생성
- 개체명 추출 (음식점, 음식, 가격 등)

### 로그 분석
- 로그 레벨별 분포
- 시간대별 패턴
- 에러 메시지 수집
- 응답 시간 분석

### 데이터 통합
- 여러 파일 형식 통합 처리
- Redis 캐싱
- 데이터베이스 저장
- 구조화된 리포트 생성

## 🚀 다음 단계

데이터 추출이 완료되면 다음 단계로 진행하세요:

1. **Kafka 스트리밍**: 추출된 데이터를 Kafka로 전송
2. **Airflow 파이프라인**: 정기적인 데이터 처리 워크플로우 구축
3. **Redis 캐싱**: 실시간 데이터 캐싱
4. **웹 서비스**: 분석 결과를 보여주는 대시보드 개발
5. **배포**: Docker, Kubernetes, AWS를 통한 배포

## 📞 지원

문제가 발생하면 다음을 확인하세요:

1. 로그 파일: `extraction.log`
2. Python 버전: 3.8 이상
3. 필요한 패키지 설치: `pip install -r requirements.txt`
4. 데이터 파일 위치: `data/` 폴더에 원본 파일들이 있어야 함
