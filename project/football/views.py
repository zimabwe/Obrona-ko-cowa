from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
# Create your views here.

from .models import Team, Game



def league_table(request):
    teams = Team.objects.order_by('-points')
    html_response = """
        <html>
            <head>
                <title>League table</title>
            </head>
            <body>
    """

    if len(teams) > 0:
        html_response += """
            <table>
        """

        for team in teams:
            html_response += """
                <tr>
                    <td>{}</td>
                    <td>{}</td>
                </tr>
            """.format(team.name, team.points)

        html_response += """
            </table>
        """

    return HttpResponse(html_response)


def games_played(request):
    if request.method == "GET":
        response = HttpResponse()
        try:
            id = int(request.GET.get('id'))
        except ValueError:
            return HttpResponse("incorrect id")

        try:
            team = Team.objects.get(id=id)
        except:
            return HttpResponse("team does not exists")

        games_home = Game.objects.filter(team_home=team)
        games_away = Game.objects.filter(team_away=team)




        response.write("<table>")
        for game in games_home:
            response.write("""
                <tr>
                    <td> {} </td>
                    <td> {} </td>
                    <td> {} - {} </td>
                </tr>
            """.format(game.team_home.name, game.team_away.name, game.team_home_goals, game.team_away_goals))
        response.write("</table>")

        return response

    return HttpResponse("")

def add_game(request):
    if request.method == "GET":
        return HttpResponse("""
            <form>
                <label>
                    Home team:
                    {}
                </label> <br />
                <label>
                    Away team:
                    {}
                </label> <br />
                <label>
                    Home team goals:
                    <input type="number" name="home_team_goals" />
                </label>
                <label>
                    Away team goals:
                    <input type="number" name="away_team_goals" />
                </label>
                <input type="submit" value="Add" />
            </form>
        """.format(generate_select("home_team"), generate_select("away_team")))
    return HttpResponse("")


def generate_select(select_name):
    output = """<select name="{}">""".format(select_name)
    teams = Team.objects.all()
    for team in teams:
        output += """<option value="{}">{}</option>""".format(team.id, team.name)
    output += """</select>"""
    return output


@csrf_exempt
def add_game(request):
    if request.method == "GET":
        return HttpResponse("""
            <form action="" method="POST">
                <label>
                    Home team:
                    {}
                </label> <br />
                <label>
                    Away team:
                    {}
                </label> <br />
                <label>
                    Home team goals:
                    <input type="number" name="home_team_goals" />
                </label>
                <label>
                    Away team goals:
                    <input type="number" name="away_team_goals" />
                </label>
                <input type="submit" value="Add" />
            </form>
        """.format(generate_select("home_team"), generate_select("away_team")))
    else:
        home_team_id = request.POST.get('home_team')
        away_team_id = request.POST.get('away_team')

        try:
            home_team_goals = int(request.POST.get('home_team_goals'))
            away_team_goals = int(request.POST.get('away_team_goals'))
        except ValueError:
            return HttpResponse("incorrect data")

        if home_team_id == away_team_id:
            return HttpResponse("same team selected")

        try:
            home_team = Team.objects.get(id=home_team_id)
            away_team = Team.objects.get(id=away_team_id)
        except ValueError:
            return HttpResponse("selected team does not exist")

        game = Game()
        game.team_home = home_team
        game.team_away = away_team
        game.team_home_goals = home_team_goals
        game.team_away_goals = away_team_goals
        game.save()

        return HttpResponse("gave saved")

    return HttpResponse("")


def generate_select(select_name):
    output = """<select name="{}">""".format(select_name)
    teams = Team.objects.all()
    for team in teams:
        output += """<option value="{}">{}</option>""".format(team.id, team.name)
    output += """</select>"""
    return output


@csrf_exempt
def add_game(request):
    if request.method == "GET":
        return HttpResponse("""
            <form action="" method="POST">
                <label>
                    Home team:
                    {}
                </label> <br />
                <label>
                    Away team:
                    {}
                </label> <br />
                <label>
                    Home team goals:
                    <input type="number" name="home_team_goals" />
                </label>
                <label>
                    Away team goals:
                    <input type="number" name="away_team_goals" />
                </label>
                <input type="submit" value="Add" />
            </form>
        """.format(generate_select("home_team"), generate_select("away_team")))
    else:
        home_team_id = request.POST.get('home_team')
        away_team_id = request.POST.get('away_team')

        try:
            home_team_goals = int(request.POST.get('home_team_goals'))
            away_team_goals = int(request.POST.get('away_team_goals'))
        except ValueError:
            return HttpResponse("incorrect data")

        if home_team_id == away_team_id:
            return HttpResponse("same team selected")

        try:
            home_team = Team.objects.get(id=home_team_id)
            away_team = Team.objects.get(id=away_team_id)
        except ObjectDoesNotExist:
            return HttpResponse("selected team does not exist")

        # here I modified the game model
        game = Game()
        game.team_home = home_team
        game.team_away = away_team
        game.team_home_goals = home_team_goals
        game.team_away_goals = away_team_goals
        game.save()

        # here I modified the team model
        if home_team_goals > away_team_goals:
            home_team.points += 3
            home_team.save()
            # team home wins +3pkt
        elif home_team_goals < away_team_goals:
            away_team.points += 3
            away_team.save()
            # away home wins +3pkt
        else:
            home_team.points += 1
            away_team.points += 1
            home_team.save()
            away_team.save()

        return HttpResponse("gave saved")

    return HttpResponse("")



@csrf_exempt
def modify_team(request):
    if request.method == "GET":
        team_id = request.GET.get('id')
        if team_id is None:
            return HttpResponse("team does not exist")
        try:
            team = Team.objects.get(id=team_id)
        except ObjectDoesNotExist:
            return HttpResponse("team does not exist")

        return HttpResponse("""
            <form action="" method="POST">
                <input name="team_id" type="hidden" value="{}" />
                <label>
                    Name:
                    <input type="text" name="name" value="{}"/>
                </label>
                <label>
                    Points:
                    <input type="number" name="points" value="{}" />
                </label>
                <input type="submit" value="Edit" />
            </form>
        """.format(team.id, team.name, team.points))
    else:
        team_id = request.POST.get('team_id')
        name = request.POST.get('name')
        points = request.POST.get('points')
        if name is None:
            return HttpResponse("incorrect name")
        if team_id is None:
            return HttpResponse("incorrect team_id")

        try:
            team = Team.objects.get(id=team_id)
        except ObjectDoesNotExist:
            return HttpResponse("team does not exist")

        team.name = name
        team.points = points
        team.save()

        return HttpResponse("team modified")

@csrf_exempt
def set_as_favourite(request):
    if request.method == "GET":
        team_id = request.GET.get('id')
        if team_id is None or team_id == "":
            return HttpResponse("team id is not correct")

        try:
            team_id = int(team_id)
        except ValueError:
            return HttpResponse("team id is not correct")

        try:
            Team.objects.get(id=team_id)
        except ObjectDoesNotExist:
            return HttpResponse("team does not exists")

        response = HttpResponse("team set as favorite")
        exp = datetime.datetime.now() + datetime.timedelta(days=365)
        response.set_cookie("favorite_team", team_id, expires=exp)
        return response



class show_tem_statistics(View):
    def get(self, request):
        if request.method == "GET":
            team_id = request.GET.get('id')
            if team_id is None or team_id == "":
                return HttpResponse("team id is not correct")

    def post(self,request):
        try:
            team_id = int(team_id)
        except ValueError:
            return HttpResponse("team id is not correct")

        try:
            Team.objects.get(id=team_id)
        except ObjectDoesNotExist:
            return HttpResponse("team does not exists")

