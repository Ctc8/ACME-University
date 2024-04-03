from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

@app.route('/')
def get_time():
    return {
        'Name': "Name", 
        "Age": "22",
        "programming": "python"
    }
    
if __name__ == '__main__':
    app.run(debug=True)