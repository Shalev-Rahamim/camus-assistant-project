import asyncio
import sys
import os
import time  # ספרייה למדידת זמן

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai.classifier import classify_question
from db.models import CategoryEnum


async def run_classification_tests():
    test_cases = [
        ("מתי המבחן במבני נתונים?", CategoryEnum.SCHEDULE),
        ("ה-WiFi לא עובד לי באולם 101", CategoryEnum.TECHNICAL),
        ("מי המרצה של קורס מערכות הפעלה?", CategoryEnum.SCHEDULE),
        ("מה שעות הפתיחה של הספרייה?", CategoryEnum.GENERAL),
        ("מה המתכון להכנת פיצה?", CategoryEnum.OUT_OF_CONTEXT),
    ]

    print(f"🚀 Starting AI Classifier Performance Tests...\n")
    passed = 0
    total_time = 0

    for question, expected in test_cases:
        try:
            # מדידת זמן התחלה
            start_time = time.perf_counter()

            result = await classify_question(question)

            # מדידת זמן סיום וחישוב הפרש
            latency = time.perf_counter() - start_time
            total_time += latency

            status = "✅ PASS" if result == expected else "❌ FAIL"
            if result == expected:
                passed += 1

            print(f"Question: '{question}'")
            print(f"Result: {result.name} | Time: {latency:.2f}s | {status}")
            print("-" * 30)

        except Exception as e:
            print(f"❌ Error testing question '{question}': {e}")

        # השהיה למניעת Rate Limit (429)
        print("⏳ Sleeping 12s to avoid Rate Limit...")
        await asyncio.sleep(12)

    # סיכום תוצאות וממוצעים
    avg_latency = total_time / len(test_cases)
    accuracy = (passed / len(test_cases)) * 100

    print(f"\n📊 Performance Summary:")
    print(f"Accuracy: {passed}/{len(test_cases)} ({accuracy:.1f}%)")
    print(f"Average Response Time: {avg_latency:.2f}s")  # מדד קריטי ל-SRS

    if avg_latency <= 5.0:
        print("⚡ Speed Goal: Met (Under 5s)")
    else:
        print("🐢 Speed Goal: Failed (Over 5s) - Consider optimizing prompt or model")


if __name__ == "__main__":
    asyncio.run(run_classification_tests())
