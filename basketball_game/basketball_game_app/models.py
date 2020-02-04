from django.db import models

from datetime import date


class Group(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


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
        return round(self.games_won / self.games_played, 3)

    def __str__(self):
        return self.name


class Players(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=128)
    date_of_birth = models.DateField()
    team = models.ForeignKey(Teams, on_delete=models.SET_NULL, null=True)

    @property
    def age(self):
        now = date.today()
        if now.month > self.date_of_birth.month or (
                now.month == self.date_of_birth.month and now.day >= self.date_of_birth.day):
            age = now.year - self.date_of_birth.year
        else:
            age = now.year - self.date_of_birth.year - 1
        return age

    def __str__(self):
        return f'{self.last_name} {self.first_name}, {self.team}'


class Games(models.Model):
    date = models.DateField()
    team_home = models.ForeignKey(Teams, on_delete=models.SET_NULL, null=True, related_name='home_games')
    team_away = models.ForeignKey(Teams, on_delete=models.SET_NULL, null=True, related_name='away_games')
    team_home_score = models.IntegerField(null=True)
    team_away_score = models.IntegerField(null=True)

    def get_team_home_stats(self):
        return self.teamstats_set.filter(team=self.team_home)

    def get_team_away_stats(self):
        return self.teamstats_set.filter(team=self.team_away)

    def __str__(self):
        return f'{self.date}, {self.team_home} vs {self.team_away}'


class Part(models.Model):
    choices = (
        (1, 'Q1'),
        (2, 'Q2'),
        (3, 'Q3'),
        (4, 'Q4'),
        (5, 'OT'),
    )
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    name = models.IntegerField(choices=choices)
    score_team_home = models.IntegerField()
    score_team_away = models.IntegerField()


class Stats(models.Model):
    game = models.ForeignKey(Games, on_delete=models.CASCADE)

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
    technical_fouls = models.IntegerField(default=0)

    @property
    def total_rebounds(self):
        return self.off_rebounds + self.def_rebounds

    @property
    def points(self):
        return self.free_throws_made * 1 + self.two_pointers_made * 2 + self.three_pointers_made * 3

    @property
    def fg_percentage(self):
        if self.three_pointers_attempted + self.two_pointers_attempted == 0:
            return 0
        return round((self.three_pointers_made + self.two_pointers_made) / (
                self.three_pointers_attempted + self.two_pointers_attempted), 2)

    @property
    def ft_percentage(self):
        if self.free_throws_attempted == 0:
            return 0
        return round(self.free_throws_made / self.free_throws_attempted, 2)

    @property
    def p3_percentage(self):
        if self.three_pointers_attempted == 0:
            return 0
        return round(self.three_pointers_made / self.three_pointers_attempted, 2)

    class Meta:
        abstract = True


class PlayerStats(Stats):
    player = models.ForeignKey(Players, on_delete=models.SET_NULL, null=True)
    minutes_played = models.IntegerField(default=0)


class TeamStats(Stats):
    team = models.ForeignKey(Teams, on_delete=models.SET_NULL, null=True)
