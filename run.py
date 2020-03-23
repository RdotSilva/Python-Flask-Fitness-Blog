from fitnessblog import create_app, db

# Create a new app instance
app = create_app()

# Add this in to recreate the database. Comment out once database is created
app_ctx = app.app_context()
app_ctx.push()
db.create_all()
app_ctx.pop()

# Run in debug mode, avoiding the use of ENV variable with the flask run command
if __name__ == "__main__":
    app.run(debug=True)
