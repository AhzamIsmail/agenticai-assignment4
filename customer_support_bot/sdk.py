# customer_support_bot/sdk.py
from dataclasses import dataclass, field
from typing import Dict, Callable, Optional, Any
import functools, re
from .logging_utils import log


@dataclass
class ModelSettings:
    tool_choice: str = "auto"
    metadata: Dict[str, Any] = field(default_factory=dict)


FUNCTION_REGISTRY = {}


# function_tool decorator
def function_tool(name: Optional[str] = None, *, is_enabled: Optional[Callable] = None, error_function: Optional[Callable] = None):
    def decorator(func: Callable):
        tool_name = name or func.__name__
        FUNCTION_REGISTRY[tool_name] = {"func": func, "is_enabled": is_enabled, "error_function": error_function}


        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log("tool_invoke", {"tool": tool_name, "args": args, "kwargs": kwargs})
            try:
               return func(*args, **kwargs)
            except Exception as e:
                if error_function:
                    return error_function(str(e), kwargs)
                raise
        return wrapper
    return decorator


# guardrail decorator
OFFENSIVE = {"idiot", "stupid", "hate"}
NEGATIVE = {"angry", "upset", "disappointed", "bad"}


def guardrail(func: Callable):
    @functools.wraps(func)
    def wrapper(agent, query: str, model_settings: ModelSettings):
        q = query.lower()
        if any(w in q for w in OFFENSIVE):
            return {"guardrail": "offensive", "message": "Please avoid offensive language."}
        if any(w in q for w in NEGATIVE):
            return {"guardrail": "negative", "message": "It seems you are upset. Escalating to human agent."}
        return func(agent, query, model_settings)
    return wrapper

