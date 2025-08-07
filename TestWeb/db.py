import pandas as pd
import random
from datetime import datetime, timedelta
import uuid

# 시드 설정 (재현 가능한 결과를 위해)
random.seed(42)

# 기본 데이터 설정
restaurants = [
    "맘스터치", "맥도날드", "버거킹", "KFC", "롯데리아",
    "교촌치킨", "BBQ", "굽네치킨", "치킨플러스", "네네치킨",
    "도미노피자", "피자헛", "미스터피자", "파파존스", "치킨마루",
    "김밥천국", "컵밥", "한솥도시락", "오니기리와이프", "더진국",
    "맛닭꼬", "봉추찜닭", "안동찜닭", "원할머니보쌈", "족발야시장",
    "중국집용", "홍콩반점", "짜장면세상", "중화루", "만리장성",
    "삼계탕집", "곰탕집", "설렁탕집", "순댓국집", "해장국집",
    "떡볶이천국", "신전떡볶이", "엽기떡볶이", "청년다방", "호떡집",
    "초밥나라", "회센터", "연어집", "참치집", "스시로",
    "파스타천국", "이태리부엌", "스파게티공장", "올리브가든", "베네치아"
]

# 메뉴 카테고리별 설정
menu_categories = {
    "치킨": ["후라이드치킨", "양념치킨", "간장치킨", "마늘치킨", "허니콤보", "치킨텐더", "핫윙", "치킨버거"],
    "피자": ["페퍼로니피자", "불고기피자", "하와이안피자", "치킨피자", "새우피자", "마르게리타", "콤비네이션피자"],
    "햄버거": ["빅맥", "와퍼", "치킨버거", "새우버거", "불고기버거", "치즈버거", "베이컨버거"],
    "중식": ["짜장면", "짬뽕", "탕수육", "양장피", "깐풍기", "볶음밥", "군만두", "잡채"],
    "한식": ["비빔밥", "된장찌개", "김치찌개", "불고기", "갈비탕", "삼계탕", "냉면", "국밥"],
    "일식": ["초밥세트", "연어회", "참치회", "라멘", "우동", "돈카츠", "규동", "연어덮밥"],
    "양식": ["파스타", "리조또", "스테이크", "샐러드", "오므라이스", "필라프", "크림파스타"],
    "분식": ["떡볶이", "순대", "튀김", "김밥", "라면", "우동", "만두", "어묵"],
    "도시락": ["불고기도시락", "치킨도시락", "생선도시락", "돈까스도시락", "스팸도시락", "김치볶음밥", "오므라이스"]
}

# 지역 설정
districts = ["강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", 
            "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", 
            "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"]

# 상세 주소 패턴
address_patterns = [
    "아파트", "빌라", "원룸", "오피스텔", "상가", "주택", "연립주택", "다세대주택"
]

# 고객 이름 패턴 (가명)
surnames = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임", "한", "오", "서", "신", "권", "황", "안", "송", "전", "홍"]
given_names = ["민수", "영희", "철수", "수진", "지훈", "예은", "준호", "소영", "동현", "미영", "성민", "하늘", "바다", "별", "달", "해", "구름", "꽃", "나무", "돌"]

# 배달 상태
delivery_status = ["주문접수", "조리중", "배달중", "배달완료", "주문취소"]

# 결제 방법
payment_methods = ["카드결제", "현금결제", "온라인결제", "쿠폰결제", "포인트결제"]

def generate_fake_data(num_records=100000):
    data = []
    
    # 시작 날짜 (2023년 1월 1일부터 2024년 12월 31일까지)
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    for i in range(num_records):
        # 주문 ID 생성
        order_id = f"ORD{str(i+1).zfill(8)}"
        
        # 랜덤 날짜 생성
        random_date = start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days),
            hours=random.randint(10, 23),
            minutes=random.randint(0, 59)
        )
        
        # 업체 선택
        restaurant = random.choice(restaurants)
        
        # 카테고리 선택 (업체명 기반으로 유추)
        if any(word in restaurant for word in ["치킨", "교촌", "BBQ"]):
            category = "치킨"
        elif "피자" in restaurant:
            category = "피자"
        elif any(word in restaurant for word in ["버거", "맥도날드", "버거킹"]):
            category = "햄버거"
        elif any(word in restaurant for word in ["중국", "짜장", "홍콩"]):
            category = "중식"
        elif any(word in restaurant for word in ["김밥", "도시락", "한솥"]):
            category = "도시락"
        elif any(word in restaurant for word in ["떡볶이", "신전", "엽기"]):
            category = "분식"
        else:
            category = random.choice(list(menu_categories.keys()))
        
        # 메뉴 선택 (1~3개)
        num_menus = random.randint(1, 3)
        selected_menus = random.sample(menu_categories[category], min(num_menus, len(menu_categories[category])))
        
        # 각 메뉴별 수량과 가격
        menu_details = []
        total_price = 0
        
        for menu in selected_menus:
            quantity = random.randint(1, 3)
            # 카테고리별 가격 범위 설정
            if category in ["치킨", "피자"]:
                unit_price = random.randint(15000, 35000)
            elif category == "햄버거":
                unit_price = random.randint(8000, 15000)
            elif category in ["중식", "한식"]:
                unit_price = random.randint(7000, 20000)
            elif category == "일식":
                unit_price = random.randint(12000, 30000)
            elif category == "양식":
                unit_price = random.randint(10000, 25000)
            else:
                unit_price = random.randint(3000, 12000)
            
            menu_price = unit_price * quantity
            total_price += menu_price
            
            menu_details.append({
                "메뉴명": menu,
                "수량": quantity,
                "단가": unit_price,
                "금액": menu_price
            })
        
        # 배달비 추가
        delivery_fee = random.choice([0, 2000, 2500, 3000]) if total_price < 15000 else 0
        final_price = total_price + delivery_fee
        
        # 고객 정보
        customer_name = random.choice(surnames) + random.choice(given_names)
        phone_number = f"010-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        
        # 주소 정보
        district = random.choice(districts)
        dong = f"{random.choice(['신', '구', '동', '서', '남', '북'])}{random.randint(1, 30)}동"
        building_number = f"{random.randint(1, 999)}-{random.randint(1, 99)}"
        building_type = random.choice(address_patterns)
        detailed_address = f"{random.randint(101, 2050)}호" if building_type in ["아파트", "오피스텔"] else f"{random.randint(1, 5)}층"
        
        full_address = f"서울시 {district} {dong} {building_number} {building_type} {detailed_address}"
        
        # 기타 정보
        status = random.choice(delivery_status)
        payment_method = random.choice(payment_methods)
        
        # 배달 예상 시간 (주문시간 + 30~60분)
        estimated_delivery = random_date + timedelta(minutes=random.randint(30, 60))
        
        # 평점 (배달완료인 경우만)
        rating = random.randint(1, 5) if status == "배달완료" else None
        
        # 리뷰 (30% 확률로 작성)
        reviews = [
            "맛있게 잘 먹었습니다!", "배달이 빨라요", "음식이 따뜻했어요", "재주문 의사 있어요",
            "포장이 깔끔해요", "양이 많아요", "가성비 좋아요", "친절해요", "다음에 또 시킬게요",
            "기대했던 맛이에요", "신선해요", "매장에서 먹는 것 같아요"
        ]
        review = random.choice(reviews) if random.random() < 0.3 and status == "배달완료" else None
        
        # 데이터 레코드 생성
        record = {
            "주문ID": order_id,
            "주문일시": random_date.strftime("%Y-%m-%d %H:%M:%S"),
            "업체명": restaurant,
            "카테고리": category,
            "메뉴상세": str(menu_details),
            "메뉴요약": ", ".join([f"{item['메뉴명']}({item['수량']}개)" for item in menu_details]),
            "총주문금액": total_price,
            "배달비": delivery_fee,
            "최종결제금액": final_price,
            "고객명": customer_name,
            "전화번호": phone_number,
            "배달주소": full_address,
            "구역": district,
            "상세주소구분": building_type,
            "주문상태": status,
            "결제방법": payment_method,
            "배달예상시간": estimated_delivery.strftime("%Y-%m-%d %H:%M:%S"),
            "평점": rating,
            "리뷰": review,
            "요청사항": "문 앞에 놓아주세요" if random.random() < 0.2 else None
        }
        
        data.append(record)
        
        # 진행상황 출력 (10000건마다)
        if (i + 1) % 10000 == 0:
            print(f"데이터 생성 진행중... {i + 1}/{num_records}")
    
    return data

# 데이터 생성
print("배달의 민족 토이 프로젝트용 가명 데이터 생성을 시작합니다...")
fake_data = generate_fake_data(100000)

# DataFrame 생성
df = pd.DataFrame(fake_data)

# CSV 파일로 저장
df.to_csv("배달의민족_가명데이터_10만건.csv", index=False, encoding='utf-8-sig')

print(f"\n데이터 생성 완료!")
print(f"총 {len(df)}건의 데이터가 생성되었습니다.")
print(f"파일명: 배달의민족_가명데이터_10만건.csv")

# 데이터 샘플 확인
print("\n=== 데이터 샘플 (처음 5건) ===")
print(df.head().to_string())

# 기본 통계 정보
print(f"\n=== 기본 통계 ===")
print(f"전체 주문 건수: {len(df):,}건")
print(f"총 매출액: {df['최종결제금액'].sum():,}원")
print(f"평균 주문금액: {df['최종결제금액'].mean():,.0f}원")
print(f"업체 수: {df['업체명'].nunique()}개")
print(f"고객 수: {df['고객명'].nunique()}명")

print(f"\n=== 주문 상태별 분포 ===")
print(df['주문상태'].value_counts())

print(f"\n=== 카테고리별 분포 ===")
print(df['카테고리'].value_counts())

print(f"\n=== 구역별 분포 (상위 10개) ===")
print(df['구역'].value_counts().head(10))
