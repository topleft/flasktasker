from project import app
print(app.debug)
app.run(debug=app.config['DEBUG'])
