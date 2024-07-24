from app import create_app

# initialize the app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
