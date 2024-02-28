# Python 베이스 이미지 사용
FROM python:3.10-slim
 
# 작업 디렉토리 설정
WORKDIR /app
 
# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# 스크립트 파일 복사
COPY stats-exporter.py  .
 
# 스크립트 실행
CMD ["python", "./stats-exporter.py"]