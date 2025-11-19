AI Kitchen Assistant CLI
Project Overview

A professional CLI application for AI-driven cooking assistance, including recipe generation, meal planning, cooking guidance, flavor pairing, and nutritional analysis. Integrates AI to provide interactive, personalized cooking experiences.

Core Features

AI Recipe Generator based on available ingredients, dietary preferences, or cuisine type

Meal Planner & Grocery Assistant with shopping lists and pantry tracking

Cooking Tutor with step-by-step instructions, optional voice guidance, and real-time tips

Flavor Pairing AI to suggest innovative ingredient combinations and drink pairings

Recipe Health Analyzer for nutritional analysis and healthier substitutions

AI Kitchen Companion combining all above features with smart kitchen integration

AI-Driven Cooking Challenges for fun, gamified cooking experiences

Tech Stack

Language: Python 3.11+

CLI Framework: Questionary (interactive menus)

UI Library: Rich (tables, panels, progress bars)

Storage: SQLite / JSON for recipes, pantry, and meal plans

AI Models: GPT-style models for recipe generation, optional computer vision for ingredient recognition

Package Manager: pip / venv

Project Structure
ai-kitchen-assistant/
├── main.py                    # Entry point with menu loop
├── database/
│   ├── recipes.json           # Stored recipes
│   ├── pantry.json            # User pantry inventory
│   └── meal_plans.json        # Generated weekly meal plans
└── features/
    ├── recipe_generator/
    │   ├── GEMINI.md
    │   └── generator.py
    ├── meal_planner/
    │   ├── GEMINI.md
    │   └── planner.py
    ├── cooking_tutor/
    │   ├── GEMINI.md
    │   └── tutor.py
    ├── flavor_pairing/
    │   ├── GEMINI.md
    │   └── pairing.py
    ├── health_analyzer/
    │   ├── GEMINI.md
    │   └── analyzer.py
    ├── kitchen_companion/
    │   ├── GEMINI.md
    │   └── companion.py
    └── cooking_challenges/
        ├── GEMINI.md
        └── challenges.py

Critical Data Handling Rule

Always normalize ingredient quantities and nutritional data to avoid rounding errors.

# Correct approach:
ingredient_amount_grams = 250   # Store weight in grams
calories = 1500                 # Store total calories as integer

# Wrong approach:
ingredient_amount = 0.25        # Avoid floats for precise measurements

Key Categories

Recipes: Breakfast, Lunch, Dinner, Snack, Dessert
Diets: Vegan, Keto, Low Sodium, Low Carb, Gluten-Free
Ingredients: Vegetables, Fruits, Meat, Dairy, Grains, Spices, Others

CLI Interaction

Uses Questionary for dropdown-style selections in the terminal.
Rich is used for tables, panels, progress bars, and visually appealing CLI elements.