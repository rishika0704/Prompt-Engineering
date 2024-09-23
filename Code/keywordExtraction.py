import nltk
nltk.download('punkt_tab')

from rake_nltk import Rake  # Import RAKE (Rapid Automatic Keyword Extraction) from nltk
from nltk.corpus import stopwords  # Import stopwords from nltk

class KeywordExtractor:
    def __init__(self):
        """
        Initialize the KeywordExtractor class.
        The Rake object is initialized with English stop words from the NLTK library.
        RAKE will use these stop words to ignore less meaningful words during keyword extraction.
        """
        # Initialize RAKE, passing in NLTK's English stop words to be ignored during extraction
        self.rake = Rake(stopwords=stopwords.words('english'))
        
    def extract_keywords(self, prompt):
        """
        Extract and filter keywords from the given prompt using the RAKE algorithm.

        Args:
            prompt (str): The text from which keywords will be extracted.

        Returns:
            list: A list of filtered keywords, excluding specific unwanted words.
        """
        # Step 1: Use RAKE to extract keywords from the input text (prompt)
        self.rake.extract_keywords_from_text(prompt)
        
        # Step 2: Define a list of words/terms that we want to exclude from the final keywords
        filter_words = ["explain", "describe", "define", "definition", "difference"]
        
        # Step 3: Get the ranked phrases extracted by RAKE
        # These are keywords or phrases ranked by importance
        keywords = self.rake.get_ranked_phrases()

        # Step 4: Filter out any keywords that contain the unwanted words (from the filter_words list)
        # This loop checks each keyword (kw) to see if any word from filter_words appears in it
        filtered_keywords = [kw for kw in keywords if not any(fw in kw.lower() for fw in filter_words)]

        # Step 5: Return the filtered list of keywords
        return filtered_keywords
