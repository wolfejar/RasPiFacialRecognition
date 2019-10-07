from flask import Flask, render_template
import viewbuilders.home_form_view_builder as home_form_view_builder

app = Flask(__name__)


@app.route('/')
def index_get():
    return render_template('index.html')


@app.route('/home')
def home():
    home_form = home_form_view_builder.build_home_form(model_id=12345, time_frame='test')
    return render_template('home.html', home_form=home_form)


@app.route('/train')
def train():
    return render_template('models.html')


@app.route('/friends')
def select_photos():
    return render_template('friends.html')


@app.route('/metrics')
def metrics():
    return render_template('metrics.html')


if __name__ == '__main__':
    app.run(debug=True)
