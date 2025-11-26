import json

with open("translations/panel_ai_translated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

review_list = []
dict_count = 0
ai_count = 0

for k, v in data.items():
    if isinstance(v, str):
        if "[DICT]" in v:
            dict_count += 1
        elif "[AI]" in v:
            ai_count += 1
            review_list.append({
                "key": k,
                "current": v,
                "english": v.replace("[AI] ", "").replace(" (AI dịch)", ""),
                "suggested": v.replace(" (AI dịch)", ""),
                "status": "pending"
            })

with open("translations/review_queue.json", "w", encoding="utf-8") as f:
    json.dump(review_list, f, ensure_ascii=False, indent=2)

print("✅ Review queue created")
print(f"📋 Items need review: {len(review_list)}")
print(f"✓ DICT (safe): {dict_count}")
print(f"⚠ AI (review): {ai_count}")
print(f"\n📝 Next steps:")
print("1. Open translations/review_queue.json")
print("2. Edit 'suggested' field with correct translation")
print("3. Change 'status' from 'pending' to 'approved'")
print("4. Run apply_human_review.py to finalize")
