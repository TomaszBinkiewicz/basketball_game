from django.db import models
from datetime import date


class Group(models.Model):
    name = models.CharField(max_length=64)


class Teams(models.Model):
    name = models.CharField(max_length=64)
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    conference = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True)

    @property
    def games_lost(self):
        return self.games_played - self.games_won

    @property
    def wins_percentage(self):
        return self.games_won / self.games_played


class Players(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=128)
    date_of_birth = models.DateField()
    team = models.ForeignKey(Teams, on_delete=models.DO_NOTHING)

    @property
    def age(self):
        now = date.today()
        if now.month > self.date_of_birth.month or (
                now.month == self.date_of_birth.month and now.day >= self.date_of_birth.day):
            age = now.year - self.date_of_birth.year
        else:
            age = now.year - self.date_of_birth.year - 1
        return age


class Quarter(models.Model):
    score_team_home = models.IntegerField()
    score_team_away = models.IntegerField()


class Games(models.Model):
    team_home = models.ForeignKey(Teams, on_delete=models.SET_NULL, null=True, related_name='home_games')
    team_away = models.ForeignKey(Teams, on_delete=models.SET_NULL, null=True, related_name='away_games')
    q1 = models.ForeignKey(Quarter, on_delete=models.CASCADE, related_name='first_q')
    q2 = models.ForeignKey(Quarter, on_delete=models.CASCADE, related_name='second_q')
    q3 = models.ForeignKey(Quarter, on_delete=models.CASCADE, related_name='third_q')
    q4 = models.ForeignKey(Quarter, on_delete=models.CASCADE, related_name='fourth_q')


class Overtime(models.Model):
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    score_team_home = models.IntegerField()
    score_team_away = models.IntegerField()


class Stats(models.Model):
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    player = models.ForeignKey(Players, on_delete=models.SET_NULL, null=True)

    minutes_played = models.IntegerField(default=0)

    three_pointers_made = models.IntegerField(default=0)
    three_pointers_attempted = models.IntegerField(default=0)
    two_pointers_made = models.IntegerField(default=0)
    two_pointers_attempted = models.IntegerField(default=0)
    free_throws_made = models.IntegerField(default=0)
    free_throws_attempted = models.IntegerField(default=0)

    off_rebounds = models.IntegerField(default=0)
    def_rebounds = models.IntegerField(default=0)

    assists = models.IntegerField(default=0)
    steals = models.IntegerField(default=0)
    blocks = models.IntegerField(default=0)
    turnovers = models.IntegerField(default=0)

    personal_fouls = models.IntegerField(default=0)

    @property
    def total_rebounds(self):
        return self.off_rebounds + self.def_rebounds

    @property
    def points(self):
        return self.free_throws_made * 1 + self.two_pointers_made * 2 + self.three_pointers_made * 3

    @property
    def fg_percentage(self):
        return (self.three_pointers_made + self.two_pointers_made) / (
                self.three_pointers_attempted + self.two_pointers_attempted)

    @property
    def ft_percentage(self):
        return self.free_throws_made / self.free_throws_attempted

    @property
    def p3_percentage(self):
        return self.three_pointers_made / self.three_pointers_attempted
