"""
Comprehensive Answer Accuracy Test
Tests the AI's ability to provide correct answers with a large dataset.
This test uses the large_test_data fixture to simulate realistic conditions.
"""

import pytest
from ai.rag import process_campus_query
from db.models import CategoryEnum


@pytest.mark.asyncio
async def test_comprehensive_answer_accuracy(large_test_data, db_session):
    """
    Comprehensive test for answer accuracy with large dataset.
    Tests multiple question types across all categories to ensure
    the AI correctly retrieves and presents information from the database.
    """
    
    # Define test cases with expected information that should appear in the answer
    test_cases = [
        # ==========================================
        # SCHEDULE Category Tests
        # ==========================================
        {
            "question": "מתי המבחן במבני נתונים ואלגוריתמים?",
            "category": CategoryEnum.SCHEDULE,
            "expected_keywords": ["20", "יוני", "2025", "אודיטוריום מרכזי"],  # Date and room
            "description": "Exam date and location query",
        },
        {
            "question": "באיזה חדר יש לי שיעור בינה מלאכותית?",
            "category": CategoryEnum.SCHEDULE,
            "expected_keywords": ["אודיטוריום מרכזי"],  # Room name
            "description": "Course room query",
        },
        {
            "question": "מי המרצה של קורס מערכות הפעלה?",
            "category": CategoryEnum.SCHEDULE,
            "expected_keywords": ["חיים מזרחי"],  # Lecturer name
            "description": "Lecturer name query",
        },
        {
            "question": "מתי יש לי שיעור פיתוח מערכות Web?",
            "category": CategoryEnum.SCHEDULE,
            "expected_keywords": ["שני", "09:00", "12:00"],  # Day and time
            "description": "Course schedule query",
        },
        {
            "question": "מתי המבחן במבוא לסייבר?",
            "category": CategoryEnum.SCHEDULE,
            "expected_keywords": ["1", "יולי", "2025"],  # Exam date
            "description": "Exam date query for specific course",
        },
        {
            "question": "באיזה יום יש שיעור מתמטיקה בדידה?",
            "category": CategoryEnum.SCHEDULE,
            "expected_keywords": ["רביעי"],  # Day of week
            "description": "Day of week query",
        },
        
        # ==========================================
        # GENERAL Category Tests
        # ==========================================
        {
            "question": "מה שעות הפתיחה של המזכירות?",
            "category": CategoryEnum.GENERAL,
            "expected_keywords": ["09:00", "14:00", "א'-ה'"],  # Office hours
            "description": "Office hours query",
        },
        {
            "question": "איפה נמצאת הקפיטריה?",
            "category": CategoryEnum.GENERAL,
            "expected_keywords": ["קומת הקרקע", "מדעי החברה"],  # Location
            "description": "Cafeteria location query",
        },
        {
            "question": "מה שעות הפתיחה של הספרייה?",
            "category": CategoryEnum.GENERAL,
            "expected_keywords": ["08:00", "20:00", "א'-ה'"],  # Library hours
            "description": "Library hours query",
        },
        {
            "question": "איך מגישים בקשה למלגת הצטיינות?",
            "category": CategoryEnum.GENERAL,
            "expected_keywords": ["15.3", "מזכירות הסטודנטים"],  # Scholarship info
            "description": "Scholarship query",
        },
        {
            "question": "כמה עולה חניה בקמפוס?",
            "category": CategoryEnum.GENERAL,
            "expected_keywords": ["10", "200", "ש\"ח"],  # Parking cost
            "description": "Parking cost query",
        },
        {
            "question": "מה התהליך לביטול קורס?",
            "category": CategoryEnum.GENERAL,
            "expected_keywords": ["שבועיים", "סמסטר"],  # Course cancellation
            "description": "Course cancellation query",
        },
        
        # ==========================================
        # TECHNICAL Category Tests
        # ==========================================
        {
            "question": "איך מאפסים סיסמה למודל?",
            "category": CategoryEnum.TECHNICAL,
            "expected_keywords": ["שכחתי סיסמה"],  # Password reset
            "description": "Password reset query",
        },
        {
            "question": "איך מתחברים ל-WiFi בקמפוס?",
            "category": CategoryEnum.TECHNICAL,
            "expected_keywords": ["Campus-WiFi", "Student2025"],  # WiFi credentials
            "description": "WiFi connection query",
        },
        {
            "question": "המקרן בכיתה לא עובד, מה לעשות?",
            "category": CategoryEnum.TECHNICAL,
            "expected_keywords": ["IT", "1234"],  # Technical support
            "description": "Equipment issue query",
        },
        {
            "question": "איך מתחברים לשרתי המעבדה?",
            "category": CategoryEnum.TECHNICAL,
            "expected_keywords": ["VPN"],  # Lab server access
            "description": "Lab server access query",
        },
    ]
    
    # Track results
    passed = 0
    failed = 0
    results = []
    
    print("\n" + "=" * 80)
    print("🧪 COMPREHENSIVE ANSWER ACCURACY TEST")
    print("=" * 80)
    print(f"Testing {len(test_cases)} questions with large dataset...\n")
    
    for i, test_case in enumerate(test_cases, 1):
        question = test_case["question"]
        expected_category = test_case["category"]
        expected_keywords = test_case["expected_keywords"]
        description = test_case["description"]
        
        try:
            # Process the query
            result = await process_campus_query(question, db_session)
            
            answer = result.get("answer", "")
            actual_category = CategoryEnum[result.get("category", "GENERAL")]
            
            # Check if category matches
            category_match = actual_category == expected_category
            
            # Check if expected keywords appear in the answer (case-insensitive)
            answer_lower = answer.lower()
            found_keywords = [
                keyword for keyword in expected_keywords 
                if keyword.lower() in answer_lower
            ]
            keywords_match = len(found_keywords) > 0
            
            # Test passes if category matches AND at least one keyword is found
            test_passed = category_match and keywords_match
            
            if test_passed:
                passed += 1
                status = "✅ PASS"
            else:
                failed += 1
                status = "❌ FAIL"
            
            # Store result
            results.append({
                "question": question,
                "description": description,
                "status": status,
                "category_match": category_match,
                "expected_category": expected_category.name,
                "actual_category": actual_category.name,
                "found_keywords": found_keywords,
                "missing_keywords": [k for k in expected_keywords if k.lower() not in answer_lower],
                "answer_preview": answer[:100] + "..." if len(answer) > 100 else answer,
            })
            
            # Print result
            print(f"[{i}/{len(test_cases)}] {status}")
            print(f"  Question: {question}")
            print(f"  Category: {actual_category.name} {'✅' if category_match else '❌ (expected ' + expected_category.name + ')'}")
            print(f"  Keywords: Found {len(found_keywords)}/{len(expected_keywords)} - {found_keywords if found_keywords else 'None'}")
            if not keywords_match:
                print(f"  Missing: {[k for k in expected_keywords if k.lower() not in answer_lower]}")
            print()
            
        except Exception as e:
            failed += 1
            results.append({
                "question": question,
                "description": description,
                "status": "❌ ERROR",
                "error": str(e),
            })
            print(f"[{i}/{len(test_cases)}] ❌ ERROR")
            print(f"  Question: {question}")
            print(f"  Error: {e}\n")
    
    # Print summary
    print("=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {len(test_cases)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Accuracy: {(passed / len(test_cases) * 100):.1f}%")
    print("=" * 80)
    
    # Print detailed results for failed tests
    if failed > 0:
        print("\n❌ FAILED TESTS DETAILS:")
        print("-" * 80)
        for result in results:
            if "❌" in result["status"]:
                print(f"\nQuestion: {result['question']}")
                print(f"Description: {result['description']}")
                if "error" in result:
                    print(f"Error: {result['error']}")
                else:
                    if not result.get("category_match", False):
                        print(f"Category Mismatch: Expected {result['expected_category']}, Got {result['actual_category']}")
                    if result.get("missing_keywords"):
                        print(f"Missing Keywords: {result['missing_keywords']}")
                    print(f"Answer Preview: {result['answer_preview']}")
        print("-" * 80)
    
    # Assert that at least 70% of tests pass (reasonable threshold)
    success_rate = passed / len(test_cases)
    assert success_rate >= 0.70, (
        f"Answer accuracy too low: {success_rate * 100:.1f}% "
        f"({passed}/{len(test_cases)} passed). Minimum required: 70%"
    )
    
    print(f"\n✅ Test suite passed! Success rate: {success_rate * 100:.1f}%")
