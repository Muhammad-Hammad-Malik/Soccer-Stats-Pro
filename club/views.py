from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponseForbidden, HttpResponseRedirect
from .models import Player, FootballClub
from .forms import PlayerForm
from .forms import ClubSignUpForm ,PlayerStatsForm , InjuryForm
from .forms import FinanceForm , StaffForm
from .models import Staff , Injury
from django.urls import reverse
from django.utils.timezone import now


# the ladning page view that first loads when project runs
def landing_page(request):
    return render(request, 'club/landing_page.html')

# the sign up page acitivty that handles all the logic for sign up
def sign_up(request):
    if request.method == 'POST':
        form = ClubSignUpForm(request.POST)
        if form.is_valid():
            club = form.save()
            roles = ['head_coach', 'assistant_coach', 'gk_coach', 'physical_coach', 'fitness_coach']
            for role in roles:
                Staff.objects.create(club=club, role=role, name="John Doe")
            club_id = club.id
            response = redirect('admin_dashboard')
            response.set_cookie('club_id', club_id, max_age=3600 * 24) 
            print(f"New Club ID: {club_id}")
            return response
    else:
        form = ClubSignUpForm()
    return render(request, 'club/sign_up.html', {'form': form})

# the sign up page acitivty that handles all the logic for admin side log in
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            club = FootballClub.objects.get(club_name=username, admin_password=password)
            club_id = club.id
            response = redirect('admin_dashboard')  # Redirect to the admin dashboard
            response.set_cookie('club_id', club_id, max_age=3600 * 24)  # Store club_id in cookies
            return response
        except FootballClub.DoesNotExist:
            # If the club doesn't exist or the credentials are incorrect
            error_message = "Invalid credentials. Please try again."
            return render(request, 'club/admin_login.html', {'error': error_message})
    else:
        return render(request, 'club/admin_login.html')


# the sign up page acitivty that handles all the logic for sign up
def admin_dashboard(request):
    club_id = request.COOKIES.get('club_id')
    club = None
    if club_id:
        club = FootballClub.objects.filter(id=club_id).first()
    return render(request, 'club/admin_dashboard.html', {'club': club})


# the create player activty to handle all the backend logic
def create_player(request):
    club_id = request.COOKIES.get('club_id')
    if not club_id:
        return HttpResponseForbidden("You are not authorized to create players.")
    club = get_object_or_404(FootballClub, id=club_id)
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.club = club
            player.save()
            return redirect('admin_dashboard')
    else:
        form = PlayerForm()
    return render(request, 'club/create_player.html', {'form': form})


# View Players acitivty backend code
def view_players(request):
    club_id = request.COOKIES.get('club_id')
    if not club_id:
        return HttpResponseForbidden("You are not authorized to view players.")
    # Handle player deletion
    if request.method == "POST":
        player_id = request.POST.get('player_id')
        if player_id:
            try:
                player = Player.objects.get(id=player_id, club_id=club_id)
                player.delete()
                print(request, "Player deleted successfully.")
            except Player.DoesNotExist:
                print(request, "Player not found.")
        return HttpResponseRedirect(reverse('view_players'))  
    players = Player.objects.filter(club_id=club_id)
    return render(request, 'club/view_players.html', {'players': players})


def view_marketplace(request):
    club_id = request.COOKIES.get('club_id')
    query = request.GET.get('search', '')
    if club_id:
        # Exclude current club players from marketplace
        if query:
            players = Player.objects.filter(name__icontains=query).exclude(club__id=club_id)
        else:
            players = Player.objects.exclude(club__id=club_id)
    else:
        # If no club ID, allow all players 
        if query:
            players = Player.objects.filter(name__icontains=query)
        else:
            players = Player.objects.all()
    return render(request, 'club/view_marketplace.html', {'players': players, 'query': query})


# the finacnes acitivty that handles all the logic for backend
def view_finances(request):
    club_id = request.COOKIES.get('club_id')
    if not club_id:
        return HttpResponseForbidden("You are not authorized to view finances.")
    club = get_object_or_404(FootballClub, id=club_id)
    finances = club.finances.all()
    if request.method == 'POST':
        form = FinanceForm(request.POST)
        if form.is_valid():
            finance = form.save(commit=False)
            finance.club = club  
            finance.date = now().date()  
            finance.time = now().time()  
            finance.save()  
            return redirect('view_finances') 
        else:
            print(request, "There was an error with your form.")  
    else:
        form = FinanceForm() 
    return render(request, 'club/view_finances.html', {
        'finances': finances,
        'form': form
    })

# the view staff acitivty that handles all the logic for backend
def view_staff(request):
    club_id = request.COOKIES.get('club_id')
    if not club_id:
        return HttpResponseForbidden("You are not authorized to view staff.")
    
    club = FootballClub.objects.get(id=club_id)

    if request.method == 'POST':
        form = StaffForm(request.POST, club=club)  
        if form.is_valid():
            for role, name in form.cleaned_data.items():
                if name:  
                    staff, created = Staff.objects.update_or_create(
                        club=club, role=role, defaults={'name': name}
                    )
            return redirect('view_staff')  
    else:
        form = StaffForm(club=club) 
    return render(request, 'club/view_staff.html', {'form': form, 'club': club})

# Allows the analyst to log in
def analyst_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            club = FootballClub.objects.get(club_name=username)
            if club.analyst_password == password:
                club_id = club.id  
                response = redirect('analyst_dashboard') 
                response.set_cookie('club_id', club_id, max_age=3600 * 24) 
                return response
            else:
                error_message = "Invalid analyst credentials. Please try again."
        except FootballClub.DoesNotExist:
            # If the club doesn't exist
            error_message = "Invalid club name. Please try again."
        return render(request, 'club/analyst_login.html', {'error': error_message})
    else:
        return render(request, 'club/analyst_login.html')
    
# the dashboard for the analyst    
def analyst_dashboard(request):
    try:
        club_id = request.COOKIES.get('club_id')
        club = FootballClub.objects.get(id=club_id)
    except FootballClub.DoesNotExist:
        club = None
    return render(request, 'club/analyst_dashboard.html', {'club': club})

# allows the analyst to manage stats of his club's players
def manage_stats(request):
    try:
        club_id = request.COOKIES.get('club_id')
        club = FootballClub.objects.get(id=club_id)
        players = Player.objects.filter(club=club)
    except FootballClub.DoesNotExist:
        club = None
        players = []
    return render(request, 'club/manage_stats.html', {'club': club, 'players': players})

# allows the analyst to update stats
def update_stats(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    if request.method == 'POST':
        form = PlayerStatsForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('manage_stats') 
    else:
        form = PlayerStatsForm(instance=player)
    return render(request, 'club/update_stats.html', {'form': form, 'player': player})


# allows the analyst to view and create injurries 
def manage_injuries(request):
    club_id = request.COOKIES.get('club_id')
    if not club_id:
        return redirect('some_error_page')  
    # Filter injuries and players based on club_id
    injuries = Injury.objects.filter(player__club_id=club_id) 
    players = Player.objects.filter(club_id=club_id) 
    if request.method == 'POST':
        form = InjuryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_injuries')
    else:
        form = InjuryForm()
        form.fields['player'].queryset = players
    
    return render(request, 'club/manage_injuries.html', {
        'form': form,
        'injuries': injuries,
    })

# allows analyst to remove injuries
def delete_injury(request, injury_id):
    injury = Injury.objects.get(id=injury_id)
    injury.delete()
    return redirect('manage_injuries')
