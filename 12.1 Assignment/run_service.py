import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition 

from tools import (weather_forecast, attraction_services, hotel_details, multiply, add, 
         itinerary_planner, currency_conversion)
from llm_model import load_model

from dotenv import load_dotenv
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

llm = load_model("gemma2-9b-it")


def get_response(content, prompt):
    prompt = PromptTemplate(
        template=prompt, 
        input_variables=["context"]
    )

    chain = prompt | llm
    response = chain.invoke({"context": content}).content

    return response

def get_travel_plan(user_input):
    # Reasoning model
    llm=ChatGroq(model_name="deepseek-r1-distill-llama-70b", 
                temperature=0)




    def Supervisor(state: MessagesState):
        user_question = state["messages"]
        input_question = [SYSTEM_PROMPT] + user_question
        response = llm_with_tools.invoke(input_question)
        return {"messages": [response]}

    tools = [weather_forecast, attraction_services, hotel_details, multiply, add, 
            itinerary_planner, currency_conversion]


    llm_with_tools = llm.bind_tools(tools)

    AITravelAssistant = StateGraph(MessagesState)

    SYSTEM_PROMPT = "You are a helpful assistant tasked with giving details of a trip planning. "

    AITravelAssistant.add_node("Supervisor", Supervisor)
    AITravelAssistant.add_node("tools", ToolNode(tools))


    AITravelAssistant.add_edge(START, "Supervisor")
    AITravelAssistant.add_conditional_edges("Supervisor", tools_condition)

    AITravelAssistant.add_edge("tools", "Supervisor")

    travel_assistant = AITravelAssistant.compile()



    response = travel_assistant.invoke({"messages": user_input})
    complete_content = ""
    for each_ in response["messages"]:
        print(each_.content)
        complete_content += each_.content    

    for m in response["messages"]:
        m.pretty_print()

        c_prompt = """
Summarize the complete travel plan. 

Text: {context}
"""
    trip_summary = get_response(complete_content, c_prompt)
    return trip_summary

if __name__ == "__main__": 
    city = "Bangalore"
    trip_duration = 7
    native_currency = "INR"
    target_currency = "USD"

    user_input = f""" 
    I am planning a {trip_duration}-day trip to {city}.  
    Please help me with the following:

    1. What's the current weather and the forecast for the next few days in {city}?
    2. Suggest top attractions, restaurants, activities, and local transport in {city}.
    3. Find me a budget-friendly hotel for {trip_duration} nights and give full details with estimated cost in {native_currency}.
    4. Plan a complete day-wise itinerary using all the above information.
    5. Convert the total hotel stay cost from {native_currency} to {target_currency}.

    Thanks!
    """
    s_response = get_travel_plan(user_input)
    print("====================================================")
    print("Summary of Trip plan")
    print("====================================================")
    print(s_response)

