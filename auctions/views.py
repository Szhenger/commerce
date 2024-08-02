from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from decimal import Decimal
from django.contrib.auth.decorators import login_required

from .models import User, Category, Bid, Listing, Comment


def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def sold(request):
    listings = Listing.objects.filter(is_active=False)
    return render(request, "auctions/sold.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]

        # Ensures that request is valid
        if not (title and description and price):
            return render(request, "auctions/error.html", {
                "error": "HTML 403 Error",
                "message": "Every listing must have a title, description, and price"
            })

        # Creates a Listing request instance
        image = request.POST["image"]
        seller = request.user
        category = Category.objects.get(category_name=request.POST["category"])

        bid = Bid(
            bid=price,
            bidder=seller
        )
        bid.save()
        listing = Listing(
            title=title,
            description=description,
            price=bid,
            seller=seller,
            image=image,
            category=category
        )
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": categories
        })


def categorize(request):
    if request.method == "POST":

        # Finds active listings by category
        category = Category.objects.get(
            category_name=request.POST["category"]
        )
        listings = Listing.objects.filter(
            is_active=True,
            category=category
        )
        return render(request, "auctions/index.html", {
            "listings": listings
        })
    else:

        # Renders page to find by category
        categories = Category.objects.all()
        return render(request, "auctions/categorize.html", {
            "categories": categories
        })


def listing(request, id):
    listing = Listing.objects.get(pk=id)
    in_list = (request.user in listing.watchlist.all())
    is_seller = (request.user.username == listing.seller.username)
    comments = Comment.objects.filter(listing=listing)

    # Renders the listing on a page
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "alert": f"Congratulations! {listing.price.bidder.username} won this Auction!",
        "in_list": in_list,
        "is_seller": is_seller,
        "comments": comments
    })


@login_required
def remove(request, id):
    listing = Listing.objects.get(pk=id)
    listing.watchlist.remove(request.user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


@login_required
def add(request, id):
    listing = Listing.objects.get(pk=id)
    listing.watchlist.add(request.user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


@login_required
def watchlist(request):
    listings = request.user.list.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


@login_required
def bid(request, id):
    listing = Listing.objects.get(pk=id)
    bid = request.POST["bid"]

    # Ensures bid is greater than price
    if Decimal(bid) > Decimal(listing.price.bid):
        price = Bid(
            bid=bid,
            bidder=request.user
        )
        price.save()
        listing.price = price
        listing.save()
        return render(request, "auctions/success.html", {
            "success": "HTML 200 Status",
            "message": "Good News! Your Bid is now the Current Bid!"
        })
    else:
        return render(request, "auctions/error.html", {
            "error": "HTML 403 Error",
            "message": "Your Bid must be greater than the Current Bid!"
        })

@login_required
def comment(request, id):
    comment = Comment(
        listing=Listing.objects.get(pk=id),
        comment=request.POST["comment"],
        commenter=request.user
    )
    comment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))


@login_required
def close(request, id):
    listing = Listing.objects.get(pk=id)

    # Ensures the close request is from seller
    is_seller = (request.user.username == listing.seller.username)
    if is_seller:
        listing.is_active = False
        listing.save()
        return render(request, "auctions/success.html", {
            "success": "HTML 200 Status",
            "message": "Congratulations, your auction has been sold!"
        })
    else:
        return HttpResponseRedirect(reverse("listing", args=(id, )))
