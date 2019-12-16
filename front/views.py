from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import Http404, HttpResponse
from .models import Games, Board
from sea.settings import BOARD_SIZE


def showmain(request, *args, **kwargs):
    from .forms import LoginRegForm
    form = LoginRegForm()
    return render(request, "index.html", {
        "ulist": User.objects.all().order_by("username"),
        'form': form,
    })

def my_logout(req):
    logout(req)
    return redirect(reverse("main"))

def continue_game(request, *args, **kwargs):
    if request.user.is_authenticated:
        if Games.objects.filter( Q(board1__user=request.user) | Q(board2__user=request.user) | Q(board2=None)  ).filter(done=False, pk=kwargs.get('game_id')).exists():
            tek_game = Games.objects.get(pk=kwargs['game_id'])
            if tek_game.board1.user != request.user and tek_game.board2 is None:
                b = Board.objects.create(user=request.user, ready_to_play=False, ships="[]", )
                tek_game.board2 = b
                tek_game.save()

            print("tek game exist")
            if request.method == 'POST':
                if 'ships' in request.POST:
                    if tek_game.board1.user == request.user:
                        if tek_game.board1.brd.can_start_game:
                            messages.add_message(request, messages.WARNING, 'Нельзя менять позиции кораблей после установки!')
                        else:
                            tek_game.board1.ships = {'ships': request.POST.get("ships"), 'hitcoords': []}
                            tek_game.board1.ready_to_play = tek_game.board1.brd.can_start_game
                            tek_game.board1.save()

                    else:

                        if tek_game.board2.brd.can_start_game:
                            messages.add_message(request, messages.WARNING, 'Нельзя менять позиции кораблей после установки!')
                        else:
                            tek_game.board2.ships = {'ships': request.POST.get("ships"), 'hitcoords': []}
                            tek_game.board2.ready_to_play = tek_game.board2.brd.can_start_game
                            tek_game.board2.save()

            return render(request, "game.html", {"game": tek_game, "dsize": range(BOARD_SIZE)})

    raise Http404


def giveup(request, *args, **kwargs):
    if request.user.is_authenticated:
        game = get_object_or_404(Games, pk=kwargs['game_id'])
        if not game.done and (game.board1.user_id == request.user.id or game.board2.user_id == request.user.id):
            game.done = True
            if game.board1.user_id == request.user.id:
                if game.board2:
                    game.winner_id = game.board2.user_id
                else:
                    game.board1.delete()
                    game.delete()
                    return redirect(reverse("home"))
            else:
                game.winner_id = game.board1.user_id
            game.save()
            return redirect(reverse("home"))
        else:
            raise Http404
    return HttpResponse('401 Unauthorized', status=401)


def home(request):
    ctx = {}
    if request.user.is_authenticated:

        if request.method == 'POST':
            if 'newgame' in request.POST:
                if Games.objects.filter( Q(board1__user=request.user) | Q(board2__user=request.user)  ).filter(done=False).exists():
                    messages.add_message(request, messages.WARNING, 'Ты еще не доиграл!')
                    return redirect(reverse("home"))
                else:
                    b = Board.objects.create(user=request.user, ready_to_play=False, ships="[]", )
                    g = Games.objects.create(
                        board1=b,
                    )

                    return redirect(reverse("game", kwargs={"game_id": g.pk }))

        ctx["mygames"] = Games.objects.filter( Q(board1__user=request.user) | Q(board2__user=request.user)  ).order_by('-start_time')
        ctx["existinggames"] = Games.objects.exclude(board1__user=request.user).filter(board2 = None).order_by('-start_time')
        print("Мы залогинены", request.user.username)
    else:
        if request.method == "POST":
            print(request.POST)
            from .forms import LoginRegForm
            form = LoginRegForm(request.POST)
            if form.is_valid():
                if User.objects.filter(username=request.POST['login']).exists():
                    u = User.objects.filter(username=request.POST['login']).first()
                    if u.check_password(request.POST['pas']):
                        login(request, u)
                        return redirect(reverse("home"))
                    else:
                        messages.add_message(request, messages.WARNING, 'Пользователь не найден')
                        return redirect(reverse("main"))
                else:
                    u = User.objects.create_user(request.POST['login'], "", request.POST['pas'])
                    login(request, u)
                    return redirect(reverse("home"))
            else:
                print(form.errors)
                messages.add_message(request, messages.WARNING, 'Вводите нормальные данные')
                return redirect(reverse("main"))

    return render(request, "home.html", ctx)