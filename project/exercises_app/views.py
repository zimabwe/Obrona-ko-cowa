from urllib import request

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.views import View
from .models import Article, Band, GENERE
from django.utils.decorators import method_decorator


def get_articles(request):
    articles = Article.objects.filter(status=2)

    html_response = """
        <html>
            <head>
                <title>List of articles</title>
            </head>
            <body>
    """

    if len(articles) > 0:
        html_response += """
            <table border="1">
                <thead>
                    <td>Title</td>
                    <td>Author</td>
                    <td>Published date</td>
                </thead>
                <tbody>
        """

        for article in articles:
            html_response += """
                <tr>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                </tr>
            """.format(article.title, article.author, article.published_date_start)

        html_response += """
                </tbody>
            </table>
        """

    html_response += """
            </body>
        </html>
    """

    return HttpResponse(html_response)


def show_band(request, id):
    html_response = """
        <html>
            <head>
                <title>Band</title>
            </head>
            <body>
    """

    # get band based on id
    band = Band.objects.get(id=id)

    html_response += """
        <h1>{}</h1>
        <h2>{} {}</h2>
    """.format(band.name, band.year, get_genre_name(band.genre))

    print(type(band.genre))

    html_response += """
            </body>
        </html>
    """

    return HttpResponse(html_response)


def get_genre_name(id):
    for single_genre in GENERE:
        if single_genre[0] == id:
            return single_genre[1]


def numbers(request):
    if request.method == "GET":
        response = HttpResponse
        start = request.GET('start')
        end = request.GET('end')
        for elem in range(int(start), int(end) + 1):
            response.write("{}<br />", format(elem))
        return response


def multiplication_table(request):
    if request.method == "GET":
        response = HttpResponse()
        width = request.GET.get('width')
        height = request.GET.get('height')

        if width is None or height is None:
            return HttpResponse("incorrect parameters")

        try:
            width = int(width)
            height = int(height)
        except ValueError:
            return HttpResponse("do you type integers?")

        response.write("<table>")
        for i in range(1, height + 1):
            response.write("<tr>")
            for j in range(1, width + 1):
                response.write("<td>{}</td>".format(i * j))
            response.write("</tr>")

        return response
    else:
        return HttpResponse("")


def form_test(request):
    if request.method == "GET":
        return HttpResponse("""
            <form action="" method="POST">
                <label>
                    Name:
                    <input type="text" name="name" />
                </label>
                <label>
                    Surname:
                    <input type="text" name="surname" />
                </label>
                <input type="submit" value="Send" />
            </form>
        """)
    else:
        name = request.POST.get('name')
        surname = request.POST.get('surname')

        if name and surname:
            return HttpResponse("Hello, {} {}".format(name, surname))

        return HttpResponse("error")

@csrf_exempt
def cel_far(request):
    if request.method == "GET":
        return HttpResponse("""
            <form action="" method="POST">
                <label>
                    Temperatura:
                    <input type="number" min="0.00" step="0.01" name="degrees">
                </label>
                <input type="submit" name="convertionType" value="celcToFahr">
                <input type="submit" name="convertionType" value="FahrToCelc">
            </form>
        """)
    else:
        degrees = float(request.POST.get('degrees'))
        convertion_type = request.POST.get('convertionType')
        if convertion_type == "celcToFahr":
            return HttpResponse("Temperatura w Fahrenheitach: {}".format(degrees * 9 / 5 + 32))
        else:
            return HttpResponse("Temperatura w Celcjuszach: {}".format((degrees - 32) * (5 / 9)))


def set_session(request):
    request.session['counter'] = 0
    return HttpResponse("session set")


def delete_session(request):
    del request.session['counter']
    return HttpResponse("session deleted")

def show_session(request):
    counter = request.session.get('counter')
    if counter is None:
        return HttpResponse("session does not set")

    counter = counter + 1
    request.session['counter'] = counter
    return HttpResponse("session modified {}".format(counter))



@csrf_exempt
def login(request):
    if request.method == "GET":
        loggedUser = request.session.get('loggedUser')
        if loggedUser is None:
            return HttpResponse("""
            <form action="" method="POST">
                <label>
                    Imię:
                    <input type="text" name="name">
                </label>
                <input type="submit">
            </form>""")
        else:
            return HttpResponse("hello, {}".format(loggedUser))
    else:
        # POST
        name = request.POST.get('name')
        if name is None:
            return HttpResponse("incorrect name")
        request.session['loggedUser'] = name
        return HttpResponse("your name {} has been saved in session".format(name))

@csrf_exempt
def add_to_session(request):
    if request.method == "GET":
        return HttpResponse("""
        <form action="#" method="POST">
            <label>
                Klucz:
                <input type="text" name="key">
            </label>
            <label>
                Wartość:
                <input type="text" name="value">
            </label>
            <input type="submit">
        </form>
        """)
    else:
        # powinien dodawać do sesji przesłaną wartość (pod odpowiedni klucz).
        key = request.POST.get('key')
        value = request.POST.get('value')

        if key is None or value is None:
            return HttpResponse("incorrect values")

        request.session[key] = value

        return HttpResponse("session saved")


def show_all_session(request):
    response = HttpResponse()
    response.write("<table>")
    for key, value in request.session.items():
        response.write("""<tr>
            <td> {}</td>
            <td> {}</td>
        </tr>""".format(key, value))
    response.write("</table>")
    return response



def set_cookie(request):
    response = HttpResponse("cookie has been send")
    response.set_cookie("User", "Mateusz")
    return response


def show_cookie(request):
    user = request.COOKIES.get('User')
    if user is None:
        return HttpResponse("cookie has not been set")
    return HttpResponse("hello, {}".format(user))


def delete_cookie(request):
    response = HttpResponse("cookie has been deleted")
    response.delete_cookie("User")
    return response


@csrf_exempt
def add_to_cookie(request):
    if request.method == "GET":
        return HttpResponse(""" 
        <form action="#" method="POST">
            <label>
                Klucz:
                <input type="text" name="key">
            </label>
            <label>
                Wartość:
                <input type="text" name="value">
            </label>
            <input type="submit" name="convertionType">
        </form>   
        """)
    else:
        key = request.POST.get('key')
        value = request.POST.get('value')

        if key is None or value is None:
            return HttpResponse("incorrect values")

        response = HttpResponse("Ciasteczko zostało dodane: {}={}".format(key, value))
        response.set_cookie(key, value)
        return response

def show_all_session_cookie(request):
    response = HttpResponse()
    response.write("<table>")
    for key, value in request.COOKIES.items():
        response.write("""<tr>
            <td> {}</td>
            <td> {}</td>
        </tr>""".format(key, value))
    response.write("</table>")
    return response

@method_decorator(csrf_exempt, name='dispatch')
class NameForm(View):
    def get(self, request):
        return HttpResponse("""
            <form action="" method="POST">
                <label>
                    Name:
                    <input type="text" name="name" />
                </label>
                <label>
                    Surname:
                    <input type="text" name="surname" />
                </label>
                <input type="submit" value="Send" />
            </form>
        """)

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')

        if name and surname:
            return HttpResponse("Hello, {} {}".format(name, surname))

        return HttpResponse("error")




@method_decorator(csrf_exempt, name='dispatch')
class Newcelcius(View):
    def get(self, request):
        return HttpResponse("""
                    <form action="" method="POST">
                        <label>
                            Temperatura:
                            <input type="number" min="0.00" step="0.01" name="degrees">
                        </label>
                        <input type="submit" name="convertionType" value="celcToFahr">
                        <input type="submit" name="convertionType" value="FahrToCelc">
                    </form>
                """)

    def post(self, request):
        degrees = float(request.POST.get('degrees'))
        convertion_type = request.POST.get('convertionType')
        if convertion_type == "celcToFahr":
            return HttpResponse("Temperatura w Fahrenheitach: {}".format(degrees * 9 / 5 + 32))
        else:
            return HttpResponse("Temperatura w Celcjuszach: {}".format((degrees - 32) * (5 / 9)))


class AddBand(View):
    def get(self, request):
        return HttpResponse("""
            <form action="" method="POST">
                <label>
                    Name:
                    <input type="text" name="name" />
                </label>
                <label>
                    Year:
                    <input type="number" name="year" />
                </label>
                 <label>
                    Is the team still active?:
                    <input type="checkbox" name="still_active" />
                </label>
                <label>
                    Select genre:
                    {}
                </label>
                <input type="submit" value="send" />
            </form>
        """.format(get_select_for_genre()))
    def post(self, request):
        name = request.POST.get('name')
        year = request.POST.get('year')
        still_active = request.POST.get('still_active')
        genre = request.POST.get('genre')

        if still_active == 'on':
            still_active = True
        else:
            still_active = False

        band = Band()
        band.name = name
        band.year = year
        band.still_active = still_active
        band.genre = genre
        band.save()

        return HttpResponse("Band save")


def get_select_for_genre():
    response = """<select name="genre">"""
    for elem in GENERE:
        response += """<option value="{}">{}</option>""".format(elem[0], elem[1])
    response += "</select>"
    return response

