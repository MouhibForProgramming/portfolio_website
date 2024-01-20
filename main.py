from flask import Flask, render_template, request, url_for, send_from_directory, redirect
from flask_wtf import FlaskForm
from wtforms.validators import Email, DataRequired
from wtforms.fields import StringField, EmailField, TextAreaField, SubmitField
from flask_bootstrap import Bootstrap5
import smtplib
import os

# initialized our flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("secret_key")
# initialize our flask bootstrap with our flask app
Bootstrap5(app)
# My Credentials
my_password = os.environ.get("my_password")
my_email = os.environ.get("my_email")


# create a contact form with flask wtforms

class ContactForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired()])
    email = EmailField(label="Email", validators=[DataRequired(), Email()])
    message = TextAreaField(label="Message", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


@app.route("/")
def home():
    contactForm = ContactForm()
    return render_template("index.html", form=contactForm)


@app.route("/upload")
def download():
    return send_from_directory(directory="static", path="file/cv.pdf")


@app.route("/contacts", methods=["GET", "POST"])
def contact():
    contactForm = ContactForm()
    print("ok")
    if contactForm.validate_on_submit():
        print("request successful")
        user_name = contactForm.name.data
        user_email = contactForm.email.data
        user_comment = contactForm.message.data
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(from_addr=user_email, to_addrs=my_email,
                                msg=f"Subject:Contact Me.I Love You\n\n I m {user_name}:{user_comment}".encode("utf-8"))
        return redirect(url_for('home'))
    return render_template("index.html",form=contactForm)


# run the program as a script not as an imported module.
if __name__ == "__main__":
    # run at the debug mode to autoload(auto-save without close and open again)
    app.run(debug=False)
