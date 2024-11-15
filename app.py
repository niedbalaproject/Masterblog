from flask import Flask, render_template
import json

app = Flask(__name__)


def load_posts():
    with open('storage.json', 'r') as handle:
        return json.load(handle)


def save_posts(posts):
    with open('storage.json', 'w') as handle:
        json.dump(posts, handle, indent=4)


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(debug=True)
