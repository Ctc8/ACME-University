from flask import Flask
from flask_cors import CORS
from flask_admin import Admin

app = Flask(__name__)
CORS(app)  

admin = Admin(app, name='My App Admin', template_mode='bootstrap3')

@app.route('/')
def get_time():
    return {
        'Name': "Name", 
        "Age": "22",
        "programming": "python"
    }
    
if __name__ == '__main__':
    app.run(debug=True)