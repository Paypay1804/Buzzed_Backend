# test.py

from smart_bar_menu import match_drinks

# Mock list of ingredients for testing
my_ingredients = [
    "lemon juice", "lime juice", "bourbon", "honey", "water",
    "dark rum", "dry vermouth", "sugar", "coconut cream", "milk",
    "simple syrup", "grenadine", "ginger beer", "cherry", "cognac"
]

# Run the match function
results = match_drinks(my_ingredients)

# Pretty print results
print("\n✅ You can make:")
for drink in results["can_make"]:
    print(f"- {drink}")

print("\n🔁 You can make with substitutions:")
for d in results["substitute_drinks"]:
    subs = ", ".join([f"{orig} → {rep}" for orig, rep in d["substitutions"]])
    print(f"- {d['name']} (substitute: {subs})")

print("\n❗ Missing 1 ingredient:")
for d in results["missing_one"]:
    print(f"- {d['name']} (missing: {', '.join(d['missing'])})")

print("\n❗❗ Missing 2 ingredients:")
for d in results["missing_two"]:
    print(f"- {d['name']} (missing: {', '.join(d['missing'])})")

print("\n🛒 High-impact ingredients to buy:")
for s in results["high_impact_ingredients"]:
    print(f"- {s['ingredient']} (unlocks {s['unlocks']} drinks)")
