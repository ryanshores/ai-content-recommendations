from config import provider
movie_mood_template = "Recommend 3 movies based on this users mood: {user_input}."

def get_mood_recommendation(user_input):
    prompt = movie_mood_template.format(user_input=user_input)
    return provider.generate_response(prompt)