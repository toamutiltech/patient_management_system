from patient import create_app
#create the app to run on the browser
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
