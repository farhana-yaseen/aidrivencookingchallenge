import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

# Mock AI pairing database
PAIRING_DATA = {
    "chicken": {
        "ingredients": ["lemon", "rosemary", "thyme", "garlic", "mushrooms", "bacon"],
        "drinks": ["Chardonnay (white wine)", "Pinot Noir (red wine)", "Light Beer"],
        "condiments": ["dijon mustard", "honey glaze", "bbq sauce"]
    },
    "beef": {
        "ingredients": ["potatoes", "onions", "carrots", "red wine", "horseradish", "blue cheese"],
        "drinks": ["Cabernet Sauvignon (red wine)", "Stout Beer", "Whiskey"],
        "condiments": ["horseradish sauce", "peppercorn sauce", "A1 sauce"]
    },
    "salmon": {
        "ingredients": ["dill", "lemon", "asparagus", "cream cheese", "capers"],
        "drinks": ["Sauvignon Blanc (white wine)", "Pinot Gris (white wine)", "Gin and Tonic"],
        "condiments": ["dill sauce", "tartar sauce", "lemon butter"]
    },
    "tofu": {
        "ingredients": ["soy sauce", "ginger", "garlic", "broccoli", "sesame oil", "chili flakes"],
        "drinks": ["Sake", "Green Tea", "Light Lager"],
        "condiments": ["peanut sauce", "sweet chili sauce", "hoisin sauce"]
    },
    "chocolate": {
        "ingredients": ["raspberries", "orange", "caramel", "sea salt", "almonds", "mint"],
        "drinks": ["Port (dessert wine)", "Coffee", "Milk"],
        "condiments": ["whipped cream", "raspberry coulis", "caramel sauce"]
    }
}


def flavor_pairing_main():
    """Main function for the Flavor Pairing AI feature."""
    console.print(Panel(
        "[bold cyan]Welcome to the Flavor Pairing AI![/bold cyan]\n"
        "Enter a main ingredient to see what pairs well with it.",
        expand=False
    ))

    while True:
        try:
            ingredient = questionary.text(
                "Enter an ingredient (or press Enter to exit):"
            ).ask()
        except KeyboardInterrupt:
            break

        if not ingredient:
            console.print("[yellow]Exiting Flavor Pairing AI. Happy cooking![/yellow]")
            break

        ingredient = ingredient.lower()
        if ingredient in PAIRING_DATA:
            pairings = PAIRING_DATA[ingredient]
            
            ingredients_text = Text("\n\n✨ Ingredient Combinations:\n", style="bold yellow")
            ingredients_text.append(", ".join(pairings["ingredients"]))

            drinks_text = Text("\n\n🍷 Beverage Pairings:\n", style="bold blue")
            drinks_text.append(", ".join(pairings["drinks"]))

            condiments_text = Text("\n\n🌶️ Spice & Condiment Pairings:\n", style="bold red")
            condiments_text.append(", ".join(pairings["condiments"]))

            console.print(Panel(
                Text.from_markup(f"[bold]Pairings for [u]{ingredient.capitalize()}[/u]:[/bold]\n") +
                ingredients_text +
                drinks_text + 
                condiments_text,
                title="[green]Flavor Profile[/green]"
            ))
        else:
            console.print(Panel(
                f"[red]Sorry, I don't have pairing data for '{ingredient}'.[/red]\n"
                f"Available ingredients are: {', '.join(PAIRING_DATA.keys())}",
                title="[red]Not Found[/red]"
            ))
        
        console.print("\n")


if __name__ == "__main__":
    flavor_pairing_main()
