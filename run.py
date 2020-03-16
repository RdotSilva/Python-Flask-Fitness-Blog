from fitnessblog import app

# Run in debug mode, avoiding the use of ENV variable with the flask run command
if __name__ == "__main__":
    app.run(debug=True)
