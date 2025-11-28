"""
Seed Courses Script
Populates Firebase with course and module content.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import get_firestore_client
from data.courses_content import ALL_COURSES, ALL_MODULES, COMPLETE_MODULES
from datetime import datetime


def seed_courses():
    """Seed all courses to Firebase"""
    db = get_firestore_client()

    print("🚀 Seeding courses...")

    for course in ALL_COURSES:
        course_data = {
            **course,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        db.collection('courses').document(course['id']).set(course_data)
        print(f"  ✅ Course: {course['title']}")

    print(f"\n📚 Seeded {len(ALL_COURSES)} courses")


def seed_modules():
    """Seed all modules to Firebase"""
    db = get_firestore_client()

    print("\n🚀 Seeding modules...")

    for module in ALL_MODULES:
        # Check if module has phases (is complete)
        has_content = len(module.get('phases', [])) > 0

        # Convert to Firebase format
        module_data = {
            "id": module['id'],
            "course_id": module['course_id'],
            "title": module['title'],
            "description": module['description'],
            "icon": module['icon'],
            "order": module['order'],
            "difficulty": module['difficulty'],
            "estimated_duration_minutes": module['estimated_duration_minutes'],
            "xp_reward": module['xp_reward'],
            "coins_reward": module['coins_reward'],
            "has_content": has_content,
            "total_phases": len(module.get('phases', [])),
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        # If module has phases, convert them to lessons format for compatibility
        if has_content:
            lessons = []
            quiz_questions = []

            for phase in module['phases']:
                # Add phase lessons
                for lesson in phase['lessons']:
                    lessons.append({
                        "id": lesson['id'],
                        "phase_id": phase['id'],
                        "phase_title": phase['title'],
                        "title": lesson['title'],
                        "content": lesson['content'],
                        "duration_minutes": lesson['duration_minutes'],
                        "order": lesson['order']
                    })

                # Add phase quiz questions
                for q in phase['quiz']['questions']:
                    quiz_questions.append({
                        **q,
                        "phase_id": phase['id']
                    })

            # Create combined quiz for module
            module_data['lessons'] = lessons
            module_data['quiz'] = {
                "id": f"quiz_{module['id']}",
                "title": f"Quiz Final: {module['title']}",
                "description": f"Teste seus conhecimentos sobre {module['title']}",
                "passing_score": 70,
                "xp_reward": module['xp_reward'],
                "coins_reward": module['coins_reward'],
                "lives_cost": 1,
                "questions": quiz_questions
            }

            # Also store phases separately for phase-by-phase progression
            module_data['phases'] = module['phases']

        db.collection('learning_modules').document(module['id']).set(module_data)
        status = "✅" if has_content else "⏳"
        print(f"  {status} Module: {module['title']} {'(complete)' if has_content else '(coming soon)'}")

    print(f"\n📖 Seeded {len(ALL_MODULES)} modules ({len(COMPLETE_MODULES)} complete)")


def seed_all():
    """Seed everything"""
    print("=" * 50)
    print("🌱 FINAP Course Seeder")
    print("=" * 50)

    seed_courses()
    seed_modules()

    print("\n" + "=" * 50)
    print("✨ Seeding complete!")
    print("=" * 50)


def clear_and_seed():
    """Clear existing data and re-seed"""
    db = get_firestore_client()

    print("🗑️  Clearing existing courses and modules...")

    # Delete courses
    courses = db.collection('courses').stream()
    for doc in courses:
        doc.reference.delete()

    # Delete modules
    modules = db.collection('learning_modules').stream()
    for doc in modules:
        doc.reference.delete()

    print("  ✅ Cleared existing data")

    seed_all()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Seed FINAP courses to Firebase')
    parser.add_argument('--clear', action='store_true', help='Clear existing data before seeding')

    args = parser.parse_args()

    if args.clear:
        clear_and_seed()
    else:
        seed_all()
