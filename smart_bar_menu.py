# smart_bar_menu.py

from collections import Counter
from typing import List, Dict, Tuple

# --- Liquor Families for Substitution ---
LIQUOR_FAMILIES = {
    "whiskey": ["bourbon", "rye whiskey", "irish whiskey", "whiskey"],
    "tequila": ["blanco tequila", "reposado tequila", "tequila"],
    "gin": ["gin", "dry gin", "london dry gin"],
    "rum": ["white rum", "dark rum", "jamacian rum"],
    "vermouth": ["sweet vermouth", "dry vermouth", "vermouth", "vermouth rosso"],
    "cognac": ["cognac"],
    "orange liquer": ["triple sec", "cointreau"],
    "bitters": ["angostura bitters", "peychaud bitters", "orange bitters"],
    "syrup": ["simple syrup", "raspberry syrup", "orgeat syrup", "rock candy syrup"],
    "cream": ["milk", "whipped cream", "creamer"],
    "sweetener": ["sugar", "sugar cube"],
    "lemon": ["lemon", "lemon juice"],
    "lime": ["lime", "lime juice"]
}

# Reverse substitution lookup
LIQUOR_SUBSTITUTIONS = {}
for family, members in LIQUOR_FAMILIES.items():
    for liquor in members:
        LIQUOR_SUBSTITUTIONS[liquor] = set(members) - {liquor}

# --- DRINKS database (leave as-is) ---
from drinks_db import DRINKS  # Split out DRINKS to a separate file optionally (cleaner)

# --- Main Matching Function ---
def match_drinks(user_ingredients: List[str]) -> Dict:
    user_ingredients = [i.strip().lower() for i in user_ingredients]
    
    can_make = []
    missing_one = []
    missing_two = []
    substitute_drinks = []
    all_missing_ingredients = Counter()

    for drink in DRINKS:
        missing = []
        subs = []

        for ing in drink["ingredients"]:
            if ing in user_ingredients:
                continue
            elif ing in LIQUOR_SUBSTITUTIONS:
                found_sub = next((s for s in LIQUOR_SUBSTITUTIONS[ing] if s in user_ingredients), None)
                if found_sub:
                    subs.append((ing, found_sub))
                    continue
            missing.append(ing)

        if len(missing) == 0 and not subs:
            can_make.append(drink["name"])
        elif len(missing) == 0 and subs:
            substitute_drinks.append({
                "name": drink["name"],
                "substitutions": subs
            })
        elif len(missing) == 1:
            missing_one.append({"name": drink["name"], "missing": missing})
            for ing in missing:
                normalized = next((fam for fam, members in LIQUOR_FAMILIES.items() if ing in members), ing)
                all_missing_ingredients[normalized] += 1
        elif len(missing) == 2:
            # NEW: only count each missing ingredient if the other one is already in inventory
            missing_two.append({"name": drink["name"], "missing": missing})
            for ing in missing:
                other = [m for m in missing if m != ing][0]  # the other missing one
                if other in user_ingredients or any(s in user_ingredients for s in LIQUOR_SUBSTITUTIONS.get(other, [])):
                    normalized = next((fam for fam, members in LIQUOR_FAMILIES.items() if ing in members), ing)
                    all_missing_ingredients[normalized] += 1

    high_impact = [{"ingredient": ing, "unlocks": count} for ing, count in all_missing_ingredients.most_common(5)]

    return {
        "can_make": can_make,
        "substitute_drinks": substitute_drinks,
        "missing_one": missing_one,
        "missing_two": missing_two,
        "high_impact_ingredients": high_impact
    }
