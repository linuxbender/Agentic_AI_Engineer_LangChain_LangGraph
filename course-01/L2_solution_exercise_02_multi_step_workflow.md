# Exercise - Multi step Workflow - SOLUTION

In this exercise, you’ll build a multi-step workflow using LCEL to solve a more complex task than simply generating a joke. 

**Challenge**

Create an AI Business Advisor that:

1. Accepts an industry as input.
2. Generates a business idea.
3. Analyzes the strengths and weaknesses.
4. Formats the results as a final report.


## 0. Import the necessary libs


```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from pydantic import BaseModel, Field
```

## 1. Instantiate Chat Model with your API Key

To be able to connect with OpenAI, you need to instantiate an ChatOpenAI client passing your OpenAI key.

You can pass the `api_key` argument directly.
```python
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.0,
    api_key="voc-",
)
```


```python
from dotenv import load_dotenv
load_dotenv()
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.0,
)
```

## 2. Your first Chain

In the end of each chain, you should parse the output and save the logs


```python
logs = []
```


```python
parser = StrOutputParser()
```


```python
parse_and_log_output_chain = RunnableParallel(
    output=parser, 
    log=RunnableLambda(lambda x: logs.append(x))
)
```

## 3. Idea Generation

Craft a prompt to generate a business idea for the given industry. 

Make sure {industry} placeholder is inside your template, so it can be filled when the chain is invoked.


```python
idea_prompt = PromptTemplate(
    template=(
        "You are a creative business advisor. "
        "Generate one innovative business idea in the industry: "
        "{industry}. "
        "Provide a brief description of the idea."
    )
)
```


```python
idea_chain = (
    idea_prompt 
    | llm 
    | parse_and_log_output_chain
)
```


```python
idea_result = idea_chain.invoke("agro")
```


```python
idea_result["output"]
```




    '**Business Idea: Smart Vertical Farming Pods**\n\n**Description:**\nSmart Vertical Farming Pods are modular, self-sustaining farming units designed for urban environments and small spaces. Each pod utilizes hydroponic and aeroponic systems to grow a variety of crops, from leafy greens to herbs, without the need for soil. Equipped with IoT sensors, these pods monitor and optimize conditions such as light, temperature, humidity, and nutrient levels in real-time, ensuring maximum yield with minimal resource use.\n\nThe pods can be installed in homes, schools, or community centers, promoting local food production and reducing the carbon footprint associated with transporting produce. Users can connect to a mobile app that provides guidance on crop selection, growth tracking, and even recipes for using their fresh produce. Additionally, the business can offer subscription services for seed kits, nutrients, and maintenance support, creating a recurring revenue model.\n\nThis innovative approach not only addresses food security in urban areas but also fosters a sense of community and sustainability, encouraging individuals to engage with agriculture in a modern, tech-savvy way.'




```python
logs
```




    [AIMessage(content='**Business Idea: Smart Vertical Farming Pods**\n\n**Description:**\nSmart Vertical Farming Pods are modular, self-sustaining farming units designed for urban environments and small spaces. Each pod utilizes hydroponic and aeroponic systems to grow a variety of crops, from leafy greens to herbs, without the need for soil. Equipped with IoT sensors, these pods monitor and optimize conditions such as light, temperature, humidity, and nutrient levels in real-time, ensuring maximum yield with minimal resource use.\n\nThe pods can be installed in homes, schools, or community centers, promoting local food production and reducing the carbon footprint associated with transporting produce. Users can connect to a mobile app that provides guidance on crop selection, growth tracking, and even recipes for using their fresh produce. Additionally, the business can offer subscription services for seed kits, nutrients, and maintenance support, creating a recurring revenue model.\n\nThis innovative approach not only addresses food security in urban areas but also fosters a sense of community and sustainability, encouraging individuals to engage with agriculture in a modern, tech-savvy way.', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 214, 'prompt_tokens': 33, 'total_tokens': 247, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_13eed4fce1', 'finish_reason': 'stop', 'logprobs': None}, id='run-997ebaa6-0ea5-498a-a505-f33487a3358a-0', usage_metadata={'input_tokens': 33, 'output_tokens': 214, 'total_tokens': 247, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})]



## 4. Idea Analysis

Craft a prompt to analyze the generated idea's strengths and weaknesses


```python
analysis_prompt = PromptTemplate(
    template=(
        "Analyze the following business idea: "
        "Idea: {idea} "
        "Identify 3 key strengths and 3 potential weaknesses of the idea."
    )
)
```


```python
analysis_chain = (
    analysis_prompt 
    | llm 
    | parse_and_log_output_chain
)
```


```python
analysis_result = analysis_chain.invoke(idea_result["output"])
```


```python
analysis_result["output"]
```




    '### Key Strengths\n\n1. **Sustainability and Environmental Impact:**\n   - The Smart Vertical Farming Pods promote sustainable agriculture by reducing the need for arable land and minimizing water usage through hydroponic and aeroponic systems. This aligns with growing consumer demand for eco-friendly products and practices, potentially attracting environmentally conscious customers.\n\n2. **Urban Food Security:**\n   - By enabling local food production in urban settings, these pods can help address food security issues, particularly in areas with limited access to fresh produce. This can be particularly appealing in densely populated cities where traditional farming is not feasible.\n\n3. **Technological Integration and User Engagement:**\n   - The incorporation of IoT sensors and a mobile app enhances user experience by providing real-time data and personalized guidance. This tech-savvy approach can attract a younger demographic interested in smart home technologies and sustainable living, fostering a community of engaged users who can share their experiences and tips.\n\n### Potential Weaknesses\n\n1. **High Initial Investment:**\n   - The cost of developing and manufacturing the Smart Vertical Farming Pods, along with the technology integration (IoT sensors, mobile app development), may be significant. This could limit market entry, especially for price-sensitive consumers or those in lower-income urban areas.\n\n2. **Maintenance and Technical Challenges:**\n   - While the pods are designed to be self-sustaining, users may still face challenges related to maintenance, troubleshooting, and technical issues. If the technology fails or if users do not have the necessary knowledge to operate the system effectively, it could lead to dissatisfaction and reduced adoption rates.\n\n3. **Market Competition and Differentiation:**\n   - The vertical farming and home gardening market is becoming increasingly competitive, with various players offering similar solutions. The business will need to clearly differentiate its product and value proposition to stand out, which may require ongoing innovation and marketing efforts to maintain a competitive edge.'




```python
logs
```




    [AIMessage(content='**Business Idea: Smart Vertical Farming Pods**\n\n**Description:**\nSmart Vertical Farming Pods are modular, self-sustaining farming units designed for urban environments and small spaces. Each pod utilizes hydroponic and aeroponic systems to grow a variety of crops, from leafy greens to herbs, without the need for soil. Equipped with IoT sensors, these pods monitor and optimize conditions such as light, temperature, humidity, and nutrient levels in real-time, ensuring maximum yield with minimal resource use.\n\nThe pods can be installed in homes, schools, or community centers, promoting local food production and reducing the carbon footprint associated with transporting produce. Users can connect to a mobile app that provides guidance on crop selection, growth tracking, and even recipes for using their fresh produce. Additionally, the business can offer subscription services for seed kits, nutrients, and maintenance support, creating a recurring revenue model.\n\nThis innovative approach not only addresses food security in urban areas but also fosters a sense of community and sustainability, encouraging individuals to engage with agriculture in a modern, tech-savvy way.', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 214, 'prompt_tokens': 33, 'total_tokens': 247, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_13eed4fce1', 'finish_reason': 'stop', 'logprobs': None}, id='run-997ebaa6-0ea5-498a-a505-f33487a3358a-0', usage_metadata={'input_tokens': 33, 'output_tokens': 214, 'total_tokens': 247, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}),
     AIMessage(content='### Key Strengths\n\n1. **Sustainability and Environmental Impact:**\n   - The Smart Vertical Farming Pods promote sustainable agriculture by reducing the need for arable land and minimizing water usage through hydroponic and aeroponic systems. This aligns with growing consumer demand for eco-friendly products and practices, potentially attracting environmentally conscious customers.\n\n2. **Urban Food Security:**\n   - By enabling local food production in urban settings, these pods can help address food security issues, particularly in areas with limited access to fresh produce. This can be particularly appealing in densely populated cities where traditional farming is not feasible.\n\n3. **Technological Integration and User Engagement:**\n   - The incorporation of IoT sensors and a mobile app enhances user experience by providing real-time data and personalized guidance. This tech-savvy approach can attract a younger demographic interested in smart home technologies and sustainable living, fostering a community of engaged users who can share their experiences and tips.\n\n### Potential Weaknesses\n\n1. **High Initial Investment:**\n   - The cost of developing and manufacturing the Smart Vertical Farming Pods, along with the technology integration (IoT sensors, mobile app development), may be significant. This could limit market entry, especially for price-sensitive consumers or those in lower-income urban areas.\n\n2. **Maintenance and Technical Challenges:**\n   - While the pods are designed to be self-sustaining, users may still face challenges related to maintenance, troubleshooting, and technical issues. If the technology fails or if users do not have the necessary knowledge to operate the system effectively, it could lead to dissatisfaction and reduced adoption rates.\n\n3. **Market Competition and Differentiation:**\n   - The vertical farming and home gardening market is becoming increasingly competitive, with various players offering similar solutions. The business will need to clearly differentiate its product and value proposition to stand out, which may require ongoing innovation and marketing efforts to maintain a competitive edge.', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 384, 'prompt_tokens': 242, 'total_tokens': 626, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_13eed4fce1', 'finish_reason': 'stop', 'logprobs': None}, id='run-70782599-70aa-472a-ba65-78ff7c837555-0', usage_metadata={'input_tokens': 242, 'output_tokens': 384, 'total_tokens': 626, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})]



## 5. Report Generation

Craft a prompt to structure the information into a business report.


```python
report_prompt = PromptTemplate(
    template=(
        "Here is a business analysis: "
        "Strengths & Weaknesses: {output} "
        "Generate a structured business report." 
    )
)
```


```python
class AnalysisReport(BaseModel):
    """Strengths and Weaknesses about a business idea"""
    strengths: list = Field(default=[], description="Idea's strength list")
    weaknesses: list = Field(default=[], description="Idea's weaknesse list")
```


```python
report_chain = (
    report_prompt | llm.with_structured_output(schema=AnalysisReport, method="function_calling")
)
```


```python
report_result = report_chain.invoke(analysis_result["output"])
```


```python
report_result
```




    AnalysisReport(strengths=['Sustainability and Environmental Impact: The Smart Vertical Farming Pods promote sustainable agriculture by reducing the need for arable land and minimizing water usage through hydroponic and aeroponic systems, aligning with consumer demand for eco-friendly products.', 'Urban Food Security: These pods enable local food production in urban settings, addressing food security issues in areas with limited access to fresh produce, appealing to densely populated cities.', 'Technological Integration and User Engagement: Incorporating IoT sensors and a mobile app enhances user experience with real-time data and personalized guidance, attracting a younger demographic interested in smart home technologies and sustainable living.'], weaknesses=['High Initial Investment: The cost of developing and manufacturing the Smart Vertical Farming Pods and technology integration may be significant, limiting market entry for price-sensitive consumers.', 'Maintenance and Technical Challenges: Users may face challenges related to maintenance and technical issues, leading to dissatisfaction and reduced adoption rates if the technology fails or if users lack the necessary knowledge.', 'Market Competition and Differentiation: The vertical farming and home gardening market is competitive, requiring clear differentiation of the product and ongoing innovation and marketing efforts to maintain a competitive edge.'])



## 6. End to End Chain


```python
e2e_chain = ( 
    RunnablePassthrough() 
    | idea_chain
    | RunnableParallel(idea=RunnablePassthrough())
    | analysis_chain
    | report_chain
)
```


```python
e2e_chain.get_graph().print_ascii()
```

                +------------------+         
                | PassthroughInput |         
                +------------------+         
                          *                  
                          *                  
                          *                  
                  +-------------+            
                  | Passthrough |            
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
           +---------------------------+     
           | Parallel<output,log>Input |     
           +---------------------------+     
                   ***         ***           
                  *               *          
                **                 **        
    +-----------------+          +--------+  
    | StrOutputParser |          | Lambda |  
    +-----------------+          +--------+  
                   ***         ***           
                      *       *              
                       **   **               
           +----------------------------+    
           | Parallel<output,log>Output |    
           +----------------------------+    
                          *                  
                          *                  
                          *                  
                  +-------------+            
                  | Passthrough |            
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
           +---------------------------+     
           | Parallel<output,log>Input |     
           +---------------------------+     
                   ***         ***           
                  *               *          
                **                 **        
    +-----------------+          +--------+  
    | StrOutputParser |          | Lambda |  
    +-----------------+          +--------+  
                   ***         ***           
                      *       *              
                       **   **               
           +----------------------------+    
           | Parallel<output,log>Output |    
           +----------------------------+    
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
              +---------------------+        
              | PydanticToolsParser |        
              +---------------------+        
                          *                  
                          *                  
                          *                  
           +---------------------------+     
           | PydanticToolsParserOutput |     
           +---------------------------+     



```python
# Change the industry if you want
e2e_result = e2e_chain.invoke("agro")
```


```python
e2e_result
```




    AnalysisReport(strengths=['Sustainability and Local Food Production', 'Technological Integration', 'Recurring Revenue Model'], weaknesses=['Initial Cost and Accessibility', 'Technical Complexity', 'Market Competition and Differentiation'])




```python
e2e_result.strengths
```




    ['Sustainability and Local Food Production',
     'Technological Integration',
     'Recurring Revenue Model']




```python
e2e_result.weaknesses
```




    ['Initial Cost and Accessibility',
     'Technical Complexity',
     'Market Competition and Differentiation']




```python
logs
```




    [AIMessage(content='**Business Idea: Smart Vertical Farming Pods**\n\n**Description:**\nSmart Vertical Farming Pods are modular, self-sustaining farming units designed for urban environments and small spaces. Each pod utilizes hydroponic and aeroponic systems to grow a variety of crops, from leafy greens to herbs, without the need for soil. Equipped with IoT sensors, these pods monitor and optimize conditions such as light, temperature, humidity, and nutrient levels in real-time, ensuring maximum yield with minimal resource use.\n\nThe pods can be installed in homes, schools, or community centers, promoting local food production and reducing the carbon footprint associated with transporting produce. Users can connect to a mobile app that provides guidance on crop selection, growth tracking, and even recipes for using their fresh produce. Additionally, the business can offer subscription services for seed kits, nutrients, and maintenance support, creating a recurring revenue model.\n\nThis innovative approach not only addresses food security in urban areas but also fosters a sense of community and sustainability, encouraging individuals to engage with agriculture in a modern, tech-savvy way.', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 214, 'prompt_tokens': 33, 'total_tokens': 247, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_13eed4fce1', 'finish_reason': 'stop', 'logprobs': None}, id='run-997ebaa6-0ea5-498a-a505-f33487a3358a-0', usage_metadata={'input_tokens': 33, 'output_tokens': 214, 'total_tokens': 247, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}),
     AIMessage(content='### Key Strengths\n\n1. **Sustainability and Environmental Impact:**\n   - The Smart Vertical Farming Pods promote sustainable agriculture by reducing the need for arable land and minimizing water usage through hydroponic and aeroponic systems. This aligns with growing consumer demand for eco-friendly products and practices, potentially attracting environmentally conscious customers.\n\n2. **Urban Food Security:**\n   - By enabling local food production in urban settings, these pods can help address food security issues, particularly in areas with limited access to fresh produce. This can be particularly appealing in densely populated cities where traditional farming is not feasible.\n\n3. **Technological Integration and User Engagement:**\n   - The incorporation of IoT sensors and a mobile app enhances user experience by providing real-time data and personalized guidance. This tech-savvy approach can attract a younger demographic interested in smart home technologies and sustainable living, fostering a community of engaged users who can share their experiences and tips.\n\n### Potential Weaknesses\n\n1. **High Initial Investment:**\n   - The cost of developing and manufacturing the Smart Vertical Farming Pods, along with the technology integration (IoT sensors, mobile app development), may be significant. This could limit market entry, especially for price-sensitive consumers or those in lower-income urban areas.\n\n2. **Maintenance and Technical Challenges:**\n   - While the pods are designed to be self-sustaining, users may still face challenges related to maintenance, troubleshooting, and technical issues. If the technology fails or if users do not have the necessary knowledge to operate the system effectively, it could lead to dissatisfaction and reduced adoption rates.\n\n3. **Market Competition and Differentiation:**\n   - The vertical farming and home gardening market is becoming increasingly competitive, with various players offering similar solutions. The business will need to clearly differentiate its product and value proposition to stand out, which may require ongoing innovation and marketing efforts to maintain a competitive edge.', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 384, 'prompt_tokens': 242, 'total_tokens': 626, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_13eed4fce1', 'finish_reason': 'stop', 'logprobs': None}, id='run-70782599-70aa-472a-ba65-78ff7c837555-0', usage_metadata={'input_tokens': 242, 'output_tokens': 384, 'total_tokens': 626, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}),
     AIMessage(content='**Business Idea: Smart Vertical Farming Pods**\n\n**Description:**\nSmart Vertical Farming Pods are self-contained, modular farming units designed for urban environments and small spaces. Each pod utilizes advanced hydroponic and aeroponic systems to grow a variety of crops, from leafy greens to herbs, without the need for soil. Equipped with IoT sensors, these pods monitor and optimize conditions such as light, temperature, humidity, and nutrient levels in real-time, ensuring maximum yield with minimal resource use.\n\nThe pods can be installed in homes, schools, or community centers, promoting local food production and sustainability. Users can connect to a mobile app that provides guidance on crop selection, growth tracking, and even recipes for the produce harvested. Additionally, the business can offer a subscription service for seed pods and nutrient solutions, creating a recurring revenue stream.\n\nBy combining technology with urban agriculture, Smart Vertical Farming Pods not only address food security in densely populated areas but also foster a culture of sustainability and healthy eating.', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 198, 'prompt_tokens': 33, 'total_tokens': 231, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_13eed4fce1', 'finish_reason': 'stop', 'logprobs': None}, id='run-d3e8ac93-ee71-4cb7-9505-db7a2224ce37-0', usage_metadata={'input_tokens': 33, 'output_tokens': 198, 'total_tokens': 231, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}),
     AIMessage(content='### Key Strengths\n\n1. **Sustainability and Local Food Production**: The Smart Vertical Farming Pods promote sustainable agriculture by enabling local food production in urban areas. This reduces the carbon footprint associated with transporting food and encourages consumers to grow their own produce, fostering a culture of sustainability.\n\n2. **Technological Integration**: The use of IoT sensors for real-time monitoring and optimization of growing conditions enhances the efficiency and yield of the crops. This technological aspect can attract tech-savvy consumers and provide a competitive edge in the market.\n\n3. **Recurring Revenue Model**: The subscription service for seed pods and nutrient solutions creates a steady revenue stream. This model not only ensures customer retention but also provides ongoing engagement with users, as they will need to regularly purchase supplies to maintain their pods.\n\n### Potential Weaknesses\n\n1. **Initial Cost and Accessibility**: The upfront cost of purchasing a Smart Vertical Farming Pod may be a barrier for some consumers, particularly in lower-income urban areas. If the price point is too high, it could limit the target market and reduce widespread adoption.\n\n2. **Technical Complexity**: While the integration of technology is a strength, it can also be a weakness. Users who are not tech-savvy may find it challenging to operate the pods or troubleshoot issues. This could lead to frustration and a potential decrease in customer satisfaction.\n\n3. **Market Competition and Differentiation**: The vertical farming and hydroponics market is becoming increasingly competitive, with various players offering similar solutions. The business will need to clearly differentiate its product and value proposition to stand out in a crowded market, which may require significant marketing efforts and innovation.', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 334, 'prompt_tokens': 242, 'total_tokens': 576, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_13eed4fce1', 'finish_reason': 'stop', 'logprobs': None}, id='run-6c09c91a-88d9-483d-b5dc-749b1dad113b-0', usage_metadata={'input_tokens': 242, 'output_tokens': 334, 'total_tokens': 576, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})]



## 7. Experiment

Now that you understood how it works, experiment with new things.
- Improve memory
- Explore the Runnables
- Add More Complexity
