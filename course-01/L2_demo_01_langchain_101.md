```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
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
    api_key="voc-xxx",
    base_url="https://openai.vocareum.com/v1"
)
```


```python
llm.invoke("Hello there")
```




    AIMessage(content='Hello! How can I assist you today?', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 9, 'prompt_tokens': 9, 'total_tokens': 18, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_373a14eb6f', 'finish_reason': 'stop', 'logprobs': None}, id='run-9d3d491f-4ecf-4d10-870a-30d3b05732c4-0', usage_metadata={'input_tokens': 9, 'output_tokens': 9, 'total_tokens': 18, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})



**Chat Structure**


```python
messages = [ 
    SystemMessage("You are a geography tutor"),
    HumanMessage("What's the capital of Brazil?")
]

```


```python
llm.invoke(messages)
```




    AIMessage(content='The capital of Brazil is Brasília. It was officially inaugurated as the capital on April 21, 1960, and was designed by the architect Oscar Niemeyer and urban planner Lúcio Costa.', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 40, 'prompt_tokens': 22, 'total_tokens': 62, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_373a14eb6f', 'finish_reason': 'stop', 'logprobs': None}, id='run-60d01a2c-5209-4882-b04f-1fce68bfec09-0', usage_metadata={'input_tokens': 22, 'output_tokens': 40, 'total_tokens': 62, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})




```python
messages = [ 
    SystemMessage("You are a geography tutor"),
    HumanMessage("What's the capital of Brazil?"),
    AIMessage("The capital of Brazil is Brasília"),
    HumanMessage("What's the capital of Canada?"),
]
```


```python
llm.invoke(messages)
```




    AIMessage(content='The capital of Canada is Ottawa.', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 7, 'prompt_tokens': 42, 'total_tokens': 49, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_373a14eb6f', 'finish_reason': 'stop', 'logprobs': None}, id='run-b006b31a-1c16-42ac-b66b-fa5547b012b3-0', usage_metadata={'input_tokens': 42, 'output_tokens': 7, 'total_tokens': 49, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})



**Pure Python prompts: f-strings and str.format()**


```python
topic = "Python"
prompt = f"Tell me a joke about {topic}"
llm.invoke(prompt)
```




    AIMessage(content='Why do Python programmers prefer dark mode?\n\nBecause light attracts bugs!', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 13, 'prompt_tokens': 13, 'total_tokens': 26, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_373a14eb6f', 'finish_reason': 'stop', 'logprobs': None}, id='run-ec564d12-2edd-4a11-9983-fd27081aef5b-0', usage_metadata={'input_tokens': 13, 'output_tokens': 13, 'total_tokens': 26, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})




```python
prompt
```




    'Tell me a joke about Python'




```python
prompt = "Tell me a joke about {topic}"
llm.invoke(prompt.format(topic = "Python"))
```




    AIMessage(content='Why do Python programmers prefer dark mode?\n\nBecause light attracts bugs!', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 13, 'prompt_tokens': 13, 'total_tokens': 26, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_373a14eb6f', 'finish_reason': 'stop', 'logprobs': None}, id='run-9203fbc5-2ce6-4aa4-8e11-eb255da100f0-0', usage_metadata={'input_tokens': 13, 'output_tokens': 13, 'total_tokens': 26, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})




```python
prompt.format(topic = "Python")
```




    'Tell me a joke about Python'



**Prompt Templates**


```python
prompt_template = PromptTemplate(
    template="Tell me a joke about {topic}"
)
```


```python
prompt_template
```




    PromptTemplate(input_variables=['topic'], input_types={}, partial_variables={}, template='Tell me a joke about {topic}')




```python
prompt_template.format(topic="Python")
```




    'Tell me a joke about Python'




```python
prompt_template.invoke({"topic":"Python"})
```




    StringPromptValue(text='Tell me a joke about Python')




```python
llm.invoke(
    prompt_template.invoke({"topic":"Python"})
)
```




    AIMessage(content='Why do Python programmers prefer dark mode?\n\nBecause light attracts bugs!', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 13, 'prompt_tokens': 13, 'total_tokens': 26, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_373a14eb6f', 'finish_reason': 'stop', 'logprobs': None}, id='run-145fe0e3-3c4b-4f40-8a30-97c1731a6fae-0', usage_metadata={'input_tokens': 13, 'output_tokens': 13, 'total_tokens': 26, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})



**Few Shot Prompt**


```python
example_prompt = PromptTemplate(
    template="Question: {input}\nThought: {thought}\nResponse: {output}"
)
```


```python
examples = [
    {
        "input": "A train leaves city A for city B at 60 km/h, and another train leaves city B for city A at 40 km/h. If the distance between them is 200 km, how long until they meet?", 
        "thought": "The trains are moving towards each other, so their relative speed is 60 + 40 = 100 km/h. The time to meet is distance divided by relative speed: 200 / 100 = 2 hours.",
        "output": "2 hours",
    },
    {
        "input": "If a store applies a 20% discount to a $50 item, what is the final price?", 
        "thought": "A 20% discount means multiplying by 0.8. So, $50 × 0.8 = $40.",
        "output": "$40",
    },
    {
        "input": "A farmer has chickens and cows. If there are 10 heads and 32 legs, how many of each animal are there?", 
        "thought": "Let x be chickens and y be cows. We have two equations: x + y = 10 (heads) and 2x + 4y = 32 (legs). Solving: x + y = 10 → x = 10 - y. Substituting: 2(10 - y) + 4y = 32 → 20 - 2y + 4y = 32 → 2y = 12 → y = 6, so x = 4.",
        "output": "4 chickens, 6 cows",
    },
    {
        "input": "If a car travels 90 km in 1.5 hours, what is its average speed?", 
        "thought": "Speed is distance divided by time: 90 km / 1.5 hours = 60 km/h.",
        "output": "60 km/h",
    },
    {
        "input": "John is twice as old as Alice. In 5 years, their combined age will be 35. How old is Alice now?", 
        "thought": "Let Alice's age be x. Then John’s age is 2x. In 5 years, their ages will be x+5 and 2x+5. Their sum is 35: x+5 + 2x+5 = 35 → 3x + 10 = 35 → 3x = 25 → x = 8.33.",
        "output": "8.33 years old",
    },
]
```


```python
print(example_prompt.invoke(examples[0]).to_string())
```

    Question: A train leaves city A for city B at 60 km/h, and another train leaves city B for city A at 40 km/h. If the distance between them is 200 km, how long until they meet?
    Thought: The trains are moving towards each other, so their relative speed is 60 + 40 = 100 km/h. The time to meet is distance divided by relative speed: 200 / 100 = 2 hours.
    Response: 2 hours



```python
prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Question: {input}",
    input_variables=["input"],
)
```


```python
response = llm.invoke(
    prompt_template.invoke({"input":"If today is Wednesday, what day will it be in 10 days?"})
)
print(response.content) # Response should be Saturday
```

    Thought: To find the day of the week in 10 days, we can calculate the remainder of 10 divided by 7 (since there are 7 days in a week). 10 ÷ 7 = 1 remainder 3. This means 10 days from Wednesday is 3 days later. Counting from Wednesday: Thursday (1), Friday (2), Saturday (3). 
    
    Response: Saturday



```python

```
