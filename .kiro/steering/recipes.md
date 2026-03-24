---
inclusion: fileMatch
fileMatchPattern: "r/*.md"
---

# Recipe Site Guidelines

## Adding a New Recipe

1. Create the recipe file in `r/` as a markdown file (e.g., `r/my-recipe.md`).
2. Use metric measurements only (grams, milliliters, °C). No cups, tablespoons, teaspoons, or Fahrenheit.
3. Use this front matter and format:
   ```markdown
   ---
   title: Recipe Name
   source: https://original-source-url (if applicable)
   ---

   ## Ingredients

   - item 1
   - item 2

   ## Steps

   1. Step one.
   2. Step two.

   ## Notes

   - Optional tips and variations.
   ```
3. Add a link to `index.md` under the appropriate category (Drinks, Desserts and Sweets, Mains, etc.). Create a new category section if needed.
4. Commit both the new recipe file and the updated `index.md`.

Recipes will not appear on the site unless they are linked from `index.md`.
