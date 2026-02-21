```python
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers.datetime import DatetimeOutputParser
from langchain.output_parsers.boolean import BooleanOutputParser
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain.output_parsers import OutputFixingParser
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

## Output Parsers

**String Parser**


```python
llm.invoke("hello")
```




    AIMessage(content='Hello! How can I assist you today?', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 9, 'prompt_tokens': 8, 'total_tokens': 17, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_373a14eb6f', 'finish_reason': 'stop', 'logprobs': None}, id='run-8687c8b4-fcf0-4c72-a74a-27c50b472d2f-0', usage_metadata={'input_tokens': 8, 'output_tokens': 9, 'total_tokens': 17, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})




```python
llm.invoke("hello").content
```




    'Hello! How can I assist you today?'




```python
parser = StrOutputParser()
```


```python
parser.invoke(
    llm.invoke("hello")
)
```




    'Hello! How can I assist you today?'



### Other Parsers

**Datetime**


```python
llm.invoke(
    "Output a random datetime in %Y-%m-%dT%H:%M:%S.%fZ. "
    "Don't say anything else"
)
```




    AIMessage(content='2023-10-05T14:23:45.123456Z', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 16, 'prompt_tokens': 33, 'total_tokens': 49, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_373a14eb6f', 'finish_reason': 'stop', 'logprobs': None}, id='run-cf74c745-b4fd-4c10-82aa-0bb9b27ed9c8-0', usage_metadata={'input_tokens': 33, 'output_tokens': 16, 'total_tokens': 49, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})




```python
parser = DatetimeOutputParser()
```


```python
parser.invoke(
    llm.invoke(
        "Output a random datetime in %Y-%m-%dT%H:%M:%S.%fZ. "
        "Don't say anything else"
    )
)
```




    datetime.datetime(2023, 10, 5, 14, 23, 45, 123456)



**Boolean**


```python
llm.invoke(
    "Are you an AI? YES or NO only"
)
```




    AIMessage(content='YES', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 2, 'prompt_tokens': 16, 'total_tokens': 18, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_06737a9306', 'finish_reason': 'stop', 'logprobs': None}, id='run-56e74bdc-c848-46e8-a9a4-caa9f8b64b72-0', usage_metadata={'input_tokens': 16, 'output_tokens': 2, 'total_tokens': 18, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})




```python
parser = BooleanOutputParser()
```


```python
parser.invoke(
    input=llm.invoke(
        "Are you an AI? YES or NO only"
    )
)
```




    True




```python
parser.invoke(
    input=llm.invoke(
        "Are you Human? YES or NO only"
    )
)
```




    False



## Structured

**Dict Schema**


```python
from typing_extensions import Annotated, TypedDict

class UserInfo(TypedDict):
    """User's info."""
    name: Annotated[str, "", "User's name. Defaults to ''"]
    country: Annotated[str, "", "Where the user lives. Defaults to ''"]

```


```python
llm_with_structure = llm.with_structured_output(UserInfo)
```


```python
llm_with_structure.invoke(
    "My name is Henrique, and I am from Brazil"
)
```




    {'name': 'Henrique', 'country': 'Brazil'}




```python
llm_with_structure.invoke(
    "The sky is blue"
)
```




    {'name': '', 'country': ''}




```python
llm_with_structure.invoke(
    "Hello, my name is the same as the capital of the U.S.  "
    "But I'm from a country where we usually associate with kangaroos"
)
```




    {'name': 'Washington', 'country': 'Australia'}



**Pydantic**


```python
from pydantic import BaseModel, Field

class PydanticUserInfo(BaseModel):
    """User's info."""
    name: Annotated[str, Field(description="User's name. Defaults to ''", default=None)]
    country: Annotated[str, Field(description="Where the user lives. Defaults to ''", default=None, )]
```


```python
llm_with_structure = llm.with_structured_output(PydanticUserInfo)
```


```python
structured_output = llm_with_structure.invoke("The sky is blue")
```


```python
structured_output
```




    PydanticUserInfo(name='', country='')




```python
print(structured_output.name)
```

    



```python
print(structured_output.country)
```

    



```python
structured_output = llm_with_structure.invoke(
    "Hello, my name is the same as the capital of the U.S.  "
    "But I'm from a country where we usually associate with kangaroos"
)
```


```python
structured_output
```




    PydanticUserInfo(name='Washington', country='Australia')



## Dealing with Errors


```python
class Performer(BaseModel):
    """Filmography info about an actor/actress"""
    name: Annotated[str, Field(description="name of an actor/actress")]
    film_names: Annotated[List[str], Field(description="list of names of films they starred in")]
```


```python
llm_with_structure = llm.with_structured_output(Performer)
```


```python
response = llm_with_structure.invoke(
    "Generate the filmography for Scarlett Johansson. Top 5 only"
)
response
```




    Performer(name='Scarlett Johansson', film_names=['Lost in Translation (2003)', 'The Avengers (2012)', 'Her (2013)', 'Lucy (2014)', 'Marriage Story (2019)'])



**Fixing Parser**


```python
response.json()
```

    /var/folders/9j/22z22w295s397xgsptrk9ln40000gn/T/ipykernel_37751/690762135.py:1: PydanticDeprecatedSince20: The `json` method is deprecated; use `model_dump_json` instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.10/migration/
      response.json()





    '{"name":"Scarlett Johansson","film_names":["Lost in Translation (2003)","The Avengers (2012)","Her (2013)","Lucy (2014)","Marriage Story (2019)"]}'




```python
parser = PydanticOutputParser(pydantic_object=Performer)
```


```python
parser.parse(response.json())
```

    /var/folders/9j/22z22w295s397xgsptrk9ln40000gn/T/ipykernel_37751/2130552313.py:1: PydanticDeprecatedSince20: The `json` method is deprecated; use `model_dump_json` instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.10/migration/
      parser.parse(response.json())





    Performer(name='Scarlett Johansson', film_names=['Lost in Translation (2003)', 'The Avengers (2012)', 'Her (2013)', 'Lucy (2014)', 'Marriage Story (2019)'])




```python
misformatted_result = "{'name': 'Scarlett Johansson', 'film_names': ['The Avengers']}"
```


```python
try:
    parser.parse(misformatted_result)
except OutputParserException as e:
    print(e)
```

    Invalid json output: {'name': 'Scarlett Johansson', 'film_names': ['The Avengers']}
    For troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE 



```python
new_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
```


```python
new_parser.parse(misformatted_result)
```




    Performer(name='Scarlett Johansson', film_names=['The Avengers', 'Lost in Translation', 'Marriage Story', 'Black Widow'])




```python

```
