
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


def display_user():
    response = table.scan() #get all of the movies
    rows = 0
    user_list= []
    for user in response["Items"]:
        user_list.append((user["Username"], user['Preferred_Language'], user['Favorite_Genre'], user['Favorite_Movie'], user['Rating']))
    return user_list
def change_user(name, language, genre, movie, rating):
    try:
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
        flash("User updated", "success")
    except:
        flash("error in updating user")


def remove_user(name):
    try:
        table.delete_item(
            Key = {'Username' : name}
        )
        flash('User deleted successfully!', 'success')
    except:
        flash("There was an error when creating the user")
        return





