from ollama import Client
from .tools import Tool
from functools import reduce

class Agent:
    tools: list[Tool]
    system: str | None
    client: Client

    def __init__(self, tools: list[Tool], system: str | None = None) -> None:
        """
        - system (`str | None`): Override the default system prompt
        - tools (`list[Tool]`): List the tools that the LLM could use
        """
        self.tools = tools
        self.system = system
        self.client = Client()

    def run(self, prompt: str, model: str, stream: bool = False, verbose: bool = False):
        messages = [
        {"role": "system", "content": "You will decompose all tasks into subtasks and use the tools available to you in order to comply with the user's request. Once you have the answers that you need, stop calling tools and inform the user of your answer" if not self.system else self.system},
            {"role": "user", "content": prompt}
        ]

        available_fn = [{t.name: t.execute} for t in self.tools]
        available_fn = reduce(lambda a, b: dict(a, **b), available_fn) if len(available_fn) > 0 else {}

        
        def loop(messages: list) -> tuple[list, bool]:
            response = self.client.chat(model, messages, tools=[t.schema() for t in self.tools])

            if response.message.tool_calls:
                for tool in response.message.tool_calls:
                    if fn := available_fn.get(tool.function.name):
                        print(f"[->] Calling tool `{tool.function.name}` with arguments: {tool.function.arguments}") if verbose else None
                        output = fn(**tool.function.arguments)
                        messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})
                        return messages, False
            
            return messages, True

        done = False
        i = 0
        while  i < 10:
            m, done = loop(messages)
            messages = m
            if done:
                break
            i += 1


        if not stream:
            final_response = self.client.chat(model, messages)
            return final_response.message.content
        final_response = self.client.chat(model, messages, stream=True)
        for part in final_response:
            yield part.message.content
