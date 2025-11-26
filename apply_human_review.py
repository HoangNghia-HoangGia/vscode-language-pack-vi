import json

# Load reviewed queue
with open("translations/review_queue.json", "r", encoding="utf-8") as f:
    review_queue = json.load(f)

# Load AI translated base
with open("translations/panel_ai_translated.json", "r", encoding="utf-8") as f:
    base = json.load(f)

# Apply human reviews
approved_count = 0
pending_count = 0

for item in review_queue:
    key = item["key"]
    
    if item["status"] == "approved":
        # Replace [AI] with [HUMAN] tag
        base[key] = item["suggested"].replace("[AI]", "[HUMAN]")
        approved_count += 1
    else:
        pending_count += 1

# Save final output
with open("translations/panel_human_reviewed.json", "w", encoding="utf-8") as f:
    json.dump(base, f, ensure_ascii=False, indent=2)

print("✅ Human review applied")
print(f"✓ Approved: {approved_count}")
print(f"⚠ Still pending: {pending_count}")
print(f"📁 Output: translations/panel_human_reviewed.json")

if pending_count > 0:
    print(f"\n⚠️ Warning: {pending_count} items still pending review")
    print("Complete review in review_queue.json before deploying to production")
