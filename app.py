from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index_get():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/train')
def train():
    return render_template('models.html')

@app.route('/select_photos')
def select_photos():
    return render_template('friends.html')

@app.route('/metrics')
def metrics():
    return render_template('metrics.html')

if __name__ == '__main__':
    app.run(debug=True)
