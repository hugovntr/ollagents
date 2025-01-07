from typing import Callable, Optional, ParamSpec, TypeVar
from functools import wraps, reduce
import inspect

P = ParamSpec("P")
T = TypeVar("T")

class Tool:
    name: str
    description: str|None = None
    signature: dict[str, type]
    fn: Callable

    def __init__(self, name: str, description:str|None, signature: dict[str, type], fn: Callable[P, T]) -> None:
        self.name = name
        self.signature = signature
        self.description = description
        self.fn = fn

    def schema(self):
        properties = [
            {name: {"type": ty.__name__}}
            for name, ty in self.signature.items() if not isinstance(ty, type(None))
        ]
        properties = reduce(lambda a, b: dict(a, **b), properties) if len(properties) > 0 else {}
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "required": [name for name, ty in self.signature.items() if not isinstance(ty, type(None) or not isinstance(ty, Optional))],
                    "properties": properties,
                }
            }
        }

    def execute(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

def tool(fn: Callable[P, T]):
    """
    Decorator for Agent Tools
    """
    @wraps(fn)
    def wrapper():
        fn_sig = inspect.signature(fn)
        signature: dict[str, type] = {}
        for p in fn_sig.parameters.values():
            signature[p.name] = p.annotation

        return Tool(
            name= fn.__name__,
            description = fn.__doc__,
            signature= signature,
            fn = fn,
        )
    return wrapper
