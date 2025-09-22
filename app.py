# app.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from smart_bar_menu import match_drinks

app = FastAPI()

class IngredientsRequest(BaseModel):
    ingredients: List[str]

@app.post("/match")
def get_drink_matches(request: IngredientsRequest):
    return match_drinks(request.ingredients)

from drinks_db import DRINKS

@app.get("/ingredients")
def get_all_ingredients():
    unique_ingredients = set()
    for drink in DRINKS:
        for ing in drink["ingredients"]:
            unique_ingredients.add(ing.lower().strip())
    return {"ingredients": sorted(unique_ingredients)}

print("✅ FastAPI started with ingredients endpoint loaded")
