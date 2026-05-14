---
name: shopping-list
description: Generate a merged shopping list for one or more recipes from this site, with portion scaling. Outputs a clean, pastable list for Google Docs or notes apps. Omits common pantry staples you likely already have.
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

1. Read ALL requested recipe files from `r/<recipe-slug>.md`
2. Extract all ingredients from each recipe
3. Apply portion scaling if requested (see Scaling section)
4. Merge ingredients across all recipes — combine duplicates, sum quantities
5. Categorize them and remove pantry staples (see below)
6. Output a single unified shopping list

## Multi-Recipe Merging

This skill is designed to work across multiple recipes at once. When the user requests a list for multiple recipes:

- You MUST read every requested recipe file.
- You MUST merge all ingredients into a single unified list (not separate lists per recipe).
- You MUST sum quantities for the same ingredient across recipes. For example:
  - Recipe A needs 4 eggs, Recipe B needs 3 eggs → list "7 eggs"
  - Recipe A needs 2 green onions, Recipe B needs 4 green onions → list "6 green onions"
- If units differ for the same ingredient (e.g., one recipe uses grams, another uses "1 bunch"), use your best judgment to combine or list separately with a note.
- You SHOULD add a small annotation showing which recipe(s) need an ingredient if it helps the user shop (e.g., "4 green onions (gamjatang, ankake don)"). This is optional for common items but helpful for specialty items.

## Portion Scaling

Recipes have a `yield` field in their frontmatter (e.g., `yield: 4` means serves 4). When the user specifies how many people they're cooking for:

- You MUST scale all quantities proportionally.
- Formula: `scaled_quantity = original_quantity × (desired_servings / recipe_yield)`
- Round to practical amounts (don't say "1.33 onions" — say "1–2 onions").
- If no yield is specified in the recipe, assume it serves 2.
- The user MAY say things like:
  - "for 6 people" → scale to 6 servings
  - "double batch" → multiply by 2
  - "half batch" → multiply by 0.5
  - "for 2" → scale to 2 servings (may mean scaling down)

When combining multiple recipes with different scales:
- Each recipe MAY have a different scale factor. E.g., "gamjatang for 6, ankake don for 2"
- If the user gives one scale for all (e.g., "shopping list for picnic sandwiches, for 4 people"), apply that scale to all recipes.

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
Serves: [X people / or note per-recipe scaling]

**Protein**
- [ ] 1.3kg pork neck bones
- [ ] 7 eggs (tamago sando ×4, ankake don ×3)

**Produce**
- [ ] 500g Yukon Gold potatoes
- [ ] 6 green onions (gamjatang ×4, ankake don ×2)
- [ ] 300g napa cabbage
- [ ] 100g mung bean sprouts
- [ ] 8–10 perilla leaves
- [ ] 1 onion

**Bread/Bakery**
- [ ] 1 loaf soft white bread (cucumber sandwiches, watercress sandwiches, ham sandwiches)

**Korean/Asian Grocery**
- [ ] 10g gochugaru
- [ ] 30g doenjang
- [ ] 15g gochujang
- [ ] 30g fish sauce
- [ ] 15g ground perilla seed powder — Korean grocery store
- [ ] 15g perilla seed oil — Korean grocery store

**Dairy**
- [ ] 4 tbsp cream cheese

**Liquor**
- [ ] 60ml umeshu

**Pantry (check you have)**
- Salt, black pepper, soy sauce, mirin, sesame oil, rice vinegar, neutral oil, butter, white rice
```

## Rules

1. You MUST read the actual recipe file(s) — do not guess ingredients from memory.
2. You MUST produce a single merged list, not separate lists per recipe.
3. You MUST group items by category. Use these categories as appropriate:
   - Protein
   - Produce
   - Dairy
   - Bread/Bakery
   - Asian Grocery (or Korean/Japanese/etc. as appropriate)
   - Liquor (for cocktail recipes)
   - Pantry (check you have)
4. You MUST combine duplicate ingredients across all recipes and sum their quantities.
5. You MUST include quantities from the recipe (scaled if applicable).
6. You SHOULD note when an ingredient is specialty or hard to find (e.g., "perilla seed powder — Korean grocery store").
7. You SHOULD annotate which recipe needs a specialty ingredient if it's not obvious.
8. The output MUST use markdown checkboxes (`- [ ]`) for easy copy-paste into task apps.
9. For cocktail recipes, list spirits and mixers under "Liquor" and garnishes under "Produce."
10. If the user doesn't specify portions, use the recipe's default yield and note it.
