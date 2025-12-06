import json
import random
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import streamlit as st

console = Console()

# Mock 'AI' recipe generation
def generate_ai_recipe(ingredients, diet, cuisine):
    """
    Generates a recipe based on user inputs.
    In a real scenario, this would call a generative AI model.
    """
    # Simple mock logic
    base_recipe = {
        "title": f"{cuisine.capitalize()} {diet.capitalize()} Delight with {', '.join(ingredients)}",
        "servings": 2,
        "ingredients": {
            "main ingredient (e.g., chicken, tofu)": "200g",
            "vegetable (e.g., broccoli, bell pepper)": "100g",
            "carb (e.g., rice, pasta)": "150g",
            "sauce/spice (e.g., soy sauce, curry powder)": "2 tbsp"
        },
        "instructions": [
            "Prepare the ingredients.",
            "Cook the main ingredient until browned.",
            "Add vegetables and cook until tender.",
            "Serve over your carb of choice, with the sauce.",
        ]
    }
    # Customize based on input
    if ingredients:
        base_recipe["ingredients"][ingredients[0]] = "200g"
    
    return base_recipe

def suggest_substitutions_streamlit(missing_ingredients):
    """Suggests substitutions for missing ingredients."""
    # Dummy substitution logic
    substitutions = {
        "chicken": "tofu or chickpeas",
        "rice": "quinoa or couscous",
        "olive oil": "butter or coconut oil"
    }
    suggestions_text = []
    for item in missing_ingredients:
        if item.lower() in substitutions:
            suggestions_text.append(f"For {item}, you could use {substitutions[item.lower()]}.")
    
    if suggestions_text:
        st.subheader("Substitution Suggestions")
        st.write("\n".join(suggestions_text))


def adjust_serving_size(recipe, new_servings):
    """Adjusts ingredient quantities based on serving size."""
    original_servings = recipe.get("servings", 1)
    if original_servings == 0: return recipe # Avoid division by zero
    
    ratio = new_servings / original_servings
    adjusted_ingredients = {}

    for ingredient, amount_str in recipe["ingredients"].items():
        try:
            # Simple parsing - this is a limitation of a mock
            amount = float(amount_str.split('g')[0].split(' ')[0])
            unit = ''.join(filter(str.isalpha, amount_str))
            adjusted_amount = amount * ratio
            adjusted_ingredients[ingredient] = f"{adjusted_amount:.1f}{unit}"
        except (ValueError, IndexError):
            # If parsing fails, keep original amount
            adjusted_ingredients[ingredient] = amount_str
    
    recipe["ingredients"] = adjusted_ingredients
    recipe["servings"] = new_servings
    return recipe

def display_recipe_streamlit(recipe):
    """Displays a recipe using Streamlit."""
    st.title(recipe['title'])
    st.write(f"Serves {recipe['servings']}")
    
    st.subheader("Ingredients")
    ingredients_data = {"Ingredient": [], "Amount": []}
    for ingredient, amount in recipe["ingredients"].items():
        ingredients_data["Ingredient"].append(ingredient)
        ingredients_data["Amount"].append(amount)
    st.table(ingredients_data)
    
    st.subheader("Instructions")
    for i, step in enumerate(recipe["instructions"]):
        st.write(f"{i+1}. {step}")

def save_recipe_streamlit(recipe):
    """Saves the recipe to a JSON file."""
    try:
        with open("ai-kitchen-assistant/database/recipes.json", "r+") as f:
            try:
                recipes = json.load(f)
            except json.JSONDecodeError:
                recipes = []
            recipes.append(recipe)
            f.seek(0)
            json.dump(recipes, f, indent=4)
    except FileNotFoundError:
        with open("ai-kitchen-assistant/database/recipes.json", "w") as f:
            json.dump([recipe], f, indent=4)
    st.success("Recipe saved successfully!")

def recipe_generator_page():
    """Main function for the recipe generator feature."""
    st.header("AI Recipe Generator")
    
    ingredients_str = st.text_input("What ingredients do you have? (comma-separated)")
    ingredients = [i.strip() for i in ingredients_str.split(',')] if ingredients_str else []
    
    diet = st.selectbox(
        "Any dietary preference?",
        ["None", "Vegan", "Keto", "Low Sodium", "Gluten-Free"]
    )
    
    cuisine = st.text_input("What cuisine would you like? (e.g., Italian, Mexican)", "Any")
    
    if st.button("Generate Recipe"):
        if not ingredients:
            st.warning("Please enter at least one ingredient.")
            return

        st.write("Generating a recipe for you...")
        recipe = generate_ai_recipe(ingredients, diet, cuisine)
        
        st.session_state.recipe = recipe
        
    if 'recipe' in st.session_state:
        recipe = st.session_state.recipe
        new_servings = st.number_input(f"The recipe is for {recipe['servings']} servings. How many would you like?", min_value=1, value=recipe['servings'])
        
        if new_servings != recipe['servings']:
            recipe = adjust_serving_size(recipe, new_servings)
            st.session_state.recipe = recipe

        display_recipe_streamlit(recipe)

        missing = st.text_input("Are you missing any common ingredients for this? (e.g., chicken, olive oil)")
        if missing:
            suggest_substitutions_streamlit([i.strip() for i in missing.split(',')])

        if st.button("Save Recipe"):
            save_recipe_streamlit(recipe)

# CLI functions
def suggest_substitutions_cli(missing_ingredients):
    """Suggests substitutions for missing ingredients."""
    # Dummy substitution logic
    substitutions = {
        "chicken": "tofu or chickpeas",
        "rice": "quinoa or couscous",
        "olive oil": "butter or coconut oil"
    }
    suggestions_text = []
    for item in missing_ingredients:
        if item.lower() in substitutions:
            suggestions_text.append(f"For [bold red]{item}[/bold red], you could use [bold green]{substitutions[item.lower()]}[/bold green].")
    
    if suggestions_text:
        console.print(Panel("\n".join(suggestions_text), title="[yellow]Substitution Suggestions[/yellow]"))

def display_recipe_cli(recipe):
    """Displays a recipe using Rich."""
    panel_content = f"[bold cyan]{recipe['title']}[/bold cyan]\n[italic]Serves {recipe['servings']}[/italic]\n"
    
    # Ingredients Table
    ingredients_table = Table(title="Ingredients")
    ingredients_table.add_column("Ingredient", style="magenta")
    ingredients_table.add_column("Amount", style="green")
    for ingredient, amount in recipe["ingredients"].items():
        ingredients_table.add_row(ingredient, amount)
        
    # Instructions
    instructions_text = "\n[bold]Instructions:[/bold]\n" + "\n".join(f"{i+1}. {step}" for i, step in enumerate(recipe["instructions"]))
    
    console.print(Panel(panel_content, expand=False))
    console.print(ingredients_table)
    console.print(instructions_text)

def save_recipe_cli(recipe):
    """Saves the recipe to a JSON file."""
    try:
        with open("database/recipes.json", "r+") as f:
            recipes = json.load(f)
            recipes.append(recipe)
            f.seek(0)
            json.dump(recipes, f, indent=4)
    except (FileNotFoundError, json.JSONDecodeError):
        with open("database/recipes.json", "w") as f:
            json.dump([recipe], f, indent=4)
    console.print("\n[bold green]Recipe saved successfully![/bold green]")

def recipe_generator_main():
    """Main function for the recipe generator feature."""
    console.print(Panel("[bold cyan]Welcome to the AI Recipe Generator![/bold cyan]"))
    
    ingredients_str = questionary.text("What ingredients do you have? (comma-separated)").ask()
    ingredients = [i.strip() for i in ingredients_str.split(',')] if ingredients_str else []
    
    diet = questionary.select(
        "Any dietary preference?",
        choices=["None", "Vegan", "Keto", "Low Sodium", "Gluten-Free"]
    ).ask()
    
    cuisine = questionary.text("What cuisine would you like? (e.g., Italian, Mexican)", default="Any").ask()
    
    # Generate recipe
    console.print("\n[yellow]Generating a recipe for you...[/yellow]")
    recipe = generate_ai_recipe(ingredients, diet, cuisine)
    
    # Adjust servings
    servings_str = questionary.text(f"The recipe is for {recipe['servings']} servings. How many would you like?", default=str(recipe['servings'])).ask()
    try:
        new_servings = int(servings_str)
        if new_servings != recipe['servings']:
            recipe = adjust_serving_size(recipe, new_servings)
    except ValueError:
        console.print("[red]Invalid number, keeping original serving size.[/red]")

    display_recipe_cli(recipe)

    # Substitution suggestion (mock)
    if random.choice([True, False]): # Randomly decide to show substitution
        missing = questionary.text("Are you missing any common ingredients for this? (e.g., chicken, olive oil)").ask()
        if missing:
            suggest_substitutions_cli([i.strip() for i in missing.split(',')])

    # Save recipe
    if questionary.confirm("Do you want to save this recipe?").ask():
        save_recipe_cli(recipe)

if __name__ == "__main__":
    recipe_generator_main()