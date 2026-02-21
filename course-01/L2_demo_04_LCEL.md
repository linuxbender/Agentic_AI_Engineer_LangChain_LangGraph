```python
%pip install grandalf
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableLambda, RunnableParallel
from langchain_core.tracers.context import collect_runs
from dotenv import load_dotenv
```

    Collecting grandalf
      Downloading grandalf-0.8-py3-none-any.whl (41 kB)
    [2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m41.8/41.8 kB[0m [31m2.3 MB/s[0m eta [36m0:00:00[0m
    [?25hCollecting pyparsing
      Downloading pyparsing-3.3.2-py3-none-any.whl (122 kB)
    [2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m122.8/122.8 kB[0m [31m5.4 MB/s[0m eta [36m0:00:00[0m
    [?25hInstalling collected packages: pyparsing, grandalf
    Successfully installed grandalf-0.8 pyparsing-3.3.2
    
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m A new release of pip is available: [0m[31;49m23.0.1[0m[39;49m -> [0m[32;49m26.0.1[0m
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m To update, run: [0m[32;49mpip install --upgrade pip[0m
    Note: you may need to restart the kernel to use updated packages.



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

## Chaining invocations


```python
prompt = PromptTemplate(
    template="Tell me a joke about {topic}"
)
```


```python
parser = StrOutputParser()
```


```python
parser.invoke(
    llm.invoke(
        prompt.invoke(
            {"topic": "Python"}
        )
    )
)
```




    'Why do Python programmers prefer dark mode?\n\nBecause light attracts bugs! 🐍✨'



## Runnables

Runnables can be 
- executed
    - invoke(), 
    - batch() 
    - and stream()
- inspected,
- and composed


```python
runnables = [prompt, llm, parser]
```

**Execute methods**


```python
for runnable in runnables:
    print(f"{repr(runnable).split('(')[0]}")
    print(f"\tINVOKE: {repr(runnable.invoke)}")
    print(f"\tBATCH: {repr(runnable.batch)}")
    print(f"\tSTREAM: {repr(runnable.stream)}\n")
```

    PromptTemplate
    	INVOKE: <bound method BasePromptTemplate.invoke of PromptTemplate(input_variables=['topic'], input_types={}, partial_variables={}, template='Tell me a joke about {topic}')>
    	BATCH: <bound method Runnable.batch of PromptTemplate(input_variables=['topic'], input_types={}, partial_variables={}, template='Tell me a joke about {topic}')>
    	STREAM: <bound method Runnable.stream of PromptTemplate(input_variables=['topic'], input_types={}, partial_variables={}, template='Tell me a joke about {topic}')>
    
    ChatOpenAI
    	INVOKE: <bound method BaseChatModel.invoke of ChatOpenAI(client=<openai.resources.chat.completions.Completions object at 0x7c9e3e6df940>, async_client=<openai.resources.chat.completions.AsyncCompletions object at 0x7c9e50293850>, root_client=<openai.OpenAI object at 0x7c9e3e6dcaf0>, root_async_client=<openai.AsyncOpenAI object at 0x7c9e3e6df970>, model_name='gpt-4o-mini', temperature=0.0, model_kwargs={}, openai_api_key=SecretStr('**********'), openai_api_base='https://openai.vocareum.com/v1')>
    	BATCH: <bound method Runnable.batch of ChatOpenAI(client=<openai.resources.chat.completions.Completions object at 0x7c9e3e6df940>, async_client=<openai.resources.chat.completions.AsyncCompletions object at 0x7c9e50293850>, root_client=<openai.OpenAI object at 0x7c9e3e6dcaf0>, root_async_client=<openai.AsyncOpenAI object at 0x7c9e3e6df970>, model_name='gpt-4o-mini', temperature=0.0, model_kwargs={}, openai_api_key=SecretStr('**********'), openai_api_base='https://openai.vocareum.com/v1')>
    	STREAM: <bound method BaseChatModel.stream of ChatOpenAI(client=<openai.resources.chat.completions.Completions object at 0x7c9e3e6df940>, async_client=<openai.resources.chat.completions.AsyncCompletions object at 0x7c9e50293850>, root_client=<openai.OpenAI object at 0x7c9e3e6dcaf0>, root_async_client=<openai.AsyncOpenAI object at 0x7c9e3e6df970>, model_name='gpt-4o-mini', temperature=0.0, model_kwargs={}, openai_api_key=SecretStr('**********'), openai_api_base='https://openai.vocareum.com/v1')>
    
    StrOutputParser
    	INVOKE: <bound method BaseOutputParser.invoke of StrOutputParser()>
    	BATCH: <bound method Runnable.batch of StrOutputParser()>
    	STREAM: <bound method Runnable.stream of StrOutputParser()>
    


**Inspect**


```python
for runnable in runnables:
    print(f"{repr(runnable).split('(')[0]}")
    print(f"\tINPUT: {repr(runnable.get_input_schema())}")
    print(f"\tOUTPUT: {repr(runnable.get_output_schema())}")
    print(f"\tCONFIG: {repr(runnable.config_schema())}\n")
```

    PromptTemplate
    	INPUT: <class 'langchain_core.utils.pydantic.PromptInput'>
    	OUTPUT: <class 'langchain_core.prompts.prompt.PromptTemplateOutput'>
    	CONFIG: <class 'langchain_core.utils.pydantic.PromptTemplateConfig'>
    
    ChatOpenAI
    	INPUT: <class 'langchain_openai.chat_models.base.ChatOpenAIInput'>
    	OUTPUT: <class 'langchain_openai.chat_models.base.ChatOpenAIOutput'>
    	CONFIG: <class 'langchain_core.utils.pydantic.ChatOpenAIConfig'>
    
    StrOutputParser
    	INPUT: <class 'langchain_core.output_parsers.string.StrOutputParserInput'>
    	OUTPUT: <class 'langchain_core.output_parsers.string.StrOutputParserOutput'>
    	CONFIG: <class 'langchain_core.utils.pydantic.StrOutputParserConfig'>
    


**Config**


```python
with collect_runs() as run_collection:
    result = llm.invoke(
        "Hello", 
        config={
            'run_name': 'demo_run', 
            'tags': ['demo', 'lcel'], 
            'metadata': {'lesson': 2}
        }
    )
```


```python
run_collection.traced_runs
```




    [RunTree(id=a512302d-b84a-4e08-8559-aa86f652bb3a, name='demo_run', run_type='llm', dotted_order='20260221T115838806926Za512302d-b84a-4e08-8559-aa86f652bb3a')]




```python
run_collection.traced_runs[0].dict()
```




    {'id': UUID('a512302d-b84a-4e08-8559-aa86f652bb3a'),
     'name': 'demo_run',
     'start_time': datetime.datetime(2026, 2, 21, 11, 58, 38, 806926, tzinfo=datetime.timezone.utc),
     'run_type': 'llm',
     'end_time': datetime.datetime(2026, 2, 21, 11, 58, 39, 879265, tzinfo=datetime.timezone.utc),
     'extra': {'invocation_params': {'model': 'gpt-4o-mini',
       'model_name': 'gpt-4o-mini',
       'stream': False,
       'n': 1,
       'temperature': 0.0,
       '_type': 'openai-chat',
       'stop': None},
      'options': {'stop': None},
      'batch_size': 1,
      'metadata': {'lesson': 2,
       'ls_provider': 'openai',
       'ls_model_name': 'gpt-4o-mini',
       'ls_model_type': 'chat',
       'ls_temperature': 0.0}},
     'error': None,
     'serialized': {'lc': 1,
      'type': 'constructor',
      'id': ['langchain', 'chat_models', 'openai', 'ChatOpenAI'],
      'kwargs': {'model_name': 'gpt-4o-mini',
       'temperature': 0.0,
       'openai_api_key': {'lc': 1, 'type': 'secret', 'id': ['OPENAI_API_KEY']},
       'openai_api_base': 'https://openai.vocareum.com/v1',
       'max_retries': 2,
       'n': 1},
      'name': 'ChatOpenAI'},
     'events': [{'name': 'start',
       'time': datetime.datetime(2026, 2, 21, 11, 58, 38, 806926, tzinfo=datetime.timezone.utc)},
      {'name': 'end',
       'time': datetime.datetime(2026, 2, 21, 11, 58, 39, 879265, tzinfo=datetime.timezone.utc)}],
     'inputs': {'prompts': ['Human: Hello']},
     'outputs': {'generations': [[{'text': 'Hello! How can I assist you today?',
         'generation_info': {'finish_reason': 'stop', 'logprobs': None},
         'type': 'ChatGeneration',
         'message': {'lc': 1,
          'type': 'constructor',
          'id': ['langchain', 'schema', 'messages', 'AIMessage'],
          'kwargs': {'content': 'Hello! How can I assist you today?',
           'additional_kwargs': {'refusal': None},
           'response_metadata': {'token_usage': {'completion_tokens': 9,
             'prompt_tokens': 8,
             'total_tokens': 17,
             'completion_tokens_details': {'accepted_prediction_tokens': 0,
              'audio_tokens': 0,
              'reasoning_tokens': 0,
              'rejected_prediction_tokens': 0},
             'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}},
            'model_name': 'gpt-4o-mini-2024-07-18',
            'system_fingerprint': 'fp_373a14eb6f',
            'finish_reason': 'stop',
            'logprobs': None},
           'type': 'ai',
           'id': 'run-a512302d-b84a-4e08-8559-aa86f652bb3a-0',
           'usage_metadata': {'input_tokens': 8,
            'output_tokens': 9,
            'total_tokens': 17,
            'input_token_details': {'audio': 0, 'cache_read': 0},
            'output_token_details': {'audio': 0, 'reasoning': 0}},
           'tool_calls': [],
           'invalid_tool_calls': []}}}]],
      'llm_output': {'token_usage': {'completion_tokens': 9,
        'prompt_tokens': 8,
        'total_tokens': 17,
        'completion_tokens_details': {'accepted_prediction_tokens': 0,
         'audio_tokens': 0,
         'reasoning_tokens': 0,
         'rejected_prediction_tokens': 0},
        'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}},
       'model_name': 'gpt-4o-mini-2024-07-18',
       'system_fingerprint': 'fp_373a14eb6f'},
      'run': None,
      'type': 'LLMResult'},
     'reference_example_id': None,
     'parent_run_id': None,
     'tags': ['demo', 'lcel'],
     'attachments': {},
     'child_runs': [],
     'session_name': 'default',
     'session_id': None,
     'dotted_order': '20260221T115838806926Za512302d-b84a-4e08-8559-aa86f652bb3a',
     'trace_id': UUID('a512302d-b84a-4e08-8559-aa86f652bb3a')}



**Compose Runnables**


```python
chain = RunnableSequence(prompt, llm, parser)
```


```python
type(chain)
```




    langchain_core.runnables.base.RunnableSequence




```python
chain.invoke({"topic": "Python"})
```




    'Why do Python programmers prefer dark mode?\n\nBecause light attracts bugs!'




```python
for chunk in chain.stream({"topic": "Python"}):
    print(chunk, end="", flush=True)
```

    Why do Python programmers prefer dark mode?
    
    Because light attracts bugs!


```python
chain.batch([
    {"topic": "Python"},
    {"topic": "Data"},
    {"topic": "Machine Learning"},
])
```




    ['Why do Python programmers prefer dark mode?\n\nBecause light attracts bugs!',
     'Why did the data break up with the database?\n\nBecause it found someone more relational!',
     'Why did the neural network break up with the decision tree?\n\nBecause it found someone with more layers!']




```python
chain.get_graph().print_ascii()
```

         +-------------+       
         | PromptInput |       
         +-------------+       
                *              
                *              
                *              
        +----------------+     
        | PromptTemplate |     
        +----------------+     
                *              
                *              
                *              
          +------------+       
          | ChatOpenAI |       
          +------------+       
                *              
                *              
                *              
       +-----------------+     
       | StrOutputParser |     
       +-----------------+     
                *              
                *              
                *              
    +-----------------------+  
    | StrOutputParserOutput |  
    +-----------------------+  


**Turn any function into a runnable**


```python
def double(x:int)->int:
    return 2*x
```


```python
runnable = RunnableLambda(double)
runnable.invoke(2)
```




    4



**Parallel Runnables**


```python
parallel_chain = RunnableParallel(
    double=RunnableLambda(lambda x: x * 2),
    triple=RunnableLambda(lambda x: x * 3),
)
```


```python
parallel_chain.invoke(3)
```




    {'double': 6, 'triple': 9}




```python
parallel_chain.get_graph().print_ascii()
```

    +------------------------------+   
    | Parallel<double,triple>Input |   
    +------------------------------+   
               **        **            
             **            **          
            *                *         
      +--------+          +--------+   
      | Lambda |          | Lambda |   
      +--------+          +--------+   
               **        **            
                 **    **              
                   *  *                
    +-------------------------------+  
    | Parallel<double,triple>Output |  
    +-------------------------------+  


## LCEL


```python
prompt
```




    PromptTemplate(input_variables=['topic'], input_types={}, partial_variables={}, template='Tell me a joke about {topic}')




```python
llm
```




    ChatOpenAI(client=<openai.resources.chat.completions.Completions object at 0x7c9e3e6df940>, async_client=<openai.resources.chat.completions.AsyncCompletions object at 0x7c9e50293850>, root_client=<openai.OpenAI object at 0x7c9e3e6dcaf0>, root_async_client=<openai.AsyncOpenAI object at 0x7c9e3e6df970>, model_name='gpt-4o-mini', temperature=0.0, model_kwargs={}, openai_api_key=SecretStr('**********'), openai_api_base='https://openai.vocareum.com/v1')




```python
parser
```




    StrOutputParser()




```python
chain = RunnableSequence(prompt, llm, parser)
chain
```




    PromptTemplate(input_variables=['topic'], input_types={}, partial_variables={}, template='Tell me a joke about {topic}')
    | ChatOpenAI(client=<openai.resources.chat.completions.Completions object at 0x7c9e3e6df940>, async_client=<openai.resources.chat.completions.AsyncCompletions object at 0x7c9e50293850>, root_client=<openai.OpenAI object at 0x7c9e3e6dcaf0>, root_async_client=<openai.AsyncOpenAI object at 0x7c9e3e6df970>, model_name='gpt-4o-mini', temperature=0.0, model_kwargs={}, openai_api_key=SecretStr('**********'), openai_api_base='https://openai.vocareum.com/v1')
    | StrOutputParser()




```python
prompt | llm | parser
```




    PromptTemplate(input_variables=['topic'], input_types={}, partial_variables={}, template='Tell me a joke about {topic}')
    | ChatOpenAI(client=<openai.resources.chat.completions.Completions object at 0x7c9e3e6df940>, async_client=<openai.resources.chat.completions.AsyncCompletions object at 0x7c9e50293850>, root_client=<openai.OpenAI object at 0x7c9e3e6dcaf0>, root_async_client=<openai.AsyncOpenAI object at 0x7c9e3e6df970>, model_name='gpt-4o-mini', temperature=0.0, model_kwargs={}, openai_api_key=SecretStr('**********'), openai_api_base='https://openai.vocareum.com/v1')
    | StrOutputParser()




```python
chain = prompt | llm | parser
```


```python
chain.invoke(
    {"topic": "computer"}
)
```




    'Why did the computer go to therapy?\n\nBecause it had too many bytes from its past!'




```python
chain2 = prompt | llm | parser
```


```python
chain2.invoke({"topic": "weahter"})
```




    'Why did the weather report bring a ladder?\n\nBecause it wanted to reach new heights!'




```python

```
