# [Bug] Bedrock tool call arguments silently dropped — tool invoked with empty input

- Source: https://github.com/crewAIInc/crewAI/issues/5275
- Author: krishnamohanathota
- Created: 2026-04-05T00:01:04Z

## Original issue description

### Description

When using CrewAI with an AWS Bedrock LLM (e.g. Amazon Nova Pro via bedrock/us.amazon.nova-pro-v1:0), tool arguments are silently discarded. The LLM correctly calls the tool with the right arguments, but the tool receives an empty dict {},
  causing either a TypeError (missing required positional argument) or a Pydantic ValidationError (field required).                                                                                                                                 
   
  Affected versions: Confirmed in 1.9.3 and 1.13.0.        

### Steps to Reproduce

1. Define a BaseTool with a required parameter:
  from crewai.tools import BaseTool                                                                                                                                                                                                                 
  from pydantic import BaseModel, Field
  from typing import Type                                                                                                                                                                                                                           
                                                            
  class CityInput(BaseModel):                                                                                                                                                                                                                       
      city: str = Field(..., description="City name")       
                                                     
  class TravelTool(BaseTool):
      name: str = "get_travel_details"                                                                                                                                                                                                              
      description: str = "Get travel details for a city."
      args_schema: Type[BaseModel] = CityInput                                                                                                                                                                                                      
                                                            
      def _run(self, city: str) -> str:                                                                                                                                                                                                             
          return f"Details for {city}" 
                                                                                                                                                                                                                                                    
  2. Assign this tool to a CrewAI agent backed by a Bedrock LLM:
  llm = LLM(model="bedrock/us.amazon.nova-pro-v1:0", temperature=0)                                                                                                                                                                                 
  agent = Agent(tools=[TravelTool()], llm=llm, ...)                
                                                                                                                                                                                                                                                    
  3. Run the crew. The Bedrock LLM correctly calls get_travel_details with {"city": "Paris"}, but the tool receives {}.                                                                                                                             
                                                                                                                                                                                                                                                    
  Error in 1.9.3:                                                                                                                                                                                                                                   
  TravelDetailsTool._run() missing 1 required positional argument: 'city'                                                                                                                                                                           
                                                            
  Error in 1.13.0:                                                                                                                                                                                                                                  
  Tool 'get_travel_details' arguments validation failed: 1 validation error for CityInput
  city                                                                                                                                                                                                                                              
    Field required [type=missing, input_value={}, input_type=dict] 

Root Cause                                                
                                                                                                                                                                                                                                                    
  File: crewai/agents/crew_agent_executor.py                
                                                                                                                                                                                                                                                    
  In _handle_native_tool_calls / _extract_tool_call_info (line varies by version), the code that extracts tool arguments handles multiple LLM response formats:                                                                                     
                                                                                                                                                                                                                                                    
  func_info = tool_call.get("function", {})                                                                                                                                                                                                         
  func_args = func_info.get("arguments", "{}") or tool_call.get("input", {})
                                                                                                                                                                                                                                                    
  Bedrock's Converse API returns tool calls in this format:                                                                                                                                                                                         
  {"name": "get_travel_details", "toolUseId": "abc123", "input": {"city": "Paris"}}                                                                                                                                                                 
                                                                                                                                                                                                                                                    
  There is no "function" wrapper, so func_info = {}.                                                                                                                                                                                                
                                                                                                                                                                                                                                                    
  func_info.get("arguments", "{}") returns the default string "{}", which is truthy.                                                                                                                                                                
                                                                                                                                                                                                                                                    
  The or short-circuits — tool_call.get("input", {"city": "Paris"}) is never evaluated.                                                                                                                                                             
                                                            
  func_args becomes "{}", and after json.loads("{}"), args_dict = {}. The actual Bedrock arguments are completely lost.   

### Expected behavior

The tool should be invoked with the arguments from tool_call["input"] when processing a Bedrock-format tool call response.

### Screenshots/Code snippets

Change the default from "{}" to None:
                                                                                                                                                                                                                                                    
  # Before
  func_args = func_info.get("arguments", "{}") or tool_call.get("input", {})                                                                                                                                                                        
                                                            
  # After
  func_args = func_info.get("arguments") or tool_call.get("input", {})
                                                                                                                                                                                                                                                    
  With None as default, func_info.get("arguments") returns None (falsy) when no "function" wrapper is present, so the or correctly falls through to tool_call.get("input", {...}).                                                                  
                                                                                                                                                                                         

### Operating System

Ubuntu 20.04

### Python Version

3.12

### crewAI Version

1.13.0

### crewAI Tools Version

1.13.0

### Virtual Environment

Venv

### Evidence

Iteration: 1                                                                                                                                                                                                                                     
│                                                                                                                                                                                                                                                   
│  Attempt: 0                                                                                                                                                                                                                                       
│                                                                                                                                                                                                                                                   
│  Error: Tool 'get_travel_details' arguments validation failed: 1 validation error for TravelDetailsInput                                                                                                                                          
│                                                                                                                                                                                                                                                   
│  city                                                                                                                                                                                                                                             
│                                                                                                                                                                                                                                                   
│    Field required [type=missing, input_value={}, input_type=dict]                                                                                                                                                                                 
│                                                                                                                                                                                                                                                   
│      For further information visit https://errors.pydantic.dev/2.11/v/missing                                                                                                                                                                     
│                                                                                                                                                                                                                                                   
│  Expected arguments: {"city": {"description": "Name of the city to retrieve travel details for.", "title": "City", "type": "string"}}                                                                                                             
│                                                                                                                                                                                                                                                   
│  Required: ["city"]                                                                                       

### Possible Solution


   Change the default from "{}" to None:
                                                                                                                                                                                                                                                    
  # Before
  func_args = func_info.get("arguments", "{}") or tool_call.get("input", {})                                                                                                                                                                        
                                                            
  # After
  func_args = func_info.get("arguments") or tool_call.get("input", {})
                                                                                                                                                                                                                                                    
  With None as default, func_info.get("arguments") returns None (falsy) when no "function" wrapper is present, so the or correctly falls through to tool_call.get("input", {...}).    

### Additional context

NA
