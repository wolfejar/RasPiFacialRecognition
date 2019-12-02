from flask import Flask, render_template, request, session, redirect, url_for
import viewbuilders.home_form_view_builder as home_form_view_builder
import viewbuilders.friends_form_view_builder as friends_form_view_builder
import viewbuilders.edit_friend_form_view_builder as edit_friend_form_view_builder
from viewbuilders.models_form_view_builder import build_model_form
from models.time_frame_enum import TimeFrameEnum
import models.crop_faces as cf
import models.model_train_pipeline as mtp
import models.friend
import models.classify_embeddings as ce
import validators.add_friend_validator as add_friend_validator
import validators.sign_in_validator as sign_in_validator
import validators.sign_up_validator as sign_up_validator
import validators.delete_friend_validator as delete_friend_validator
import os
import json
from models.sql import SQL
import ast

from OpenSSL import SSL

app = Flask(__name__)
app.secret_key = 'super secret key'

# context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
# context.use_privatekey_file('server.key')
# context.use_certificate_file('server.crt')


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
        session['id'] = models.friend.load(session['email'], session['email']).user_id
        sql_instance = SQL()
        results = sql_instance.get_friends(username=email)
        friends = []
        for friend in results:
            friends.append(models.friend.Friend(username=friend[0], user_id=friend[1], first_name=friend[2], last_name=friend[3]))
        session['friends'] = [friend.__dict__ for friend in friends]
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
        session['id'] = models.friend.load(session['email'], session['email']).user_id
        return redirect(url_for('home_get'))
    else:
        return sign_up_get()


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('email', None)
    session.pop('id', None)
    return index_get()


@app.route('/home_get', methods=['GET'])
def home_get():
    home_form = home_form_view_builder.build_home_form(model_id=1, time_frame=TimeFrameEnum.Today)
    return render_template('home.html', home_form=home_form)


@app.route('/home_post', methods=['POST'])
def home_post():
    time_frame = TimeFrameEnum(int(request.form.get('timeframe')))
    home_form = home_form_view_builder.build_home_form(model_id=1, time_frame=time_frame)
    return render_template('home.html', home_form=home_form)


@app.route('/train_get', methods=['GET'])
def train_get():
    models_form = build_model_form(session['email'])
    return render_template('models.html', models_form=models_form)


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
    return friends_get()


@app.route('/edit_or_delete_friend_post', methods=['POST'])
def edit_or_delete_friend_post():
    if request.form['submit_button'] == 'Edit':
        return edit_friend_from_list_post(request.form['username'])
    else:
        return delete_friend_post(request.form)


@app.route('/edit_friend_from_list_post', methods=['POST'])
def edit_friend_from_list_post(username):
    edit_friend_form = edit_friend_form_view_builder.build_edit_friend_form(
        home_username=session['email'], friend_username=username, review=False)
    return render_template('edit_friend.html', friend_form=edit_friend_form)


@app.route('/review_images_get', methods=['GET'])
def review_images_get(home_username, friend_username, review):
    print('rendering review images page')
    review_images_form = edit_friend_form_view_builder.build_edit_friend_form(
        home_username=home_username, friend_username=friend_username, review=review)
    return render_template('review_faces.html', friend_form=review_images_form)


@app.route('/review_images_post', methods=['POST'])
def review_images_post():
    print('Saving selected review images')
    print(request.form.getlist('option'))
    selected_images = request.form.getlist('option')
    friend = models.friend.load(session['email'], request.form['email'])
    cf.save_reviewed_faces(selected_images, str(friend.user_id), './static/img/out/training/')
    friend_form = friends_form_view_builder.build_friends_form(session['email'])
    return render_template('friends.html', friends_form=friend_form)


@app.route('/delete_friend', methods=['POST'])
def delete_friend_post(form):
    # delete friend here
    friend_to_delete = form['username']
    delete_friend_validator.validate_delete_friend(session['email'], friend_to_delete)
    return redirect(url_for('friends_get'))


@app.route('/add_model_get', methods=['GET'])
def add_model_get():
    # get friends list here and add to form
    models_form = build_model_form(session['email'])
    return render_template('add_model.html', models_form=models_form)


@app.route('/add_model_post', methods=['POST'])
def add_model_post():
    # will initialize model training here.
    selected_friends = request.form.getlist('friend')
    print(selected_friends)
    selected_friends = [int(friend) for friend in selected_friends]
    loaded_friends = []
    for fr in selected_friends:
        loaded_friends.append(models.friend.load_by_id(session['email'], fr))
    # create the embeddings and save to directory
    model_name = request.form['model-name']
    mtp.init_model_train_pipeline(session['id'], loaded_friends, model_name)
    models_form = build_model_form(session['email'])
    return render_template('models.html', models_form=models_form)


@app.route('/metrics_get', methods=['GET'])
def metrics_get():
    return render_template('metrics.html')


@app.route('/realtime_get', methods=['GET'])
def realtime_get():
    return render_template('realtime.html')


@app.route('/classify_embeddings', methods=['POST'])
def classify_embeddings():
    classifier = ce.EmbeddingsClassifier(session['id'], 'test_2')
    embeddings_str = request.data.decode("utf-8")
    result = classifier.classify_embeddings(json.loads(embeddings_str)['embeddings']).tolist()
    print(result)
    classified_friend = session['friends'][result.index(max(result))]
    print(classified_friend)
    # if result not in request.form['queue']:
    return classified_friend['first_name']
    # else:
        # return None


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')
