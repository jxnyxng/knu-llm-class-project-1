_store: dict = {
    "user_profile": [],    # 예: 투자 성향, 관심 종목
    "goals": [],            # 투자 목표 기록
    "portfolio_plans": [], # AI 포트폴리오 기록
    "analyzed_news": [],   # 최근 분석한 종목 판단 기록
}

def get_store():
    return _store