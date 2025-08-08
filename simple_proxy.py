from flask import Flask, request, Response
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Django server URL (this will be your local server)
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
        
        return Response(response.content, response.status_code, response.headers.items())
    except Exception as e:
        return f"Error connecting to Django server: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
