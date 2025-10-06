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
    alcohols = {"vodka", "gin", "rum", "tequila", "whiskey", "bourbon", "brandy", "scotch", "cognac", "amaretto", "aperol", "campari", "vermouth", "liqueur"}
    fruits = {"lemon", "lime", "orange", "cherry", "pineapple", "grapefruit", "mint", "raspberry"}
    mixers = {"juice", "soda", "beer", "cola", "syrup", "tonic", "coffee", "cream", "water", "honey"}
    
    categories = {"Alcohol": [], "Fruit": [], "Mixer": [], "Misc": []}
    unique_ingredients = set()

    for drink in DRINKS:
        for ing in drink["ingredients"]:
            clean = ing.lower().strip()
            if clean not in unique_ingredients:
                unique_ingredients.add(clean)
                # Categorize
                if any(word in clean for word in alcohols):
                    categories["Alcohol"].append(ing)
                elif any(word in clean for word in fruits):
                    categories["Fruit"].append(ing)
                elif any(word in clean for word in mixers):
                    categories["Mixer"].append(ing)
                else:
                    categories["Misc"].append(ing)

    return {"categories": categories}

from smart_bar_menu import get_high_impact_ingredients  # move import to top of file

@app.get("/high_impact")
def get_high_impact():
    return get_high_impact_ingredients()

@app.on_event("startup")
async def startup_event():
    print("🚦 Registered routes:", [route.path for route in app.router.routes])