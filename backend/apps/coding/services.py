"""Business logic for the 'coding' module, kept out of views."""

import time
import subprocess
import tempfile
import os

from .models import Problem, Submission, TestCase


class CodeExecutionService:
    """Service for executing and validating code submissions."""
    
    @staticmethod
    def execute_code(submission):
        """Execute code against test cases and update submission status."""
        submission.status = Submission.Status.RUNNING
        submission.save()
        
        test_cases = submission.problem.test_cases.all()
        submission.total_test_cases = test_cases.count()
        passed = 0
        
        for test_case in test_cases:
            result = CodeExecutionService._run_single_test(
                submission.code,
                submission.language,
                test_case.input_data,
                test_case.expected_output,
                submission.problem.time_limit
            )
            
            if result["status"] == "passed":
                passed += 1
            elif result["status"] == "failed":
                submission.status = Submission.Status.WRONG_ANSWER
                submission.error_message = f"Test case {test_case.order} failed"
                break
            elif result["status"] == "tle":
                submission.status = Submission.Status.TIME_LIMIT_EXCEEDED
                submission.error_message = f"Time limit exceeded on test case {test_case.order}"
                break
            elif result["status"] == "error":
                submission.status = Submission.Status.RUNTIME_ERROR
                submission.error_message = result.get("error", "Runtime error")
                break
        
        submission.passed_test_cases = passed
        
        if passed == submission.total_test_cases and submission.total_test_cases > 0:
            submission.status = Submission.Status.ACCEPTED
        
        submission.save()
        return submission
    
    @staticmethod
    def _run_single_test(code, language, input_data, expected_output, time_limit):
        """Run a single test case (simplified implementation)."""
        # In production, this would use a sandboxed execution environment
        # For now, we'll do a basic Python execution simulation
        
        if language == Problem.Language.PYTHON:
            try:
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                    f.write(code)
                    temp_file = f.name
                
                try:
                    result = subprocess.run(
                        ['python', temp_file],
                        input=input_data,
                        capture_output=True,
                        text=True,
                        timeout=time_limit
                    )
                    
                    output = result.stdout.strip()
                    if output == expected_output.strip():
                        return {"status": "passed", "output": output}
                    else:
                        return {"status": "failed", "expected": expected_output, "got": output}
                except subprocess.TimeoutExpired:
                    return {"status": "tle"}
                except Exception as e:
                    return {"status": "error", "error": str(e)}
                finally:
                    os.unlink(temp_file)
            except Exception as e:
                return {"status": "error", "error": str(e)}
        
        # For other languages, return a placeholder response
        # In production, implement actual execution for each language
        return {"status": "error", "error": f"Execution for {language} not yet implemented"}
    
    @staticmethod
    def create_submission(user, problem, code, language):
        """Create a new submission and queue it for execution."""
        submission = Submission.objects.create(
            user=user,
            problem=problem,
            code=code,
            language=language,
            status=Submission.Status.PENDING
        )
        # In production, this would be queued for async execution
        # For now, execute synchronously
        CodeExecutionService.execute_code(submission)
        return submission
