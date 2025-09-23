# app.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

try:
    from smart_bar_menu import match_drinks
    from drinks_db import DRINKS
except Exception as e:
    print("❌ Import failed:", e)

class IngredientsRequest(BaseModel):
    ingredients: List[str]

@app.post("/match")
def get_drink_matches(request: IngredientsRequest):
    return match_drinks(request.ingredients)

@app.get("/ingredients")
def get_all_ingredients():
    unique_ingredients = set()
    for drink in DRINKS:
        for ing in drink["ingredients"]:
            unique_ingredients.add(ing.lower().strip())
    return {"ingredients": sorted(unique_ingredients)}

@app.on_event("startup")
async def startup_event():
    print("🚦 Registered routes:", [route.path for route in app.router.routes])