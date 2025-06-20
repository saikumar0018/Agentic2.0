from langchain.tools import tool

from weather import WeatherForecast
from attraction_services import AttractionService
from hotel_estimate import HotelService

@tool
def weather_forecast(city: str) -> str:
    """
    Weather forecast of a city for current day and for next 3 days. 

    Args: 
        city (str): Name of the city. 

    Returns: 
        str: Weather forecast of a city for current day and for next 3 days
    """

    weather_respone = WeatherForecast.get_weather(city)

    return weather_respone

@tool
def attraction_services(city: str) -> str:
    """
    Gives Top attractions, restaurants, activities, modes of transportation for a city. 

    Args: 
        city (str): Name of the city. 

    Returns: 
        str: Top attractions, restaurants, activities, modes of transportation for a city

    """
    attraction_response = AttractionService.get_attraction_service(city)
    return attraction_response

@tool
def hotel_details(city: str) -> str:
    """
    Gives Top hotels considering all categories (Budget, Mid-range, Premium, Luxury) for a city. 

    Args: 
        city (str): Name of the city. 
    
    Returns: 
        str: Top hotels considering all categories (Budget, Mid-range, Premium, Luxury) for a city.
    """
    hotel_response = HotelService.get_hotel_details(city)
    return hotel_response

@tool
def itinerary_planner(attractions_activities: str, weather: str, hotel: str) -> str:
    """
    Creates a full itinerary plan for complete trip. 
    Also provides day wise plan. 

    Args: 
        attractions_activities (str): Contains attractions, restauants, activities, modes of transportation. 
        weather (str): Information of current and next days forecast. 
        hotel (str): Details of hotel for accommodation. 
    
    Returns:
    str: A complete itinerary with accommodation, day-wise plan, and activity suggestions.
    """
    pass


@tool
def currency_conversion(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Converts amount from one currency to another using exchange rate.

    Args:
        amount (float): Amount to convert.
        from_currency (str): Source currency code (e.g., "USD").
        to_currency (str): Target currency code (e.g., "INR").

    Returns:
        str: Converted amount with exchange rate.
    """
    pass



@tool
def multiply(a: int, b: int) -> int:
    """
    Multiply two integers.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The product of a and b.
    """
    return a * b

@tool
def add(a: int, b: int) -> int:
    """
    Add two integers.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The sum of a and b.
    """
    return a + b