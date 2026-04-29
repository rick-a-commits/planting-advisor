import os
from dotenv import load_dotenv
from openai import OpenAI
import concurrent.futures
from opencage.geocoder import OpenCageGeocode

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI()




def get_geo_location(country, place):
    api_key = os.getenv("OPENCAGE_API_KEY")
    geocoder = OpenCageGeocode(api_key)
    
    query = f"{place}, {country}"
    results = geocoder.geocode(query)
    
    if results and len(results) > 0:
        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        return f"{lat}° N, {lng}° E"
    else:
        return None


def planting_advice(country, place, crop):
    
    location = get_geo_location(country, place)


    planting_system_prompt = """
        You are an agronomist and meteorologist. Study weather patterns of the given location 
        for the past and next four weeks using historical and forecast data. Assess whether 
        the geography and soil suit the crop. Even if the weather and soil conditions are condusive, check the crop life cycle and determine if the planting window has been missed or not.
        Be concise but thorough."""

    user_prompt = f"""Is it a good time to plant {crop} at {location} ({place}, {country})?
        Start with: The weather conditions for {place} in {country} for the last four weeks...
        Followed by your recommendation and then add the reason for the recommendation.
        IF either of the  {crop}, {location}, ({place} or {country} are not recognizable, state that they are not recognisable and therefore you cannot give advice"""

    translation_system_prompt = """You are a skilled Asanti Twi translator. 
        Translate accurately while respecting cultural nuance. Maintain the same structure."""

   
    advice_response = openai.chat.completions.create(
        model='gpt-4o',  # 🔁 was gpt-4 — gpt-4o is faster and cheaper
        messages=[
            {'role': 'system', 'content': planting_system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
    )

    
    result = advice_response.choices[0].message.content

    
    translation_prompt = f"Translate the following to Asanti Twi. Maintain the same structure:\n\n{result}"

    translation_response = openai.chat.completions.create(
        model='gpt-4o-mini',  # 🔁 was gpt-4 — translation doesn't need the big model
        messages=[
            {'role': 'system', 'content': translation_system_prompt},
            {'role': 'user', 'content': translation_prompt}
        ]
    )
    result_twi = translation_response.choices[0].message.content

    return result, result_twi

###
