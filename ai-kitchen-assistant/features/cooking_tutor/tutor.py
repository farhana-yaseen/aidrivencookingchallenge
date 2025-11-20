import questionary
from rich.console import Console
from rich.panel import Panel
import time

console = Console()

# Sample recipe with tips
SAMPLE_RECIPE = {
    "title": "Classic Spaghetti Bolognese",
    "servings": 4,
    "ingredients": {
        "spaghetti": "400g",
        "ground beef": "500g",
        "onion": "1 large",
        "canned tomatoes": "800g",
        "olive oil": "2 tbsp",
    },
    "instructions": [
        {"step": "Finely chop the onion.", "tip": "For less tearing, chill the onion for 30 minutes before chopping."},
        {"step": "Heat olive oil in a large pan over medium heat.", "tip": "Use a heavy-bottomed pan for even heat distribution."},
        {"step": "Add the ground beef and cook until browned, breaking it up with a spoon.", "tip": "Don't overcrowd the pan; cook in batches if necessary for a better brown sear."},
        {"step": "Add the chopped onion and cook until softened.", "tip": "Cook until translucent, not browned, for a sweeter flavor."},
        {"step": "Pour in the canned tomatoes, bring to a simmer, then lower the heat and let it simmer for at least 20 minutes.", "tip": "The longer it simmers, the richer the flavor. Add a splash of red wine if you have it!"},
        {"step": "Meanwhile, cook spaghetti according to package directions.", "tip": "Salt the water generously! It should taste like the sea."},
        {"step": "Serve the bolognese sauce over the spaghetti.", "tip": "Garnish with fresh basil or parmesan cheese for an extra touch."}
    ]
}

def cooking_tutor_main(recipe=None):
    """
    Provides step-by-step cooking instructions for a given recipe.
    
    Args:
        recipe (dict, optional): A recipe dictionary. If None, a sample is used.
    """
    if recipe is None:
        recipe = SAMPLE_RECIPE

    console.print(Panel(
        f"[bold cyan]Let's start cooking: {recipe['title']}[/bold cyan]\n"
        "[italic]We will go through the instructions step by step.[/italic]",
        expand=False
    ))
    
    instructions = recipe.get("instructions", [])
    if not instructions:
        console.print("[red]No instructions found for this recipe.[/red]")
        return

    num_steps = len(instructions)
    for i, instruction in enumerate(instructions):
        step_text = instruction.get("step", "No instruction text.")
        tip_text = instruction.get("tip")

        console.print(Panel(
            f"[bold]Step {i+1}/{num_steps}:[/bold]\n{step_text}",
            title="[green]Instruction[/green]"
        ))

        if tip_text:
            console.print(f"[yellow]💡 Pro Tip:[/] [italic]{tip_text}[/italic]")

        # Mock voice guidance
        console.print("[dim](Voice guidance would read the step aloud here)[/dim]")

        # Countdown timer simulation for timed steps
        if "minute" in step_text:
            try:
                minutes = int(''.join(filter(str.isdigit, step_text.split("minute")[0])))
                console.print(f"[cyan]Starting a {minutes}-minute timer...[/cyan]")
                # for second in range(minutes * 60, 0, -1):
                #     time.sleep(1) # In a real app, this would be non-blocking
                console.print(f"[green]Timer finished for: {step_text}[/green]")
            except (ValueError, IndexError):
                pass # No valid time found


        if i < num_steps - 1:
            if not questionary.confirm("Ready for the next step?", default=True).ask():
                console.print("[yellow]Pausing cooking session. See you next time![/yellow]")
                return
    
    console.print(Panel(
        "[bold green]🎉 You've completed the recipe! Enjoy your meal! 🎉[/bold green]",
        expand=False
    ))


if __name__ == "__main__":
    cooking_tutor_main()
