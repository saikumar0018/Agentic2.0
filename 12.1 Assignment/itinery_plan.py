from llm_model import load_model
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
import re
import ast
import os
tavily_api_key = os.getenv("TAVILY_API_KEY") 

llm = load_model("gemma2-9b-it")

tool = TavilySearchResults()
tool = TavilySearchResults(tavily_api_key = tavily_api_key)


class ItineraryTool:

    @classmethod
    def get_response(cls, content, prompt):
        prompt = PromptTemplate(
            template=prompt, 
            input_variables=["context"]
        )

        chain = prompt | llm
        response = chain.invoke({"context": content}).content

        return response
    
    @classmethod
    def generate_full_itinerary(cls, city: str, daywise_plan: str, travel_type: str = "family"):
        prompt_template = """
You're an expert travel planner. Based on the following city and day-wise plan, create a full detailed itinerary.

Include:
- Time estimates
- Start/end times for each item
- Suggestions for breakfast/lunch/dinner
- Transport tips between places (optional)
- Keep it practical and concise

City: {city}

Day-wise Plan:
{daywise_plan}

Full Itinerary:
"""

        return cls.get_response(prompt_template, {
            "city": city,
            "daywise_plan": daywise_plan,
            "travel_type": travel_type
        })


if __name__ == "__main__":
    print(ItineraryTool.generate_full_itinerary)