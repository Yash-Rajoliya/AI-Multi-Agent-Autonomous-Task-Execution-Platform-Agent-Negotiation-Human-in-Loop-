from typing import Dict


class SystemPrompts:
    """
    Central registry for global system prompts
    """

    BASE_SYSTEM_PROMPT = """
You are an autonomous AI system operating in a multi-agent environment.
You must:
- Think step-by-step
- Use tools when necessary
- Minimize cost and latency
- Ensure correctness and safety
"""

    SAFETY_PROMPT = """
You must avoid:
- Harmful instructions
- Unauthorized data access
- Unsafe code execution
"""

    EVALUATION_PROMPT = """
Evaluate outputs critically.
Focus on:
- correctness
- completeness
- clarity
"""

    @classmethod
    def get_all(cls) -> Dict[str, str]:
        return {
            "base": cls.BASE_SYSTEM_PROMPT,
            "safety": cls.SAFETY_PROMPT,
            "evaluation": cls.EVALUATION_PROMPT
        }

    @classmethod
    def build_system_prompt(cls) -> str:
        prompts = cls.get_all()
        return "\n\n".join(prompts.values())