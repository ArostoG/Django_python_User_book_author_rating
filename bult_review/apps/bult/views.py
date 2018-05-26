# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,HttpResponse 
from django.contrib import messages
from django.db.models import Q
import bcrypt
import re
from time import gmtime, strftime
from datetime import datetime
from . models import *

# Create your views here.
def index(request):
    return render(request, 'bult/index.html')

def register(request):
    if request.method == "POST":
        error = False
        if len(request.POST['name']) < 1 or len(request.POST['alisa']) < 1 or len(request.POST['password']) < 1 or len(request.POST['password_confirmation']) < 1:
            messages.error(request, "Fields cannot be blank!")
            error = True

        if not request.POST['name'].isalpha():
            messages.error(request, "First name and last name must be non numeric characters")
            error = True
        if not request.POST['alisa'].isalpha():
            messages.error(request, "First name and last name must be non numeric characters")
            error = True
        if len(request.POST['password']) < 8:
            messages.error(request, "Password must contain at least 8 characters; and at least 1 number, 1 letter, and 1 special character!")
            error = True
        if request.POST['password_confirmation'] != request.POST['password']:
            messages.error(request, "Passwords do not match!")
            error = True
        if error:
            return redirect('/')
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            print hashed_pw
            users=User.objects.create(name=request.POST['name'],alisa=request.POST['alisa'],email=request.POST['email'],password=hashed_pw)
            request.session['user_id']=users.id
            print(request.session['user_id'])
    
    return redirect('/')

def login(request):
    if request.method == "POST":
        user = User.objects.filter(email = request.POST["email"])
        if len(user)> 0:
            user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(),user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/books')
            else:
                messages.error(request, "user_name and/or password is incorrect!")
                return redirect('/')
        else:
            messages.error(request, "user_name and/or password is incorrect!")
            return redirect('/')

    else:
        messages.error(request, "user_name is incorrect!")
        return redirect('/')

def books(request):
    user = User.objects.get(id=request.session['user_id'])
    others_books=Book.objects.all()
    
    user_review=Review.objects.filter(users=user)
    
    context ={
        'users':user,
        'books':others_books,
        'recent': user_review,

     

    }

    return render(request, 'bult/books.html',context)


def logout(request):
    request.session.clear()
    print(request.session.clear())
    return redirect('/')


def add(request):
    author=Author.objects.all()
    context={
    'Old_author':author,
    }


    return render(request, 'bult/add.html',context)


def record(request):

    user=User.objects.get(id=request.session['user_id'])


    if request.POST['add_aouthor']==request.POST['old_author']:

         author=Author.objects.get(auth_name=request.POST['old_author'])

    elif len(request.POST['add_aouthor']) >0:

        author=Author.objects.create(auth_name=request.POST['add_aouthor'])
        
    else:
        author=Author.objects.get(auth_name=request.POST['old_author'])



    book=Book.objects.create(tital=request.POST['book_tital'],author=author)
 

    review=Review.objects.create(review=request.POST['review'],rating=request.POST['rating'],books=book,users=user)
    

    return redirect('/books/'+str(book.id))

def detail(request,book_id):
    user=User.objects.get(id=request.session['user_id'])
    book=Book.objects.get(id=book_id)
    review = Review.objects.filter(books=book,users=user)
   

    context={
        'books':book,
        'reviews':review,

    }

    return render(request, 'bult/review.html',context)


def review(request,book_id):
    user=User.objects.get(id=request.session['user_id'])
    book=Book.objects.get(id=book_id)
    review=Review.objects.create(review=request.POST['review'],rating=request.POST['rating'],books=book,users=user)


    return redirect('/books')

def user(request,user_id):
    user=User.objects.get(id=user_id)
    review = Review.objects.filter(users=user)
    count = review.count()


    context={
        'users':user,
        'reviews':review,
        'counter':count,

    }

    return render(request, 'bult/user.html',context)

def delete(request,review_id):
    user=User.objects.get(id=request.session['user_id'])
    review=Review.objects.get(id=review_id)
    review.delete()


    return redirect('/books/'+str(review.books.id))
  
