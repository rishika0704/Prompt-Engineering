import streamlit as st

# Assuming these are custom modules for processing prompts
from classification import PromptClassifier
from keywordExtraction import KeywordExtractor
from webScraping import WikipediaScraper
from refinement import PromptRefiner

# Define the function to process the user prompt
def process_prompt(user_prompt):
    # Initialize instances of the required classes
    classifier = PromptClassifier()
    extractor = KeywordExtractor()
    scraper = WikipediaScraper()
    refiner = PromptRefiner()

    # Step 1: Classify the prompt to determine its type
    classification = classifier.classify_prompt(user_prompt)
    
    # Step 2: Extract keywords from the user prompt
    keywords = extractor.extract_keywords(user_prompt)
    
    # Step 3: If keywords were extracted, find related terms from Wikipedia
    if keywords:
        related_terms = scraper.get_keywords_for_all(keywords)
    else:
        related_terms = []  # If no keywords, set related_terms to an empty list
    
    # Step 4: Generate a refined prompt based on classification, keywords, and related terms
    refined_prompt = refiner.generate_refined_prompt(user_prompt, classification, keywords, related_terms)
    
    # Step 5: Send the original prompt and keywords to the Gemini API for further refinement
    gemini_refined_prompt = refiner.send_to_gemini(user_prompt, keywords)
    
    # Return both refined prompts
    return {'manual': refined_prompt, 'gemini': gemini_refined_prompt}

# Streamlit app definition
def main():
    # Set the page configuration and theme
    st.set_page_config(page_title="Prompt Engineering", page_icon="🤖", layout="centered", initial_sidebar_state="collapsed")

    # Apply a dark theme to the app
    st.markdown(
        """
        <style>
        body {
            color: #fff;
            background-color: #1e1e1e;
        }
        .stButton button {
            color: #fff;
            background-color: #333;
            border-color: #444;
        }
        .text_area {
            max-width: 100%;  /* Adjust to desired width */
            overflow: auto;    /* Enable scrolling if content is too large */
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Display the title of the app
    st.title("Prompt Engineering")

    # Input box for the user to enter their prompt
    user_prompt = st.text_input("Enter your prompt:", "")

    # Process the prompt if it's not empty
    if user_prompt:
        # Call the process_prompt function to get refined prompts
        refined_prompts = process_prompt(user_prompt)

        # Display the first refined prompt with a copy button
        st.subheader("Refined prompt 1:")
        st.text_area("Manual Refined Prompt:", refined_prompts['manual'], height=150, key="manual_prompt")

        # Copy button for Refined Prompt 1
        if st.button("Copy Refined Prompt 1"):
            st.write(f"Copied: {refined_prompts['manual']}")
            st.experimental_clipboard(refined_prompts['manual'])

        # Display the second refined prompt with a copy button
        st.subheader("Refined prompt 2:")
        st.text_area("Gemini Refined Prompt:", refined_prompts['gemini'], height=150, key="gemini_prompt")

        # Copy button for Refined Prompt 2
        if st.button("Copy Refined Prompt 2"):
            st.write(f"Copied: {refined_prompts['gemini']}")
            st.experimental_clipboard(refined_prompts['gemini'])

# Run the app
if __name__ == "__main__":
    main()
