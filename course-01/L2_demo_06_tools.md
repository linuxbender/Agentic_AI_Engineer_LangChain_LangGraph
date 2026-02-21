```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    HumanMessage, 
    SystemMessage, 
    ToolMessage
)
from langchain.tools import tool
from langchain_core.output_parsers.openai_tools import parse_tool_calls
from dotenv import load_dotenv
```


```python
load_dotenv()
```




    False




```python
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.0,
    api_key ="voc-xxx",
    base_url="https://openai.vocareum.com/v1"
)
```

**Tool creation**


```python
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b
```


```python
tools = [multiply]
tool_map = {tool.name:tool for tool in tools}
```


```python
tool_map
```




    {'multiply': StructuredTool(name='multiply', description='Multiply two numbers.', args_schema=<class 'langchain_core.utils.pydantic.multiply'>, func=<function multiply at 0x7a0f659c2560>)}



**Binding Tools**


```python
llm_with_tools = llm.bind_tools(tools)
```


```python
question = "3 multiplied by 2"
```


```python
messages = [
    SystemMessage("You're a helpful assistant"),
    HumanMessage(question)
]
```


```python
ai_message = llm_with_tools.invoke(messages)
```


```python
ai_message
```




    AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_eOh7gA3TMvRdGPeyRsOJRvgM', 'function': {'arguments': '{"a":3,"b":2}', 'name': 'multiply'}, 'type': 'function'}], 'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 17, 'prompt_tokens': 54, 'total_tokens': 71, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_084a28d6e8', 'finish_reason': 'tool_calls', 'logprobs': None}, id='run-3130fc30-f423-4d75-b48d-73e1ec016a2b-0', tool_calls=[{'name': 'multiply', 'args': {'a': 3, 'b': 2}, 'id': 'call_eOh7gA3TMvRdGPeyRsOJRvgM', 'type': 'tool_call'}], usage_metadata={'input_tokens': 54, 'output_tokens': 17, 'total_tokens': 71, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})




```python
messages.append(ai_message)
```


```python
messages
```




    [SystemMessage(content="You're a helpful assistant", additional_kwargs={}, response_metadata={}),
     HumanMessage(content='3 multiplied by 2', additional_kwargs={}, response_metadata={}),
     AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_eOh7gA3TMvRdGPeyRsOJRvgM', 'function': {'arguments': '{"a":3,"b":2}', 'name': 'multiply'}, 'type': 'function'}], 'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 17, 'prompt_tokens': 54, 'total_tokens': 71, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_084a28d6e8', 'finish_reason': 'tool_calls', 'logprobs': None}, id='run-3130fc30-f423-4d75-b48d-73e1ec016a2b-0', tool_calls=[{'name': 'multiply', 'args': {'a': 3, 'b': 2}, 'id': 'call_eOh7gA3TMvRdGPeyRsOJRvgM', 'type': 'tool_call'}], usage_metadata={'input_tokens': 54, 'output_tokens': 17, 'total_tokens': 71, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})]



**Using Tool Calls**


```python
parsed_tool_calls = parse_tool_calls(
    ai_message.additional_kwargs.get("tool_calls")
)
```


```python
parsed_tool_calls
```




    [{'name': 'multiply',
      'args': {'a': 3, 'b': 2},
      'id': 'call_eOh7gA3TMvRdGPeyRsOJRvgM',
      'type': 'tool_call'}]




```python
for tool_call in parsed_tool_calls:
    tool_call_id = tool_call['id']
    function_name = tool_call['name']
    arguments = tool_call['args']
    func = tool_map[function_name]
    result = func.invoke(arguments)
    tool_message = ToolMessage(
        content=result,
        name=function_name,
        tool_call_id=tool_call_id,
    )
    messages.append(tool_message)
```

**Sending the result back to the LLM**


```python
messages
```




    [SystemMessage(content="You're a helpful assistant", additional_kwargs={}, response_metadata={}),
     HumanMessage(content='3 multiplied by 2', additional_kwargs={}, response_metadata={}),
     AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_eOh7gA3TMvRdGPeyRsOJRvgM', 'function': {'arguments': '{"a":3,"b":2}', 'name': 'multiply'}, 'type': 'function'}], 'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 17, 'prompt_tokens': 54, 'total_tokens': 71, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_084a28d6e8', 'finish_reason': 'tool_calls', 'logprobs': None}, id='run-3130fc30-f423-4d75-b48d-73e1ec016a2b-0', tool_calls=[{'name': 'multiply', 'args': {'a': 3, 'b': 2}, 'id': 'call_eOh7gA3TMvRdGPeyRsOJRvgM', 'type': 'tool_call'}], usage_metadata={'input_tokens': 54, 'output_tokens': 17, 'total_tokens': 71, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}),
     ToolMessage(content='6', name='multiply', tool_call_id='call_eOh7gA3TMvRdGPeyRsOJRvgM')]




```python
ai_message = llm_with_tools.invoke(messages)
```


```python
ai_message
```




    AIMessage(content='3 multiplied by 2 is 6.', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 10, 'prompt_tokens': 79, 'total_tokens': 89, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_084a28d6e8', 'finish_reason': 'stop', 'logprobs': None}, id='run-542940b0-2096-4189-b933-14ec83f422d7-0', usage_metadata={'input_tokens': 79, 'output_tokens': 10, 'total_tokens': 89, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})




```python

```
