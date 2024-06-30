from django.db import models

# Create your models here.
class Sport(models.Model):
    name = models.CharField(default="", max_length=255)
    def __str__(self) -> str:
        return self.name
    

class Team(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    name = models.CharField(default="", max_length=255)

    def __str__(self) -> str:
        return self.name

class Player(models.Model):
    name = models.CharField(default="", max_length=255)
    pic = models.ImageField(upload_to="sports/",default=None, blank=True, null=True)

    def __str__(self) -> str:
        return self.name
    

class Match(models.Model):
    name = models.CharField(default="", max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    status = models.CharField(default="pending", max_length=10)
    
    def __str__(self) -> str:
        return self.name

class TeamPlayer(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.match} {self.team}, player : {self.player}"


class Score(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    inning = models.CharField(default="1", max_length=2)
    total_score = models.IntegerField(default=0)
    over = models.IntegerField(default=0)
    current_over = models.DecimalField(default=0,max_digits=3, decimal_places=1, db_index=True)
    status = models.CharField(default="not started", max_length=15)
    win_loss = models.CharField(default="", max_length=5, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.match.name} {self.match.team}'
    

class ScoreAdd(models.Model):
    score = models.ForeignKey(Score, on_delete=models.CASCADE)
    ball = models.IntegerField(default=0)
    run = models.IntegerField(default=0)
    comment = models.CharField(default="",max_length=10)

    def __str__(self) -> str:
        return f'{self.score.match.team}'

# pic = models.ImageField(upload_to="sports/",default=None, blank=True, null=True)
