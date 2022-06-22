from app import app
from os import getenv

if __name__ == "__main__":
    port = getenv("PORT", "5000")
    app.run(host="0.0.0.0", port=port)
