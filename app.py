from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import User, Feedback, connect_db, db
from forms import RegisterUserForm, LoginForm, FeedbackForm
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///feedback_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config["SECRET_KEY"] = "54321secret"

toolbar = DebugToolbarExtension(app)

connect_db(app)

db.create_all()

@app.route('/')
def homepage():
    if 'username' not in session:
        return redirect('login')
    else:
        return redirect(f'/users/{session["username"]}')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, pwd, email, first_name, last_name)
    
        db.session.add(new_user)
        db.session.commit()

        session['username'] = new_user.username

        return redirect(f'/users/{session["username"]}')

    else:
        if 'username' in session:
            flash("You already logged in", 'secondary')
            return redirect("/")
        return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if "username" in session:
        flash("You already logged in", 'secondary')
        return redirect("/")
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        user = User.authenticate(username, pwd)

        if user:
            session['username'] = user.username
            return redirect(f'/users/{session["username"]}')
        
        else:
            form.username.errors = ['invalid username or password']
            flash('Invalid username or password combination', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username')
    flash('Logged out successfully', 'success')
    return redirect('/')
        


@app.route('/users/<username>')
def user_details(username):
    if 'username' not in session:
        flash("You must be logged in", "warning")
        return redirect('/login')
        
    else:
        user = User.query.filter_by(username=username).first_or_404()
        return render_template("user.html", user=user)

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if 'username' not in session:
        flash('Please login first', 'warning')
        return redirect('/')

    user = User.query.filter_by(username=username).first_or_404()
    if session['username'] == user.username:
        session.pop('username')
        db.session.delete(user)
        db.session.commit()

        flash('User Deleted','success')
        return redirect('/')
    flash("You don't have permission to do that", "warning")
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    if 'username' not in session:
        flash('Please login first', 'warning')
        return redirect('/')
    user = User.query.filter_by(username=username).first_or_404()
    feedback = Feedback()
    form = FeedbackForm()
    if session['username'] == user.username:
        if form.validate_on_submit():
            form.populate_obj(feedback)
            feedback.username = session['username']
            db.session.add(feedback)
            db.session.commit()
            flash("Feedback Created", 'success')
            return redirect(f'/users/{session["username"]}')

        return render_template('feedback-form.html', form=form)

    flash("You don't have permission to do that", "warning")
    return redirect('/')

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    if 'username' not in session:
        flash('Please login first', 'warning')
        return redirect('/')
    
    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)
    if session['username'] == feedback.username:

        if form.validate_on_submit():
            form.populate_obj(feedback)
            db.session.commit()
            flash('Feedback Updated', 'success')
            return redirect(f'/users/{session["username"]}')
        return render_template('update-feedback.html', form=form)
    
    flash("You don't have permission to do that", "warning")
    return redirect('/')

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    if 'username' not in session:
        flash('Please login first', 'warning')
        return redirect('/')
    
    feedback = Feedback.query.get_or_404(feedback_id)

    if session['username'] == feedback.username:
        db.session.delete(feedback)
        db.session.commit()
        flash('Feedback successfully deleted', 'success')
        return redirect(f'/users/{session["username"]}')
    
    flash("You don't have permission to do that", "warning")
    return redirect('/')