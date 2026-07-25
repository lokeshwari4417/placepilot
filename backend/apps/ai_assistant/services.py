"""
Routes AI assistant requests by 'type' to the appropriate prompt-builder,
then delegates completion to the configured provider (see providers/).
"""
from .providers.factory import get_ai_provider

PROMPT_BUILDERS = {
    # "explain": build_explain_prompt,
    # "interview_questions": build_interview_questions_prompt,
    # "resume_review": build_resume_review_prompt,
    # "project_suggestions": build_project_suggestions_prompt,
    # "plan": build_plan_prompt,
}


class AIAssistantService:
    def __init__(self):
        self.provider = get_ai_provider()

    def handle(self, request_type: str, payload: dict) -> str:
        builder = PROMPT_BUILDERS.get(request_type)
        if builder is None:
            raise ValueError(f"Unsupported AI assistant request type: {request_type}")
        prompt = builder(payload)
        return self.provider.generate(prompt, context=payload)
