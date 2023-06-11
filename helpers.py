import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def random_recipe():
    url = "https://www.themealdb.com/api/json/v1/1/random.php"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    prefix_ing = "strIngredient"
    prefix_meas = "strMeasure"

    ings = []
    meas = []

    ings_count = 0
    meas_count = 0
    try:
        meal = response.json()['meals'][0]
        for key, value in meal.items():
            if key.startswith(prefix_ing):
                if value != "" and value != " ":
                    if value is not None:
                        ings.append(value)
                        ings_count += 1
            if key.startswith(prefix_meas):
                if value != "" and value != " ":
                    if value is not None:
                        meas.append(value)
                        meas_count += 1
    except (KeyError, TypeError, ValueError):
        return None

    recipe = {
        "name": meal["strMeal"],
        "instructions": meal["strInstructions"],
        "image": meal["strMealThumb"],
        "youtube_link": meal["strYoutube"],
        "ingredients": ings,
        "measurments": meas
    }
    return recipe