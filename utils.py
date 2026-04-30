import os
from dotenv import load_dotenv
from openai import OpenAI
import concurrent.futures
from opencage.geocoder import OpenCageGeocode
from datetime import date

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI()




def get_geo_location(country, place):
    api_key = os.getenv("GEO_CODE_API")
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
    today = date.today()
    location = get_geo_location(country, place)


    planting_system_prompt = """
        You are an agronomist and meteorologist. Study weather patterns of the given location 
        for the past and next four weeks using historical and forecast data. Assess whether 
        the geography and soil suit the crop. Even if the weather and soil conditions are condusive, check the crop life cycle and determine if the planting window has been missed or not.
        Be concise but thorough.
        Use this format: 
                The weather conditions for Akropong in Ghana for the last four weeks primarily featured temperatures ranging from 23°C to 32°C, with moderate to high humidity levels. Rainfall was intermittent but sufficient, as Akropong is currently transitioning from the dry season to the main rainy season, which typically lasts from March to July.

                Recommendation: Yes, it is a good time to plant maize in Akropong starting from 30th April, 20266 in Akropong for Maize.

                Reason for the recommendation:

                * **Weather Conditions**: The onset of the rainy season provides a conducive environment for maize germination and growth, with adequate water supply reducing irrigation needs.

                * **Soil Suitability**: The region is known for having fertile soils with good drainage, which are excellent for maize cultivation. Akropong lies within a major maize-growing region in Ghana.

                * **Crop Life Cycle**: Maize planted at the end of April will benefit from the onset of consistent rains and adequate sunlight. The crop typically requires about 90 to 110 days to reach maturity. Starting at this time aligns well with the May to July peak rainfall period, ensuring proper growth phase development before the subsequent dry period.

                * **Geographical Suitability**: Akropong's location within a tropical climate zone and its average elevations provide suitable temperature ranges for maize, with daily highs typically favoring photosynthesis.

                Thus, given the climatological transition into the main rainy season and the suitability of the regional soil and climate conditions, planting maize at this time is advisable."""

    user_prompt = f"""Is it a good time to plant {crop} at {location} ({place}, {country}) starting {today}?
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
