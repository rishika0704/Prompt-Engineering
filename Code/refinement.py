import google.generativeai as genai
import requests 

class PromptRefiner:
    def __init__(self):
        # Configure the Google Generative AI with the provided API key
        genai.configure(api_key="AIzaSyD0O-LCb0wL4Q7ESz13IM_gXfNaYuxm_yw")

    def generate_refined_prompt(self, prompt, classification, keywords, related_terms):
        """
        Generate a refined prompt based on the classification, keywords, and related terms.

        Args:
            prompt (str): The initial user prompt.
            classification (str): The classification of the prompt (e.g., description, explanation).
            keywords (list): List of extracted keywords.
            related_terms (list): List of related terms from Wikipedia.

        Returns:
            str: A refined prompt.
        """
        # Join all keywords into a string for use in the prompt
        all_keywords = ', '.join(keywords)

        if len(related_terms) == 0:
            # Generate prompts based on classification without related terms
            if classification == "description":
                return f"Can you describe in detail {all_keywords}?"
            elif classification == "explanation":
                return f"Can you explain how {all_keywords} work?"
            elif classification == "definition":
                return f"Please provide clear definitions of {all_keywords}."
            elif classification == "comparison":
                return f"Can you compare {all_keywords}?"
        else:
            # Generate prompts based on classification with related terms
            if classification == "description":
                return f"Can you describe in detail {all_keywords} and their related terms: {', '.join(related_terms)}?"
            elif classification == "explanation":
                return f"Can you explain how {all_keywords} work and their relationships to {', '.join(related_terms)}?"
            elif classification == "definition":
                return f"Please provide clear definitions of {all_keywords}, including {', '.join(related_terms)}."
            elif classification == "comparison":
                return f"Can you compare {all_keywords} with {', '.join(related_terms)}?"

    def send_to_gemini(self, initial_prompt, extracted_keywords):
        """
        Send the initial prompt and extracted keywords to the Gemini API for refinement.

        Args:
            initial_prompt (str): The initial user prompt.
            extracted_keywords (list): The list of keywords extracted from the prompt.

        Returns:
            str: The refined prompt received from the Gemini API or an error message.
        """
        try:
            # Initialize the Gemini model
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(f"""You are a prompt engineer; your task is to refine and enhance the initial prompt so that the output of the refined prompt should be better while staying true to the intent of the initial prompt. Use the important keywords to refine the initial prompt. 
                                                initial_prompt = {initial_prompt}
                                                extracted_keywords = {extracted_keywords}
                                                refined_prompt =""")
            return response.text
        except requests.exceptions.RequestException as e:
            # Handle API call errors
            return "Error occurred while contacting the Gemini API."
