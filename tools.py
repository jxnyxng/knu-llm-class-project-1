"""
종목 분석 에이전트
"""
from langchain_core.tools import tool
import os
import requests
from dotenv import load_dotenv
from langchain.tools import tool
from models import UserProfile, UserGoal
from mock_db import _store

load_dotenv()

@tool
def search_stock_news(query: str) -> str:
    """주어진 주식 종목명으로 네이버 최신 뉴스 10개를 검색해서 요약합니다

    Args:
        query (str): 주식 종목명

    Returns:
        str: 뉴스 요약 결과
    """
    
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }

    # 최신순으로 10개 가져오기
    params = {
        "query": query,
        "display": 10,
        "sort": "date"
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        return f"뉴스 검색 실패. 에러 코드: {response.status_code}"
        
    items = response.json().get("items", [])
    if not items:
        return f"'{query}'에 대한 최근 뉴스가 없습니다."

    result_text = []
    for i, item in enumerate(items, 1):
        # 네이버 API에서 오는 HTML태그 지우기
        title = item['title'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"')
        desc = item['description'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"')
        pub_date = item.get('pubDate', '날짜 모름')
        
        result_text.append(f"[{i}] 제목: {title}\n요약: {desc}\n발행일: {pub_date}\n")

    return "\n".join(result_text)

# @tool(args_schema=UserProfile)
# def save_user_profile(age: int, salary: int):
#     """사용자의 나이와 연봉 정보를 알게 되면 mock_db에 저장합니다.

#     Args:
#         age (int): 사용자의 나이
#         salary (int): 사용자의 연봉

#     Returns:
#         str: 프로필 덮어쓰기 완료 메시지
#     """

#     _store["user_profile"] = [{"age": age, "salary": salary}]
#     return "프로필 덮어쓰기 완료"

# @tool(args_schema=UserGoal)
# def save_user_goal(goal_type: str, principal: int, target_amount: int, current_yield: float):
#     """사용자의 투자 목표를 알게 되면 mock_db에 덮어씁니다.

#     Args:
#         goal_type (str): 투자 목표의 종류
#         principal (int): 초기 투자 금액
#         target_amount (int): 목표 금액
#         current_yield (float): 현재 수익률

#     Returns:
#         str: 투자 목표 덮어쓰기 완료 메시지
#     """

#     _store["goals"] = [{
#         "goal_type": goal_type, 
#         "principal": principal, 
#         "target_amount": target_amount, 
#         "current_yield": current_yield
#     }]

#     return "투자 목표 덮어쓰기 완료"