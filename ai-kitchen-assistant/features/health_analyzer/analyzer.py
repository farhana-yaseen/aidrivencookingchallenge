import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Dummy nutritional database (ingredient: {calories, protein, carbs, fat}) per 100g
NUTRITIONAL_DATA = {
    "chicken breast": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6},
    "salmon": {"calories": 208, "protein": 20, "carbs": 0, "fat": 13},
    "rice": {"calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3},
    "broccoli": {"calories": 55, "protein": 3.7, "carbs": 11, "fat": 0.6},
    "olive oil": {"calories": 884, "protein": 0, "carbs": 0, "fat": 100},
    "white bread": {"calories": 265, "protein": 9, "carbs": 49, "fat": 3.2},
    "whole wheat bread": {"calories": 247, "protein": 13, "carbs": 41, "fat": 3.4},
    "sugar": {"calories": 387, "protein": 0, "carbs": 100, "fat": 0},
    "stevia": {"calories": 0, "protein": 0, "carbs": 0, "fat": 0},
}

# Dummy substitution data (unhealthy: healthy)
SUBSTITUTIONS = {
    "white bread": "whole wheat bread",
    "sugar": "stevia",
    "olive oil": "a lighter oil or use air frying",
}

console = Console()

def analyze_recipe_nutrition(recipe):
    """
    Analyzes the nutritional content of a given recipe.

    Args:
        recipe (dict): A dictionary with ingredients as keys and amounts in grams as values.
    """
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0

    for ingredient, amount in recipe.items():
        # Normalize ingredient name to lower case for lookup
        ingredient_name = ingredient.lower()
        if ingredient_name in NUTRITIONAL_DATA:
            data = NUTRITIONAL_DATA[ingredient_name]
            total_calories += data["calories"] * (amount / 100)
            total_protein += data["protein"] * (amount / 100)
            total_carbs += data["carbs"] * (amount / 100)
            total_fat += data["fat"] * (amount / 100)
        else:
            console.print(f"[yellow]Warning: No nutritional data for '{ingredient}'[/yellow]")

    console.print(Panel(
        Text(
            f"Total Calories: {total_calories:.2f}\n"
            f"Total Protein: {total_protein:.2f}g\n"
            f"Total Carbs: {total_carbs:.2f}g\n"
            f"Total Fat: {total_fat:.2f}g"
        ),
        title="[bold green]Nutritional Analysis[/bold green]",
        expand=False
    ))

def suggest_substitutions(recipe):
    """
    Suggests healthier substitutions for ingredients in a recipe.

    Args:
        recipe (dict): A dictionary with ingredients as keys.
    """
    suggestions = []
    for ingredient in recipe.keys():
        ingredient_name = ingredient.lower()
        if ingredient_name in SUBSTITUTIONS:
            suggestions.append(f"Consider replacing [bold red]{ingredient}[/bold red] with [bold green]{SUBSTITUTIONS[ingredient_name]}[/bold green].")

    if suggestions:
        console.print(Panel(
            "\n".join(suggestions),
            title="[bold yellow]Healthier Substitutions[/bold yellow]",
            expand=False
        ))
    else:
        console.print("[green]No immediate substitution suggestions. The recipe looks healthy![/green]")

def health_analyzer_main():
    """Main function for the health analyzer feature."""
    console.print(Panel(
        "[bold cyan]Welcome to the Recipe Health Analyzer![/bold cyan]\n"
        "Enter your recipe ingredients and their amounts in grams.",
        expand=False
    ))

    recipe = {}
    while True:
        ingredient = questionary.text("Enter an ingredient (or press Enter to finish):").ask()
        if not ingredient:
            break
        
        while True:
            try:
                amount_str = questionary.text(f"Enter amount for {ingredient} (in grams):").ask()
                if amount_str is None: # User cancelled
                    return
                amount = float(amount_str)
                recipe[ingredient] = amount
                break
            except (ValueError, TypeError):
                console.print("[red]Invalid amount. Please enter a number.[/red]")

    if not recipe:
        console.print("[yellow]No ingredients entered. Exiting Health Analyzer.[/yellow]")
        return

    console.print("\n[bold]Analyzing your recipe...[/bold]\n")
    
    analyze_recipe_nutrition(recipe)
    console.print("\n")
    suggest_substitutions(recipe)


if __name__ == "__main__":
    health_analyzer_main()
