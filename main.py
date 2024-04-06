from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
  return "<html><body><h1>BITCH FUCK U</h1></body></html>"

@app.route('/page')
def page():
  return "this is another page"

@app.route('/page/<name>')
def name(name):
  return "HEllo there %s!" % name


 
if __name__ == '__main__':
  app.run()