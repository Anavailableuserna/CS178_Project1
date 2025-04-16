
import boto3
from flask import flash

TABLE_NAME = "Movies"

        
dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table(TABLE_NAME)

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
        flash('User added successfully!', 'success')
    except:
        flash("There was an error when creating the user")
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

def display_user():
    response = table.scan() #get all of the movies
    rows = 0
    user_list= []
    for user in response["Items"]:
        user_list.append((user["Username"], user['Preferred_Language'], user['Favorite_Genre'], user['Favorite_Movie'], user['Rating']))
    return user_list
def change_user(name, language, genre, movie, rating):
    try:
        user_list= []
        for user in response["Items"]:
            user_list.append((user["Username"]))
        if user name not in user_list
            throw Exception():
        
        table.update_item(
            Key = {"Username": name}, 
            UpdateExpression = "SET Preferred_Language = :str", 
            ExpressionAttributeValues = {':str': language,}
        )
        table.update_item(
            Key = {"Username": name}, 
            UpdateExpression = "SET Favorite_Genre = :str", 
            ExpressionAttributeValues = {':str': genre,}
        )
        table.update_item(
            Key = {"Username": name}, 
            UpdateExpression = "SET Favorite_Movie = :str", 
            ExpressionAttributeValues = {':str': movie,}
        )
        table.update_item(
            Key = {"Username": name}, 
            UpdateExpression = "SET Rating = :r", 
            ExpressionAttributeValues = {':r': rating,}
        )
        flask("User updated", "success")
    except:
        print("error in updating user")




def remove_user(name):
    try:
        table.delete_item(
            Key = {'Username' : name}
        )
        flash('User deleted successfully!', 'success')
    except:
        flash("There was an error when creating the user")
        return

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



