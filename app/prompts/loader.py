import os
import re
from typing import Dict, Any

import yaml


PROMPTS_DIR = os.path.dirname(__file__)


def _render_template(template: str, variables: Dict[str, Any]) -> str:
    """Render a template using ``{{ var }}`` placeholders.

    This function supports simple variable substitution only. Each ``{{ name }}``
    in the template is replaced with the corresponding value from ``variables``.
    """
    if not variables:
        variables = {}
    pattern = re.compile(r"{{\s*(\w+)\s*}}")

    def repl(match: re.Match) -> str:
        key = match.group(1)
        if key not in variables:
            raise KeyError(f"Variable '{key}' not provided")
        return str(variables[key])

    return pattern.sub(lambda m: str(repl(m)), template)


def load_prompt(name: str, variables: Dict[str, Any] | None = None) -> str:
    """Load a YAML prompt and render it with variables.

    Parameters
    ----------
    name: str
        Name of the YAML file (without directory; ``.yaml`` extension optional).
    variables: dict, optional
        Dictionary of values used to render the template.

    Returns
    -------
    str
        The rendered prompt string.
    """
    if not name.endswith(".yaml"):
        filename = f"{name}.yaml"
    else:
        filename = name

    path = os.path.join(PROMPTS_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    template = data.get("template")
    if template is None:
        raise ValueError("YAML file must contain a 'template' field")

    return _render_template(template, variables or {})
