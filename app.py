from flask import Flask, render_template, request, redirect, url_for
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


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        blog_posts = load_posts()

        new_post = {
            'id': len(blog_posts) + 1,  # ensure the ID is unique
            'author': author,
            'title': title,
            'content': content
        }
        blog_posts.append(new_post)
        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


if __name__ == '__main__':
    app.run(debug=True)
