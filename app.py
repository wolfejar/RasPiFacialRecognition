from flask import Flask, render_template, request, session
import viewbuilders.home_form_view_builder as home_form_view_builder
import viewbuilders.friends_form_view_builder as friends_form_view_builder
from models.time_frame_enum import TimeFrameEnum
import validators.sign_in_validator as sign_in_validator
import validators.sign_up_validator as sign_up_validator
app = Flask(__name__)
app.secret_key = 'super secret key'


@app.route('/')
@app.route('/index', methods=['GET'])
def index_get():
    return render_template('index.html')


@app.route('/index_post', methods=['POST'])
def index_post():
    # sign-in logic here
    email = request.form['email']
    password = request.form['password']
    if sign_in_validator.validate_sign_in(username=email, password=password):
        session['email'] = email
        return home_get()
    else:
        return index_get()  # change to render sign in page once mysql connected


@app.route('/sign_up_get', methods=['GET'])
def sign_up_get():
    # sign-in logic here
    return render_template('sign_up.html')


@app.route('/sign_up_post', methods=['POST'])
def sign_up_post():
    email = request.form['email']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    role = 'User'
    success = sign_up_validator.validate_sign_up(
        username=email, password=password, first_name=first_name, last_name=last_name, role=role
    )
    if success:
        return home_get()
    else:
        return sign_up_get()


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('email', None)
    return index_get()


@app.route('/home_get', methods=['GET'])
def home_get():
    home_form = home_form_view_builder.build_home_form(model_id=12345, time_frame='2009-01-28 21:00:00')
    return render_template('home.html', home_form=home_form)


@app.route('/home_post', methods=['POST'])
def home_post():
    time_frame = TimeFrameEnum(int(request.form.get('timeframe'))).name
    home_form = home_form_view_builder.build_home_form(model_id=12345, time_frame='2009-01-28 21:00:00')
    return render_template('home.html', home_form=home_form)


@app.route('/train_get', methods=['GET'])
def train_get():
    return render_template('models.html')


@app.route('/friends_get', methods=['GET'])
def friends_get():
    friends_form = friends_form_view_builder.build_friends_form(session['email'])
    return render_template('friends.html', friends_form=friends_form)


@app.route('/metrics_get', methods=['GET'])
def metrics_get():
    return render_template('metrics.html')


if __name__ == '__main__':
    app.run(debug=True)
