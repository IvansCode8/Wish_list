from __future__ import unicode_literals
from django.db import models
from datetime import datetime

import re

now = str(datetime.now())

class UserManager(models.Manager):

    def login_validator(self, postData):
        print(" i am in login validator-------!!!!!!!")
        print("POSTDATA is", postData)
        errors = {}
        
        #Username Validation
        if len(postData["username"]) < 1:
            print(" I am in less than 1 letter of username")
            errors["username"] = "username is required"
        elif not User.objects.filter(username = postData["username"]):
            errors["username"] = "This username does not exist. Please register!"

        #Password Validation
        if len(postData['password']) < 1:
            errors['password'] = "password is required"
        elif len(postData['password']) < 8: 
            errors['password_length'] = "password needs to be at least 8 characters"

        return errors

# registration validator here
    def reg_validator(self, postData):
        print(" i am in reg validator-------!!!!!!!")
        print("POSTDATA is", postData)
        errors = {}
        
        if len(postData["name"]) < 1:
            errors["name"] = "name is required"
        if len(postData["name"]) < 3:
            errors["name"] = "name needs to be at least 3 characters long"

        #Username Validation
        if len(postData["username"]) < 1:
            print(" I am in less than 1 letter of username")
            errors["username"] = "username is required"
        elif len(postData["username"]) < 3:
            errors["username_length"] = "username needs to be at least 3 characters"
        elif User.objects.filter(username = postData["username"]):
            errors["username"] = "This username is already registered. Please log in!"
        elif postData['password'] != postData['confirm_password']:
            errors["password_no_match"] = "Passwords do not match"

        #Password Validation
        if len(postData['password']) < 1:
            errors['password'] = "password is required"
        return errors


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_hired = models.DateField()

    objects = UserManager()


class WishManager(models.Manager):
    def basic_validator(self, postData):
        print("POSTDATA is: ", postData)
        errors = {}
        #Item validation
        if len(postData["item"]) < 1:
            errors["item"] = "item is required"
        if len(postData["item"]) < 3:
            errors["item_length"] = "item should be longer than 3 chars"
        
        print("About to return from basic validator")
        return errors


class Wish(models.Model):
    item = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    added_by_user = models.CharField(max_length=255) 
    
    #ONE TO MANY RELATIONSHIP
    added_by = models.ForeignKey(User, related_name="items", on_delete=models.CASCADE)

    objects = WishManager()

    #represent method
    def __repr__(self):
        return f"Wish: {self.id} {self.item}"

#MANY TO MANY RELATIONSHIP
class Join(models.Model):
    user = models.ForeignKey(User, related_name="user_joining_wishes", on_delete=models.CASCADE)
    wish = models.ForeignKey(Wish, related_name="wishes_joined_by_users", on_delete=models.CASCADE)
