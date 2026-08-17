import re

with open("/Users/kazisis/.gemini/antigravity-ide/brain/d1531a6a-c6fd-4c64-adc2-e96f8505f1fb/.system_generated/steps/3110/content.md", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

urls = re.findall(r"https?://[^\s\)\"\'<>]+", text)
print(f"Found {len(urls)} URLs:")
for u in urls[:30]:
    print("-", u)
