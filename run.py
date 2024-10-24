import os
from app import create_app

# initialize the app
app = create_app()


def main():
    host = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_RUN_PORT", 5000))
    app.run(host=host, port=port, debug=True)


if __name__ == "__main__":
    main()
