from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline


class MyEmotionAnalyzer:
    """Load a pre-trained emotion classification model using transformers API.
    """

    def __init__(self, model_name="j-hartmann/emotion-english-distilroberta-base"):
        """Load the model given a name. If no name is provided, a default pre-trained emotion classification model is loaded.

        Args:
            model_name (str, optional): the name of the model to load from transformers API. Defaults to "j-hartmann/emotion-english-distilroberta-base".
        """
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.classifier = pipeline(
            task="sentiment-analysis", model=model, tokenizer=tokenizer)

    def get_emotion(self, text):
        """Return a string label representing the emotion found by the model reading a given text

        Args:
            text (string): A string containing a message (usually a sentence)

        Returns:
            string: the emotion extracted by the model reading the text. 
            The default classifier has 7 labels (emotions): [anger, disgust, fear, , joy, neutral, sadness, surprise]
        """
        return self.classifier(text)[0]['label']
