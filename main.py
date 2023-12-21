from recommender import Recommender
from db_access import DatabaseAccess

from fastapi import FastAPI

app = FastAPI()
recommender_instance = Recommender()

@app.post("/recommender")
def get_recommended_recipes(user_input: str):
    recommended_recipes = recommender_instance.recommend_recipes(user_input)
    return {"recommended_recipes": recommended_recipes}
        