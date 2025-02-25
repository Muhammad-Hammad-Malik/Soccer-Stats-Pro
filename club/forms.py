from django import forms
from .models import FootballClub
from .models import Player
from .models import Finance,Staff
from .models import Injury

# the sign up form for the club
class ClubSignUpForm(forms.ModelForm):
    class Meta:
        model = FootballClub
        fields = ['club_name', 'club_location', 'established_year', 'admin_password', 'analyst_password']
        widgets = {
            'admin_password': forms.PasswordInput(),
            'analyst_password': forms.PasswordInput(),
        }
#the player creation form
class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'position', 'goals', 'assists', 'yellow_cards', 
                  'red_cards', 'matches_played', 'minutes_played', 
                  'clean_sheets', 'shots_on_target', 'passes_completed', 
                  'tackles']
        
#the finance creation form        
class FinanceForm(forms.ModelForm):
    # Add the choices for the 'type' field
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    type = forms.ChoiceField(
        choices=TRANSACTION_TYPE_CHOICES,  # Set the choices for dropdown
        widget=forms.Select(attrs={'class': 'form-select'})  # Bootstrap 5 class for styling
    )
    class Meta:
        model = Finance
        fields = ['name', 'type', 'amount']

#the staff updation form
class StaffForm(forms.Form):  # Use forms.Form instead of forms.ModelForm
    head_coach = forms.CharField(label="Head Coach", required=False)
    assistant_coach = forms.CharField(label="Assistant Coach", required=False)
    gk_coach = forms.CharField(label="Goalkeeper Coach", required=False)
    physical_coach = forms.CharField(label="Physical Coach", required=False)
    fitness_coach = forms.CharField(label="Fitness Coach", required=False)

    def __init__(self, *args, **kwargs):
        club = kwargs.pop('club', None)  # Get the club dynamically
        super().__init__(*args, **kwargs)

        if club:
            # Fetch staff data based on the club
            staff_members = Staff.objects.filter(club=club)
            for staff in staff_members:
                # Set the field values to match the staff member's name if data exists
                if staff.role == 'head_coach':
                    self.fields['head_coach'].initial = staff.name
                elif staff.role == 'assistant_coach':
                    self.fields['assistant_coach'].initial = staff.name
                elif staff.role == 'gk_coach':
                    self.fields['gk_coach'].initial = staff.name
                elif staff.role == 'physical_coach':
                    self.fields['physical_coach'].initial = staff.name
                elif staff.role == 'fitness_coach':
                    self.fields['fitness_coach'].initial = staff.name
                    
# the stats updation form
class PlayerStatsForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['position', 'goals', 'assists', 'yellow_cards', 
                  'red_cards', 'matches_played', 'minutes_played', 
                  'clean_sheets', 'shots_on_target', 'passes_completed', 
                  'tackles']

#injury creation form
class InjuryForm(forms.ModelForm):
    class Meta:
        model = Injury
        fields = ['player', 'name', 'duration']
