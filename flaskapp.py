
from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *
from UserInterface import *

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['username']
        language = request.form['language']
        genre = request.form['genre']
        movie = request.form['movie']
        rating = request.form['rating']

        create_user(name, language, genre, movie, rating)

        # Redirect to home page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_user.html')

@app.route('/delete-user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        #located in UserInterface
        remove_user(name)
        
        # Redirect to home page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('delete_user.html')


@app.route('/display-users')
def display_users():
    #located in UserInterface
    users_list = display_user()
    return render_template('display_users.html', users = users_list)

@app.route('/update-user', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['username']
        language = request.form['language']
        genre = request.form['genre']
        movie = request.form['movie']
        rating = request.form['rating']
        #located in UserInterface
        change_user(name, language, genre, movie, rating)
        # Redirect to home page upon successful submission
        return redirect(url_for('home'))
    else:
        return render_template('update_user.html')
@app.route('/popularity')
def popularity():
    #Gets 25 most popular movies
    rows = execute_query("""SELECT movie_id, title, popularity,
                        FROM movie
                        ORDER BY popularity DESC
                        Limit 25""")
    return display_html(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)