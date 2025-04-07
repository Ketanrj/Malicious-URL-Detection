import joblib, re

def tokenizer(url):
  """Separates feature words from the raw data
  Keyword arguments:
    url ---- The full URL

  :Returns -- The tokenized words; returned as a list
  """

  # Split by slash (/) and dash (-)
  tokens = re.split('[/-]', url)

  for i in tokens:
    # Include the splits extensions and subdomains
    if i.find(".") >= 0:
      dot_split = i.split('.')

      # Remove .com and www. since they're too common
      if "com" in dot_split:
        dot_split.remove("com")
      if "www" in dot_split:
        dot_split.remove("www")

      tokens += dot_split

  return tokens


import re

def _tokenizer(url):
    """Separates feature words from the raw data
    Keyword arguments:
      url ---- The full URL

    :Returns -- The tokenized words; returned as a list
    """

    # Common words to remove
    common_words = {"www", "com", "net", "org", "io", "co", "uk", "https", "http", "ftp"}

    # Convert URL to lowercase for case insensitivity
    url = url.lower()

    # Remove protocol and fragments
    url = re.sub(r'^https?:\/\/|ftp:\/\/', '', url)  # Remove protocol
    url = re.sub(r'\?.*|#.*', '', url)  # Remove query parameters and fragments

    # Tokenize using regex to extract meaningful parts
    tokens = re.findall(r'[a-zA-Z0-9]+', url)  # Extract alphanumeric parts

    # Remove common words
    tokens = [token for token in tokens if token not in common_words]

    return tokens



def predict_url(url, model, vectorizer):
    # Tokenize and vectorize the URL
    url_vector = vectorizer.transform([url])
    # Predict
    prediction = model.predict(url_vector)[0]
    probability = model.predict_proba(url_vector)[0].max()
    return prediction, probability


# Example usage:
test_url = "https://apify-uploads-prod.s3.us-east-1.amazonaws.com/cp8pPgPdDeqgsGPC..."
model = joblib.load('model/mnb_tfidf_model.pkl')
vectorizer = joblib.load('model/tfidf_vectorizer.pkl')
prediction, confidence = predict_url(test_url, model, vectorizer)
print(f"Prediction: {prediction}, Confidence: {confidence:.2f}")