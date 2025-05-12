import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

# 🔹 .env 로드
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

ACCESS_TOKEN = os.getenv("KAKAO_ACCESS_TOKEN")

# 🔹 공통 헤더
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
}

API_URL = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

# 🔹 ping(): 카카오톡 메시지 전송 테스트
def ping() -> bool:
    if not ACCESS_TOKEN:
        print("[KAKAO] ❌ 액세스 토큰 없음")
        return False
    try:
        data = {
            "template_object": '{"object_type":"text","text":"✅ [Ping 테스트] 카카오 알림 연결 성공","link":{"web_url":"https://github.com","mobile_web_url":"https://github.com"}}'
        }
        resp = requests.post(API_URL, headers=HEADERS, data=data, timeout=5)
        if resp.status_code == 200:
            result = resp.json()
            if result.get("result_code") == 0:
                return True
            else:
                print(f"[KAKAO] ❌ result_code: {result.get('result_code')} | message: {result}")
        else:
            print(f"[KAKAO] ❌ HTTP 오류: {resp.status_code} | {resp.text}")
        return False
    except Exception as e:
        print(f"[KAKAO] ❌ 예외 발생: {e}")
        return False

# 🔹 send(): 커밋 결과 메시지 전송
def send(commit_msg: str, status: str = "success") -> bool:
    if not ACCESS_TOKEN:
        return False

    prefix = "✅ Git Push 성공" if status == "success" else "❌ Git Push 실패"
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    text = f"{prefix}\n🕒 {time_str}\n\n📝 Commit Message:\n{commit_msg}"

    template_object = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": "https://github.com",
            "mobile_web_url": "https://github.com"
        }
    }

    try:
        data = { "template_object": json_string(template_object) }
        resp = requests.post(API_URL, headers=HEADERS, data=data, timeout=10)
        return resp.status_code == 200 and resp.json().get("result_code") == 0
    except:
        return False


# 🔧 JSON 문자열로 변환 (인코딩 주의)
import json
def json_string(obj):
    return json.dumps(obj, ensure_ascii=False)
