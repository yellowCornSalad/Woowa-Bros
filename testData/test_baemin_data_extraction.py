import json
import random
from datetime import datetime, timedelta
import uuid
import pickle

# 시드 설정
random.seed(42)

# 기본 데이터 설정 (이전과 동일)
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

districts = ["강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", 
            "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", 
            "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"]

surnames = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임", "한", "오", "서", "신", "권", "황", "안", "송", "전", "홍"]
given_names = ["민수", "영희", "철수", "수진", "지훈", "예은", "준호", "소영", "동현", "미영", "성민", "하늘", "바다", "별", "달", "해", "구름", "꽃", "나무", "돌"]

# 비정형 데이터 생성 함수들
def generate_json_format_data():
    """JSON 형태의 비정형 데이터 생성"""
    data = []
    
    for i in range(25000):  # 10만건 중 25%
        order_time = datetime(2023, 1, 1) + timedelta(
            days=random.randint(0, 730),
            hours=random.randint(10, 23),
            minutes=random.randint(0, 59)
        )
        
        restaurant = random.choice(restaurants)
        customer = random.choice(surnames) + random.choice(given_names)
        
        # 중첩된 JSON 구조
        order_data = {
            "order_info": {
                "id": f"JSON_{i+1:06d}",
                "timestamp": order_time.isoformat(),
                "status": random.choice(["pending", "confirmed", "preparing", "delivering", "completed", "cancelled"]),
                "restaurant": {
                    "name": restaurant,
                    "category": random.choice(list(menu_categories.keys())),
                    "rating": round(random.uniform(3.5, 5.0), 1),
                    "location": {
                        "district": random.choice(districts),
                        "coordinates": {
                            "lat": round(random.uniform(37.4, 37.7), 6),
                            "lng": round(random.uniform(126.8, 127.2), 6)
                        }
                    }
                }
            },
            "customer": {
                "name": customer,
                "phone": f"010-{random.randint(1000,9999)}-{random.randint(1000,9999)}",
                "address": {
                    "full": f"서울시 {random.choice(districts)} {random.randint(1,30)}동 {random.randint(1,999)}-{random.randint(1,99)}",
                    "detail": f"{random.randint(101,2050)}호",
                    "note": random.choice(["문앞에 놓아주세요", "벨 누르지 마세요", "경비실에 맡겨주세요", None])
                }
            },
            "items": [
                {
                    "name": random.choice(menu_categories[random.choice(list(menu_categories.keys()))]),
                    "qty": random.randint(1, 3),
                    "price": random.randint(8000, 25000),
                    "options": random.choice([
                        {"spice": "보통", "size": "일반"},
                        {"spice": "매움", "pickles": "추가"},
                        {"sauce": "케찹", "drink": "콜라"},
                        {}
                    ])
                } for _ in range(random.randint(1, 4))
            ],
            "payment": {
                "method": random.choice(["card", "cash", "online", "coupon"]),
                "amount": random.randint(15000, 50000),
                "delivery_fee": random.choice([0, 2000, 2500, 3000])
            },
            "metadata": {
                "user_agent": random.choice([
                    "BaedalApp/1.2.3 iOS/15.0",
                    "BaedalApp/1.2.3 Android/11.0",
                    "Mozilla/5.0 Web/Safari"
                ]),
                "session_id": str(uuid.uuid4()),
                "referrer": random.choice(["app", "web", "kakao", "naver"])
            }
        }
        
        data.append(order_data)
        
        if (i + 1) % 5000 == 0:
            print(f"JSON 데이터 생성 중... {i + 1}/25000")
    
    return data

def generate_log_format_data():
    """로그 형태의 비정형 데이터 생성"""
    log_entries = []
    
    for i in range(25000):  # 10만건 중 25%
        order_time = datetime(2023, 1, 1) + timedelta(
            days=random.randint(0, 730),
            hours=random.randint(10, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        
        # 다양한 로그 포맷
        log_formats = [
            # Apache 스타일 로그
            f"{order_time.strftime('%Y-%m-%d %H:%M:%S')} [INFO] ORDER_CREATED order_id=LOG_{i+1:06d} restaurant='{random.choice(restaurants)}' customer='{random.choice(surnames)}{random.choice(given_names)}' amount={random.randint(15000,50000)} district={random.choice(districts)} payment={random.choice(['CARD','CASH','ONLINE'])}",
            
            # 시스템 로그 스타일
            f"[{order_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}] [TRACE] com.baedalapp.order.OrderService - Processing order LOG_{i+1:06d} | Restaurant: {random.choice(restaurants)} | Items: {random.randint(1,4)} | Status: {random.choice(['PENDING','CONFIRMED','PREPARING'])} | Location: {random.choice(districts)}",
            
            # JSON 라인 로그
            json.dumps({
                "timestamp": order_time.isoformat(),
                "level": "INFO",
                "service": "order-service",
                "event": "order_status_changed",
                "order_id": f"LOG_{i+1:06d}",
                "restaurant": random.choice(restaurants),
                "status": random.choice(["created", "accepted", "preparing", "pickup", "delivered"]),
                "amount": random.randint(15000, 50000),
                "delivery_address": f"서울시 {random.choice(districts)}"
            }, ensure_ascii=False),
            
            # 에러 로그
            f"{order_time.strftime('%Y-%m-%d %H:%M:%S')} [ERROR] Payment failed for order LOG_{i+1:06d} - Restaurant: {random.choice(restaurants)}, Customer: {random.choice(surnames)}{random.choice(given_names)}, Error: {random.choice(['CARD_DECLINED', 'NETWORK_ERROR', 'TIMEOUT', 'INVALID_AMOUNT'])}"
        ]
        
        log_entry = random.choice(log_formats)
        log_entries.append(log_entry)
        
        if (i + 1) % 5000 == 0:
            print(f"로그 데이터 생성 중... {i + 1}/25000")
    
    return log_entries

def generate_message_format_data():
    """메시지/채팅 형태의 비정형 데이터 생성"""
    messages = []
    
    for i in range(25000):  # 10만건 중 25%
        order_time = datetime(2023, 1, 1) + timedelta(
            days=random.randint(0, 730),
            hours=random.randint(10, 23),
            minutes=random.randint(0, 59)
        )
        
        customer = random.choice(surnames) + random.choice(given_names)
        restaurant = random.choice(restaurants)
        
        # 채팅 대화 형태
        conversation = [
            {
                "sender": "customer",
                "message": f"안녕하세요! {random.choice(menu_categories[random.choice(list(menu_categories.keys()))])} 주문하고 싶어요",
                "timestamp": order_time.isoformat(),
                "message_id": f"MSG_{i+1:06d}_01"
            },
            {
                "sender": "restaurant",
                "message": f"네 {customer}님, {restaurant}입니다. 주문 도와드리겠습니다!",
                "timestamp": (order_time + timedelta(minutes=1)).isoformat(),
                "message_id": f"MSG_{i+1:06d}_02"
            },
            {
                "sender": "customer", 
                "message": f"배달주소는 서울시 {random.choice(districts)} {random.randint(1,30)}동이고요, {random.choice(['문앞에 놓아주세요', '벨 눌러주세요', '전화주세요'])}",
                "timestamp": (order_time + timedelta(minutes=2)).isoformat(),
                "message_id": f"MSG_{i+1:06d}_03"
            },
            {
                "sender": "system",
                "message": f"주문이 접수되었습니다. 주문번호: MSG_{i+1:06d}, 예상배달시간: {random.randint(30,60)}분",
                "timestamp": (order_time + timedelta(minutes=3)).isoformat(),
                "message_id": f"MSG_{i+1:06d}_04"
            }
        ]
        
        # 주문 상태 업데이트 메시지들
        status_updates = [
            {
                "sender": "system",
                "message": random.choice([
                    "음식 준비가 시작되었습니다",
                    "조리가 완료되어 배달을 시작합니다",
                    "배달기사가 픽업했습니다",
                    "배달이 완료되었습니다"
                ]),
                "timestamp": (order_time + timedelta(minutes=random.randint(5, 50))).isoformat(),
                "message_id": f"MSG_{i+1:06d}_{len(conversation)+1:02d}"
            }
        ]
        
        full_conversation = {
            "conversation_id": f"MSG_{i+1:06d}",
            "participants": [customer, restaurant, "system"],
            "messages": conversation + status_updates,
            "order_summary": {
                "restaurant": restaurant,
                "customer": customer,
                "amount": random.randint(15000, 50000),
                "status": random.choice(["active", "completed", "cancelled"])
            }
        }
        
        messages.append(full_conversation)
        
        if (i + 1) % 5000 == 0:
            print(f"메시지 데이터 생성 중... {i + 1}/25000")
    
    return messages

def generate_xml_format_data():
    """XML 형태의 비정형 데이터 생성"""
    xml_data = []
    
    for i in range(25000):  # 10만건 중 25%
        order_time = datetime(2023, 1, 1) + timedelta(
            days=random.randint(0, 730),
            hours=random.randint(10, 23),
            minutes=random.randint(0, 59)
        )
        
        restaurant = random.choice(restaurants)
        customer = random.choice(surnames) + random.choice(given_names)
        
        xml_string = f"""<?xml version="1.0" encoding="UTF-8"?>
<order xmlns="http://baedalapp.com/schema/order" id="XML_{i+1:06d}">
    <header>
        <timestamp>{order_time.isoformat()}</timestamp>
        <version>2.1</version>
        <source>mobile_app</source>
    </header>
    <restaurant name="{restaurant}" id="REST_{random.randint(1000,9999)}">
        <category>{random.choice(list(menu_categories.keys()))}</category>
        <location district="{random.choice(districts)}" />
        <contact phone="02-{random.randint(100,999)}-{random.randint(1000,9999)}" />
    </restaurant>
    <customer>
        <name>{customer}</name>
        <phone>010-{random.randint(1000,9999)}-{random.randint(1000,9999)}</phone>
        <address>
            <main>서울시 {random.choice(districts)} {random.randint(1,30)}동</main>
            <detail>{random.randint(101,2050)}호</detail>
            <instructions>{random.choice(['문앞배치', '경비실보관', '직접수령', ''])}</instructions>
        </address>
    </customer>
    <items total="{random.randint(1,4)}">
        <item id="ITEM_{random.randint(1,999)}" name="{random.choice(menu_categories[random.choice(list(menu_categories.keys()))])}" 
              quantity="{random.randint(1,3)}" price="{random.randint(8000,25000)}" />
    </items>
    <payment method="{random.choice(['CARD','CASH','ONLINE'])}" 
            amount="{random.randint(15000,50000)}" 
            delivery_fee="{random.choice([0,2000,2500,3000])}" />
    <status current="{random.choice(['PENDING','CONFIRMED','PREPARING','DELIVERING','COMPLETED'])}" 
            estimated_delivery="{(order_time + timedelta(minutes=random.randint(30,60))).isoformat()}" />
</order>"""
        
        xml_data.append(xml_string)
        
        if (i + 1) % 5000 == 0:
            print(f"XML 데이터 생성 중... {i + 1}/25000")
    
    return xml_data

# 메인 실행 함수
def generate_unstructured_delivery_data():
    print("배달의 민족 비정형 데이터 생성을 시작합니다...")
    
    # 1. JSON 형태 데이터 생성
    print("\n1. JSON 형태 데이터 생성 중...")
    json_data = generate_json_format_data()
    
    # 2. 로그 형태 데이터 생성
    print("\n2. 로그 형태 데이터 생성 중...")
    log_data = generate_log_format_data()
    
    # 3. 메시지 형태 데이터 생성
    print("\n3. 메시지/채팅 형태 데이터 생성 중...")
    message_data = generate_message_format_data()
    
    # 4. XML 형태 데이터 생성
    print("\n4. XML 형태 데이터 생성 중...")
    xml_data = generate_xml_format_data()
    
    # 파일로 저장
    print("\n데이터 파일 저장 중...")
    
    # JSON 파일 저장
    with open("배달의민족_JSON_데이터_25000건.json", "w", encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    # 로그 파일 저장
    with open("배달의민족_로그_데이터_25000건.log", "w", encoding='utf-8') as f:
        for log_entry in log_data:
            f.write(log_entry + "\n")
    
    # 메시지 데이터 저장
    with open("배달의민족_메시지_데이터_25000건.json", "w", encoding='utf-8') as f:
        json.dump(message_data, f, ensure_ascii=False, indent=2)
    
    # XML 데이터 저장
    with open("배달의민족_XML_데이터_25000건.xml", "w", encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<orders>\n')
        for xml_entry in xml_data:
            f.write(xml_entry + "\n")
        f.write('</orders>')
    
    # 통합 비정형 데이터 (Pickle)
    all_unstructured_data = {
        "json_orders": json_data,
        "log_entries": log_data,
        "conversations": message_data,
        "xml_orders": xml_data,
        "metadata": {
            "total_records": len(json_data) + len(log_data) + len(message_data) + len(xml_data),
            "generated_at": datetime.now().isoformat(),
            "data_types": ["JSON", "LOG", "MESSAGE", "XML"],
            "description": "배달의민족 토이 프로젝트용 비정형 데이터"
        }
    }
    
    with open("배달의민족_통합_비정형데이터_10만건.pickle", "wb") as f:
        pickle.dump(all_unstructured_data, f)
    
    print(f"\n=== 비정형 데이터 생성 완료! ===")
    print(f"총 데이터 건수: {len(json_data) + len(log_data) + len(message_data) + len(xml_data):,}건")
    print(f"- JSON 형태: {len(json_data):,}건")
    print(f"- 로그 형태: {len(log_data):,}건") 
    print(f"- 메시지 형태: {len(message_data):,}건")
    print(f"- XML 형태: {len(xml_data):,}건")
    
    print(f"\n생성된 파일들:")
    print(f"1. 배달의민족_JSON_데이터_25000건.json")
    print(f"2. 배달의민족_로그_데이터_25000건.log")
    print(f"3. 배달의민족_메시지_데이터_25000건.json")
    print(f"4. 배달의민족_XML_데이터_25000건.xml")
    print(f"5. 배달의민족_통합_비정형데이터_10만건.pickle")
    
    # 샘플 데이터 출력
    print(f"\n=== JSON 데이터 샘플 ===")
    print(json.dumps(json_data[0], ensure_ascii=False, indent=2)[:500] + "...")
    
    print(f"\n=== 로그 데이터 샘플 ===")
    for i in range(3):
        print(log_data[i])
    
    print(f"\n=== 메시지 데이터 샘플 ===")
    print(f"대화 ID: {message_data[0]['conversation_id']}")
    print(f"참여자: {message_data[0]['participants']}")
    print(f"메시지 수: {len(message_data[0]['messages'])}")
    
    return all_unstructured_data

# 실행
if __name__ == "__main__":
    data = generate_unstructured_delivery_data()
