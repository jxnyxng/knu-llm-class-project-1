"""
주식 투자 코칭 시스템을 위한 데이터 모델 정의
"""
from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    age: int = Field(description="사용자의 나이")
    salary: int = Field(description="사용자의 연봉 (단위: 원)")

class UserGoal(BaseModel):
    goal_type: str = Field(description="주식 투자 목표 (예: 자산증식, 은퇴자금 마련 등)")
    principal: int = Field(description="사용자의 원금 (단위: 원)")
    target_amount: int = Field(description="목표 금액 (단위: 원)")
    current_yield: float = Field(description="현재 전체 계좌 투자 수익률 (%)")

class InvestmentPlan(BaseModel):
    plan_type: str = Field(description="투자의 유형 (예: 단기, 중기, 장기)")
    plan_content: str = Field(description="계획의 구체적인 내용")
