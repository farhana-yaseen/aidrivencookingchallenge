import random
import questionary
from rich.console import Console
from rich.panel import Panel

console = Console()

# Data for challenges
MYSTERY_INGREDIENTS = {
    "proteins": ["Tofu", "Canned Sardines", "Black Beans", "Chicken Thighs", "Quail Eggs"],
    "vegetables": ["Artichoke", "Fennel", "Beetroot", "Okra", "Celeriac"],
    "pantry_staples": ["Polenta", "Miso Paste", "Gochujang", "Rosewater", "Nutritional Yeast"],
    "wildcard": ["Edible Flowers", "Seaweed", "Fruit Loops", "Pickle Juice", "Date Syrup"]
}

def generate_mystery_challenge():
    """Generates and displays a mystery ingredient challenge."""
    console.print(Panel("[bold cyan]Generating a Mystery Box Challenge![/bold cyan]"))

    box = {
        "Protein": random.choice(MYSTERY_INGREDIENTS["proteins"]),
        "Vegetable": random.choice(MYSTERY_INGREDIENTS["vegetables"]),
        "Pantry Staple": random.choice(MYSTERY_INGREDIENTS["pantry_staples"]),
        "Wildcard": random.choice(MYSTERY_INGREDIENTS["wildcard"]),
    }

    panel_content = "[bold]Your mystery box contains:[/bold]\n\n"
    for category, ingredient in box.items():
        panel_content += f"  - [bold magenta]{category}:[/bold magenta] {ingredient}\n"
    
    panel_content += "\nYour challenge is to create a cohesive dish featuring all these ingredients. Good luck!"

    console.print(Panel(
        panel_content,
        title="[yellow]Mystery Box[/yellow]",
        expand=False
    ))

def score_dish():
    """Takes a user's description of their dish and provides a mock AI score."""
    console.print(Panel("[bold cyan]Describe your dish for scoring![/bold cyan]"))
    
    description = questionary.text("Describe the dish you made and how you used the ingredients:").ask()

    if not description:
        console.print("[yellow]No description provided. Cannot score.[/yellow]")
        return

    # Mock AI scoring
    console.print("[yellow]Analyzing your dish description... (mock AI evaluation)[/yellow]\n")
    
    creativity_score = random.randint(5, 10)
    presentation_score = random.randint(5, 10)
    use_of_ingredients_score = random.randint(3, 10)
    
    overall_score = (creativity_score + presentation_score + use_of_ingredients_score) / 3

    # Mock AI feedback
    feedback = ""
    if overall_score >= 8:
        feedback = "An outstanding dish! Your creativity and use of ingredients are commendable. A chef-worthy creation!"
    elif overall_score >= 6:
        feedback = "A solid effort! The dish sounds appealing, with good use of the mystery ingredients. A few tweaks could make it a masterpiece."
    else:
        feedback = "A valiant attempt! It's tough working with mystery ingredients. Some elements might not have harmonized perfectly, but it's a great learning experience."

    console.print(Panel(
        f"[bold]Overall Score: {overall_score:.1f}/10[/bold]\n\n"
        f"  - Creativity: {creativity_score}/10\n"
        f"  - Presentation (as described): {presentation_score}/10\n"
        f"  - Use of Ingredients: {use_of_ingredients_score}/10\n\n"
        f"[bold]Feedback:[/bold]\n[italic]{feedback}[/italic]",
        title="[green]AI Score & Feedback[/green]"
    ))

def cooking_challenges_main():
    """Main function for the Cooking Challenges feature."""
    console.print(Panel("[bold cyan]Welcome to AI-Driven Cooking Challenges![/bold cyan]"))
    
    while True:
        choice = questionary.select(
            "Choose a challenge:",
            choices=[
                "Generate Mystery Ingredient Challenge",
                "Get My Dish Scored",
                "Exit"
            ]
        ).ask()

        if choice == "Generate Mystery Ingredient Challenge":
            generate_mystery_challenge()
        elif choice == "Get My Dish Scored":
            score_dish()
        elif choice == "Exit":
            break
        
        console.print("\n")


if __name__ == "__main__":
    cooking_challenges_main()
