import streamlit as st

from features.recipe_generator.generator import recipe_generator_page


def kitchen_companion_main():
    """
    Main entry point for the AI Kitchen Assistant web app.
    This acts as the unified menu for all features.
    """
    st.sidebar.title("AI Kitchen Assistant")

    features = [
        "Recipe Generator",
        "Meal Planner",
        "Cooking Tutor",
        "Flavor Pairing",
        "Health Analyzer",
        "Cooking Challenges",
    ]
    selection = st.sidebar.radio("Go to", features)

    if selection == "Recipe Generator":
        recipe_generator_page()
    elif selection == "Meal Planner":
        st.write("Meal Planner is not yet implemented.")
    elif selection == "Cooking Tutor":
        st.write("Cooking Tutor is not yet implemented.")
    elif selection == "Flavor Pairing":
        st.write("Flavor Pairing is not yet implemented.")
    elif selection == "Health Analyzer":
        st.write("Health Analyzer is not yet implemented.")
    elif selection == "Cooking Challenges":
        st.write("Cooking Challenges is not yet implemented.")
