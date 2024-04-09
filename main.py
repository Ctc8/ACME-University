from flask import Flask, request, render_template, redirect, url_for, flash
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

user_courses = db.Table('user_courses',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    teacher = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    students = db.relationship('User', secondary=user_courses, backref=db.backref('courses', lazy='dynamic'))

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
admin.add_view(AdminModelView(Course, db.session))

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
    
    all_courses = Course.query.all()
    available_courses_info = [{
        'id': course.id,
        'name': course.name,
        'teacher': course.teacher,
        'time': course.time,
        'student_count': len(course.students),
        'capacity': course.capacity
    } for course in all_courses if course not in current_user.courses]

    enrolled_courses_info = [{
        'id': course.id,
        'name': course.name,
        'teacher': course.teacher,
        'time': course.time,
        'student_count': len(course.students),
        'capacity': course.capacity
    } for course in current_user.courses]
    
    return render_template('dashboard.html', user=current_user, 
                           available_courses=available_courses_info, 
                           courses_info=enrolled_courses_info)

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

@app.route('/enroll_course/<int:course_id>', methods=['POST'])
@login_required
def enroll_course(course_id):
    course = Course.query.get(course_id)
    if course and not course in current_user.courses:
        if len(course.students) < course.capacity:
            current_user.courses.append(course)
            db.session.commit()
            flash('You have been enrolled in the course.', 'success')
        else:
            flash('This course is already at full capacity.', 'error')
    else:
        flash('Course not found or already enrolled.', 'error')
    return redirect(url_for('dashboard'))


if __name__ == "__main__":
  app.run(debug=True, port=5001)
  with app.app_context():
    ahepworth_user = User.query.filter_by(username='ahepworth').first()
    if ahepworth_user:
      ahepworth_user.is_admin = True
      db.session.commit()
  app.run(debug=True, port=5001)
