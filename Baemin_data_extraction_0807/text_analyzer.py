"""
텍스트 데이터 분석 도구
배달의민족 메시지 데이터에서 텍스트 분석을 수행합니다.
"""

import re
import json
import pandas as pd
import numpy as np
from collections import Counter, defaultdict
from typing import Dict, List, Any, Tuple
import logging
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import jieba
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# NLTK 데이터 다운로드 (최초 실행 시)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

logger = logging.getLogger(__name__)


class TextAnalyzer:
    """텍스트 데이터 분석 클래스"""
    
    def __init__(self, language: str = 'korean'):
        """
        초기화
        
        Args:
            language: 분석할 언어 ('korean', 'english')
        """
        self.language = language
        self.stop_words = set()
        self.lemmatizer = WordNetLemmatizer()
        
        # 언어별 설정
        if language == 'english':
            self.stop_words = set(stopwords.words('english'))
        elif language == 'korean':
            # 한국어 불용어 설정
            self.stop_words = {
                '이', '그', '저', '것', '수', '등', '들', '때', '곳', '말', '일',
                '또', '더', '많', '적', '가', '나', '다', '라', '마', '바', '사',
                '아', '자', '차', '카', '타', '파', '하', '거', '너', '더', '러',
                '머', '버', '서', '어', '저', '거', '너', '더', '러', '머', '버',
                '서', '어', '저', '고', '는', '을', '를', '이', '가', '의', '에',
                '로', '으로', '와', '과', '도', '만', '부터', '까지', '에서', '에게',
                '께서', '한테', '에게서', '로부터', '로서', '로써', '같이', '처럼',
                '만큼', '만치', '쯤', '정도', '쯤', '쯤', '쯤', '쯤', '쯤'
            }
        
        logger.info(f"TextAnalyzer 초기화 완료 - 언어: {language}")
    
    def preprocess_text(self, text: str) -> str:
        """텍스트 전처리"""
        if not text:
            return ""
        
        # 소문자 변환 (영어의 경우)
        if self.language == 'english':
            text = text.lower()
        
        # 특수문자 제거 (한국어의 경우 일부 보존)
        if self.language == 'korean':
            text = re.sub(r'[^\w\s가-힣]', ' ', text)
        else:
            text = re.sub(r'[^\w\s]', ' ', text)
        
        # 여러 공백을 하나로
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize_text(self, text: str) -> List[str]:
        """텍스트 토큰화"""
        if self.language == 'korean':
            # 한국어 토큰화
            tokens = jieba.lcut(text)
        else:
            # 영어 토큰화
            tokens = word_tokenize(text)
        
        # 불용어 제거 및 길이 필터링
        tokens = [token for token in tokens if token not in self.stop_words and len(token) > 1]
        
        return tokens
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """감정 분석"""
        try:
            if self.language == 'english':
                blob = TextBlob(text)
                return {
                    'polarity': blob.sentiment.polarity,  # -1 (부정) ~ 1 (긍정)
                    'subjectivity': blob.sentiment.subjectivity  # 0 (객관) ~ 1 (주관)
                }
            else:
                # 한국어 감정 분석 (간단한 키워드 기반)
                positive_words = ['좋', '맛있', '훌륭', '완벽', '최고', '감사', '만족']
                negative_words = ['나쁘', '별로', '최악', '불만', '실망', '화나', '짜증']
                
                text_lower = text.lower()
                positive_count = sum(1 for word in positive_words if word in text_lower)
                negative_count = sum(1 for word in negative_words if word in text_lower)
                
                total_words = len(text.split())
                if total_words == 0:
                    return {'polarity': 0, 'subjectivity': 0}
                
                polarity = (positive_count - negative_count) / total_words
                subjectivity = (positive_count + negative_count) / total_words
                
                return {
                    'polarity': max(-1, min(1, polarity)),
                    'subjectivity': max(0, min(1, subjectivity))
                }
        except Exception as e:
            logger.error(f"감정 분석 실패: {e}")
            return {'polarity': 0, 'subjectivity': 0}
    
    def extract_keywords(self, texts: List[str], top_n: int = 20) -> List[Tuple[str, int]]:
        """키워드 추출"""
        all_tokens = []
        
        for text in texts:
            processed_text = self.preprocess_text(text)
            tokens = self.tokenize_text(processed_text)
            all_tokens.extend(tokens)
        
        # 빈도 계산
        word_freq = Counter(all_tokens)
        
        # 상위 키워드 반환
        return word_freq.most_common(top_n)
    
    def analyze_message_patterns(self, messages: List[Dict]) -> Dict[str, Any]:
        """메시지 패턴 분석"""
        analysis = {
            'total_messages': len(messages),
            'message_lengths': [],
            'sentiment_scores': [],
            'time_patterns': defaultdict(int),
            'user_patterns': defaultdict(int),
            'keyword_frequency': Counter(),
            'response_times': []
        }
        
        for message in messages:
            # 메시지 길이
            text = message.get('text', '')
            analysis['message_lengths'].append(len(text))
            
            # 감정 분석
            sentiment = self.analyze_sentiment(text)
            analysis['sentiment_scores'].append(sentiment['polarity'])
            
            # 시간 패턴
            timestamp = message.get('timestamp', '')
            if timestamp:
                try:
                    hour = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).hour
                    analysis['time_patterns'][hour] += 1
                except:
                    pass
            
            # 사용자 패턴
            user_id = message.get('user_id', 'unknown')
            analysis['user_patterns'][user_id] += 1
            
            # 키워드 빈도
            tokens = self.tokenize_text(self.preprocess_text(text))
            analysis['keyword_frequency'].update(tokens)
        
        # 통계 계산
        analysis['avg_message_length'] = np.mean(analysis['message_lengths'])
        analysis['avg_sentiment'] = np.mean(analysis['sentiment_scores'])
        analysis['top_keywords'] = analysis['keyword_frequency'].most_common(20)
        analysis['top_users'] = dict(analysis['user_patterns'].most_common(10))
        
        return analysis
    
    def generate_wordcloud(self, texts: List[str], output_path: str = None) -> WordCloud:
        """워드클라우드 생성"""
        # 모든 텍스트 결합
        combined_text = ' '.join(texts)
        
        # 한국어 폰트 설정
        if self.language == 'korean':
            font_path = '/System/Library/Fonts/AppleGothic.ttf'  # macOS
            # Windows: 'C:/Windows/Fonts/malgun.ttf'
            # Linux: '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
        else:
            font_path = None
        
        # 워드클라우드 생성
        wordcloud = WordCloud(
            font_path=font_path,
            width=800,
            height=400,
            background_color='white',
            max_words=100,
            colormap='viridis'
        ).generate(combined_text)
        
        # 저장
        if output_path:
            wordcloud.to_file(output_path)
            logger.info(f"워드클라우드 저장 완료: {output_path}")
        
        return wordcloud
    
    def analyze_customer_feedback(self, feedback_data: List[Dict]) -> Dict[str, Any]:
        """고객 피드백 분석"""
        analysis = {
            'total_feedback': len(feedback_data),
            'rating_distribution': defaultdict(int),
            'sentiment_by_rating': defaultdict(list),
            'common_issues': Counter(),
            'positive_keywords': Counter(),
            'negative_keywords': Counter(),
            'response_time_analysis': {},
            'category_analysis': defaultdict(list)
        }
        
        for feedback in feedback_data:
            rating = feedback.get('rating', 0)
            text = feedback.get('text', '')
            category = feedback.get('category', 'general')
            
            # 평점 분포
            analysis['rating_distribution'][rating] += 1
            
            # 평점별 감정 분석
            sentiment = self.analyze_sentiment(text)
            analysis['sentiment_by_rating'][rating].append(sentiment['polarity'])
            
            # 카테고리별 분석
            analysis['category_analysis'][category].append({
                'rating': rating,
                'sentiment': sentiment['polarity'],
                'text': text
            })
            
            # 키워드 분석
            tokens = self.tokenize_text(self.preprocess_text(text))
            if rating >= 4:
                analysis['positive_keywords'].update(tokens)
            elif rating <= 2:
                analysis['negative_keywords'].update(tokens)
        
        # 통계 계산
        for rating in analysis['sentiment_by_rating']:
            analysis['sentiment_by_rating'][rating] = np.mean(analysis['sentiment_by_rating'][rating])
        
        analysis['top_positive_keywords'] = analysis['positive_keywords'].most_common(10)
        analysis['top_negative_keywords'] = analysis['negative_keywords'].most_common(10)
        
        return analysis
    
    def detect_anomalies(self, texts: List[str], threshold: float = 2.0) -> List[int]:
        """이상 텍스트 탐지"""
        anomalies = []
        
        # 텍스트 길이 기반 이상 탐지
        lengths = [len(text) for text in texts]
        mean_length = np.mean(lengths)
        std_length = np.std(lengths)
        
        for i, length in enumerate(lengths):
            z_score = abs(length - mean_length) / std_length
            if z_score > threshold:
                anomalies.append(i)
        
        return anomalies
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """개체명 추출 (간단한 규칙 기반)"""
        entities = {
            'restaurants': [],
            'food_items': [],
            'locations': [],
            'times': [],
            'prices': []
        }
        
        # 음식점명 패턴
        restaurant_patterns = [
            r'([가-힣]+[집|점|당|관])',
            r'([가-힣]+[치킨|피자|햄버거|카페])'
        ]
        
        # 음식명 패턴
        food_patterns = [
            r'([가-힣]+[치킨|피자|햄버거|스테이크|파스타|샐러드])',
            r'([가-힣]+[김치|된장|순두부|갈비|삼겹살])'
        ]
        
        # 가격 패턴
        price_pattern = r'(\d{1,3}(?:,\d{3})*원)'
        
        # 시간 패턴
        time_pattern = r'(\d{1,2}:\d{2})'
        
        # 패턴 매칭
        for pattern in restaurant_patterns:
            matches = re.findall(pattern, text)
            entities['restaurants'].extend(matches)
        
        for pattern in food_patterns:
            matches = re.findall(pattern, text)
            entities['food_items'].extend(matches)
        
        price_matches = re.findall(price_pattern, text)
        entities['prices'].extend(price_matches)
        
        time_matches = re.findall(time_pattern, text)
        entities['times'].extend(time_matches)
        
        return entities
    
    def generate_report(self, analysis_results: Dict[str, Any]) -> str:
        """분석 리포트 생성"""
        report = []
        report.append("=" * 50)
        report.append("텍스트 분석 리포트")
        report.append("=" * 50)
        report.append(f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # 기본 통계
        if 'total_messages' in analysis_results:
            report.append("📊 기본 통계")
            report.append(f"- 총 메시지 수: {analysis_results['total_messages']:,}개")
            report.append(f"- 평균 메시지 길이: {analysis_results.get('avg_message_length', 0):.1f}자")
            report.append(f"- 평균 감정 점수: {analysis_results.get('avg_sentiment', 0):.3f}")
            report.append("")
        
        # 키워드 분석
        if 'top_keywords' in analysis_results:
            report.append("🔍 주요 키워드 (상위 10개)")
            for i, (keyword, count) in enumerate(analysis_results['top_keywords'][:10], 1):
                report.append(f"{i:2d}. {keyword}: {count:,}회")
            report.append("")
        
        # 시간 패턴
        if 'time_patterns' in analysis_results:
            report.append("⏰ 시간대별 메시지 분포")
            for hour in sorted(analysis_results['time_patterns'].keys()):
                count = analysis_results['time_patterns'][hour]
                report.append(f"- {hour:02d}시: {count:,}개")
            report.append("")
        
        # 사용자 패턴
        if 'top_users' in analysis_results:
            report.append("👥 활성 사용자 (상위 5명)")
            for i, (user_id, count) in enumerate(analysis_results['top_users'].items(), 1):
                report.append(f"{i}. 사용자 {user_id}: {count:,}개 메시지")
            report.append("")
        
        return "\n".join(report)


def main():
    """메인 실행 함수"""
    # TextAnalyzer 초기화
    analyzer = TextAnalyzer(language='korean')
    
    # 예시 데이터
    sample_texts = [
        "맛있는 치킨 배달해주세요!",
        "피자 주문했는데 너무 늦게 왔어요",
        "감사합니다! 정말 맛있었어요",
        "배달 시간이 너무 오래 걸려요",
        "음식이 맛있고 서비스도 좋아요"
    ]
    
    # 키워드 추출
    keywords = analyzer.extract_keywords(sample_texts)
    print("주요 키워드:")
    for keyword, count in keywords[:10]:
        print(f"- {keyword}: {count}회")
    
    # 감정 분석
    print("\n감정 분석:")
    for text in sample_texts:
        sentiment = analyzer.analyze_sentiment(text)
        print(f"- '{text}': {sentiment['polarity']:.3f}")
    
    # 개체명 추출
    print("\n개체명 추출:")
    for text in sample_texts:
        entities = analyzer.extract_entities(text)
        print(f"- '{text}':")
        for entity_type, items in entities.items():
            if items:
                print(f"  {entity_type}: {items}")


if __name__ == "__main__":
    main()
