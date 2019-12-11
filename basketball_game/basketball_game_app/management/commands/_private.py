from basketball_game_app.models import Players, Teams
from faker import Factory
from random import randint
from datetime import date

TEAMS = (
    ("Miami Heat", 0, 0),
    ("Boston Celtics", 0, 0),
    ("Toronto Raptors", 0, 0),
    ("Atlanta Hawks", 0, 0),
    ("Orlando Magic", 0, 0),
    ("Indiana Pacers", 0, 0),
    ("New York Knikcs", 0, 0),
    ("Brooklyn Nets", 0, 0),
    ("Milwaukee Bucks", 0, 0),
    ("Chicago Bulls", 0, 0),
    ("Charlotte Hornets", 0, 0),
    ("Philadelphia 76ers", 0, 0),
    ("Washington Wizards", 0, 0),
    ("Detroit Pistons", 0, 0),
    ("Cleveland Cavaliers", 0, 0),

    ("Golden State Warriors", 0, 0),
    ("Utah Jazz", 0, 0),
    ("Denver Nuggets", 0, 0),
    ("Phoenix Suns", 0, 0),
    ("Sacramento Kings", 0, 0),
    ("Houston Rockets", 0, 0),
    ("Los Angeles Lakers", 0, 0),
    ("Los Angeles Clippers", 0, 0),
    ("Portland Trail Blazers", 0, 0),
    ("Memphis Grizzlies", 0, 0),
    ("San Antonio Spurs", 0, 0),
    ("New Orleans Pelicans", 0, 0),
    ("Dallas Mavericks", 0, 0),
    ("Minnesota Timberwolves", 0, 0),
    ("Oklahoma City Thunder", 0, 0),
)


def create_teams():
    for team in TEAMS:
        Teams.objects.create(name=team[0], games_played=team[1], games_won=team[2])


def create_name():
    fake = Factory.create("en_US")
    first_name = fake.first_name_male()
    last_name = fake.last_name()
    return first_name, last_name


def fake_date():
    year = randint(1980, 2000)
    month = randint(1, 12)
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = randint(1, 31)
    elif month == 2:
        day = randint(1, 28)
    else:
        day = randint(1, 30)
    return date(year=year, month=month, day=day)


def create_players(n):
    for team in Teams.objects.all():
        for player in range(n):
            birth_date = fake_date()
            first_name, last_name = create_name()
            Players.objects.create(first_name=first_name, last_name=last_name, team=team, date_of_birth=birth_date)
