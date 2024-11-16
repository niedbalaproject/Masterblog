from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

STORAGE_FILE = "storage.json"


def load_posts():
    """
    Load blog posts from the JSON file.
    :return: list: A list of blog posts (dictionaries) loaded from the JSON file.
    """
    if not os.path.exists(STORAGE_FILE):
        return []
    with open(STORAGE_FILE, 'r') as handle:
        return json.load(handle)


def save_posts(posts):
    """
    Save blog posts to the JSON file.
    :param: posts (list): The list of blog posts to be saved.
    """
    with open(STORAGE_FILE, 'w') as handle:
        json.dump(posts, handle, indent=4)


def fetch_post_by_id(post_id):
    """
    Fetch a single blog post by its ID.
    :param post_id: The ID of the blog post to fetch (int).
    :return: dict or None: The blog post is found, otherwise None.
    """
    posts = load_posts()
    for post in posts:
        if post['id'] == post_id:
            return post
    return None


@app.route('/')
def index():
    """
    Display the homepage with a list of all blog posts.
    :return: str: Rendered HTML for the homepage.
    """
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Add a new blog post.
    The new post is fetched from the form fata, assigned a unique ID, and saved to
    the JSON file.

    :return: str: Redirects to the homepage after adding the post.
    """
    if request.method == 'POST':
        posts = load_posts()
        new_post = {
            'id': posts[-1]['id'] + 1 if posts else 1,  # Incremental ID based on the current number of posts
            'author': request.form['author'],
            'title': request.form['title'],
            'content': request.form['content'],
            'likes': 0
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect('/')
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """
    Delete a blog post.
    :param post_id: The ID of the blog post to delete.
    :return: Redirects to the homepage after deleting the post.
    """
    blog_posts = load_posts()  # load the current list of posts
    blog_posts = [post for post in blog_posts if post['id'] != post_id]  # remove the post with a matching ID
    save_posts(blog_posts)  # save the updated list back to the file
    return redirect('/')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Handle the updating of a blog post.
    :param post_id: int: The ID of the blog post to update.
    :return: str: Rendered HTML for the ypdate page (GET) or redirects to index (POST).
    """
    posts = load_posts()
    post = fetch_post_by_id(post_id)
    if not post:
        return "Post not found", 404

    if request.method == 'POST':
        for post in posts:
            if post['id'] == post_id:
                post['title'] = request.form['title']
                post['author'] = request.form['author']
                post['content'] = request.form['content']
                break

        save_posts(posts)
        return redirect('/')

    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    """
    Handle liking a blog post.
    :param post_id: int: The ID of the blog post to like.
    :return: Redirects to the homepage after liking the post.
    """
    posts = load_posts()
    for post in posts:
        if post['id'] == post_id:
            post['likes'] += 1
            break
    save_posts(posts)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
