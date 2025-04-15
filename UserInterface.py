
import boto3
from flask import flash

TABLE_NAME = "Movies"

        
dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table(TABLE_NAME)

session = boto3.Session()
dynamodb = session.client('dynamodb', region_name="us-east-1")


def create_user(name, language, genre, movie, rating):
    try:

        table.put_item(
            Item={
                'Username': name,
                'Favorite_Genre' : genre,
                'Favorite_Movie' : movie,
                'Preferred_Language' : language,
                'Rating' : int(rating)
                }
            )
    except:
        flash("There was an error when creating the user", 'failure')
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



