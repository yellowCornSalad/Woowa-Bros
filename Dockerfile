FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
COPY . .

# 포트 노출
EXPOSE 5000

# 환경 변수 설정
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 애플리케이션 실행
CMD ["python", "app.py"] 