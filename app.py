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
