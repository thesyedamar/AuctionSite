from flask import Flask, request
from flask_ngrok import run_with_ngrok
import requests
import threading
import time

app = Flask(__name__)
run_with_ngrok(app)

# Django server URL
DJANGO_URL = "http://localhost:8080"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    """Proxy all requests to Django server"""
    url = f"{DJANGO_URL}/{path}"
    if request.query_string:
        url += f"?{request.query_string.decode()}"
    
    # Forward the request to Django
    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers={key: value for key, value in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )
        
        return response.content, response.status_code, response.headers.items()
    except Exception as e:
        return f"Error connecting to Django server: {str(e)}", 500

if __name__ == '__main__':
    print("Starting tunnel server...")
    app.run()
