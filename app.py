from agents import get_stock_analysis_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from mock_db import get_store
# from tools import save_user_profile, save_user_goal 
from email_service import send_stock_report_email

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-20b",
)

stock_analysis_agent = get_stock_analysis_agent(model)

print("=== 📈 주식 AI 분석가 ===")
age = int(input("나이를 입력하세요: "))
salary = int(input("연봉을 입력하세요 (단위: 원): "))
principal = int(input("투자 원금을 입력하세요 (단위: 원): "))
target_amount = int(input("목표 금액을 입력하세요 (단위: 원): "))
goal_type = input("투자 목표를 적어주세요 (예: 자산증식, 내집마련): ")
current_yield = float(input("현재 수익률을 입력하세요 (%): "))
print("============================")

# print("=== 📈 주식 AI 분석가 ===")
# age = 35
# salary = 70000000
# principal = 10000000
# target_amount = 20000000
# goal_type = "자산증식"
# current_yield = 5.0
# print("============================")

stock = input("\n분석할 주식 종목명을 입력하세요: ")

# 분석 요청
print(f"\n[{stock}] 분석 중... 잠시만 기다려주세요")
result = stock_analysis_agent.invoke({
    "messages": [
        {
            "role": "user", 
            "content": f"나는 {age}살이고 연봉은 {salary}원이야. 현재 원금 {principal}원으로 {target_amount}원을 만드는 '{goal_type}'이 목표고, 현재 계좌 수익률은 {current_yield}%야. {stock}에 대한 2026년 최신 뉴스를 분석하고 내 재무 상황에 딱 맞는 헷징 포트폴리오를 짜줘."
        }
    ]
})

print("\n=== 🤖 AI 분석가 답변 ===")
print(result['messages'][-1].content)

print("\n=== 📧 이메일 리포트 발송 ===")
# AI 분석 결과 가져오기
report = result['messages'][-1].content
user_email = input("리포트를 받을 이메일 주소를 입력하세요: ")

# 이메일 발송
print("📧 이메일 리포트 발송 중...")
send_result = send_stock_report_email(user_email, stock, report)

if send_result['success']:
    print("✨ 이메일 발송 완료! 편지함을 확인해보세요.")
else:
    print(f"❌ 이메일 발송 실패: {send_result['error']}")