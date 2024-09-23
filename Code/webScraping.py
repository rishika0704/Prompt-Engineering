import wikipediaapi
from bs4 import BeautifulSoup
import requests

class WikipediaScraper:
    @staticmethod
    def get_wikipedia_url(keyword):
        """
        Fetch the Wikipedia URL for a given keyword using the Wikipedia API.
        
        Args:
            keyword (str): The keyword to search for on Wikipedia.
            
        Returns:
            str: The full URL of the Wikipedia page, or None if the page does not exist.
        """
        # Create a Wikipedia API object for the English language
        wiki_wiki = wikipediaapi.Wikipedia("MyProject", 'en')
        # Fetch the Wikipedia page for the given keyword
        page = wiki_wiki.page(keyword)

        # Check if the page exists
        if page.exists():
            return page.fullurl  # Return the full URL of the page
        else:
            return None  # Return None if the page does not exist

    @staticmethod
    def scrape_wikipedia_terms(keyword):
        """
        Scrape headings from the Wikipedia page of a given keyword.
        
        Args:
            keyword (str): The keyword to scrape from Wikipedia.
            
        Returns:
            list: A list of relevant headings from the Wikipedia page.
        """
        # Get the Wikipedia URL for the given keyword
        url = WikipediaScraper.get_wikipedia_url(keyword)

        # If no valid URL is found, return an empty list
        if url is None:
            return []

        # Fetch the page content from the URL
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all headings (h2 tags in this case)
        paragraphs = soup.find_all('h2')

        # Extract text from headings and filter out irrelevant ones
        keywords = [para.get_text() for para in paragraphs if para.get_text() not in [
            'Overview', 'Contents', 'See also', 'References', 'External links', 'Further reading'
        ]]

        return keywords  # Return the list of relevant keywords

    @staticmethod
    def get_keywords_for_all(keywords):
        """
        Find keywords for all given keywords and aggregate them into a single list.
        
        Args:
            keywords (list): A list of keywords to scrape.
            
        Returns:
            list: A combined list of unique keywords scraped from Wikipedia pages.
        """
        all_keywords = []  # Initialize a list to hold all keywords

        # Iterate over each keyword and scrape terms
        for keyword in keywords:
            scraped_keywords = WikipediaScraper.scrape_wikipedia_terms(keyword)  # Get keywords for the current keyword
            all_keywords.extend(scraped_keywords)  # Add the scraped keywords to the overall list

        # Remove duplicates by converting the list to a set and back to a list
        all_keywords = list(set(all_keywords))
        return all_keywords  # Return the aggregated list of unique keywords
