# 배달의민족 데이터 분석 토이프로젝트 가이드

## 📋 프로젝트 개요

이 프로젝트는 배달의민족의 실제 고객 주문 데이터를 활용하여 데이터 사이언티스트의 실제 업무 환경을 체험해보는 토이프로젝트입니다. Kafka, Airflow, Redis, Kubernetes, AWS 등 실제 기업에서 사용하는 기술 스택을 활용하여 엔드투엔드 데이터 파이프라인을 구축합니다.

## 🎯 학습 목표

1. **실제 데이터 처리 경험**: 10만건의 실제 배달 데이터를 다루며 데이터 전처리, 분석, 시각화 경험
2. **현대적 기술 스택 습득**: Kafka, Airflow, Redis, Docker, Kubernetes, AWS 등 실제 기업에서 사용하는 기술들
3. **데이터 파이프라인 구축**: 데이터 수집부터 웹 서비스 배포까지 전체 과정 이해
4. **클라우드 배포 경험**: AWS를 통한 실제 서비스 배포 및 운영 경험

## 📊 데이터 소개

### 제공된 데이터 파일들
- `배달의민족_가명데이터_10만건.csv` (39MB): 주요 주문 데이터
- `배달의민족_메시지_데이터_25000건.json` (33MB): 고객-가게 간 메시지 데이터
- `배달의민족_JSON_데이터_25000건.json` (32MB): JSON 형태의 주문 데이터
- `배달의민족_XML_데이터_25000건.xml` (25MB): XML 형태의 주문 데이터
- `배달의민족_로그_데이터_25000건.log` (4.3MB): 시스템 로그 데이터
- `배달의민족_통합_비정형데이터_10만건.pickle` (55MB): 통합된 비정형 데이터

### 예상 데이터 구조
- **주문 정보**: 주문 시간, 배달 주소, 주문 금액, 메뉴 정보
- **고객 정보**: 고객 ID, 선호 메뉴, 주문 패턴
- **가게 정보**: 가게 ID, 메뉴 카테고리, 평점
- **배달 정보**: 배달 시간, 배달 거리, 배달료
- **메시지 데이터**: 고객-가게 간 소통 내용

## 🏗️ 프로젝트 아키텍처

```
[데이터 소스] → [Kafka] → [Airflow] → [Redis/PostgreSQL] → [웹 서비스] → [Kubernetes] → [AWS]
```

### 1단계: 데이터 수집 및 스트리밍 (Kafka)
### 2단계: 데이터 처리 및 정리 (Airflow)
### 3단계: 데이터 저장 및 관리 (Redis + PostgreSQL)
### 4단계: 웹 서비스 개발 (Flask/FastAPI)
### 5단계: 컨테이너화 (Docker)
### 6단계: 오케스트레이션 (Kubernetes)
### 7단계: 클라우드 배포 (AWS)

## 📝 상세 진행 단계

### Phase 1: 환경 설정 및 데이터 탐색 (1-2주)

#### 1.1 Windows 개발 환경 구축
```bash
# 1. Python 가상환경 생성 (Windows)
python -m venv delivery_project
delivery_project\Scripts\activate

# 2. 필요한 패키지 설치
pip install pandas numpy matplotlib seaborn plotly
pip install kafka-python apache-airflow
pip install flask fastapi uvicorn
pip install docker kubernetes
pip install boto3  # AWS SDK
pip install redis psycopg2-binary  # Redis, PostgreSQL
pip install beautifulsoup4 lxml  # XML 파싱
```

#### 1.2 비정형 데이터 추출 도구 설치
```bash
# 데이터 추출 관련 패키지
pip install openpyxl xlrd  # Excel 파일 처리
pip install PyPDF2 pdfplumber  # PDF 파일 처리
pip install requests  # API 호출
pip install selenium  # 웹 스크래핑
```

#### 1.3 데이터 탐색 및 분석 (EDA)
```python
# 예시 코드
import pandas as pd
import json
import xml.etree.ElementTree as ET

# CSV 데이터 로드
df_orders = pd.read_csv('data/배달의민족_가명데이터_10만건.csv')

# JSON 데이터 로드
with open('data/배달의민족_메시지_데이터_25000건.json', 'r') as f:
    messages_data = json.load(f)

# 기본 통계 분석
print("데이터 크기:", df_orders.shape)
print("컬럼 정보:", df_orders.columns.tolist())
print("결측값 확인:", df_orders.isnull().sum())
```

**분석해야 할 주요 내용:**
- 데이터 품질 확인 (결측값, 이상치, 중복값)
- 기본 통계 분석 (평균, 분산, 분포)
- 시각화를 통한 패턴 발견
- 비즈니스 인사이트 도출

#### 1.4 데이터 전처리 계획 수립
- **데이터 클리닝**: 결측값 처리, 이상치 제거, 데이터 타입 변환
- **피처 엔지니어링**: 시간대별 분석, 지역별 분석, 고객 세분화
- **데이터 통합**: 여러 파일의 데이터를 하나로 통합

### Phase 2: Kafka 스트리밍 파이프라인 구축 (1주)

#### 2.1 Kafka 환경 설정 (Windows)
```bash
# Docker Desktop for Windows 설치 후
docker-compose up -d zookeeper kafka
```

#### 2.2 데이터 프로듀서 개발
```python
# 예시 코드
from kafka import KafkaProducer
import json
import pandas as pd

def create_producer():
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

def send_order_data():
    producer = create_producer()
    df = pd.read_csv('data/배달의민족_가명데이터_10만건.csv')
    
    for _, row in df.iterrows():
        message = {
            'order_id': row['order_id'],
            'customer_id': row['customer_id'],
            'restaurant_id': row['restaurant_id'],
            'order_amount': row['order_amount'],
            'order_time': row['order_time']
        }
        producer.send('delivery_orders', message)
    
    producer.flush()
```

#### 2.3 데이터 컨슈머 개발
```python
from kafka import KafkaConsumer
import json

def create_consumer():
    return KafkaConsumer(
        'delivery_orders',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

def process_messages():
    consumer = create_consumer()
    for message in consumer:
        # 데이터 처리 로직
        process_order_data(message.value)
```

### Phase 3: Airflow 워크플로우 구축 (1주)

#### 3.1 Airflow 환경 설정 (Windows)
```bash
# Airflow 설치
pip install apache-airflow

# Airflow 초기화 (Windows)
set AIRFLOW_HOME=C:\airflow
airflow db init
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
```

#### 3.2 DAG (Directed Acyclic Graph) 설계
```python
# 예시 DAG 코드
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_scientist',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'delivery_data_pipeline',
    default_args=default_args,
    description='배달 데이터 처리 파이프라인',
    schedule_interval=timedelta(hours=1),
)

def extract_data():
    # 데이터 추출 로직
    pass

def transform_data():
    # 데이터 변환 로직
    pass

def load_data():
    # 데이터 로드 로직
    pass

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

extract_task >> transform_task >> load_task
```

### Phase 4: Redis + PostgreSQL 데이터베이스 설계 및 구축 (1주)

#### 4.1 Redis 설정 (Windows)
```bash
# Redis for Windows 설치
# https://github.com/microsoftarchive/redis/releases 에서 다운로드
# 또는 Docker 사용
docker run -d -p 6379:6379 redis:latest
```

#### 4.2 Redis 데이터 구조 설계
```python
import redis
import json

# Redis 연결
r = redis.Redis(host='localhost', port=6379, db=0)

# 실시간 주문 데이터 캐싱
def cache_order_data(order_data):
    r.setex(f"order:{order_data['order_id']}", 3600, json.dumps(order_data))

# 고객 세션 데이터 저장
def store_customer_session(customer_id, session_data):
    r.hset(f"customer:{customer_id}", mapping=session_data)

# 실시간 통계 데이터
def update_realtime_stats(stats_data):
    r.hset("realtime_stats", mapping=stats_data)
```

#### 4.3 PostgreSQL 데이터베이스 스키마 설계
```sql
-- 예시 스키마
CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    restaurant_id VARCHAR(50),
    order_amount DECIMAL(10,2),
    order_time TIMESTAMP,
    delivery_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(100),
    phone_number VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE restaurants (
    restaurant_id VARCHAR(50) PRIMARY KEY,
    restaurant_name VARCHAR(100),
    category VARCHAR(50),
    rating DECIMAL(3,2),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    order_id VARCHAR(50),
    item_name VARCHAR(100),
    quantity INT,
    price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
```

#### 4.4 데이터 적재 스크립트 개발
```python
import psycopg2
import pandas as pd
import redis
import json

def load_data_to_db():
    # PostgreSQL 연결
    conn = psycopg2.connect(
        host="localhost",
        database="delivery_db",
        user="postgres",
        password="password"
    )
    
    # Redis 연결
    r = redis.Redis(host='localhost', port=6379, db=0)
    
    # 데이터 로드
    df = pd.read_csv('processed_data.csv')
    
    # PostgreSQL에 삽입
    for _, row in df.iterrows():
        # INSERT 로직
        pass
    
    # Redis에 캐시
    for _, row in df.iterrows():
        cache_data = {
            'order_id': row['order_id'],
            'amount': row['order_amount'],
            'timestamp': row['order_time']
        }
        r.setex(f"order:{row['order_id']}", 3600, json.dumps(cache_data))
    
    conn.close()
```

### Phase 5: 웹 서비스 개발 (2주)

#### 5.1 Flask/FastAPI 애플리케이션 구조
```
web_service/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── templates/
├── static/
├── tests/
├── requirements.txt
└── main.py
```

#### 5.2 Redis 통합 웹 서비스
```python
# 예시 FastAPI 코드
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import redis
import json

app = FastAPI()

# Redis 연결
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/")
async def home():
    return {"message": "배달의민족 데이터 분석 대시보드"}

@app.get("/analytics/order-trends")
async def get_order_trends():
    # Redis에서 실시간 데이터 조회
    realtime_data = redis_client.hgetall("realtime_stats")
    # 주문 트렌드 분석
    # 시간대별, 요일별, 월별 주문 패턴
    pass

@app.get("/analytics/customer-segments")
async def get_customer_segments():
    # 고객 세분화 분석
    # RFM 분석, 고객 생애 가치 분석
    pass

@app.get("/analytics/restaurant-performance")
async def get_restaurant_performance():
    # 가게 성과 분석
    # 매출, 평점, 주문량 분석
    pass

@app.get("/analytics/delivery-optimization")
async def get_delivery_optimization():
    # 배달 최적화 분석
    # 배달 시간, 거리, 비용 분석
    pass

@app.get("/cache/order/{order_id}")
async def get_cached_order(order_id: str):
    # Redis에서 주문 데이터 조회
    cached_data = redis_client.get(f"order:{order_id}")
    if cached_data:
        return json.loads(cached_data)
    else:
        raise HTTPException(status_code=404, detail="Order not found in cache")
```

#### 5.3 대시보드 구현
- **주문 트렌드 대시보드**: 시간대별, 요일별 주문 패턴
- **고객 분석 대시보드**: 고객 세분화, 생애 가치 분석
- **가게 성과 대시보드**: 매출, 평점, 인기도 분석
- **배달 최적화 대시보드**: 배달 시간, 거리, 비용 분석
- **실시간 모니터링**: Redis를 통한 실시간 데이터 표시

### Phase 6: Docker 컨테이너화 (1주)

#### 6.1 Dockerfile 작성
```dockerfile
# 예시 Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 6.2 Docker Compose 설정 (Redis 포함)
```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
      - kafka
  
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: delivery_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:latest
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
  
  kafka:
    image: confluentinc/cp-kafka:latest
    depends_on:
      - zookeeper
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
  
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

volumes:
  postgres_data:
  redis_data:
```

### Phase 7: Kubernetes 배포 (1주)

#### 7.1 Kubernetes 매니페스트 작성
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: delivery-analytics
spec:
  replicas: 3
  selector:
    matchLabels:
      app: delivery-analytics
  template:
    metadata:
      labels:
        app: delivery-analytics
    spec:
      containers:
      - name: web-app
        image: delivery-analytics:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          value: "postgresql://postgres:password@db:5432/delivery_db"
        - name: REDIS_URL
          value: "redis://redis:6379"
```

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: delivery-analytics-service
spec:
  selector:
    app: delivery-analytics
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

#### 7.2 Helm Chart 구성 (선택사항)
```bash
# Helm Chart 생성
helm create delivery-analytics
```

### Phase 8: AWS 클라우드 배포 (1주)

#### 8.1 AWS 서비스 선택
- **EC2**: 웹 서버 호스팅
- **RDS**: PostgreSQL 데이터베이스
- **ElastiCache**: Redis 캐시
- **EKS**: Kubernetes 클러스터
- **S3**: 데이터 저장소
- **CloudWatch**: 모니터링

#### 8.2 AWS 배포 스크립트
```bash
# AWS CLI 설정
aws configure

# EKS 클러스터 생성
eksctl create cluster --name delivery-cluster --region us-west-2

# 애플리케이션 배포
kubectl apply -f k8s/
```

## 📊 데이터 사이언티스트 관점의 분석 과제

### 1. 고객 행동 분석
- **RFM 분석**: Recency, Frequency, Monetary 분석
- **고객 생애 가치 (CLV)**: 고객별 예상 수익 분석
- **고객 세분화**: 행동 패턴에 따른 고객 그룹 분류

### 2. 가게 성과 분석
- **매출 분석**: 시간대별, 요일별 매출 패턴
- **메뉴 분석**: 인기 메뉴, 조합 분석
- **평점 분석**: 고객 만족도 분석

### 3. 배달 최적화 분석
- **배달 시간 분석**: 평균 배달 시간, 지연 요인 분석
- **배달 거리 분석**: 거리별 배달료, 시간 분석
- **배달 경로 최적화**: 효율적인 배달 경로 제안

### 4. 예측 모델링
- **주문량 예측**: 시간대별, 요일별 주문량 예측
- **고객 이탈 예측**: 다음 주문 가능성 예측
- **가게 성과 예측**: 매출, 평점 예측

### 5. 실시간 분석 (Redis 활용)
- **실시간 주문 모니터링**: 현재 진행 중인 주문 추적
- **실시간 통계**: 현재 시간의 주문량, 매출 등
- **실시간 알림**: 특정 조건 달성 시 알림

## 🛠️ 기술 스택 학습 가이드

### 필수 기술
1. **Python**: 데이터 분석, 웹 개발
2. **SQL**: 데이터베이스 쿼리, 데이터 관리
3. **Redis**: 캐싱, 실시간 데이터 처리
4. **Docker**: 컨테이너화
5. **Kubernetes**: 오케스트레이션
6. **AWS**: 클라우드 서비스

### 추가 학습 권장사항
1. **Apache Spark**: 대용량 데이터 처리
2. **Elasticsearch**: 로그 분석
3. **Grafana**: 모니터링 대시보드
4. **Prometheus**: 메트릭 수집

## 📈 성과 측정 지표

### 기술적 지표
- 데이터 처리 속도 (records/second)
- API 응답 시간 (ms)
- Redis 캐시 히트율 (%)
- 시스템 가용성 (%)
- 에러율 (%)

### 비즈니스 지표
- 일일 활성 사용자 수
- 평균 세션 시간
- 페이지 뷰 수
- 사용자 만족도
- 실시간 주문 처리량

## 🚀 프로젝트 완료 후 다음 단계

### 1. 고급 분석
- **머신러닝 모델**: 추천 시스템, 이상 탐지
- **실시간 분석**: 스트리밍 데이터 실시간 처리
- **A/B 테스트**: 기능 개선 효과 측정

### 2. 확장성 개선
- **마이크로서비스**: 서비스 분리
- **로드 밸런싱**: 트래픽 분산
- **캐싱**: Redis를 통한 성능 최적화

### 3. 모니터링 및 운영
- **로깅**: 시스템 로그 수집
- **알림**: 장애 알림 시스템
- **백업**: 데이터 백업 전략

## 💡 학습 팁

### 1. 단계별 접근
- 각 단계를 완료한 후 다음 단계로 진행
- 각 단계에서 문제가 발생하면 충분히 해결 후 진행

### 2. 문서화
- 코드 주석 작성
- README 파일 업데이트
- 기술 블로그 작성

### 3. 커뮤니티 활용
- GitHub: 코드 공유 및 피드백
- Stack Overflow: 문제 해결
- 기술 블로그: 학습 내용 정리

### 4. 실무 경험
- 실제 기업 프로젝트와 유사한 환경 구성
- 실제 데이터로 작업하여 실무 감각 습득
- 팀 프로젝트로 진행하여 협업 경험

## 📚 참고 자료

### 도서
- "데이터 사이언스 핸드북" - Jake VanderPlas
- "Designing Data-Intensive Applications" - Martin Kleppmann
- "Kubernetes in Action" - Marko Lukša
- "Redis in Action" - Josiah L. Carlson

### 온라인 강의
- Coursera: Data Science Specialization
- Udemy: Apache Kafka Series
- AWS Training: Cloud Practitioner
- Redis University: Redis Courses

### 기술 문서
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Redis Documentation](https://redis.io/documentation)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [AWS Documentation](https://docs.aws.amazon.com/)

---

**이 가이드를 따라 프로젝트를 진행하면서 실제 데이터 사이언티스트의 업무 환경을 체험하고, 현대적인 기술 스택을 습득할 수 있습니다. 각 단계에서 어려움이 있으면 충분히 학습하고 해결한 후 다음 단계로 진행하세요!** 🚀
