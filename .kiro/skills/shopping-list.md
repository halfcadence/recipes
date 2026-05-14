---
name: shopping-list
description: Generate a shopping list for one or more recipes from this site. Outputs a clean, pastable list for Google Docs or notes apps. Omits common pantry staples you likely already have.
triggers:
  - "shopping list"
  - "generate shopping list"
  - "what do I need to buy"
  - "grocery list"
---

# Shopping List Generator

The key words "MUST", "MUST NOT", "SHOULD", "SHOULD NOT", and "MAY" in this document are to be interpreted as described in RFC 2119.

## How It Works

When the user asks to generate a shopping list for one or more recipes:

1. Read the recipe file(s) from `r/<recipe-slug>.md`
2. Extract all ingredients
3. Categorize them and remove pantry staples (see below)
4. Output a clean, formatted shopping list

## Pantry Staples (OMIT from list)

These items SHOULD be omitted from the shopping list because most home cooks already have them. However, you MUST mention them in a brief "check you have" note at the bottom.

- Salt (kosher salt, flaky salt, table salt)
- Black pepper
- Sugar (white, brown)
- Neutral oil (vegetable, canola, sunflower)
- Olive oil
- Sesame oil
- Soy sauce
- Rice vinegar
- Mirin
- Sake (cooking)
- All-purpose flour
- Potato starch / cornstarch
- Butter (salted and unsalted)
- White rice

## Output Format

The output MUST be formatted as a clean, pastable list suitable for Google Docs or a notes app. Use this structure:

```
## Shopping List: [Recipe Name(s)]

**Protein**
- [ ] 1.3kg pork neck bones

**Produce**
- [ ] 500g Yukon Gold potatoes
- [ ] 300g napa cabbage
- [ ] 100g mung bean sprouts
- [ ] 4 green onions
- [ ] 8–10 perilla leaves
- [ ] 1 onion

**Korean/Asian Grocery**
- [ ] 10g gochugaru
- [ ] 30g doenjang
- [ ] 15g gochujang
- [ ] 30g fish sauce
- [ ] 15g ground perilla seed powder
- [ ] 15g perilla seed oil

**Pantry (check you have)**
- Salt, black pepper, garlic, ginger, rice wine/mirin, sesame oil, sesame seeds, water
```

## Rules

1. You MUST read the actual recipe file(s) — do not guess ingredients from memory.
2. You MUST group items by category. Use these categories as appropriate:
   - Protein
   - Produce
   - Dairy
   - Bread/Bakery
   - Asian Grocery (or Korean/Japanese/etc. as appropriate)
   - Liquor (for cocktail recipes)
   - Pantry (check you have)
3. You MUST combine duplicate ingredients when generating a list for multiple recipes (e.g., if two recipes need green onions, list the total amount once).
4. You MUST include quantities from the recipe.
5. You SHOULD note when an ingredient is specialty or hard to find (e.g., "perilla seed powder — Korean grocery store").
6. If the user specifies a yield multiplier (e.g., "double batch"), scale quantities accordingly.
7. The output MUST use markdown checkboxes (`- [ ]`) for easy copy-paste into task apps.
8. For cocktail recipes, list spirits and mixers under "Liquor" and garnishes under "Produce."
