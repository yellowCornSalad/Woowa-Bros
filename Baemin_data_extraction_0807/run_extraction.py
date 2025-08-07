#!/usr/bin/env python3
"""
데이터 추출 실행 스크립트
배달의민족 비정형 데이터를 추출하고 분석합니다.
"""

import os
import sys
import json
import argparse
from datetime import datetime
import logging

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_extraction.data_extractor import DataExtractor
from data_extraction.text_analyzer import TextAnalyzer

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('extraction.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def setup_environment():
    """환경 설정"""
    # 필요한 디렉토리 생성
    directories = ['extracted_data', 'reports', 'visualizations']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    logger.info("환경 설정 완료")


def run_data_extraction():
    """데이터 추출 실행"""
    logger.info("데이터 추출 시작")
    
    # DataExtractor 초기화
    extractor = DataExtractor()
    
    # Redis 설정 (선택사항)
    try:
        extractor.setup_redis()
        logger.info("Redis 연결 성공")
    except Exception as e:
        logger.warning(f"Redis 연결 실패: {e}")
    
    # 모든 데이터 추출
    results = extractor.extract_all_data()
    
    # 요약 리포트 생성
    summary = extractor.generate_summary_report(results)
    
    # 요약 리포트 저장
    extractor.save_to_file(summary, "extraction_summary.json")
    
    logger.info("데이터 추출 완료")
    return results, summary


def run_text_analysis(results):
    """텍스트 분석 실행"""
    logger.info("텍스트 분석 시작")
    
    # TextAnalyzer 초기화
    analyzer = TextAnalyzer(language='korean')
    
    # 메시지 데이터 분석
    message_files = [
        '배달의민족_메시지_데이터_25000건.json',
        '배달의민족_JSON_데이터_25000건.json'
    ]
    
    all_texts = []
    all_messages = []
    
    for filename in message_files:
        if filename in results and 'data' in results[filename]:
            data = results[filename]['data']
            
            # 텍스트 추출
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        text = item.get('text', item.get('message', ''))
                        if text:
                            all_texts.append(text)
                            all_messages.append(item)
    
    if all_texts:
        # 키워드 추출
        keywords = analyzer.extract_keywords(all_texts, top_n=50)
        
        # 메시지 패턴 분석
        message_analysis = analyzer.analyze_message_patterns(all_messages)
        
        # 워드클라우드 생성
        try:
            wordcloud = analyzer.generate_wordcloud(
                all_texts, 
                'visualizations/wordcloud.png'
            )
            logger.info("워드클라우드 생성 완료")
        except Exception as e:
            logger.warning(f"워드클라우드 생성 실패: {e}")
        
        # 분석 결과 저장
        analysis_results = {
            'keywords': keywords,
            'message_analysis': message_analysis,
            'total_texts': len(all_texts),
            'analysis_time': datetime.now().isoformat()
        }
        
        with open('reports/text_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, ensure_ascii=False, indent=2, default=str)
        
        # 리포트 생성
        report = analyzer.generate_report(message_analysis)
        with open('reports/text_analysis_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info("텍스트 분석 완료")
        return analysis_results
    
    return None


def run_log_analysis(results):
    """로그 데이터 분석"""
    logger.info("로그 분석 시작")
    
    log_file = '배달의민족_로그_데이터_25000건.log'
    if log_file in results and 'data' in results[log_file]:
        log_data = results[log_file]['data']
        
        # 로그 레벨별 분석
        level_counts = {}
        time_patterns = {}
        error_messages = []
        
        for log_entry in log_data:
            level = log_entry.get('level', 'UNKNOWN')
            level_counts[level] = level_counts.get(level, 0) + 1
            
            # 시간 패턴 분석
            timestamp = log_entry.get('timestamp')
            if timestamp:
                try:
                    hour = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).hour
                    time_patterns[hour] = time_patterns.get(hour, 0) + 1
                except:
                    pass
            
            # 에러 메시지 수집
            if level in ['ERROR', 'CRITICAL']:
                error_messages.append(log_entry.get('message', ''))
        
        log_analysis = {
            'total_logs': len(log_data),
            'level_distribution': level_counts,
            'time_patterns': time_patterns,
            'error_count': len(error_messages),
            'top_errors': error_messages[:10]
        }
        
        # 분석 결과 저장
        with open('reports/log_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(log_analysis, f, ensure_ascii=False, indent=2, default=str)
        
        logger.info("로그 분석 완료")
        return log_analysis
    
    return None


def generate_final_report(results, summary, text_analysis=None, log_analysis=None):
    """최종 리포트 생성"""
    logger.info("최종 리포트 생성")
    
    report = {
        'extraction_summary': summary,
        'text_analysis': text_analysis,
        'log_analysis': log_analysis,
        'generated_at': datetime.now().isoformat(),
        'file_statistics': {}
    }
    
    # 파일별 통계
    for filename, result in results.items():
        if 'error' not in result:
            if 'count' in result:
                report['file_statistics'][filename] = {
                    'type': result['type'],
                    'records': result['count']
                }
            elif 'shape' in result:
                report['file_statistics'][filename] = {
                    'type': result['type'],
                    'shape': result['shape']
                }
    
    # 리포트 저장
    with open('reports/final_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    
    # 텍스트 리포트 생성
    text_report = []
    text_report.append("=" * 60)
    text_report.append("배달의민족 데이터 추출 및 분석 리포트")
    text_report.append("=" * 60)
    text_report.append(f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    text_report.append("")
    
    text_report.append("📊 추출 요약")
    text_report.append(f"- 총 파일 수: {summary['total_files']}")
    text_report.append(f"- 성공: {summary['successful_extractions']}")
    text_report.append(f"- 실패: {summary['failed_extractions']}")
    text_report.append(f"- 총 레코드 수: {summary['total_records']:,}")
    text_report.append("")
    
    text_report.append("📁 파일별 통계")
    for filename, stats in report['file_statistics'].items():
        if 'records' in stats:
            text_report.append(f"- {filename}: {stats['records']:,}개 레코드")
        elif 'shape' in stats:
            text_report.append(f"- {filename}: {stats['shape'][0]:,}행 x {stats['shape'][1]}열")
    text_report.append("")
    
    if text_analysis:
        text_report.append("📝 텍스트 분석 결과")
        text_report.append(f"- 분석된 텍스트: {text_analysis['total_texts']:,}개")
        text_report.append(f"- 주요 키워드 수: {len(text_analysis['keywords'])}개")
        if 'message_analysis' in text_analysis:
            msg_analysis = text_analysis['message_analysis']
            text_report.append(f"- 평균 메시지 길이: {msg_analysis.get('avg_message_length', 0):.1f}자")
            text_report.append(f"- 평균 감정 점수: {msg_analysis.get('avg_sentiment', 0):.3f}")
    text_report.append("")
    
    if log_analysis:
        text_report.append("📋 로그 분석 결과")
        text_report.append(f"- 총 로그 수: {log_analysis['total_logs']:,}개")
        text_report.append(f"- 에러 수: {log_analysis['error_count']:,}개")
        text_report.append("- 로그 레벨 분포:")
        for level, count in log_analysis['level_distribution'].items():
            text_report.append(f"  * {level}: {count:,}개")
    text_report.append("")
    
    text_report.append("🎯 다음 단계")
    text_report.append("1. 추출된 데이터를 Kafka로 스트리밍")
    text_report.append("2. Airflow를 통한 데이터 파이프라인 구축")
    text_report.append("3. Redis에 실시간 데이터 캐싱")
    text_report.append("4. PostgreSQL에 구조화된 데이터 저장")
    text_report.append("5. 웹 서비스 개발 및 배포")
    text_report.append("")
    
    text_report.append("=" * 60)
    
    with open('reports/final_report.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(text_report))
    
    logger.info("최종 리포트 생성 완료")


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='배달의민족 데이터 추출 및 분석')
    parser.add_argument('--skip-text-analysis', action='store_true', 
                       help='텍스트 분석 건너뛰기')
    parser.add_argument('--skip-log-analysis', action='store_true', 
                       help='로그 분석 건너뛰기')
    parser.add_argument('--redis-host', default='localhost', 
                       help='Redis 호스트')
    parser.add_argument('--redis-port', type=int, default=6379, 
                       help='Redis 포트')
    
    args = parser.parse_args()
    
    try:
        # 환경 설정
        setup_environment()
        
        # 데이터 추출
        results, summary = run_data_extraction()
        
        # 텍스트 분석
        text_analysis = None
        if not args.skip_text_analysis:
            text_analysis = run_text_analysis(results)
        
        # 로그 분석
        log_analysis = None
        if not args.skip_log_analysis:
            log_analysis = run_log_analysis(results)
        
        # 최종 리포트 생성
        generate_final_report(results, summary, text_analysis, log_analysis)
        
        print("\n" + "=" * 50)
        print("✅ 데이터 추출 및 분석 완료!")
        print("=" * 50)
        print(f"📊 총 파일 수: {summary['total_files']}")
        print(f"✅ 성공: {summary['successful_extractions']}")
        print(f"❌ 실패: {summary['failed_extractions']}")
        print(f"📈 총 레코드 수: {summary['total_records']:,}")
        print("\n📁 결과 파일 위치:")
        print("- 추출된 데이터: extracted_data/")
        print("- 분석 리포트: reports/")
        print("- 시각화: visualizations/")
        print("\n🚀 다음 단계: README.md의 Phase 2부터 진행하세요!")
        
    except Exception as e:
        logger.error(f"실행 중 오류 발생: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
