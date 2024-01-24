from flask import Flask, render_template, redirect, session, flash
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
############################################################
from forms import Registration, Login, FeedbackForm, DeleteForm


app=Flask(__name__)
app.app_context().push()
migrate = Migrate(app, db)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///authentication'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

toolbar=DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def go_to_registrationPage():
    return redirect ('/register')


@app.route('/register')
def register():
    form=Registration()
    return render_template('register.html', form=form)



@app.route('/register_user', methods=['POST'])
def register_user():
    # if "username" in session:
    #     return redirect(f"/users/{session['username']}")
    form=Registration()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        email=form.email.data
        first_name=form.first_name.data
        last_name=form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template("users/register.html", form=form)
        #     new_user=User.authenticate(username, password, email, first_name, last_name)
    #     db.session.add(new_user)
    #     db.session.commit()
    #     session['username'] = new_user.username
    #     target_url = f'/users/{username}'
    #     return redirect(target_url)
    #     # return redirect('/users/<username>')
    
    # else:
    #     return render_template('register.html', form=form)
    

    
@app.route('/login')
def go_to_login_page():
    form=Login()
    return render_template('login.html', form=form)
    


@app.route('/login_user', methods=['POST'])
def login_user():
    form=Login()
    if form.validate_on_submit():
        username=form.username.data
        pwd=form.password.data

        user=User.login(username, pwd)
        if user:
            session['username'] = user.username
            target_url = f'/users/{username}'
            return redirect(target_url)
    
        else:
            form.username.errors = ['invalid name or password']
            return render_template('login.html', form=form)
    else:
        return redirect('/secret')
    
    
@app.route('/users/<username>')
def show_user_info(username):
    if username != session['username']:
        # flash("Please login first!", "danger")
        return redirect('/login')
#############################################################
    user=User.query.get(username)
    return render_template('user.html', user=user)


@app.route('/secret')
def after_registering():
    return "You made it!"


@app.route('/logout')
def clear_session_info():
##################################################
    session.pop('username')
    return redirect('/login')


@app.route('/users/<username>/feedback/add')
def go_to_add_feedback_page(username):
#######################################################
    
    if username != session['username']:
        return redirect('/login')

    form=FeedbackForm()
    return render_template('feedback.html', form=form)
    

@app.route('/users/<username>/feedback/add', methods=["POST"])
def add_feedback(username):
    if username != session['username']:
        return redirect('/login')
    form=FeedbackForm()
    if form.validate_on_submit():
        title=form.title.data
        content=form.content.data
        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.username}')
    

@app.route('/feedback/<int:id>/update')
def go_to_edit_feedback(id):
    feedback=Feedback.query.get(id)
    ################################################################
    if feedback.username != session['username']:
        return redirect('/login')
    form=FeedbackForm(feedback=feedback)
    return render_template('/feedback/edit.html', feedback=feedback, form=form)



@app.route('/feedback/<int:id>/update', methods=['POST'])
def edit_feedback(id):
    ####################################################
    feedback = Feedback.query.get(id)
    ####################################################
    if feedback.username != session['username']:
        return redirect('/login')
    form = FeedbackForm(feedback=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f"/users/{feedback.username}")
    return render_template("/feedback/edit.html", form=form, feedback=feedback)
    


@app.route('/feedback/<int:id>/delete', methods=['POST'])
def delete_feedback(id):
    feedback=Feedback.query.get(id)
    ####################################################
    # form = DeleteForm()
    # form = FeedbackForm()
    # if form.validate_on_submit():
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f'/users/{feedback.username}')


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if "username" not in session or username != session['username']:
        flash("You need to register")
        return redirect('/')
    user=User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')
