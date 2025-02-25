from django.db import models
from django.utils.timezone import now


#the football club class for the db
class FootballClub(models.Model):
    club_name = models.CharField(max_length=255)
    club_location = models.CharField(max_length=255)  
    established_year = models.IntegerField()  
    admin_password = models.CharField(max_length=255)  
    analyst_password = models.CharField(max_length=255) 

    def __str__(self):
        return self.club_name

# the player model class for the db
class Player(models.Model):
    club = models.ForeignKey(FootballClub, on_delete=models.CASCADE)  # Fixed reference to FootballClub
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=100)

    # Stats fields
    goals = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    yellow_cards = models.PositiveIntegerField(default=0)
    red_cards = models.PositiveIntegerField(default=0)
    matches_played = models.PositiveIntegerField(default=0)
    minutes_played = models.PositiveIntegerField(default=0) 
    clean_sheets = models.PositiveIntegerField(default=0)  # Number of clean sheets for goalkeepers
    shots_on_target = models.PositiveIntegerField(default=0)
    passes_completed = models.PositiveIntegerField(default=0)
    tackles = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.name} ({self.position})'
    
# the marketplace model class for the db
class Marketplace(models.Model):
    club = models.ForeignKey(FootballClub, on_delete=models.CASCADE)  # Fixed reference to FootballClub
    item_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)





# the finance model class for the db
class Finance(models.Model):
    club = models.ForeignKey(
        'FootballClub', 
        on_delete=models.CASCADE, 
        related_name='finances'
    )
    name = models.CharField(max_length=255)  # Name of the transaction
    type = models.CharField(max_length=255)
    date = models.DateField(default=now)  # Default to today's date
    time = models.TimeField(default=now)  # Default to current time
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # Transaction amount

    def __str__(self):
        return f"{self.name} - {self.amount}"
    

# the staff model class for the db
class Staff(models.Model):
    ROLE_CHOICES = [
        ('head_coach', 'Head Coach'),
        ('assistant_coach', 'Assistant Coach'),
        ('gk_coach', 'Goalkeeper Coach'),
        ('physical_coach', 'Physical Coach'),
        ('fitness_coach', 'Fitness Coach'),
    ]

    club = models.ForeignKey(FootballClub, on_delete=models.CASCADE, related_name='staff_members')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.role} - {self.name}"

# the injury model class for the db
class Injury(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='injuries')
    name = models.CharField(max_length=255)  # Name of the injury
    duration = models.PositiveIntegerField()  # Duration in months
    
    def __str__(self):
        return f"{self.name} - {self.player.name}"