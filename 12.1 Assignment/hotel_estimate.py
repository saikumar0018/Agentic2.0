from llm_model import load_model
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate


import os
tavily_api_key = os.getenv("TAVILY_API_KEY") 

llm = load_model("gemma2-9b-it")

tool = TavilySearchResults()
tool = TavilySearchResults(tavily_api_key = tavily_api_key)

class HotelService:

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
    def format_hotel_details(cls, hotel_details: dict) -> str:
        output = []
        for category, details in hotel_details.items():
            output.append(f"{category} Hotels:\n{details.strip()}\n")
        return "\n".join(output)

    @classmethod
    def get_hotel_details(cls, city_name = "Hyderabad"):
        
        hotel_categories = ["Budget", "Mid-range", "Premium", "Luxury"]

        hotel_details = {}
        for each_category in hotel_categories: 
            #print("-------------------")
            response = tool.invoke({"query": f"{each_category} hotels in {city_name} with costs"})
            content = '\n\n'.join( [each_r['content'] for each_r in response])
            #print(content)
            prompt = f"""
                From the following text, extract the names of {each_category} hotels with cost.
                Do not include descriptions or any extra text.

                Text:
                {content}"""

            response = HotelService.get_response(content, prompt)
            hotel_details[each_category] = response

        return HotelService.format_hotel_details(hotel_details)
if __name__ == "__main__":
    print(HotelService.get_hotel_details())