from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from .forms import RegisterForm, BookForm, HolidayTimeForm
from django.shortcuts import redirect
from .models import Room


# home page
# Contains a search form to filter all rooms available on the db
def home(request):

    if request.method == "POST":
        form = HolidayTimeForm(request.POST,)

        if form.is_valid():
            form.save(commit=False,)

            startD = form.cleaned_data['startDate']
            endD = form.cleaned_data['endDate']
            city = form.cleaned_data['city']

            days = endD - startD
            days = days.days

            request.session['days'] = days
            request.session['city'] = city

            return redirect('/feed')
    else:
        form = HolidayTimeForm()
        return render(request, "book/home.html", {"form": form})


# Function that handles booking by users
def feed(request):
    # Get all rooms objects
    rooms = Room.objects.all()

    if request.method == "POST":

        _id = request.POST.get("id", "")

        # There's a form for each room containing the book button
        # Filter to find out which room is calling the function
        currentRoom = rooms.filter(id=_id)

        # Set the form correctly to update the right room
        form = BookForm(request.POST, instance=currentRoom[0])

        if form.is_valid():

            book = form.save(commit=False,)
            book.booked = True
            book.whoBooked = request.user.username
            # Uncomment below if you want all bookings validated on blockchain
            # book.writeOnChain()

            book.save()
            # form = BookForm()
        return render(request, "book/confirm.html", {"room": currentRoom[0]})
    else:
        form = BookForm()

        days = request.session.get('days', 1)
        city = request.session.get('city', '')

        return render(request, 'book/feed.html', {"days": days, "city": city, 'rooms': rooms, 'form': form})


def orders(request):
    # Get rooms booked by this user
    rooms = Room.objects.filter(whoBooked=request.user.username)
    # default value set after
    return render(request, 'book/orders.html', {'rooms': rooms, })


# registration form
def register(request):
    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        # initialise blank form and ip info
        form = RegisterForm()
    # render the page
    return render(request, "book/register.html", {"form": form,})


# handle logout
def logoutReq(request):
    logout(request)
    return redirect("/")


# handle login
def loginReq(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:

                login(request, user)
                return redirect('/')
            else:
                return render(request, "book/login.html", {"form": form})
        else:
            return render(request, "book/login.html", {"form": form})

    form = AuthenticationForm()
    return render(request, "book/login.html", {"form": form})
