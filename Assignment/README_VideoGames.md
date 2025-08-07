# 게임 데이터 분석 대시보드

비디오 게임 산업의 성공 요인을 데이터로 분석한 통계 프로젝트를 웹 대시보드로 구현한 프로젝트입니다.

## 프로젝트 개요

이 프로젝트는 2004년부터 2010년까지 출시된 비디오 게임들의 데이터를 분석하여 게임 산업의 성공 요인을 파악하는 것을 목표로 합니다. Dr. Joe Cox가 수집한 데이터셋을 기반으로 하여, 게임 장르, 리뷰 점수, 출시 연도, 중고가격 등의 다양한 변수들이 게임의 매출 성과에 미치는 영향을 분석합니다.

## 프로젝트 구성

### 프로젝트 1: 게임 장르별 매출 분석
- **목표**: 비디오 게임 장르가 매출 성과에 미치는 영향 분석
- **방법**: 장르별 총 매출과 평균 매출 비교 분석
- **결과**: Action 장르의 우위, Educational/Sports 장르의 높은 평균 매출 발견

### 프로젝트 2: 통계적 추론
- **목표**: 신뢰구간과 가설검정을 통한 통계적 분석
- **방법**: Platform 게임 비율의 신뢰구간, Action vs Platform 장르 간 매출 차이 가설검정
- **결과**: 부트스트랩 방법을 사용한 통계적 추론 수행

### 프로젝트 3: 머신러닝 모델링
- **목표**: 선형회귀와 로지스틱 회귀를 통한 게임 매출 예측
- **방법**: 리뷰 점수, 출시 연도, 중고가격을 변수로 한 예측 모델 구축
- **결과**: 매출 예측 및 성공 가능성 분류 모델 개발

## 기술 스택

- **Backend**: Python, Flask
- **Data Analysis**: Pandas, NumPy, Matplotlib, Seaborn
- **Machine Learning**: Scikit-learn, Statsmodels
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Docker, Kubernetes (예정)

## 설치 및 실행

### 로컬 실행

1. 저장소 클론
```bash
git clone <repository-url>
cd WooIn
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 패키지 설치
```bash
pip install -r requirements.txt
```

4. 애플리케이션 실행
```bash
python app.py
```

5. 브라우저에서 접속
```
http://localhost:5000
```

### Docker 실행

1. Docker 이미지 빌드
```bash
docker build -t game-analysis-dashboard .
```

2. 컨테이너 실행
```bash
docker run -p 5000:5000 game-analysis-dashboard
```

3. 브라우저에서 접속
```
http://localhost:5000
```

## 프로젝트 구조

```
WooIn/
├── app.py                 # Flask 애플리케이션 메인 파일
├── requirements.txt       # Python 패키지 의존성
├── Dockerfile            # Docker 설정 파일
├── README.md             # 프로젝트 설명서
├── templates/            # HTML 템플릿
│   ├── base.html        # 기본 템플릿
│   ├── index.html       # 메인 페이지
│   ├── project1.html    # 프로젝트 1 페이지
│   ├── project2.html    # 프로젝트 2 페이지
│   └── project3.html    # 프로젝트 3 페이지
├── static/              # 정적 파일
│   ├── css/            # CSS 파일
│   └── js/             # JavaScript 파일
└── data/               # 데이터 파일 (선택사항)
    └── video_games.csv # 게임 데이터
```

## 주요 기능

### 대시보드
- 프로젝트별 분석 결과 시각화
- 인터랙티브 차트 및 그래프
- 반응형 웹 디자인

### 데이터 분석
- 장르별 매출 분석
- 통계적 추론 (신뢰구간, 가설검정)
- 머신러닝 모델링 (선형회귀, 로지스틱 회귀)

### 시각화
- Matplotlib과 Seaborn을 사용한 차트 생성
- Base64 인코딩을 통한 이미지 표시
- 반응형 차트 레이아웃

## 분석 결과 요약

### 프로젝트 1: 게임 장르별 매출 분석
- Action 장르가 전체 매출에서 가장 높은 비중 차지
- Educational/Sports 장르가 게임당 평균 매출에서 우수한 성과
- 플랫폼별 장르 선호도 차이 확인

### 프로젝트 2: 통계적 추론
- Platform 게임의 비율에 대한 95% 신뢰구간 계산
- Action과 Platform 장르 간 매출 차이 가설검정
- 부트스트랩 방법을 사용한 통계적 추론

### 프로젝트 3: 머신러닝 모델링
- 선형회귀 모델로 매출 예측 (R² 점수 확인)
- 로지스틱 회귀 모델로 성공 가능성 분류 (AUC 점수 확인)
- 모델 성능 평가 및 개선 방향 제시

## 향후 계획

- [ ] Kubernetes 배포 설정
- [ ] 추가 데이터셋 분석
- [ ] 고급 머신러닝 모델 적용
- [ ] 실시간 데이터 업데이트 기능
- [ ] 사용자 인터랙션 기능 추가

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 기여

프로젝트에 기여하고 싶으시면 Pull Request를 보내주세요.

## 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해주세요. 