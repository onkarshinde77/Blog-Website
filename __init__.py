from flask import Flask, render_template, request,session,redirect,flash
import json
from flask_mail import Mail
import os
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.secret_key = "5390//1631\\7777"

app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_COOKIE_SECURE'] = True  # For HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True

with open("config.json",'r') as f:
    per_info = json.load(f)["per_info"]
   
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/blog_website"
db = SQLAlchemy(app)

class Contact_info(db.Model):
    Sr = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20),nullable=False)
    Mobile = db.Column(db.String(12),nullable = False)
    Email = db.Column(db.String(30),nullable=False)
    description = db.Column(db.String(50),nullable=False)
    time = db.Column(db.DateTime, server_default=db.func.now())
    
class Blogs_data(db.Model):
    Sr = db.Column(db.Integer, primary_key=True)
    image_link = db.Column(db.String(20),nullable=False)
    Heading = db.Column(db.String(12),nullable = False)
    description = db.Column(db.String(30),nullable=False)
    read_more_link = db.Column(db.String(50),nullable=False)
    Slug = db.Column(db.String(50),nullable=False)
    date = db.Column(db.DateTime, server_default=db.func.now())

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Increased for hashed passwords
    avatar = db.Column(db.String(200), nullable=True, default="static/uploads/user.png")  # Default avatar
 
class SettingsForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    avatar = FileField('Profile Picture')
 
app.config['UPLOAD_FOLDER'] = per_info["upload_location"]
# mail logic
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = per_info["email"],
    MAIL_PASSWORD = per_info["email_key"],
)

mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    post = Blogs_data.query.filter_by().all()
    return render_template("index.html",post=post)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/blogs")
def blogs():
    post = Blogs_data.query.filter_by().all()
    return render_template("blogs.html",post = post)

@app.route("/post/<string:post_slug>",methods=["GET"])
def post_method(post_slug):
    post = Blogs_data.query.filter_by(Slug=post_slug).first()
    return render_template("post.html",post=post)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect('/')
        
    if request.method == "POST":
        identifier = request.form.get("email1")
        password = request.form.get("password1")
        
        # Check admin login (now using hashed password)
        if (identifier == per_info['email']) and check_password_hash(per_info["password"],str(password)):
            admin_user = User.query.filter_by(email=per_info['email']).first()
            if admin_user:
                login_user(admin_user)
                return redirect('/admin')
            else:
                flash('Admin user not found in database.', 'danger')
            return redirect('/login')
        
        # Check regular user login
        user = User.query.filter(User.email == identifier).first()
        
        if user and check_password_hash(user.password, str(password)):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('/')
            return redirect(next_page) if next_page else redirect('/')
        else:
            flash('Login failed. Please check your credentials or sign up.', 'danger')
            return redirect('/signUp')
    
    return render_template("login.html")

    
@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        current_user.name = form.username.data
        current_user.email = form.email.data

        avatar_file = form.avatar.data
        if avatar_file:
            filename = secure_filename(avatar_file.filename)
            avatar_path = os.path.join(app.root_path, 'static/uploads', filename)
            avatar_file.save(avatar_path)
            current_user.avatar = filename

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect('/profile')

    form.username.data = current_user.name
    form.email.data = current_user.email
    return render_template('settings.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop('username', None)
    return redirect('/login')

@app.route("/signUp", methods=["GET", "POST"])
def signUp():
    if current_user.is_authenticated:
        return redirect('/')
        
    if request.method == "POST":
        email = request.form.get("email1")
        name = request.form.get('name')
        password = request.form.get('password1')
        confirm_password = request.form.get('confirm_password1')
        if password != confirm_password:
            print('Passwords do not match')
            return redirect('/signUp')
        
        if User.query.filter_by(name=name).first():
            flash('Username already exists', 'error')
            return redirect('/signUp')
            
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect('/signUp')
            
        # Add password hashing here:
        hashed_password = generate_password_hash(str(password))
        new_user = User(email=email, name=name, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please login.', 'success')
        return render_template('sign.html',display1=None,display2=True,success=None)
    
    return render_template("sign.html",display1=True,display2=None,success=None)

@app.route('/contact',methods=["GET", "POST"])
def contact():
    if request.method == "POST" :
        name = request.form.get("name")
        mobile = request.form.get("mobile")
        email = request.form.get("email")
        description = request.form.get("message")
        entry = Contact_info(Name = name,Email = email,Mobile = mobile , description = description)
        db.session.add(entry)
        db.session.commit()
        # sent to mail
        # try :
        #     mail.send_message(
        #         "New message from : " + name,
        #         sender=email,
        #         recipients=[per_info['email']],
        #         body="Message : \n" +description + "\n" + "Mobile No. : "+mobile + "\n"+email
        #     )
        # except Exception as e:
        #     print(f"An error occurred: {e}")
        return render_template("contact.html",display1=None,display2=True,success=True)
    else:
        return render_template("contact.html",display1=True,display2=None ,success = False)

@app.route("/admin",methods=["GET","POST"])
@login_required
def admin():
     # Check if current user is admin
    if not current_user.is_authenticated or current_user.email != per_info["email"]:
        flash('Admin access required', 'danger')
        return redirect('/')
    if current_user.email != per_info["email"]:
        flash('Admin access required', 'danger')
        return redirect('/')
    post = Blogs_data.query.filter_by().all()
    
    if request.method == "POST" :
        image_link = request.form.get("image_link")
        heading = request.form.get("heading")
        description = request.form.get("description")
        read_more_link = request.form.get("read_more_link")
        slug = request.form.get("slug")
        file = request.files.get('files')
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("File uploaded successfully!", "success")
        else:
            flash("Please upload a file.", "warning")
            
        if image_link and heading and description and read_more_link and slug:
            entry = Blogs_data(image_link=image_link,Heading=heading,description=description,read_more_link=read_more_link,Slug=slug)
            db.session.add(entry)
            db.session.commit()
        return render_template("admin.html",success=True,post=post)
    return render_template("admin.html",success=None,post=post)

@app.route("/edit/<string:Sr>",methods=["GET","POST"])
@login_required
def edit_post(Sr):
    if not current_user.is_authenticated or current_user.username != per_info["username"]:
        flash('Admin access required', 'danger')
        return redirect('/')
    post = Blogs_data.query.filter_by(Sr=Sr).first()
    if request.method =="POST":
        post.image_link = request.form.get("image_link")
        post.Heading = request.form.get("heading")
        post.description = request.form.get("description")
        post.read_more_link = request.form.get("read_more_link")
        post.Slug = request.form.get("slug")
        db.session.commit()
        return redirect('/edit/'+Sr)
    return render_template("edit.html",post=post,success=None)  

@app.route("/delete/<string:Sr>",methods=['GET','POST'])
def delete(Sr):
    if not current_user.is_authenticated or current_user.username != per_info["username"]:
        flash('Admin access required', 'danger')
        return redirect('/')

    post = Blogs_data.query.filter_by(Sr=Sr).first()
    db.session.delete(post)
    db.session.commit()
    return redirect("/admin")

if __name__ == '__main__':
    app.run(debug=True)