from flask import Flask, render_template, request, session
import viewbuilders.home_form_view_builder as home_form_view_builder
from models.time_frame_enum import TimeFrameEnum
import validators.sign_in_validator as sign_in_validator
app = Flask(__name__)


@app.route('/')
@app.route('/index', methods=['GET'])
def index_get():
    return render_template('index.html')


@app.route('/index_post', methods=['POST'])
def index_post():
    # sign-in logic here
    email = request.form['email']
    password = request.form['password']
    success = sign_in_validator.validate_sign_in(username=email, password=password)
    if success:
        session['email'] = email
        return home_get()
    else:
        return home_get()  # change to render sign in page once mysql connected


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('email', None)
    return index_get()


@app.route('/home_get', methods=['GET'])
def home_get():
    home_form = home_form_view_builder.build_home_form(model_id=12345, time_frame=TimeFrameEnum(1).name)
    return render_template('home.html', home_form=home_form)


@app.route('/home_post', methods=['POST'])
def home_post():
    time_frame = TimeFrameEnum(int(request.form.get('timeframe'))).name
    home_form = home_form_view_builder.build_home_form(model_id=12345, time_frame=time_frame)
    return render_template('home.html', home_form=home_form)


@app.route('/train_get', methods=['GET'])
def train_get():
    return render_template('models.html')


@app.route('/friends_get', methods=['GET'])
def select_photos_get():
    return render_template('friends.html')


@app.route('/metrics_get', methods=['GET'])
def metrics_get():
    return render_template('metrics.html')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)
