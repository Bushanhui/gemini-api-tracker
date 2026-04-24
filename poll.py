import json
import os
from sources import github_issues, forum_rss
from notifiers import discord

KEYWORD   = "batch"
SEEN_FILE = "seen.json"

def load_seen() -> set:
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    return set()

def save_seen(seen: set) -> None:
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f, indent=2)

def main():
    print(f"=== Gemini Batch Tracker 실행 (키워드: '{KEYWORD}') ===")
    
    seen = load_seen()
    print(f"이미 처리된 항목: {len(seen)}개")
    
    all_items = []
    all_items += github_issues.fetch(KEYWORD)
    all_items += forum_rss.fetch(KEYWORD)
    
    new_items = [item for item in all_items if item["id"] not in seen]
    print(f"새 항목: {len(new_items)}개")
    
    if new_items:
        discord.send(new_items)
        seen.update(item["id"] for item in new_items)
        save_seen(seen)
    else:
        print("새 항목 없음 — Discord 전송 스킵")
    
    print("=== 완료 ===")

if __name__ == "__main__":
    main()