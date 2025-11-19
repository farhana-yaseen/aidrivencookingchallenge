Day 1: AI Recipe Generator
Goal

Build the core feature: generate recipes based on user input (ingredients, dietary preferences, cuisine).

Learning Focus

 * Handling user input in CLI
 * Text generation with AI
 * String formatting and display
 * File operations (store favorite recipes)

Concepts

 * Recipe: A structured set of ingredients and instructions
 * Ingredient: Item used in a recipe
 * Cuisine/Diet: Filters for recipe generation (e.g., Vegan, Keto)

Features to Build
1. Generate Recipe

Flow:

 * Ask for available ingredients
 * Ask for dietary preference (Vegan, Keto, Low Sodium, etc.)
 * Ask for cuisine type (optional)
 * Generate recipe using AI
 * Show ingredients and steps in Rich table/panel
 * Ask if user wants to save it to recipes.json

2. Suggest Substitutions

 * For missing ingredients, suggest replacements
 * Display substitutions in colored output

3. Adjust Recipe for Serving Size

 * Ask number of servings
 * Adjust ingredient quantities proportionally

Success Criteria

✅ Can generate recipe from input
✅ Can suggest substitutions
✅ Can adjust ingredient quantities
✅ Beautiful formatted output




<!-- **Run:**
gemini 

**Prompt:**
"Read all gemini.md files and build recipe generator" 

**Save conversation:**
gemini /save features/transactions  -->
