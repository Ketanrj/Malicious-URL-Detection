from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re
import os
import whois
import socket
from urllib.parse import urlparse
from datetime import datetime

app = Flask(__name__)
CORS(app)
file_path = '../model/mnb_tfidf_model.pkl'
print("File exists:", os.path.exists(file_path))

file_path = '../model/tfidf_vectorizer.pkl'
print("File exists:", os.path.exists(file_path))

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

def normalize_url(url):
    """ Normalize URL by removing protocol and 'www.' """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith('www.'):
        domain = domain[4:]  # Remove 'www.'
    return domain + parsed_url.path  # Keep path if necessary


##Get Domain related Information
def get_domain_info(url):
    try:
        # Ensure URL has a protocol
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        
        print(f"Attempting WHOIS lookup for domain: {domain}")
        w = whois.whois(domain)
        
        if not w or not any([w.creation_date, w.registrar, w.whois_server]):
            print(f"Insufficient WHOIS data for domain: {domain}")
            raise Exception("Incomplete WHOIS data")

        # Handle IP address lookup
        try:
            ip = socket.gethostbyname(domain)
        except socket.gaierror as e:
            print(f"IP lookup failed: {str(e)}")
            ip = "Unknown"

        # Handle creation date - could be list or single date
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        formatted_date = creation_date.strftime("%Y-%m-%d") if creation_date else "Unknown"

        # Handle status codes
        status = w.status if w.status else []
        if isinstance(status, str):
            status = [status]
        status_str = status[0] if status else "Unknown"

        # Handle registrar
        registrar = w.registrar if w.registrar else "Unknown"
        if isinstance(registrar, list):
            registrar = registrar[0]

        # Handle country
        country = w.country if w.country else "Unknown"
        if isinstance(country, list):
            country = country[0]

        result = {
            'domain_registration': formatted_date,
            'domain_information': {
                'registrar': registrar,
                'whois_server': w.whois_server if w.whois_server else "Unknown",
                'status': status_str
            },
            'ip_address': ip,
            'server_location': country,
            'city': w.city[0] if isinstance(w.city, list) and w.city else w.city if hasattr(w, 'city') and w.city else "Unknown",
            'region': w.state[0] if isinstance(w.state, list) and w.state else w.state if hasattr(w, 'state') and w.state else "Unknown"
        }

        print(f"Successfully retrieved domain info for: {domain}")
        print(f"Domain info: {result}")
        return result

    except whois.parser.PywhoisError as e:
        print(f"WHOIS lookup error for {domain}: {str(e)}")
        return get_unknown_response()
    except Exception as e:
        print(f"Unexpected error getting domain info: {str(e)}")
        return get_unknown_response()

def get_unknown_response():
    """Helper function to return unknown values"""
    return {
        'domain_registration': "Unknown",
        'domain_information': {
            'registrar': "Unknown",
            'whois_server': "Unknown",
            'status': "Unknown"
        },
        'ip_address': "Unknown",
        'server_location': "Unknown",
        'city': "Unknown",
        'region': "Unknown"
    }

# Load the model and vectorizer
try:
    print("Loading model and vectorizer...")
    model = joblib.load('../model/mnb_tfidf_model.pkl')
    vectorizer = joblib.load('../model/tfidf_vectorizer.pkl')
    print("Model loaded successfully")
    # Test prediction with a known URL
    test_url = "https://yegshfgsa.weebly.com/"
    test_vector = vectorizer.transform([test_url])
    test_prediction = model.predict(test_vector)[0]
    print(f"Test prediction for known malicious URL: {test_prediction}")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    raise

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        raw_url = data['url']
        
        # Normalize the URL before prediction
        normalized_url = normalize_url(raw_url)

        # Get model prediction
        url_vector = vectorizer.transform([normalized_url])  # Use normalized URL
        prediction = model.predict(url_vector)[0]  # 'bad' or 'good'
        probability = model.predict_proba(url_vector)[0].max()

        # Get domain information
        domain_info = get_domain_info(raw_url)

        # Format detection status
        detection_status = "Malicious" if prediction == "bad" else "Safe"
        confidence_percentage = f"{probability * 100:.2f}%"

        return jsonify({
            'website_address': raw_url,
            'last_analysis': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'detection_counts': detection_status,
            'confidence': confidence_percentage,
            'raw_prediction': prediction,
            **domain_info
        })
    except Exception as e:
        print(f"Error in prediction: {str(e)}")  # Debug logging
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)