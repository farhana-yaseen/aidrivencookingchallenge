import questionary
from rich.console import Console

from features.recipe_generator.generator import recipe_generator_main
from features.meal_planner.planner import meal_planner_main
from features.cooking_tutor.tutor import cooking_tutor_main
from features.flavor_pairing.pairing import flavor_pairing_main
from features.health_analyzer.analyzer import health_analyzer_main
from features.cooking_challenges.challenges import cooking_challenges_main

def kitchen_companion_main():
    """
    Main entry point for the AI Kitchen Assistant CLI.
    This acts as the unified menu for all features.
    """
    console = Console()
    console.print("[bold green]Welcome to your AI Kitchen Companion![/bold green]")

    while True:
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "Generate a Recipe",
                "Plan Weekly Meals",
                "Get Cooking Guidance",
                "Find Flavor Pairings",
                "Analyze Recipe Health",
                "Start a Cooking Challenge",
                "Exit"
            ]
        ).ask()

        if choice == "Generate a Recipe":
            recipe_generator_main()
        elif choice == "Plan Weekly Meals":
            meal_planner_main()
        elif choice == "Get Cooking Guidance":
            cooking_tutor_main()
        elif choice == "Find Flavor Pairings":
            flavor_pairing_main()
        elif choice == "Analyze Recipe Health":
            health_analyzer_main()
        elif choice == "Start a Cooking Challenge":
            cooking_challenges_main()
        elif choice == "Exit":
            console.print("[bold blue]Goodbye! Happy cooking![/bold blue]")
            break
        
        console.print("\n")

if __name__ == "__main__":
    kitchen_companion_main()
