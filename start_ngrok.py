from pyngrok import ngrok
import time

# Start ngrok tunnel
public_url = ngrok.connect(8080)
print(f"Public URL: {public_url}")

# Keep the tunnel open
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down tunnel...")
    ngrok.kill()
