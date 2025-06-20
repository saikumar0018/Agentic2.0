# Load the model 
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import os
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

def load_model(model_name = "deepseek-r1-distill-llama-70b"):
    """ Loading the model """
    try:
        llm=ChatGroq(model_name = model_name,  
             temperature=0)
    except Exception as error:
        print("Error while loading model --> ", error)
    return llm