# Ollagents

[Ollama](https://ollama.com) powered AI Agent Framework

Ollagents is a minimalistic python framework to build AI Agents on top of Ollama's function calling feature with the least amount of friction possible. 
No bloat / no learning curve. Simple, yet effective.

---

## Getting Started

### Installation
Start by installing `ollagents`:
```bash
# With PIP
pip install ollagents

# With UV
uv add ollagents
```

### Tool setup
Next, you go hop into the code and start defining your tools using the tool decorator:
```python
from ollagents import tool

@tool
def web_search(url: str):
    """Search information on a specific website via its URL"""
    pass
```
There are quite a few things to unpack from the code above:
- Use the `@tool` decorator on your function to mark it as being a tool.
- The function name will be directly tied to you tool visible name for the LLM (_in this case, `web_search`_)
- The description of your tool, that will be visible by the LLM on request, is made using regular python documentation
- Arguments, much like the function name, will also be visible by the LLM — So are their types! 
    - To mark an argument as optional, use the `Optional` type from the `typings` package
- For simplicity’s sake, it's **highly recommended** to always return a `str` from a tool.

### Agent
Now that you have your tools defined, you can move on to the definition of your agent. For that we will update the previous code to import the `Agent` class from `ollagents`
```python
from ollagents import Agent, tool
...
```

Next, we simply tell our agent what tool it can use:
```python
agent = Agent(tools=[web_search()])
```
Optionally here you can also change the system prompt by passing a string to the `system` argument:
```python
agent = Agent(tools=[web_search()], system="You are an helpful agent")
```

### Running all together
With the `Agent` and the list of tools defined, you are now ready to make a request.
There are a few arguments that you can pass to the agent's `run` function:
| Argument | Usage | Default Value|
| ------------- | -------------- | -------------- |
| `model` | The model that Ollama's backend will use to fulfil your request | None |
| `prompt` | The prompt (a.k.a. the question) | None |
| `stream` | Whether to use the agent in streaming mode (_requires some code adjustments_) | False |
| `verbose` | Agent will report all tool usage, as well as the arguments used | False |

Here's a basic example, following our above code:
```python
response = agent.run(
    model="qwen2.5:7b",
    prompt="Tell me more about runtime44.com"
)
```

### Streaming Mode
As mentioned in the table above, you can use streaming mode to receive partial response from your agent. To do that you will need to modify the `run` section of the code to handle python generators as follows:
```python
final_answer = ""
for part in agent.run(model="qwen2.5:7b", prompt="Tell me more about runtime44.com", stream=True):
    final_answer += part
    print(part, end="", flush=True)
```
> [!NOTE]
> Here, the `final_answer` variable is only necessary if you want to keep the final output of the agent somewhere to reuse. If you don't plan to, you can omit it.

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
