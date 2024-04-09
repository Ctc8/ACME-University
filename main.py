
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, UserMixin, login_required, current_user, logout_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config['SECRET_KEY'] = "secretkey"
app.config['LOGIN_VIEW'] = 'login'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(30), unique=True) 
  password = db.Column(db.String(30))  
  is_admin = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

admin = Admin(app, name='Admin', template_mode='bootstrap3')
admin.add_view(AdminModelView(User, db.session))

@app.route('/')
def home():
  return render_template('login.html', user=current_user)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
       return redirect(url_for('admin.index'))
    return render_template('dashboard.html', user=current_user)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user:
            error = 'Username is already taken'
            return render_template('signup.html', error=error)

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('dashboard'))

    return render_template('signup.html')

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.password == password:  
      login_user(user)
      return redirect(url_for('dashboard'))

    error = 'Invalid username or password'

  signup_url = url_for('signup')
  return render_template('login.html', error=error, signup_url=signup_url)

if __name__ == "__main__":
  app.run(debug=True, port=5001)
  with app.app_context():
    ahepworth_user = User.query.filter_by(username='ahepworth').first()
    if ahepworth_user:
      ahepworth_user.is_admin = True
      db.session.commit()
  app.run(debug=True, port=5001)
