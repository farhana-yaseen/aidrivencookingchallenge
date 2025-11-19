import json
import questionary
from rich.console import Console
from rich.table import Table
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize Rich Console
console = Console()

# Initialize Gemini Client
def init_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        console.print("[bold red]Error: GEMINI_API_KEY environment variable not set.[/bold red]")
        console.print("Please set the GEMINI_API_KEY environment variable to use the AI recipe generator.")
        exit(1)
    genai.configure(api_key=api_key)

init_gemini()


def recipe_generator_cli():
    """
    Main function to run the recipe generator flow.
    """
    console.print("[bold green]Welcome to the AI Recipe Generator![/bold green]")

    # 1. Get user input
    ingredients = questionary.text("What ingredients do you have? (comma-separated)").ask()
    diet = questionary.select(
        "Any dietary preferences?",
        choices=["None", "Vegan", "Keto", "Low Sodium", "Low Carb", "Gluten-Free"]
    ).ask()
    cuisine = questionary.text("What cuisine would you like? (optional)").ask()

    # 2. Generate recipe using Gemini
    recipe = generate_ai_recipe(ingredients, diet, cuisine)

    # 3. Display recipe
    display_recipe(recipe)

    # 4. Adjust serving size
    recipe = adjust_serving_size(recipe)
    display_recipe(recipe)

    # 5. Suggest substitutions
    suggest_substitutions(recipe)

    # 6. Save recipe
    save_recipe(recipe)


# -----------------------------
#  AI RECIPE GENERATION (GEMINI)
# -----------------------------
def generate_ai_recipe(ingredients, diet, cuisine):
    console.print("\n[bold yellow]Generating a recipe for you using Gemini...[/bold yellow]\n")

    prompt = (
    "You are a helpful AI kitchen assistant. "
    "Generate a recipe in JSON format ONLY, no explanations or extra text.\n\n"
    "The JSON must have exactly these keys:\n"
    "name (string), description (string), servings (number), "
    "ingredients (list of {name, quantity}), instructions (list of strings).\n\n"
    f"Ingredients: {ingredients}\n"
    f"Dietary preference: {diet}\n"
    f"Cuisine: {cuisine if cuisine else 'Any'}\n\n"
    "Return ONLY a valid JSON object. Do not include markdown, code blocks, or extra text."
)


    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 1500
            }
        )

        recipe_text = response.text
        recipe = json.loads(recipe_text)
        return recipe

    except json.JSONDecodeError:
        console.print("[bold red]Error: Gemini did not return valid JSON. Try again.[/bold red]")
        exit(1)
    except Exception as e:
        console.print(f"[bold red]Gemini API Error: {e}[/bold red]")
        exit(1)


# -----------------------------
#  DISPLAY RECIPE
# -----------------------------
def display_recipe(recipe):
    console.print(f"[bold cyan]Recipe: {recipe['name']}[/bold cyan]")
    console.print(f"[italic]{recipe['description']}[/italic]")
    console.print(f"Servings: {recipe['servings']}")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Ingredient", style="dim")
    table.add_column("Quantity")

    for ingredient in recipe['ingredients']:
        table.add_row(ingredient['name'], ingredient['quantity'])

    console.print(table)

    console.print("\n[bold]Instructions:[/bold]")
    for i, step in enumerate(recipe['instructions'], 1):
        console.print(f"{i}. {step}")
    console.print("\n")


# -----------------------------
#  ADJUST SERVING SIZE
# -----------------------------
def adjust_serving_size(recipe):
    try:
        new_servings_str = questionary.text(
            f"This recipe serves {recipe['servings']}. How many servings would you like?"
        ).ask()

        if new_servings_str:
            new_servings = int(new_servings_str)
            if new_servings != recipe['servings']:
                ratio = new_servings / recipe['servings']

                for ingredient in recipe['ingredients']:
                    try:
                        quantity_parts = ingredient['quantity'].split()
                        if len(quantity_parts) == 2 and quantity_parts[0].replace('.', '', 1).isdigit():
                            original_amount = float(quantity_parts[0])
                            new_amount = original_amount * ratio
                            ingredient['quantity'] = f"{new_amount:.2f} {quantity_parts[1]}"
                    except:
                        pass

                recipe['servings'] = new_servings
                console.print(f"\n[bold green]Recipe adjusted to {new_servings} servings.[/bold green]")

    except:
        console.print("[bold red]Invalid input for servings.[/bold red]")

    return recipe


# -----------------------------
#  SUBSTITUTION SUGGESTIONS
# -----------------------------
def suggest_substitutions(recipe):
    if questionary.confirm("Would you like to see ingredient substitutions?").ask():
        console.print("\n[bold yellow]Generating substitution suggestions with Gemini...[/bold yellow]")

        model = genai.GenerativeModel("gemini-pro")

        for ingredient in recipe['ingredients']:
            prompt = (
                f"Suggest common kitchen substitutions for the ingredient "
                f"'{ingredient['name']}' used in a recipe called '{recipe['name']}'. "
                "Provide a comma-separated list (no JSON)."
            )

            try:
                response = model.generate_content(prompt)
                substitutions = response.text.strip()
                console.print(f"- For [bold]{ingredient['name']}[/bold], try: {substitutions}")

            except Exception as e:
                console.print(f"[bold red]Error generating suggestions: {e}[/bold red]")

        console.print("\n")


# -----------------------------
#  SAVE RECIPE
# -----------------------------
def save_recipe(recipe):
    if questionary.confirm("Save this recipe?").ask():
        path = 'ai-kitchen-assistant/database/recipes.json'

        try:
            with open(path, 'r+') as f:
                try:
                    recipes = json.load(f)
                except json.JSONDecodeError:
                    recipes = []

                recipes.append(recipe)
                f.seek(0)
                json.dump(recipes, f, indent=4)

            console.print("[bold green]Recipe saved successfully![/bold green]")

        except FileNotFoundError:
            with open(path, 'w') as f:
                json.dump([recipe], f, indent=4)
            console.print("[bold green]Recipe saved successfully![/bold green]")


# -----------------------------
#  ENTRY POINT
# -----------------------------
if __name__ == '__main__':
    recipe_generator_cli()




















































# import json
# import questionary
# from rich.console import Console
# from rich.table import Table
# import openai
# import os

# # Initialize Rich Console
# console = Console()

# # Initialize OpenAI Client
# def get_openai_client():
#     api_key = os.getenv("OPENAI_API_KEY")
#     if not api_key:
#         console.print("[bold red]Error: OPENAI_API_KEY environment variable not set.[/bold red]")
#         console.print("Please set the OPENAI_API_KEY environment variable to use the AI recipe generator.")
#         exit(1)
#     return openai.OpenAI(api_key=api_key)

# openai_client = get_openai_client()

# def recipe_generator_cli():
#     """
#     Main function to run the recipe generator flow.
#     """
#     console.print("[bold green]Welcome to the AI Recipe Generator![/bold green]")

#     # 1. Get user input
#     ingredients = questionary.text("What ingredients do you have? (comma-separated)").ask()
#     diet = questionary.select(
#         "Any dietary preferences?",
#         choices=["None", "Vegan", "Keto", "Low Sodium", "Low Carb", "Gluten-Free"]
#     ).ask()
#     cuisine = questionary.text("What cuisine would you like? (e.g., Italian, Mexican) (optional)").ask()

#     # 2. Generate recipe (mocked)
#     recipe = generate_ai_recipe(ingredients, diet, cuisine)

#     # 3. Display recipe
#     display_recipe(recipe)

#     # 4. Adjust serving size
#     recipe = adjust_serving_size(recipe)
#     display_recipe(recipe)

#     # 5. Suggest substitutions
#     suggest_substitutions(recipe)

#     # 6. Save recipe
#     save_recipe(recipe)

# def generate_ai_recipe(ingredients, diet, cuisine):
#     """
#     Generates a recipe using a generative AI model (OpenAI).
#     """
#     console.print("\n[bold yellow]Generating a recipe for you using AI...[/bold yellow]\n")

#     prompt_messages = [
#         {"role": "system", "content": "You are a helpful AI kitchen assistant. Generate a recipe based on the user's input. The output should be a JSON object with 'name', 'description', 'servings', 'ingredients' (list of {'name': 'item', 'quantity': 'amount'}), and 'instructions' (list of strings)."},
#         {"role": "user", "content": f"Generate a recipe with the following criteria:\nIngredients: {ingredients}\nDietary Preference: {diet}\nCuisine: {cuisine if cuisine else 'Any'}\n\nEnsure the output is a valid JSON object."}
#     ]

#     try:
#         response = openai_client.chat.completions.create(
#             model="gpt-3.5-turbo",  # Or another suitable model like "gpt-4"
#             messages=prompt_messages,
#             response_format={"type": "json_object"},
#             temperature=0.7,
#             max_tokens=1500
#         )
        
#         recipe_content = response.choices[0].message.content
#         recipe = json.loads(recipe_content)
#         return recipe
#     except openai.APIError as e:
#         console.print(f"[bold red]OpenAI API Error: {e}[/bold red]")
#         console.print("[bold red]Could not generate recipe. Please check your API key and try again.[/bold red]")
#         exit(1)
#     except json.JSONDecodeError:
#         console.print("[bold red]Error: AI did not return a valid JSON recipe. Please try again.[/bold red]")
#         exit(1)
#     except Exception as e:
#         console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
#         exit(1)

# def display_recipe(recipe):
#     """
#     Displays the recipe in a formatted table.
#     """
#     console.print(f"[bold cyan]Recipe: {recipe['name']}[/bold cyan]")
#     console.print(f"[italic]{recipe['description']}[/italic]")
#     console.print(f"Servings: {recipe['servings']}")

#     table = Table(show_header=True, header_style="bold magenta")
#     table.add_column("Ingredient", style="dim")
#     table.add_column("Quantity")

#     for ingredient in recipe['ingredients']:
#         table.add_row(ingredient['name'], ingredient['quantity'])

#     console.print(table)

#     console.print("\n[bold]Instructions:[/bold]")
#     for i, step in enumerate(recipe['instructions'], 1):
#         console.print(f"{i}. {step}")
#     console.print("\n")


# def adjust_serving_size(recipe):
#     """
#     Adjusts the recipe ingredients based on the desired number of servings.
#     """
#     try:
#         new_servings_str = questionary.text(f"This recipe serves {recipe['servings']}. How many servings would you like?").ask()
#         if new_servings_str:
#             new_servings = int(new_servings_str)
#             if new_servings != recipe['servings']:
#                 ratio = new_servings / recipe['servings']
#                 for ingredient in recipe['ingredients']:
#                     try:
#                         quantity_parts = ingredient['quantity'].split()
#                         if len(quantity_parts) == 2 and quantity_parts[0].replace('.', '', 1).isdigit():
#                             original_amount = float(quantity_parts[0])
#                             new_amount = original_amount * ratio
#                             ingredient['quantity'] = f"{new_amount:.2f} {quantity_parts[1]}"
#                     except (ValueError, IndexError):
#                         # Handle cases where quantity is not easily parseable, e.g., "to taste"
#                         pass
#                 recipe['servings'] = new_servings
#                 console.print(f"\n[bold green]Recipe adjusted for {new_servings} servings.[/bold green]")
#     except (ValueError, TypeError):
#         console.print("[bold red]Invalid input for servings. Sticking to the original.[/bold red]")

#     return recipe


# def suggest_substitutions(recipe):
#     """
#     Suggests substitutions for ingredients using the OpenAI API.
#     """
#     if questionary.confirm("Would you like to see some ingredient substitutions?").ask():
#         console.print("\n[bold yellow]Generating substitution suggestions using AI...[/bold yellow]")
#         for ingredient in recipe['ingredients']:
#             prompt_messages = [
#                 {"role": "system", "content": "You are a helpful AI kitchen assistant. Suggest a few common substitutions for the given ingredient, considering it's part of a recipe. Provide a comma-separated list of substitutions."},
#                 {"role": "user", "content": f"What are some substitutions for {ingredient['name']} in a recipe like {recipe['name']}?"}
#             ]
#             try:
#                 response = openai_client.chat.completions.create(
#                     model="gpt-3.5-turbo",
#                     messages=prompt_messages,
#                     temperature=0.7,
#                     max_tokens=50
#                 )
#                 substitutions = response.choices[0].message.content.strip()
#                 if substitutions:
#                     console.print(f"- For [bold]{ingredient['name']}[/bold], you could try: {substitutions}")
#             except openai.APIError as e:
#                 console.print(f"[bold red]OpenAI API Error for substitutions: {e}[/bold red]")
#                 console.print("[bold red]Could not generate substitutions. Please check your API key and try again.[/bold red]")
#             except Exception as e:
#                 console.print(f"[bold red]An unexpected error occurred while suggesting substitutions: {e}[/bold red]")
#         console.print("\n")


# def save_recipe(recipe):
#     """
#     Saves the recipe to a JSON file if the user agrees.
#     """
#     if questionary.confirm("Would you like to save this recipe?").ask():
#         try:
#             with open('ai-kitchen-assistant/database/recipes.json', 'r+') as f:
#                 try:
#                     recipes = json.load(f)
#                 except json.JSONDecodeError:
#                     recipes = []
#                 recipes.append(recipe)
#                 f.seek(0)
#                 json.dump(recipes, f, indent=4)
#             console.print("[bold green]Recipe saved successfully![/bold green]")
#         except FileNotFoundError:
#             with open('ai-kitchen-assistant/database/recipes.json', 'w') as f:
#                 json.dump([recipe], f, indent=4)
#             console.print("[bold green]Recipe saved successfully![/bold green]")


# if __name__ == '__main__':
#     recipe_generator_cli()
