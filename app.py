from flask import Flask, render_template, request, redirect
import hashlib

app = Flask(__name__)

# Shorten URLs mapping
url_mapping = {}

# URL shortening function
def shorten_url(long_url):
    short_hash = hashlib.md5(long_url.encode()).hexdigest()[:6]
    return short_hash

# Display the form and process the POST request
@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    if request.method == 'POST':
        long_url = request.form.get('url-input')
        if long_url:
            if len(long_url) > 5:
                short_hash = shorten_url(long_url)
                short_url = f"http://{request.host}/{short_hash}" 
                url_mapping[short_hash] = long_url
                print(f"Mapped {short_url} to {long_url}")
            else:
                print("URL is too short or invalid.")
        else:
            print("No URL provided. Invalid input.")
    
    return render_template('index.html', short_url=short_url)

# Redirecting from shortened URL to long one
@app.route('/<short_hash>')
def redirect_to_url(short_hash):
    long_url = url_mapping.get(short_hash)
    
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404

# Route to Privacy Policy
@app.route('/privacy-policy')
def privacy_policy():
    return render_template('pp.html')

# Route to Terms of Use
@app.route('/terms-of-use')
def terms_of_use():
    return render_template('termsofuse.html')
    
# App start with debugging and access on all IPs on port 5000
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

