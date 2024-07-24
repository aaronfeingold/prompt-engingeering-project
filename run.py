from app import create_app

# initialize the app
app = create_app()


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
