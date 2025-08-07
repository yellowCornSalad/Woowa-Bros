"""
비정형 데이터 추출 도구
배달의민족 데이터에서 다양한 형태의 비정형 데이터를 추출하고 처리합니다.
"""

import os
import json
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
from datetime import datetime
import logging
from typing import Dict, List, Any, Optional
import redis
import psycopg2
from sqlalchemy import create_engine
import requests
from bs4 import BeautifulSoup
import re

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataExtractor:
    """비정형 데이터 추출 클래스"""
    
    def __init__(self, data_dir: str = "data", output_dir: str = "extracted_data"):
        """
        초기화
        
        Args:
            data_dir: 원본 데이터 디렉토리
            output_dir: 추출된 데이터 저장 디렉토리
        """
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.redis_client = None
        self.db_engine = None
        
        # 출력 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info(f"DataExtractor 초기화 완료 - 데이터 디렉토리: {data_dir}")
    
    def setup_redis(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        """Redis 연결 설정"""
        try:
            self.redis_client = redis.Redis(host=host, port=port, db=db)
            self.redis_client.ping()
            logger.info("Redis 연결 성공")
        except Exception as e:
            logger.warning(f"Redis 연결 실패: {e}")
    
    def setup_database(self, connection_string: str):
        """데이터베이스 연결 설정"""
        try:
            self.db_engine = create_engine(connection_string)
            logger.info("데이터베이스 연결 성공")
        except Exception as e:
            logger.warning(f"데이터베이스 연결 실패: {e}")
    
    def extract_csv_data(self, filename: str) -> pd.DataFrame:
        """CSV 데이터 추출"""
        try:
            filepath = os.path.join(self.data_dir, filename)
            df = pd.read_csv(filepath)
            logger.info(f"CSV 데이터 추출 완료: {filename} - {df.shape}")
            return df
        except Exception as e:
            logger.error(f"CSV 데이터 추출 실패: {filename} - {e}")
            return pd.DataFrame()
    
    def extract_json_data(self, filename: str) -> List[Dict]:
        """JSON 데이터 추출"""
        try:
            filepath = os.path.join(self.data_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"JSON 데이터 추출 완료: {filename} - {len(data)}개 항목")
            return data
        except Exception as e:
            logger.error(f"JSON 데이터 추출 실패: {filename} - {e}")
            return []
    
    def extract_xml_data(self, filename: str) -> List[Dict]:
        """XML 데이터 추출"""
        try:
            filepath = os.path.join(self.data_dir, filename)
            tree = ET.parse(filepath)
            root = tree.getroot()
            
            data = []
            for element in root.iter():
                if element.text and element.text.strip():
                    data.append({
                        'tag': element.tag,
                        'text': element.text.strip(),
                        'attributes': dict(element.attrib)
                    })
            
            logger.info(f"XML 데이터 추출 완료: {filename} - {len(data)}개 항목")
            return data
        except Exception as e:
            logger.error(f"XML 데이터 추출 실패: {filename} - {e}")
            return []
    
    def extract_log_data(self, filename: str) -> List[Dict]:
        """로그 데이터 추출"""
        try:
            filepath = os.path.join(self.data_dir, filename)
            log_data = []
            
            with open(filepath, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    # 로그 패턴 분석
                    log_entry = self._parse_log_line(line, line_num)
                    if log_entry:
                        log_data.append(log_entry)
            
            logger.info(f"로그 데이터 추출 완료: {filename} - {len(log_data)}개 항목")
            return log_data
        except Exception as e:
            logger.error(f"로그 데이터 추출 실패: {filename} - {e}")
            return []
    
    def _parse_log_line(self, line: str, line_num: int) -> Optional[Dict]:
        """로그 라인 파싱"""
        try:
            # 기본 로그 패턴 (수정 가능)
            patterns = [
                r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (\w+): (.+)',
                r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (\w+) - (.+)',
                r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (\w+): (.+)'
            ]
            
            for pattern in patterns:
                match = re.match(pattern, line.strip())
                if match:
                    groups = match.groups()
                    return {
                        'line_number': line_num,
                        'timestamp': groups[0],
                        'level': groups[1] if len(groups) > 1 else 'INFO',
                        'message': groups[-1],
                        'raw_line': line.strip()
                    }
            
            # 패턴이 맞지 않으면 기본 정보만 반환
            return {
                'line_number': line_num,
                'timestamp': None,
                'level': 'UNKNOWN',
                'message': line.strip(),
                'raw_line': line.strip()
            }
        except Exception as e:
            logger.warning(f"로그 라인 파싱 실패 (라인 {line_num}): {e}")
            return None
    
    def extract_pickle_data(self, filename: str) -> Any:
        """Pickle 데이터 추출"""
        try:
            import pickle
            filepath = os.path.join(self.data_dir, filename)
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            logger.info(f"Pickle 데이터 추출 완료: {filename}")
            return data
        except Exception as e:
            logger.error(f"Pickle 데이터 추출 실패: {filename} - {e}")
            return None
    
    def process_text_data(self, text_data: List[str]) -> Dict[str, Any]:
        """텍스트 데이터 처리 및 분석"""
        try:
            # 기본 텍스트 통계
            total_chars = sum(len(text) for text in text_data)
            total_words = sum(len(text.split()) for text in text_data)
            avg_length = total_chars / len(text_data) if text_data else 0
            
            # 단어 빈도 분석
            word_freq = {}
            for text in text_data:
                words = text.lower().split()
                for word in words:
                    word = re.sub(r'[^\w\s]', '', word)
                    if word:
                        word_freq[word] = word_freq.get(word, 0) + 1
            
            # 상위 10개 단어
            top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            
            return {
                'total_texts': len(text_data),
                'total_chars': total_chars,
                'total_words': total_words,
                'avg_length': avg_length,
                'unique_words': len(word_freq),
                'top_words': top_words,
                'word_frequency': word_freq
            }
        except Exception as e:
            logger.error(f"텍스트 데이터 처리 실패: {e}")
            return {}
    
    def save_to_redis(self, key: str, data: Any, expire_time: int = 3600):
        """Redis에 데이터 저장"""
        if not self.redis_client:
            logger.warning("Redis가 설정되지 않았습니다.")
            return
        
        try:
            if isinstance(data, (pd.DataFrame, pd.Series)):
                data_json = data.to_json(orient='records')
            else:
                data_json = json.dumps(data, ensure_ascii=False, default=str)
            
            self.redis_client.setex(key, expire_time, data_json)
            logger.info(f"Redis에 데이터 저장 완료: {key}")
        except Exception as e:
            logger.error(f"Redis 저장 실패: {key} - {e}")
    
    def save_to_database(self, table_name: str, data: pd.DataFrame):
        """데이터베이스에 데이터 저장"""
        if self.db_engine is None:
            logger.warning("데이터베이스가 설정되지 않았습니다.")
            return
        
        try:
            data.to_sql(table_name, self.db_engine, if_exists='replace', index=False)
            logger.info(f"데이터베이스에 데이터 저장 완료: {table_name}")
        except Exception as e:
            logger.error(f"데이터베이스 저장 실패: {table_name} - {e}")
    
    def save_to_file(self, data: Any, filename: str, format: str = 'json'):
        """파일로 데이터 저장"""
        try:
            filepath = os.path.join(self.output_dir, filename)
            
            if format == 'json':
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            elif format == 'csv':
                if isinstance(data, pd.DataFrame):
                    data.to_csv(filepath, index=False, encoding='utf-8')
                else:
                    pd.DataFrame(data).to_csv(filepath, index=False, encoding='utf-8')
            elif format == 'pickle':
                import pickle
                with open(filepath, 'wb') as f:
                    pickle.dump(data, f)
            
            logger.info(f"파일 저장 완료: {filepath}")
        except Exception as e:
            logger.error(f"파일 저장 실패: {filename} - {e}")
    
    def extract_all_data(self) -> Dict[str, Any]:
        """모든 데이터 파일 추출"""
        results = {}
        
        # 데이터 파일 목록
        data_files = [
            ('배달의민족_가명데이터_10만건.csv', 'csv'),
            ('배달의민족_메시지_데이터_25000건.json', 'json'),
            ('배달의민족_JSON_데이터_25000건.json', 'json'),
            ('배달의민족_XML_데이터_25000건.xml', 'xml'),
            ('배달의민족_로그_데이터_25000건.log', 'log'),
            ('배달의민족_통합_비정형데이터_10만건.pickle', 'pickle')
        ]
        
        for filename, file_type in data_files:
            try:
                if file_type == 'csv':
                    data = self.extract_csv_data(filename)
                    results[filename] = {
                        'type': 'csv',
                        'data': data,
                        'shape': data.shape if not data.empty else (0, 0)
                    }
                elif file_type == 'json':
                    data = self.extract_json_data(filename)
                    results[filename] = {
                        'type': 'json',
                        'data': data,
                        'count': len(data)
                    }
                elif file_type == 'xml':
                    data = self.extract_xml_data(filename)
                    results[filename] = {
                        'type': 'xml',
                        'data': data,
                        'count': len(data)
                    }
                elif file_type == 'log':
                    data = self.extract_log_data(filename)
                    results[filename] = {
                        'type': 'log',
                        'data': data,
                        'count': len(data)
                    }
                elif file_type == 'pickle':
                    data = self.extract_pickle_data(filename)
                    results[filename] = {
                        'type': 'pickle',
                        'data': data,
                        'data_type': type(data).__name__
                    }
                
                # Redis에 저장
                self.save_to_redis(f"extracted_{filename}", results[filename])
                
                # 파일로 저장
                self.save_to_file(results[filename], f"extracted_{filename}.json")
                
            except Exception as e:
                logger.error(f"데이터 추출 실패: {filename} - {e}")
                results[filename] = {
                    'type': file_type,
                    'error': str(e),
                    'data': None
                }
        
        return results
    
    def generate_summary_report(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """추출 결과 요약 리포트 생성"""
        summary = {
            'extraction_time': datetime.now().isoformat(),
            'total_files': len(results),
            'successful_extractions': 0,
            'failed_extractions': 0,
            'file_types': {},
            'total_records': 0,
            'data_sizes': {}
        }
        
        for filename, result in results.items():
            if 'error' in result:
                summary['failed_extractions'] += 1
            else:
                summary['successful_extractions'] += 1
                file_type = result['type']
                summary['file_types'][file_type] = summary['file_types'].get(file_type, 0) + 1
                
                if 'count' in result:
                    summary['total_records'] += result['count']
                elif 'shape' in result:
                    summary['total_records'] += result['shape'][0]
        
        return summary


def main():
    """메인 실행 함수"""
    # DataExtractor 초기화
    extractor = DataExtractor()
    
    # Redis 설정 (선택사항)
    extractor.setup_redis()
    
    # 데이터베이스 설정 (선택사항)
    # extractor.setup_database("postgresql://user:password@localhost/dbname")
    
    # 모든 데이터 추출
    results = extractor.extract_all_data()
    
    # 요약 리포트 생성
    summary = extractor.generate_summary_report(results)
    
    # 요약 리포트 저장
    extractor.save_to_file(summary, "extraction_summary.json")
    
    print("데이터 추출 완료!")
    print(f"총 파일 수: {summary['total_files']}")
    print(f"성공: {summary['successful_extractions']}")
    print(f"실패: {summary['failed_extractions']}")
    print(f"총 레코드 수: {summary['total_records']}")


if __name__ == "__main__":
    main()
