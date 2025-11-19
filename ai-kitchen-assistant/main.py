import questionary
from rich.console import Console

from features.recipe_generator.generator import recipe_generator_cli
# from features.meal_planner.planner import meal_planner_cli
# from features.cooking_tutor.tutor import cooking_tutor_cli
# from features.flavor_pairing.pairing import flavor_pairing_cli
# from features.health_analyzer.analyzer import health_analyzer_cli
# from features.kitchen_companion.companion import kitchen_companion_cli
# from features.cooking_challenges.challenges import cooking_challenges_cli

console = Console()

def main():
    """
    Main entry point for the AI Kitchen Assistant CLI.
    """
    console.print("[bold green]Welcome to the AI Kitchen Assistant![/bold green]")

    while True:
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "Generate a Recipe",
                # "Plan Weekly Meals",
                # "Get Cooking Guidance",
                # "Find Flavor Pairings",
                # "Analyze Recipe Health",
                # "Use Kitchen Companion",
                # "Start Cooking Challenge",
                "Exit"
            ]
        ).ask()

        if choice == "Generate a Recipe":
            recipe_generator_cli()
        # elif choice == "Plan Weekly Meals":
        #     meal_planner_cli()
        # elif choice == "Get Cooking Guidance":
        #     cooking_tutor_cli()
        # elif choice == "Find Flavor Pairings":
        #     flavor_pairing_cli()
        # elif choice == "Analyze Recipe Health":
        #     health_analyzer_cli()
        # elif choice == "Use Kitchen Companion":
        #     kitchen_companion_cli()
        # elif choice == "Start Cooking Challenge":
        #     cooking_challenges_cli()
        elif choice == "Exit":
            console.print("[bold blue]Goodbye![/bold blue]")
            break

if __name__ == "__main__":
    main()
