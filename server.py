from flask_app.controllers import users_controllers, bulls_controllers, weather_controllers
from flask_app import app

if __name__=="__main__":
    app.run(debug=True, port= 5001)