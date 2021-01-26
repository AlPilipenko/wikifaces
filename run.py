from wikifaces import create_app

app = create_app()


"Grab the app and run it"
if __name__ == '__main__':
    app.run(debug=True)
