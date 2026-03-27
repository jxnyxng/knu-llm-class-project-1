import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def send_stock_report_email(to_email, stock_name, report_content):
    """
    주식 분석 및 헷징 전략 결과를 이메일로 전송해주는 함수
    """
    subject = f"📊 [{stock_name}] AI 주식 분석 및 헷징 전략 리포트"
    
    formatted_content = report_content.replace('\n', '<br>')
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2 style="color: #2c3e50;">📈 {stock_name} 투자 분석 리포트</h2>
        <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
            {formatted_content}
        </div>
        <p style="font-size: 12px; color: #7f8c8d; margin-top: 20px;">
            * 본 리포트는 AI가 분석한 내용이며, 최종 투자 판단의 책임은 본인에게 있습니다.
        </p>
    </body>
    </html>
    """

    print(f"[이메일 전송 요청] 수신: {to_email}")
    
    try:
        # SMTP 설정 가져오기
        host = os.getenv("SMTP_HOST")
        port = int(os.getenv("SMTP_PORT", 587))
        user = os.getenv("SMTP_USER")
        password = os.getenv("SMTP_PASSWORD")

        if not all([host, user, password]):
            return {"success": False, "error": "SMTP 설정이 누락되었습니다."}

        # 메시지 생성
        msg = MIMEText(html_content, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = user
        msg['To'] = to_email

        # 서버 연결 및 전송
        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(user, password)
            server.send_message(msg)
            
        print("[이메일 전송 성공!]")
        return {"success": True, "message": "리포트가 성공적으로 발송되었습니다."}
        
    except Exception as e:
        print(f"[이메일 전송 실패]: {str(e)}")
        return {"success": False, "error": str(e)}