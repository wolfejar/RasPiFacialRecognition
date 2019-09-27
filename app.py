from flask import Flask, render_template
from models.graph_data import GraphData

app = Flask(__name__)


@app.route('/')
def index_get():
    return render_template('index.html')


@app.route('/home')
def home():
    graph_data = GraphData(None)
    graph_data.load_classifications_by_time_frame(time_frame=1)
    return render_template('home.html', graph_data=graph_data)


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
