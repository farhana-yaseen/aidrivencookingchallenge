import json
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()
PANTRY_FILE = "database/pantry.json"
MEAL_PLAN_FILE = "database/meal_plans.json"

def _load_json(filename, default=[]):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def _save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def manage_pantry():
    """Adds, removes, or views items in the pantry."""
    pantry = _load_json(PANTRY_FILE)
    
    while True:
        action = questionary.select(
            "Pantry Management:",
            choices=["View Pantry", "Add Item", "Remove Item", "Back"]
        ).ask()

        if action == "View Pantry":
            if not pantry:
                console.print("[yellow]Your pantry is empty.[/yellow]")
            else:
                table = Table(title="Pantry Inventory")
                table.add_column("Item", style="cyan")
                for item in pantry:
                    table.add_row(item)
                console.print(table)
        
        elif action == "Add Item":
            item = questionary.text("Enter item to add:").ask()
            if item and item not in pantry:
                pantry.append(item)
                _save_json(PANTRY_FILE, pantry)
                console.print(f"[green]Added {item} to pantry.[/green]")
            elif item in pantry:
                console.print(f"[yellow]{item} is already in the pantry.[/yellow]")

        elif action == "Remove Item":
            if not pantry:
                console.print("[yellow]Your pantry is empty.[/yellow]")
                continue
            item_to_remove = questionary.select("Select item to remove:", choices=pantry).ask()
            if item_to_remove:
                pantry.remove(item_to_remove)
                _save_json(PANTRY_FILE, pantry)
                console.print(f"[green]Removed {item_to_remove} from pantry.[/green]")
        
        elif action == "Back":
            break


def generate_weekly_plan():
    """Generates a mock weekly meal plan and saves it."""
    console.print("[yellow]Generating a new weekly meal plan... (mock AI response)[/yellow]")
    # Mock AI generation
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    meals = ["Spaghetti", "Tofu Stir-fry", "Chicken Salad", "Lentil Soup", "Fish Tacos", "Pizza Night", "Roast Dinner"]
    
    plan = {day: meal for day, meal in zip(days, meals)}
    _save_json(MEAL_PLAN_FILE, plan)
    
    table = Table(title="Your 7-Day Meal Plan")
    table.add_column("Day", style="cyan")
    table.add_column("Meal", style="magenta")
    for day, meal in plan.items():
        table.add_row(day, meal)
    console.print(table)
    console.print("[green]Weekly meal plan saved![/green]")


def generate_shopping_list():
    """Generates a shopping list by comparing the meal plan to the pantry."""
    pantry = _load_json(PANTRY_FILE)
    meal_plan = _load_json(MEAL_PLAN_FILE, {})

    if not meal_plan:
        console.print("[red]No meal plan found. Please generate one first.[/red]")
        return
        
    # This is a very simplified logic. A real version would break down meals into ingredients.
    console.print("[yellow]Note: This is a simplified shopping list based on meal names.[/yellow]")
    
    shopping_list = []
    for meal in meal_plan.values():
        # Heuristic: if a word from the meal is not in the pantry, add the meal name to the list
        words_in_meal = meal.lower().split()
        needed = True
        for word in words_in_meal:
            if word in pantry:
                needed = False
                break
        if needed and meal not in shopping_list:
            shopping_list.append(meal)
            
    if not shopping_list:
        console.print("[green]Your pantry seems to cover your meal plan. No shopping list generated.[/green]")
        return

    table = Table(title="Shopping List")
    table.add_column("Item to Buy", style="yellow")
    for item in shopping_list:
        table.add_row(item)
    console.print(table)


def meal_planner_main():
    """Main menu for the Meal Planner feature."""
    console.print(Panel("[bold cyan]Welcome to the Meal Planner & Grocery Assistant![/bold cyan]"))
    while True:
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "Plan Weekly Meals",
                "Generate Shopping List",
                "Manage Pantry",
                "Exit"
            ]
        ).ask()

        if choice == "Plan Weekly Meals":
            generate_weekly_plan()
        elif choice == "Generate Shopping List":
            generate_shopping_list()
        elif choice == "Manage Pantry":
            manage_pantry()
        elif choice == "Exit":
            break
        
        console.print("\n")


if __name__ == "__main__":
    meal_planner_main()
