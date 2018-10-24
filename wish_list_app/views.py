from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
from time import gmtime, strftime
import bcrypt

# Create your views here.
def index(request):
    return redirect("/main")

def main(request):
    return render(request, "index.html")

def register(request):
    print(" i am in register!! yay")
    #<<--------VALIDATIONS-------->>
    errors = User.objects.reg_validator(request.POST)
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        print(errors)
        print("done with register if")
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        hash_brown = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name = request.POST['name'], username = request.POST['username'], password = hash_brown.decode("utf-8"), date_hired = request.POST["date"])

        #store user id in session
        request.session['id'] = user.id
        request.session['name'] = user.name
        print("done with register else")
        return redirect('/dashboard')


def login(request):

    errors = User.objects.login_validator(request.POST)
    print(errors)

    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        
        print(errors)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        user = User.objects.get(username=request.POST['username'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            print("password match")
            request.session['id'] = user.id
            request.session['name']=user.name
            return redirect("/dashboard")
        else:
            print("failed password")
            messages.error(request, "Wrong password")

            return redirect('/')


def create(request):

    if 'name' in request.session:

        return render(request,"create.html")
    else:
        return redirect("/")

    

def AddItem(request):

    print("adding item to database")
    # make sure no empty entries and longer than 3 characters

    #<<--------VALIDATIONS-------->>
    errors = Wish.objects.basic_validator(request.POST)
    print(" did i ever get here?")

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        print(errors)
        # redirect the user back to the form to fix the errors
        return redirect('/wish_items/create')
        
    else:
        print("Right before i build a new wish item -------------------")
        now = strftime("%Y-%m-%d %H:%M %p", gmtime())
        print("this is the time: ", now)
        new_wish = Wish(item = request.POST["item"],added_by_user = request.session['name'] , added_by = User.objects.get(id=request.session["id"]), date_added = now )
        print("before i save -------------------")
        new_wish.save()

        print(" i just created a new wish item!")
        return redirect("/dashboard")

def dashboard(request):

    if 'name' in request.session:
        my_items = Join.objects.filter(user_id = request.session['id'])
        my_items2 = Wish.objects.filter(added_by_user= request.session['name'])

        context = {
            "my_items" : my_items, "my_items2":my_items2, "items" : Wish.objects.exclude(added_by_user = request.session['name'])
        }

        return render(request, "dashboard.html", context = context)
    else:
        return redirect("/")

def show(request, id):
    print("i am in show")

    context = {
        "items" : Wish.objects.get(id =id), "Other_Users_Added_Items": Join.objects.filter(wish_id = id)
    }

    return render(request, "wish_item.html", context= context)


def AddToWishlist(request,id):
    
    print("i made it to AddToWishlist")
    print("Adding this id to my wish list: ", id )

    user = User.objects.get(id=request.session['id'])
    print("this is my user: ", user)

    wish = Wish.objects.get(id=id)

    new_wish = Join(user=user, wish=wish)
    new_wish.save()
    print(" i created a new wish item")

    return redirect("/dashboard")

def RemoveFromWishlist(request,id):
    print(" i made it to remove!!!!!!!!")

    item_to_remove = Join.objects.get(id=id)
    item_to_remove.delete()
    print("it's done! it's gone")

    return redirect("/dashboard")

def remove(request,id):
    print(" i made it to delete!!!!!!!!")
    print("this is my id: ", id)
    # b = Wish.objects.filter(id = int(id))

    # Wish.objects.raw("delete from wish_list_app_wish where id = "+id)    
    
    item_to_delete = Wish.objects.filter(id=id)
    print(item_to_delete.delete)
   
    item_to_delete.delete()
    print(" -=-=-=-=-=--=-=-=-=-=--=-=-=-=-=--=-=-=-=-=-==")
    
    return redirect("/dashboard")

def reset(request):
    print("i made it to reset")
    request.session.clear()
    return redirect("/")