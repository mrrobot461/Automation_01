import os
password = os.getenv("EMAIL_PASSWORD")
print(f"Password found: {'✅ YES' if password else '❌ NO'}")
print(f"Length: {len(password) if password else 0}")







