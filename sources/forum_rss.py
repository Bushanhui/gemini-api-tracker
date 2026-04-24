import feedparser

RSS_URL = "https://discuss.ai.google.dev/c/gemini-api/4.rss"

def fetch(keyword: str) -> list[dict]:
    """Google Developer Forum RSS에서 keyword 포함된 항목 반환"""
    
    try:
        feed = feedparser.parse(RSS_URL)
    except Exception as e:
        print(f"[Forum] 에러: {e}")
        return []
    
    results = []
    for entry in feed.entries:
        title   = entry.get("title", "").lower()
        summary = entry.get("summary", "").lower()
        
        if keyword.lower() in title or keyword.lower() in summary:
            results.append({
                "id":     f"forum-{entry.get('id', entry.get('link', ''))}",
                "title": entry.get("title", "제목 없음"),
                "url":   entry.get("link", ""),
                "source": "Google Dev Forum",
                "emoji": "💬"
            })
    
    print(f"[Forum] '{keyword}' 키워드 {len(results)}개 발견")
    return results