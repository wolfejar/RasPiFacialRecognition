from flask import Flask, render_template, request, session, redirect, url_for
import viewbuilders.home_form_view_builder as home_form_view_builder
import viewbuilders.friends_form_view_builder as friends_form_view_builder
import viewbuilders.edit_friend_form_view_builder as edit_friend_form_view_builder
from viewbuilders.models_form_view_builder import build_model_form
import viewbuilders.metrics_form_view_builder as metrics_form_view_builder
from models.time_frame_enum import TimeFrameEnum
import models.crop_faces as cf
import models.model_train_pipeline as mtp
import models.friend
import models.classify_embeddings as ce
import models.classification
import validators.add_friend_validator as add_friend_validator
import validators.sign_in_validator as sign_in_validator
import validators.sign_up_validator as sign_up_validator
import validators.delete_friend_validator as delete_friend_validator
import os
import json
from datetime import datetime, timedelta
import pickle
import realtime_classification_pipeline as rcp
import numpy
from PIL import Image

from OpenSSL import SSL

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'super secret key'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


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
        friends = models.friend.load_all_friends(session['email'])
        session['friends'] = [friend.__dict__ for friend in friends]
        print(session['friends'])
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
    home_form = home_form_view_builder.build_home_form(session['id'], time_frame=TimeFrameEnum.Today)
    return render_template('home.html', home_form=home_form)


@app.route('/home_post', methods=['POST'])
def home_post():
    time_frame = TimeFrameEnum(int(request.form.get('timeframe')))
    home_form = home_form_view_builder.build_home_form(session['id'], time_frame=time_frame)
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
        friends = models.friend.load_all_friends(session['email'])
        session['friends'] = [friend.__dict__ for friend in friends]
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
    friends = models.friend.load_all_friends(session['email'])
    session['friends'] = [friend.__dict__ for friend in friends]
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
    layers = [int(l) for l in request.form.getlist('hiddenlayer[]')]
    learning_rate = float(request.form['learning_rate'])
    momentum = float(request.form['momentum'])
    epochs = int(request.form['epochs'])
    split = float(request.form['split'])
    print("Friends:", selected_friends, "Layers:", type(layers), "Learning rate:", type(learning_rate), "Momentum:", type(momentum),
          "Epochs:", type(epochs), "Split:", type(split))
    selected_friends = [int(friend) for friend in selected_friends]
    loaded_friends = []
    for fr in selected_friends:
        loaded_friends.append(models.friend.load_by_id(session['email'], fr))
    # create the embeddings and save to directory
    model_name = request.form['model-name']
    if not os.path.exists('./static/models/' + str(session['id']) + '/'):
        os.mkdir('./static/models/' + str(session['id']) + '/')
    out_path = os.path.abspath('./static/models/' + str(session['id']) + '/' + model_name + '.pickle')
    f = open(out_path, 'wb+')
    f.write(pickle.dumps(selected_friends))
    f.close()
    mtp.init_model_train_pipeline(session['id'], loaded_friends, model_name, learning_rate=learning_rate,
                                  momentum=momentum, epochs=epochs, split=split, hidden_layers=layers)
    return redirect(url_for('train_get'))


@app.route('/metrics_get', methods=['GET'])
def metrics_get():
    form = metrics_form_view_builder.build_metrics_form(session['id'])
    return render_template('metrics.html', metrics_form=form)


@app.route('/realtime_get', methods=['GET'])
def realtime_get():
    session['queue'] = []
    return render_template('realtime.html')


@app.route('/classify_image', methods=['POST'])
def classify_image():
    print('received image to be classified')
    print('queue before', session['queue'])
    model_name = mtp.get_active_name(session['id'])
    file = request.files['fileshot']
    filename = file.filename
    file = Image.open(file)
    img_arr = numpy.array(file)
    results = rcp.classify_image_from_client(session['id'], mtp.get_active_name(session['id']), img_arr)
    friends = pickle.loads(
        open(os.path.abspath('./static/models/' + str(session['id']) + '/' + model_name + '.pickle'), 'rb').read())
    detected_friends = []
    classifications = []
    c_tuples = []
    if results == 'unknown':
        print(results)
        unknown_results = rcp.get_info_for_unknown_user(session['id'])
        print(unknown_results)
        img_path = os.path.abspath('./static/img/data/' + str(unknown_results[0]) + '/')
        if not os.path.exists(img_path):
            os.mkdir(img_path)
        cl = models.classification.Classification(unknown_results[0], unknown_results[1], unknown_results[2], 1,
                                                  datetime.now(), img_path + '/' + filename)
        models.classification.save_classification(mtp.get_active_id(session['id']), cl)
        file.save(img_path + '/' + filename, 'png')
    else:
        for result in results:
            detected_friends.append((friends[result[0].index(max(result[0]))], max(result[0])))
    for friend, c in detected_friends:
        c_tuples.append({'friend': friend, 'time': datetime.now()})
        friend = models.friend.load_by_id_with_home_id(session['id'], friend)
        img_path = os.path.abspath('./static/img/data/' + str(friend.user_id) + '/')
        classifications.append(models.classification.Classification(friend.user_id, friend.first_name, friend.last_name,
                                                                    c, datetime.now(), img_path + '/' + filename))

    for t in c_tuples:
        if len(session['queue']) == 0:
            session['queue'].append(t)
            c_to_add = [cl for cl in classifications if cl.user_id == t['friend']][0]
            models.classification.save_classification(mtp.get_active_id(session['id']), c_to_add)
            img_path = os.path.abspath('./static/img/data/' + str(c_to_add.user_id) + '/')
            file.save(img_path + '/' + filename, 'png')
        else:
            for i in range(len(session['queue'])):
                session_c = session['queue'][i]
                in_q = False
                should_add = False
                if session_c['friend'] == t['friend']:
                    in_q = True
                    if t['time'] > session_c['time'] + timedelta(minutes=5):
                        session['queue'][i] = t
                        should_add = True
                if in_q is False:
                    session['queue'].append(t)
                if in_q is False or should_add is True:
                    c_to_add = [cl for cl in classifications if cl.user_id == t['friend']][0]
                    models.classification.save_classification(mtp.get_active_id(session['id']), c_to_add)
                    img_path = os.path.abspath('./static/img/data/' + str(c_to_add.user_id) + '/')
                    file.save(img_path + '/' + filename, 'png')

    print('queue after', session['queue'])
    session['queue'] = session['queue']
    return ''


@app.route('/set_active', methods=['POST'])
def set_active():
    model_id = request.form['model_id']
    mtp.set_active(session['id'], model_id)
    return redirect(url_for('train_get'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')
