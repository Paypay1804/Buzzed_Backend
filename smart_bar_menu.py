# smart_bar_menu.py

from collections import Counter
from typing import List, Dict, Tuple
from drinks_db import DRINKS

# --- Liquor Families for Substitution ---
LIQUOR_FAMILIES = {
    "whiskey": ["bourbon", "rye whiskey", "irish whiskey", "whiskey"],
    "tequila": ["blanco tequila", "reposado tequila", "tequila"],
    "gin": ["gin", "dry gin", "london dry gin"],
    "rum": ["white rum", "dark rum", "jamaican rum"],
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

LIQUOR_SUBSTITUTIONS = {}
for family, items in LIQUOR_FAMILIES.items():
    for item in items:
        LIQUOR_SUBSTITUTIONS[item] = [alt for alt in items if alt != item]

# --- DRINKS database (leave as-is) ---
from drinks_db import DRINKS  # Split out DRINKS to a separate file optionally (cleaner)

# --- Main Matching Function ---
def match_drinks(user_ingredients: List[str]) -> Dict:
    user_ingredients = [i.strip().lower() for i in user_ingredients]
    
    can_make = []
    missing_one = []
    missing_two = []
    missing_three=[]
    missing_four=[]
    substitute_drinks = []
    all_missing_ingredients = Counter()

    for drink in DRINKS:
        missing = []
        subs = []

        for ing in drink["ingredients"]:
            if ing in user_ingredients:
                continue

            elif ing in LIQUOR_SUBSTITUTIONS:
                valid_subs = [
                    s for s in LIQUOR_SUBSTITUTIONS[ing]
                    if s in user_ingredients and any(
                        s in fam and ing in fam for fam in LIQUOR_FAMILIES.values()
                    )
                ]
                found_sub = valid_subs[0] if valid_subs else None
                if found_sub:
                    subs.append((ing, found_sub))
                    continue
                else:
                    missing.append(ing)

        # --- Only mark as Can Make if every ingredient is owned
        # or has a same-family substitute actually present ---
        if len(missing) == 0 and not subs:
            all_valid = True
            for ing in drink["ingredients"]:
                if ing not in user_ingredients:
                    same_family = any(
                        ing in fam and any(u in fam for u in user_ingredients)
                        for fam in LIQUOR_FAMILIES.values()
                    )
                    if not same_family:
                        all_valid = False
                        break
            if all_valid or any(
                all(
                    ing in fam and any(u in fam for u in user_ingredients)
                    for ing in drink["ingredients"]
                )
                for fam in LIQUOR_FAMILIES.values()
            ):
                can_make.append({
                    "name": drink["name"],
                    "ingredients": drink["ingredients"],
                    "glass": drink.get("glass", []),
                    "instructions": drink.get("instructions", [])
                })
        elif subs:
            # Recalculate from scratch using the full drink list
            covered = {orig for orig, _ in subs}
            remaining_missing = [
                ing for ing in drink["ingredients"]
                if ing not in user_ingredients
                and not any(ing == orig or (ing in fam and orig in fam)
                            for orig, _ in subs
                            for fam in LIQUOR_FAMILIES.values())
            ]
            missing_count = len(remaining_missing)

            owned_or_subbed = sum(
                1 for ing in drink["ingredients"]
                if ing in user_ingredients or ing in covered
            )
            fully_covered = owned_or_subbed == len(drink["ingredients"])

            if not remaining_missing and fully_covered:
                substitute_drinks.append({
                    "name": drink["name"],
                    "ingredients": drink["ingredients"],
                    "substitutions": [list(pair) for pair in subs],
                    "glass": drink.get("glass", []),
                    "instructions": drink.get("instructions", [])
                })
            else:
                # Recalculate full missing list, considering family substitutions
                remaining_missing = [
                    ing for ing in drink["ingredients"]
                    if ing not in user_ingredients
                    and not any(
                        ing == orig or (ing in fam and orig in fam)
                        for orig, _ in subs
                        for fam in LIQUOR_FAMILIES.values()
                    )
                ]

                missing_count = len(remaining_missing)
                target_list = (
                    missing_one if missing_count == 1 else
                    missing_two if missing_count == 2 else
                    missing_three if missing_count == 3 else
                    missing_four
                )
                target_list.append({
                    "name": drink["name"],
                    "missing": remaining_missing,
                    "ingredients": drink["ingredients"],
                    "glass": drink.get("glass", []),
                    "instructions": drink.get("instructions", [])
                })
        elif len(missing) == 1:
            missing_one.append({
                "name": drink["name"],
                "missing": missing,
                "ingredients": drink["ingredients"],
                "glass": drink.get("glass", []),
                "instructions": drink.get("instructions", [])
            })
            for ing in missing:
                normalized = next((fam for fam, members in LIQUOR_FAMILIES.items() if ing in members), ing)
                all_missing_ingredients[normalized] += 1
        elif len(missing) == 2:
            missing_two.append({
                "name": drink["name"],
                "missing": missing,
                "ingredients": drink["ingredients"],
                "glass": drink.get("glass", []),
                "instructions": drink.get("instructions", [])
            })
            for ing in missing:
                normalized = next((fam for fam, members in LIQUOR_FAMILIES.items() if ing in members), ing)
                all_missing_ingredients[normalized] += 1
        elif len(missing) == 3:
            missing_three.append({
                "name": drink["name"],
                "missing": missing,
                "ingredients": drink["ingredients"],
                "glass": drink.get("glass", []),
                "instructions": drink.get("instructions", [])
            })
            for ing in missing:
                normalized = next((fam for fam, members in LIQUOR_FAMILIES.items() if ing in members), ing)
                all_missing_ingredients[normalized] += 1
        elif len(missing) == 4:
            missing_four.append({
                "name": drink["name"],
                "missing": missing,
                "ingredients": drink["ingredients"],
                "glass": drink.get("glass", []),
                "instructions": drink.get("instructions", [])
            })
            for ing in missing:
                normalized = next((fam for fam, members in LIQUOR_FAMILIES.items() if ing in members), ing)
                all_missing_ingredients[normalized] += 1


    high_impact = [{"ingredient": ing, "unlocks": count} for ing, count in all_missing_ingredients.most_common(5)]
    import json
    print("=== DEBUG RESULTS ===")
    print(json.dumps({
        "sample_subs": substitute_drinks[:3],
        "sample_can_make": can_make[:3],
        "sample_missing": missing_one[:3]
    }, indent=2))

    return {
        "can_make": can_make,
        "substitute_drinks": substitute_drinks,
        "missing_one": missing_one,
        "missing_two": missing_two,
        "missing_three": missing_three,
        "missing_four": missing_four,
        "high_impact_ingredients": high_impact
}

def get_high_impact_ingredients(user_ingredients):
    from collections import Counter

    results = match_drinks(user_ingredients)  # reuse main logic
    missing_one = results.get("missing_one", [])
    counts = Counter()

    for drink in missing_one:
        for ing in drink["missing"]:
            counts[ing] += 1

    high_impact = [
        {"ingredient": ing, "unlocks": count}
        for ing, count in counts.most_common(5)
    ]

    return {"high_impact_ingredients": high_impact}



