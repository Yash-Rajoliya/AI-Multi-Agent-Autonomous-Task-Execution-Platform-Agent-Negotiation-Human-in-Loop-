from typing import Dict, Any
import re


class PromptTemplate:
    """
    Dynamic prompt builder with variable injection
    """

    def __init__(self, template: str):
        self.template = template

    def render(self, variables: Dict[str, Any]) -> str:
        result = self.template

        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            result = result.replace(placeholder, str(value))

        return result

    def validate(self, variables: Dict[str, Any]):
        placeholders = re.findall(r"\{\{(.*?)\}\}", self.template)

        missing = [p for p in placeholders if p not in variables]

        if missing:
            raise ValueError(f"Missing variables: {missing}")

    def safe_render(self, variables: Dict[str, Any]) -> str:
        self.validate(variables)
        return self.render(variables)