import requests
import os

def send(items: list[dict]) -> None:
    """새 항목 목록을 Discord로 전송"""
    
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("[Discord] DISCORD_WEBHOOK_URL 환경변수 없음")
        return
    
    if not items:
        return
    
    lines = ["🔍 **Gemini Batch API 관련 새 글이 있어요!**\n"]
    
    for item in items:
        lines.append(
            f"{item['emoji']} **[{item['source']}]** {item['title']}\n"
            f"> {item['url']}\n"
        )
    
    message = "\n".join(lines)
    
    if len(message) > 2000:
        message = message[:1990] + "\n...(생략)"
    
    try:
        resp = requests.post(
            webhook_url,
            json={"content": message},
            timeout=10
        )
        resp.raise_for_status()
        print(f"[Discord] {len(items)}개 항목 전송 완료")
    except Exception as e:
        print(f"[Discord] 전송 실패: {e}")