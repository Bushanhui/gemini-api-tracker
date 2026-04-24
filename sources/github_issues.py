import requests
import os

REPO = "googleapis/js-genai"
API_URL = f"https://api.github.com/repos/{REPO}/issues"

def fetch(keyword: str) -> list[dict]:
    """GitHub Issues에서 keyword 포함된 항목 반환"""
    
    headers = {"Accept": "application/vnd.github+json"}
    
    token = os.getenv("GITHUB_TOKEN_CUSTOM")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    params = {
        "state": "open",
        "per_page": 30,
        "sort": "created",
        "direction": "desc"
    }
    
    try:
        resp = requests.get(API_URL, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        issues = resp.json()
    except Exception as e:
        print(f"[GitHub] 에러: {e}")
        return []
    
    results = []
    for issue in issues:
        if "pull_request" in issue:
            continue
        
        title = issue.get("title", "").lower()
        body  = (issue.get("body") or "").lower()
        
        if keyword.lower() in title or keyword.lower() in body:
            results.append({
                "id":     f"github-{issue['number']}",
                "title": issue["title"],
                "url":   issue["html_url"],
                "source": "GitHub Issues",
                "emoji": "🐙"
            })
    
    print(f"[GitHub] '{keyword}' 키워드 {len(results)}개 발견")
    return results