import torch  # PyTorch library for tensor operations
from transformers import AutoTokenizer, AutoModelForSequenceClassification  # To load the tokenizer and model

class PromptClassifier:
    def __init__(self):
        """
        Initialize the classifier by loading a pre-trained tokenizer and model.
        The model is designed to classify prompts into specific categories.
        """
        # Load the pre-trained tokenizer to tokenize the input text
        self.tokenizer = AutoTokenizer.from_pretrained("rishika0704/promptClassifcation")
        
        # Load the pre-trained model for sequence classification
        self.model = AutoModelForSequenceClassification.from_pretrained("rishika0704/promptClassifcation")
        
        # Define the possible class labels corresponding to the model's output classes
        self.class_labels = ["description", "explanation", "definition", "comparison"]

    def classify_prompt(self, prompt):
        """
        Classify the input prompt into one of the predefined categories.
        
        Args:
            prompt (str): The input text or prompt that needs to be classified.

        Returns:
            str: The predicted class label for the input prompt.
        """
        # Tokenize the input prompt, converting it into tensors (inputs for the model)
        # 'return_tensors="pt"' means we want PyTorch tensors as output
        # 'padding=True' ensures inputs are padded to the same length if needed
        # 'truncation=True' ensures that longer inputs are truncated to fit the model's input size
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
        
        # Disable gradient calculation (not needed in inference) to save memory and improve speed
        with torch.no_grad():
            # Pass the tokenized input through the model to get predictions (logits)
            outputs = self.model(**inputs)
        
        # Get the raw logits (un-normalized scores) from the model's output
        logits = outputs.logits
        
        # Find the index of the highest logit, which corresponds to the predicted class
        predicted_class = torch.argmax(logits, dim=1).item()
        
        # Return the predicted class label (e.g., 'description', 'explanation', etc.)
        return self.class_labels[predicted_class]
