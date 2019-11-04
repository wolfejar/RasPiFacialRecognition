from flask import Flask, render_template, request, session, redirect, url_for
import viewbuilders.home_form_view_builder as home_form_view_builder
import viewbuilders.friends_form_view_builder as friends_form_view_builder
import viewbuilders.edit_friend_form_view_builder as edit_friend_form_view_builder
from models.time_frame_enum import TimeFrameEnum
import models.crop_faces as cf
import models.friend
import validators.add_friend_validator as add_friend_validator
import validators.sign_in_validator as sign_in_validator
import validators.sign_up_validator as sign_up_validator
import validators.delete_friend_validator as delete_friend_validator
import os


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
        return redirect(url_for('home_get'))
    else:
        return index_get()


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
    success = sign_up_validator.validate_sign_up(
        username=email, password=password, first_name=first_name, last_name=last_name
    )
    if success:
        session['email'] = email
        return redirect(url_for('home_get'))
    else:
        return sign_up_get()


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('email', None)
    return index_get()


@app.route('/home_get', methods=['GET'])
def home_get():
    home_form = home_form_view_builder.build_home_form(model_id=12345, time_frame=TimeFrameEnum.Today)
    return render_template('home.html', home_form=home_form)


@app.route('/home_post', methods=['POST'])
def home_post():
    time_frame = TimeFrameEnum(int(request.form.get('timeframe')))
    home_form = home_form_view_builder.build_home_form(model_id=12345, time_frame=time_frame)
    return render_template('home.html', home_form=home_form)


@app.route('/train_get', methods=['GET'])
def train_get():
    return render_template('models.html')


@app.route('/friends_get', methods=['GET'])
def friends_get():
    friends_form = friends_form_view_builder.build_friends_form(session['email'])
    return render_template('friends.html', friends_form=friends_form)


@app.route('/add_friend_manual_get', methods=['GET'])
def add_friend_manual_get():
    return render_template('add_friend_manual.html')


@app.route('/add_friend_manual_post', methods=['POST'])
def add_friend_manual_post():
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    home_username = session['email']
    if add_friend_validator.validate_friend(
            username=email, first_name=first_name, last_name=last_name, home_username=home_username):
        return add_friend_images_post()
    else:
        return redirect(url_for('add_friend_manual_get'))


@app.route('/add_friend_images_post', methods=['POST'])
def add_friend_images_post():
    images = request.files.getlist("images")
    print('save friend images')
    print(images)
    friend = models.friend.load(session['email'], request.form['email'])
    for image in images:
        save_dir = './static/img/data/' + str(friend.user_id)
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        image.save(save_dir + '/' + image.filename)
    if cf.crop_and_review_faces(str(friend.user_id), './static/img/data/', './static/img/out/training/'):
        return review_images_get(home_username=session['email'], friend_username=request.form['email'], review=True)
    return edit_friend_from_list_post(request.form)


@app.route('/edit_or_delete_friend_post', methods=['POST'])
def edit_or_delete_friend_post():
    if request.form['submit_button'] == 'Edit':
        return edit_friend_from_list_post(request.form)
    else:
        return delete_friend_post(request.form)


@app.route('/edit_friend_from_list_post', methods=['POST'])
def edit_friend_from_list_post(form):
    edit_friend_form = edit_friend_form_view_builder.build_edit_friend_form(
        home_username=session['email'], friend_username=form['email'], review=False)
    return render_template('edit_friend.html', friend_form=edit_friend_form)


@app.route('/review_images_get', methods=['GET'])
def review_images_get(home_username, friend_username, review):
    print('rendering review images page')
    review_images_form = edit_friend_form_view_builder.build_edit_friend_form(
        home_username=home_username, friend_username=friend_username, review=review)
    return render_template('review_faces.html', friend_form=review_images_form)


@app.route('/delete_friend', methods=['POST'])
def delete_friend_post(form):
    # delete friend here
    friend_to_delete = form['username']
    delete_friend_validator.validate_delete_friend(session['email'], friend_to_delete)
    return redirect(url_for('friends_get'))


@app.route('/metrics_get', methods=['GET'])
def metrics_get():
    return render_template('metrics.html')


if __name__ == '__main__':
    app.run(debug=True)
