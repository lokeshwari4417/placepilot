from django.core.management.base import BaseCommand

from apps.coding.models import Problem, TestCase


class Command(BaseCommand):
    help = "Seed the database with sample coding problems"

    def handle(self, *args, **options):
        problems_data = [
            {
                "title": "Two Sum",
                "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
                "difficulty": Problem.Difficulty.EASY,
                "default_language": Problem.Language.PYTHON,
                "time_limit": 2,
                "memory_limit": 256,
                "tags": ["arrays", "hash-table"],
                "test_cases": [
                    {"input_data": "2 7 11 15\n9", "expected_output": "0 1", "order": 1, "is_hidden": False},
                    {"input_data": "3 2 4\n6", "expected_output": "1 2", "order": 2, "is_hidden": False},
                    {"input_data": "3 3\n6", "expected_output": "0 1", "order": 3, "is_hidden": True},
                ]
            },
            {
                "title": "Palindrome Check",
                "description": "Given a string s, return true if it is a palindrome, or false otherwise.",
                "difficulty": Problem.Difficulty.EASY,
                "default_language": Problem.Language.PYTHON,
                "time_limit": 1,
                "memory_limit": 256,
                "tags": ["strings", "two-pointers"],
                "test_cases": [
                    {"input_data": "racecar", "expected_output": "True", "order": 1, "is_hidden": False},
                    {"input_data": "hello", "expected_output": "False", "order": 2, "is_hidden": False},
                    {"input_data": "a", "expected_output": "True", "order": 3, "is_hidden": True},
                ]
            },
            {
                "title": "Maximum Subarray",
                "description": "Given an integer array nums, find the contiguous subarray which has the largest sum and return its sum.",
                "difficulty": Problem.Difficulty.MEDIUM,
                "default_language": Problem.Language.PYTHON,
                "time_limit": 2,
                "memory_limit": 256,
                "tags": ["arrays", "dynamic-programming"],
                "test_cases": [
                    {"input_data": "-2 1 -3 4 -1 2 1 -5 4", "expected_output": "6", "order": 1, "is_hidden": False},
                    {"input_data": "1", "expected_output": "1", "order": 2, "is_hidden": False},
                    {"input_data": "5 4 -1 7 8", "expected_output": "23", "order": 3, "is_hidden": True},
                ]
            }
        ]

        for problem_data in problems_data:
            test_cases = problem_data.pop("test_cases")
            problem, created = Problem.objects.get_or_create(
                title=problem_data["title"],
                defaults=problem_data
            )
            
            if created:
                self.stdout.write(f"Created problem: {problem.title}")
                
                for tc_data in test_cases:
                    TestCase.objects.create(
                        problem=problem,
                        **tc_data
                    )
                self.stdout.write(f"  Added {len(test_cases)} test cases")
            else:
                self.stdout.write(f"Problem already exists: {problem.title}")

        self.stdout.write(self.style.SUCCESS("Problems seeded successfully!"))
