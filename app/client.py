from typing import Generator

from config import provider
movie_mood_template = "Recommend 3 movies based on this users mood: {user_input}."

def get_mood_recommendation(user_input) -> str:
    prompt = movie_mood_template.format(user_input=user_input)
    return provider.generate_response(prompt)

def get_mood_recommendation_stream(user_input) -> Generator[str, None, None]:
    prompt = movie_mood_template.format(user_input=user_input)
    return provider.generate_response_stream(prompt)