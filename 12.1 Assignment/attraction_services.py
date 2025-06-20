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





class AttractionService: 

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
    def format_attraction_details(cls, attraction_dict: dict) -> str:
        labels = {
            "places": "Top Attractions",
            "restaurants": "Top Restaurants",
            "activities": "Top Activities",
            "transport": "Modes of Transport"
        }

        output = []

        for key in ["places", "restaurants", "activities", "transport"]:
            if key not in attraction_dict:
                continue

            title = labels.get(key, key.title())
            raw_output = attraction_dict[key].strip()

            # Remove markdown/code block formatting like ```python ... ```
            raw_output = re.sub(r"```(?:python)?", "", raw_output).replace("```", "").strip()

            # Try to parse as list
            try:
                parsed_list = ast.literal_eval(raw_output)
                if not isinstance(parsed_list, list):
                    raise ValueError
            except Exception:
                # Fallback: Remove brackets and split by newline or comma
                cleaned = raw_output.strip("[]").replace('"', '').replace("'", "")
                # Split by newline or comma
                items = re.split(r",|\n", cleaned)
                parsed_list = [item.strip("-• ").strip() for item in items if item.strip()]

            # Format nicely
            formatted_items = '\n'.join(f"- {item}" for item in parsed_list)
            output.append(f"{title}:\n{formatted_items}\n")

        return "\n".join(output)


    @classmethod
    def get_attraction_service(cls, city_name = "Hyderabad"):

        # city_name = "Hyderabad"
        to_search = {
            "places": f"Top attraction places in {city_name}",
            "restaurants": f"Top restaurants in {city_name}",  # Fixed typo: "Restuarants" → "restaurants"
            "activities": f"Top activities to do in {city_name}",  # Added clarity
            "transport": f"Top modes of transportation in {city_name}"  # Grammar fix: "Mode" → "modes"
        }

        prompt_map = {
            "places": """
        From the following text, extract the names of tourist attractions or must-visit places.
        Return only the names in a Python array format. Do not include descriptions or any extra text.

        Text:
        {context}

        Example Output:
        ["Charminar", "Golconda Fort", "Hussain Sagar Lake"]
        """,

            "restaurants": """
        From the given text, extract only the names of the top restaurants.
        Do not include reviews, descriptions, or locations. Return the result as a Python array of strings.

        Text:
        {context}

        Example Output:
        ["Paradise", "Bawarchi", "Shah Ghouse"]
        """,

            "activities": """
        Read the text below and extract the top activities or experiences people can enjoy.
        Return only the activity names in a Python array format without extra explanation.

        Text:
        {context}

        Example Output:
        ["Boating at Hussain Sagar", "Street food tour", "Visit heritage museums"]
        """,

            "transport": """
        From the following text, extract the common modes of transportation used in the city.
        Return only the transport types in a Python array format. No explanations needed.

        Text:
        {context}

        Example Output:
        ["Metro", "Auto Rickshaw", "Bus", "Cab services"]
        """
        }


        results_dict = {}
        for each_query_key, each_query_value in to_search.items():
            results = tool.invoke(each_query_value)
            if len(results) > 0:
                content = results[0]['content']
                response = AttractionService.get_response(content, prompt_map[each_query_key])
                results_dict[each_query_key] = response
        
        return AttractionService.format_attraction_details(results_dict)

if __name__ == "__main__": 
    print(AttractionService.get_attraction_service())