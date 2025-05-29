# import sqlite3
# from flask import Flask, render_template,request, redirect, url_for
#
# app = Flask(__name__)
#
# connection = sqlite3.connect("sqlite.db")
#
#
# def close_db(connection=None):
#     if connection is not None:
#         connection.close()
#
# @app.teardown_appcontext
# def close_connection(excpetion):
#     close_db()
#
# @app.route("/")
# def index():
#     return render_template("index.html")
#
#     # return render_templaye("blog.html", **context)
#
# @app.route("/add/", methods=["GET", "POST"])
# def addPost():
#     if request.method == "POST": #sending data to server
#         title = request.form["title"]
#         content = request.form["content"]
#         cursor = connection.cursor()
#         cursor.execute("INSERT INTO post (title, content) VALUES (?,?)", (title, content))
#         connection.commit()
#         return redirect(url_for("index")) # bringing user back to main page
#     return render_template("addPost.html")
#
#
# # @app.route('/post/<post_id>')
# # def post(post_id):
# #     result = cursor.execute("SELECT * FROM post WHERE id = 7", (post_id, )).fetchone()
# #     post_dict = {'id': result[0], 'titel': result[1], 'content': result[2]}
# #     return render_template("post.html", post=post_dict)
#
#
# @app.route('/post/<post_id>')
# def post(post_id):
#     cursor = connection.cursor()
#     result = cursor.execute(
#         'SELECT * FROM post WHERE id = ?',
#         (post_id,)
#     ).fetchone()
#     post_dict = {'id': result[0], 'title': result[1], 'content': result[2]}
#     return render_template('post.html', post=post_dict)
#
# @app.route("/minecraft/")
# def minecraft():
#     return render_template("minecraft.html")
#
# @app.route("/roblox/")
# def roblox():
#     return render_template("roblox.html")
#
# @app.route("/transformers/")
# def transformers():
#     return render_template("transformers.html")
#
# @app.route("/blog/")
# def blog():
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM post")
#     result = cursor.fetchall()
#     posts = []
#     for post in result:
#         posts.append(
#             {"id": post[0], "title": post[1], "content": post[2]}
#         )
#     context = {"posts": posts}
#
#     return render_template("blog.html", **context)
#     # return render_template("blog.html", **context)
#
#
#
#
# if __name__ == "__main__":
#     app.run(debug=True)




# import sqlite3
# from flask import Flask, render_template, request, redirect, url_for, g
# from datetime import date
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
#
#
# app = Flask(__name__)
#
# today = date.today()
#
# print("Today's date is", today)
#
# DATABASE = "sqlite.db"
#
# app.config["SECRET_KEY"] = "123qwerty"
# login_manager = LoginManager(app)
# login_manager.login_view = "login"
#
# class User(UserMixin):
#     def __init__(self, id, username, password_hash):
#         self.id = id
#         self.username = username
#         self.password_hash = password_hash
#
#     def set_password(self,password):
#         self.password_hash = generate_password_hash(password) #hashing a new password
#
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password) # a method that checks whether the transmitted password matches the encrypted one
#
# @login_manager.user_loader
# def load_user(user_id):
#     user = cursor.execute("SELECT * FROM user WHERE id = ?", (user_id)).fetchone()
#     if user is not None:
#         return User(user[0], user[1], user[2])
#     return None
#
# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#     return db
#
# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()
#
# @app.route("/")
# def index():
#
#
#     db = get_db()
#     cursor = db.cursor()
#
#
#     return render_template("index.html")
#
# @app.route("/register/", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         db = get_db()
#         cursor = db.cursor()
#
#         try:
#             cursor.execute("INSERT INTO user (username, password_hash) VALUES (?, ?)", (username, generate_password_hash(password)))
#             db.commit()
#             print("User registration was successful")
#         except sqlite3.IntegrityError:
#             return render_template("register.html", message="Username already exists!")
#             print("Username already exists")
#     return render_template("register.html")
#
# @app.route("/login/", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         user = cursor.execute("SELECT * FROM user WHERE username =?", (username,)).fetchone()
#         if user and User(user[0], user[1], user[2]).check_password(password):
#             login_user(User(user[0], user[1], user[2]))
#             return render_template("login.html", message="Invalid username or password")
#     return render_template("login.html")
#
# @app.route("/logout/")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for("index"))
#
# @app.route("/add/", methods=["GET", "POST"])
# def addPost():
#     if request.method == "POST":
#         title = request.form["title"]
#         content = request.form["content"]
#         publishedDate = date.today()
#         author_id = 1
#         db = get_db()
#         cursor = db.cursor()
#         cursor.execute("INSERT INTO post (title, content, publishedDate, author_id) VALUES (?,?,?,?)", (title, content, publishedDate, author_id))
#         db.commit()
#         return redirect(url_for("blog"))
#     return render_template("addPost.html")
#
#
# @app.route('/post/<post_id>')
# def post(post_id):
#     db = get_db()
#     cursor = db.cursor()
#     result = cursor.execute(
#         'SELECT * FROM post WHERE id = ?',
#         (post_id)
#     ).fetchone()
#     if result is None:
#         return "Post not found", 404
#     post_dict = {'id': result[0], 'title': result[1], 'content': result[2]}
#     return render_template('post.html', post=post_dict)
#
# @app.route("/minecraft/")
# def minecraft():
#     return render_template("minecraft.html")
#
# @app.route("/roblox/")
# def roblox():
#     return render_template("roblox.html")
#
# @app.route("/transformers/")
# def transformers():
#     return render_template("transformers.html")
#
# @app.route("/blog/")
# def blog():
#     db = get_db()
#     cursor = db.cursor()
#
#     # cursor.execute("create table post(id integer primary key autoincrement, title text not null, content text not null);")
#     # cursor.execute("SELECT * FROM post")
#     cursor.execute("SELECT * FROM post inner JOIN user ON post.author_id = user.id")
#     result = cursor.fetchall()
#     posts = []
#     for post in reversed(result):
#         posts.append(
#             {"id": post[0], "title": post[1], "content": post[2], "publishedDate": post[3], "author_id": post[4], "username": post[6]}
#             # {"id": post[0], "title": post[1], "content": post[2], "publishedDate": post[3], "author_id": post[4]}
#         )
#     context = {"posts": posts}
#     return render_template("blog.html", **context)
#
# if __name__ == "__main__":
#     app.run(debug=True)




import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)

today = date.today()

print("Today's date is", today)

DATABASE = "sqlite.db"

app.config["SECRET_KEY"] = "123qwerty"
login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)  # hashing a new password

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)  # a method that checks whether the transmitted password matches the encrypted one


def user_is_liking(user_id, post_id):
    like = cursor.execute(
        "SELECT * FROM like WHERE user_id = ? AND post_id = ?", (user_id, post_id)).fetchone()
    return bool(like)

# @app.route("/like/<int:post_id>")
# @login_required
# def like_post(post_id):
#     post = cursor.execute("SELECT * FROM post WHERE id = ?", (post_id,)).fetchone()
#
#     if post:
#         if user_is_liking(current_user.id, post_id):
#             cursor.execute(
#                 "DELETE FROM like WHERE user_id = ? AND post_id = ?", (current_user.id, post_id))
#             connection.commit()
#             print("You unliked this post.")
#         else:
#             cursor.execute(
#                 "INSERT INTO like (user_id, post_id) VALUES (?, ?)", (current_user.id, post.id)
#             )
#             connection.commit()
#             print("You liked this post.")
#         return redirect(url_for("blog"))
#     return "Post not found", 404

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    cursor = db.cursor()
    user = cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
    if user is not None:
        return User(user[0], user[1], user[2])
    return None

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    db = get_db()
    cursor = db.cursor()
    return render_template("index.html")

@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        cursor = db.cursor()

        try:
            cursor.execute("INSERT INTO user (username, password_hash) VALUES (?, ?)", (username, generate_password_hash(password)))
            db.commit()
            print("User registration was successful")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return render_template("register.html", message="Username already exists!")
    return render_template("register.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        cursor = db.cursor()
        user = cursor.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
        if user and User(user[0], user[1], user[2]).check_password(password):
            login_user(User(user[0], user[1], user[2]))
            return redirect(url_for("index"))
        else:
            return render_template("login.html", message="Invalid username or password")
    return render_template("login.html")

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/add/", methods=["GET", "POST"])
@login_required
def addPost():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        publishedDate = date.today()
        author_id = current_user.id
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO post (title, content, publishedDate, author_id) VALUES (?, ?, ?, ?)", (title, content, publishedDate, author_id))
        db.commit()
        return redirect(url_for("blog"))
    return render_template("addPost.html")

@app.route('/post/<int:post_id>')
def post(post_id):
    db = get_db()
    cursor = db.cursor()
    result = cursor.execute(
        'SELECT * FROM post WHERE id = ?',
        (post_id,)
    ).fetchone()
    if result is None:
        return "Post not found", 404
    post_dict = {'id': result[0], 'title': result[1], 'content': result[2], 'publishedDate':result[3], 'author_id': result[4]}
    return render_template('post.html', post=post_dict)

@app.route("/delete/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    db = get_db()
    cursor = db.cursor()
    post = cursor. execute("SELECT * FROM post WHERE id = ?", (post_id,)).fetchone()
    if post and post[4] == current_user.id:
        cursor.execute("DELETE FROM post WHERE id = ?", (post_id))
        return redirect(url_for("blog"))
    else:
        return redirect(url_for("blog"))

@app.route("/minecraft/")
def minecraft():
    return render_template("minecraft.html")

@app.route("/roblox/")
def roblox():
    return render_template("roblox.html")

@app.route("/transformers/")
def transformers():
    return render_template("transformers.html")

# @app.route("/blog/")
# def blog():
#     db = get_db()
#     cursor = db.cursor()
#
#     cursor.execute("SELECT * FROM post INNER JOIN user ON post.author_id = user.id")
#     result = cursor.fetchall()
#     posts = []
#     for post in reversed(result):
#         posts.append(
#             {"id": post[0], "title": post[1], "content": post[2], "publishedDate": post[3], "author_id": post[4], "username": post[6]}
#         )
#     context = {"posts": posts}
#     return render_template("blog.html", **context)


#
# @app.route("/blog/")
# def blog():
#     db = get_db()
#     cursor = db.cursor()
#
#     # Get all posts with author info and like counts
#     cursor.execute("""
#         SELECT
#             post.id,
#             post.title,
#             post.content,
#             post.publishedDate,
#             post.author_id,
#             user.username,
#             COUNT(like.id) AS likes
#         FROM
#             post
#         INNER JOIN
#             user ON post.author_id = user.id
#         LEFT JOIN
#             like ON post.id = like.post_id
#         GROUP BY
#             post.id, post.title, post.content, post.publishedDate, post.author_id, user.username
#         ORDER BY
#             post.publishedDate DESC
#     """)
#
#     result = cursor.fetchall()
#     posts = []
#     liked_posts = []
#     for post in result:
#         posts.append({
#             "id": post[0],
#             "title": post[1],
#             "content": post[2],
#             "publishedDate": post[3],
#             "author_id": post[4],
#             "username": post[5],
#             "likes": post[6],
#             "is_liked": post[0] in liked_posts
#         })
#         if current_user.is_authenticated:
#             cursor.execute("SELECT post_id FROM like WHERE user_id = ?", (current_user.id,))
#         liked_posts = [row[0] for row in cursor.fetchall()]
#         likes_result = cursor.fetchall()
#
#         for like in likes_result:
#             liked_posts.append(like[0])
#         posts[-1]["liked_posts"] = liked_posts
#     context = {"posts": posts}
#
#
#     return render_template("blog.html", **context)
#


@app.route("/like/<int:post_id>")
@login_required
def like_post(post_id):
    db = get_db()
    cursor = db.cursor()


    post = cursor.execute("SELECT * FROM post WHERE id = ?", (post_id,)).fetchone()
    if not post:
        return "Post not found", 404


    cursor.execute("SELECT * FROM like WHERE user_id = ? AND post_id = ?",
                  (current_user.id, post_id))
    existing_like = cursor.fetchone()

    if existing_like:
        # Unlike the post
        cursor.execute("DELETE FROM like WHERE user_id = ? AND post_id = ?",
                      (current_user.id, post_id))
        db.commit()
        print("You unliked this post.")
    else:
        # Like the post
        cursor.execute("INSERT INTO like (user_id, post_id) VALUES (?, ?)",
                      (current_user.id, post_id))
        db.commit()
        print("You liked this post.")

    return redirect(url_for("blog"))

@app.route("/blog/")
def blog():
    db = get_db()
    cursor = db.cursor()

    # Get all posts with author info and like counts
    cursor.execute("""
        SELECT 
            post.id,
            post.title,
            post.content,
            post.publishedDate,
            post.author_id,
            user.username,
            COUNT(like.id) AS likes
        FROM 
            post
        INNER JOIN 
            user ON post.author_id = user.id
        LEFT JOIN 
            like ON post.id = like.post_id
        GROUP BY
            post.id, post.title, post.content, post.publishedDate, post.author_id, user.username
        ORDER BY
            post.publishedDate DESC
    """)

    result = cursor.fetchall()
    posts = []


    liked_posts = []
    if current_user.is_authenticated:
        cursor.execute("SELECT post_id FROM like WHERE user_id = ?", (current_user.id,))
        liked_posts = [row[0] for row in cursor.fetchall()]

    for post in result:
        posts.append({
            "id": post[0],
            "title": post[1],
            "content": post[2],
            "publishedDate": post[3],
            "author_id": post[4],
            "username": post[5],
            "likes": post[6],
            "is_liked": post[0] in liked_posts
        })

    return render_template("blog.html", posts=posts)






if __name__ == "__main__":
    app.run(debug=True)

