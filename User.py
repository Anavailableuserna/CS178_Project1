import boto3

TABLE_NAME = "Movie_Users"

dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table(TABLE_NAME)


def create_user(name):
    try:
        name = str(input("What is the movie name? "))
        year = int(input("What year was it made? "))
        director = str(input("Who was the director of the movie? "))
        rating = list(input("What was the rating of this movie? "))


        table.put_item(
            Item={
                'User': name,
                'Year' : year,
                'Director' : director,
                'Ratings' : rating
                }
            )
        print("creating a movie")
    except:
        print("There was an error when adding the movie")
        return


    
def print_movie(movie_dict):
    # print out the values of the movie dictionary
    print("Title: ", movie_dict["Title"])
    print("Director: ", movie_dict["Director"])
    print(" Ratings: ", end="")
    for rating in movie_dict["Ratings"]:
        print(rating, end=" ")
    print(" Year: ", movie_dict.get("Year"))
    print()

def print_all_movies():
    response = table.scan() #get all of the movies
    for movie in response["Items"]:
        print_movie(movie)

def update_rating():
    try:
        title=input("What is the movie title? ")
        rating = int(input("What is the rating: "))
    
        table.update_item(
            Key = {"Title": title}, 
            UpdateExpression = "SET Ratings = list_append(Ratings, :r)", 
            ExpressionAttributeValues = {':r': [rating],}
        )
        print("Movie updated")
    except:
        print("error in updating movie rating")




def delete_movie():

    moviename = input("What is the name of the movie you want to delete? ")
    table.delete_item(
        Key = {'Title' : moviename}
        
    )
    print("deleting movie")

def query_movie():
    """
    prompt user for the Movie title
    print out the average review for all reivews in the list
    """
    try:
        moviename = input("What is the name of the movie you want the average of? ")
        response = table.get_item(
            Key = {'Title' : moviename}
        )
        movie = response.get("Item")
        ratings_list = movie["Ratings"]
        if(len(ratings_list) == 0):
            print("movie has no ratings")
            return
        average = sum(ratings_list)/len(ratings_list)
        print("Average ratings of ", moviename, "is", average)
    except:
        print("movie not found")

    
def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new movie")
    print("Press R: to READ all movies")
    print("Press U: to UPDATE a new movie (add a review)")
    print("Press D: to DELETE a movie")
    print("Press Q: to Query a movie's average ratings")
    print("Press X: to EXIT application")
    print("----------------------------")


def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_movie()
        elif input_char.upper() == "R":
            print_all_movies()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_movie()
        elif input_char.upper() == "Q":
            query_movie()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print('Not a valid option. Try again.')
main()


from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        movie = request.form['movie']
        rating = request.form['rating']

        table.put_item(
            Item={
                'User': name,
                'Movie' : movie,
                'Rating' : rating
                }
            )
        flash('User added successfully!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_user.html')

@app.route('/delete-user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("Name:", name, "deleted from database")
        
        flash('User deleted successfully!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('delete_user.html')


@app.route('/display-users')
def display_users():
    # hard code a value to the users_list;
    # note that this could have been a result from an SQL query :) 
    users_list = (('John','Doe','Comedy'),('Jane', 'Doe','Drama'))
    return render_template('display_users.html', users = users_list)


# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)