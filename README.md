# Ollagents

[Ollama](https://ollama.com) powered AI Agent Framework

Ollagents is a minimalistic python framework to build AI Agents on top of Ollama's function calling feature with the least amount of friction possible. 
No bloat / no learning curve. Simple, yet effective.

---

## Examples
1. Basic Website Parser
```python
from ollagents import Agent, tool

@tool
def web_search(url: str);
    """Search information on a specific website"""

    from requests import request
    from markitdown import MarkItDown

    resp = request(
        method="GET",
        url=url,
    )
    if not resp or not resp.ok:
        return "Invalid URL, please try again"

    return MarkItDown().convert(resp).text_content

agent = Agent(
    tools=[web_search()]
)

response = agent.run(
    model="qwen2.5:7b",
    prompt="Tell me more about runtime44.com", 
)
print(response)
```
> [!NOTE]
> This examples requires installing `requests` and `markitdown`.

## Features

1. **Minimal footprint**
```python
from ollagents import Agent, tool

@tool
def your_tool_name():
    """Describe your tool in comments"""
    pass

agent = Agent(tools=[your_tool_name()])
response = agent.run(...)
```

2. **Fail-safe** using quantum parallel validation (_that's a lie, it's just a `while i < X`..._)
3. **Streaming Response**
```python
agent.run(..., stream=True)
```
4. **Verbose Mode** to know what your agent is doing at any time.
```python
agent.run(..., verbose=True)
```
5. **Per-request model definition**, in case you want to chain calls and use different models for a specific agent or a specific request

## How It Works

- To define a **tool**, you have to decorate your function with the `@tool` decorator — Nothing extremely complex here.
- The name of your tool (that will be visible by the LLM) is going to be inferred from the name of your function. For example, calling your function `web_seach` will result in a tool with the same name.
- You can describe your tool using python native doc, it will be extracted and passed to the LLM during the request. (c.f earlier examples)
- You can override the system prompt when creating your agent:
```python
agent = Agent(system="My custom system prompt", tools=...)
```
- Typing is important, using `Optional` for example, will make your tool argument ... optional, meaning that if the LLM decides that it is pertinent to input something here, it will otherwise it won't. As opposed to required parameters that will always be filled by the LLM

## BibTeX
```bibtex
@Misc{ollagents,
  title =        {Ollagents: Minimalistic framework to build AI agents powered by Ollama},
  author =       {Hugo Ventura},
  howpublished = {\url{https://github.com/hugovntr/ollagents}},
  year =         {2025}
}
```

---

This framework is subject to change (_a lot_), so whatever you do, don't put this in production or do anything stupid with it and blame me. From this point on, it's all on you!
