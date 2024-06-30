from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.contrib.auth.models import User
import os

# Create your views here.
loginUrl = f'/signin/'

def home(request):
    player = Player.objects.all()
    team = Team.objects.all()
    context = {
        "team":team,
        "player":player,
    }
    return render(request, "home.html",context)

def teams(request):
    team = Team.objects.all()
    
    context = {"team":team}
    return render(request, "teams.html",context)

def team(request,pk):
    team = Team.objects.get(id=pk)
    match = Match.objects.filter(team=team)
    context = {
        "team":team,
        "matchs":match,
    }
    return render(request, "team.html",context)


def teamPlayers(request,pk,pk2):
    match = Match.objects.get(id=pk)
    matchname = match.name
    match = Match.objects.filter(name=matchname)
    team = Team.objects.get(id=pk2)
    teamPlayers = TeamPlayer.objects.filter(team=team)
    player = Player.objects.all()
    
    if request.method == "POST":
        teamTossId = int(request.POST['toss'])
        teamElect = str(request.POST['elect'])
        totalOver = int(request.POST['over'])
        for i in match:
            if i.team.id == teamTossId:
                teamA = Team.objects.get(id=teamTossId)
                matchteam = Match.objects.get(name=i.name,team=teamA)
                matchteam.status = "started"
                matchteam.save()
                if teamElect == "bat":
                    inning = "1"
                else:
                    inning = "2"
                s = Score(match=matchteam, inning=inning, over=totalOver)
                s.save()
            else:
                if teamElect == "ball":
                    inning = "1"
                else:
                    inning = "2"
                teamB = Team.objects.get(id=i.team.id)
                matchteam = Match.objects.get(name=i.name,team=teamB)
                matchteam.status = "started"
                matchteam.save()
                s = Score(match=matchteam, inning=inning, over=totalOver)
                s.save()
        return redirect('/match/all/')

    # if match is completed, both innings ended
    if match[0].status == "completed" and match[1].status == "completed":
        matchStatus = match[1].status # completed

        # Winner decision based on total runs
        winnerTeam = []
        try:
            for i in match:
                matchteam = Match.objects.get(id=i.id,team=i.team)
                teamx = Score.objects.get(match=matchteam)
                winnerTeam.append(teamx)

            if winnerTeam[0].total_score > winnerTeam[1].total_score:
                winnerTeam[0].win_loss = "win"
                winnerTeam[1].win_loss = "loss"
            elif winnerTeam[0].total_score < winnerTeam[1].total_score:
                winnerTeam[0].win_loss = "loss"
                winnerTeam[1].win_loss = "win"
            elif winnerTeam[0].total_score == winnerTeam[1].total_score:
                winnerTeam[0].win_loss = "tie"
                winnerTeam[1].win_loss = "tie"

            winnerTeam[0].save()
            winnerTeam[1].save()
        except:
            pass
    else:
        matchStatus = match[1].status # started
    
    context = {
        "matchname":matchname,
        "matchStatus":matchStatus,
        "match":match,
        "team":team,
        "teamPlayers":teamPlayers,
        "player":player,
    }
    return render(request, "teamPlayers.html",context)


def teamPlayersCreate(request, pk, pk2, pk3):
    match = Match.objects.get(id=pk)
    team = Team.objects.get(id=pk2)
    player = Player.objects.get(id=pk3)
    data1 = False
    try:
        teamplayer = TeamPlayer.objects.filter(match=match, team=team,player=player)
        for i in teamplayer:
            if int(pk2) == i.team.id and int(pk3) == i.player.id:
                # if data is True item is already in wishlist
                data1 = True
                break
            else:
                data1 = False
    except:
        pass
    
    if not data1:
        t = TeamPlayer(match=match,team=team,player=player)
        t.save()
        return redirect(f'/match/{pk}/team/{pk2}/')
    else :
        return redirect(f'/match/{pk}/team/{pk2}/')
        

def teamPlayersDelete(request, pk, pk2, pk3):
    match = Match.objects.get(id=pk)
    team = Team.objects.get(id=pk2)
    player = Player.objects.get(id=pk3)
    t = TeamPlayer.objects.get(match=match, team=team,player=player)
    t.delete()
    return redirect(f'/match/{pk}/team/{pk2}/')

def match(request):
    match = Match.objects.all()
    context={"matchs":match}
    return render(request, "match.html",context)

def matchCreate(request):
    teams = Team.objects.all()
    if request.method == "POST":
        match = Match.objects.filter(name__contains="MATCH")
        name = f"MATCH-0{int(match.count()/2)+1}"
        teamA = Team.objects.get(id=request.POST['teamA'])
        teamB = Team.objects.get(id=request.POST['teamB'])
        team_two = [teamA, teamB]
        for i in team_two:
            m = Match(name=name,team=i)
            m.save()
        return redirect('/match/all/')
    context={"teams":teams}
    return render(request, "matchCreate.html",context)


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        try:
            user = auth.authenticate(username=username, password=password)
            if user == None:
                try:
                    x = User.objects.get(username=username) 
                except:
                    x = User.objects.get(email=username)
                user = auth.authenticate(username=x.username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect(f'/profile')
            else:
                messages.error(request, "Email and Password does not match")
        except:
            messages.error(request, "User does not exsist")
    return render(request, 'signin.html')

@login_required(login_url=loginUrl)
def profile(request):
    user = User.objects.get(username=auth.get_user(request))
    player = Player.objects.all()
    if request.method == "POST":
        name = request.POST["name"]
        pic = request.FILES["pic"]
        p = Player(name=name,pic=pic)
        p.save()
        return redirect(f'/profile')
    context={"profile":user,"players":player}
    return render(request, "profile.html",context)

@login_required(login_url=loginUrl)
def logout(request):
    auth.logout(request)
    return redirect(f'/signin')

@login_required(login_url=loginUrl)
def teamAdd(request):
    sports = Sport.objects.all()
    if request.method == "POST":
        sport = Sport.objects.get(id=request.POST["sport"])
        name = request.POST["name"]
        t = Team(sport=sport,name=name)
        t.save()
        return redirect(f'/profile')
    context={"sports":sports}
    return render(request, "teamAdd.html",context)

@login_required(login_url=loginUrl)
def teamEdit(request,pk):
    sports = Sport.objects.all()
    team = Team.objects.get(id=pk)
    if request.method == "POST":
        sport = Sport.objects.get(id=request.POST["sport"])
        name = request.POST["name"]
        team.sport = sport
        team.name = name
        team.save()
        return redirect(f'/team')
    context={"sports":sports,"team":team}
    return render(request, "teamEdit.html",context)

@login_required(login_url=loginUrl)
def teamDelete(request,pk):
    t = Team.objects.get(id=pk)
    t.delete()
    return redirect(f'/team')

def players(request):
    p = Player.objects.all()
    context = {"players":p}
    return render(request, "players.html",context)

@login_required(login_url=loginUrl)
def playerAdd(request):
    if request.method == "POST":
        name = request.POST["name"]
        try:
            pic = request.FILES["pic"]
            p = Player(name=name,pic=pic)
        except:
            p = Player(name=name)
        p.save()
        return redirect(f'/profile')
    return render(request, "playerAdd.html")

@login_required(login_url=loginUrl)
def playerEdit(request,pk):
    p = Player.objects.get(id=pk)
    if request.method == "POST":
        p.name = request.POST["name"]
        
        if (request.FILES.get('pic')):
            p.pic = request.FILES["pic"]
            try:
                os.remove('media/'+str(p.pic))
            except:
                pass
        p.save()
        return redirect(f'/players')
    context = {"player":p}
    return render(request, "playerEdit.html",context)

@login_required(login_url=loginUrl)
def playerDelete(request,pk):
    p = Player.objects.get(id=pk)
    os.remove('media/'+str(p.pic1))
    p.delete()
    return redirect(f'/players')


def score(request,pk):
    score = Score.objects.get(id=pk)
    scoreadd = ScoreAdd.objects.filter(score=score)
    
    matchteam = Match.objects.get(id=score.match.id,team=score.match.team)
    teamPlayers = TeamPlayer.objects.filter(match=score.match, team=score.match.team)
    teamPlayersCount = teamPlayers.count()
    t,b,w,ex=0,0,0,0
    for i in scoreadd:
        t = t + int(i.run)
        b = b + int(i.ball)
        if i.comment == "wicket":
            w = w + 1
        elif i.comment == "noball" or i.comment == "wide":
            ex = ex + 1
    extra_runs = ex
    total_score = t
    total_balls = b
    current_over = total_balls
    over = score.over

    x,y=0,0
    # if over % 6 == 0:
    x = int(current_over/6)
    if current_over % 6 != 0:
        y = current_over-x*6
    current_over = f"{x}.{y}"
    # innings started
    if total_balls >0:
        score.status = "playing"
    # all wickets out of team
    if teamPlayersCount == w:
        score.status = "ends"
        matchteam.status = "completed"
    # all over completed
    if int(over) == int(x):
        score.status = "ends"
        matchteam.status = "completed"

    match = Match.objects.filter(name=score.match.name)
    if match[0].status == "completed" and match[1].status == "started":
        # ending match innings 
        winnerTeam = []
        try:
            for i in match:
                matchteam = Match.objects.get(id=i.id,team=i.team)
                teamx = Score.objects.get(match=matchteam)
                winnerTeam.append(teamx)

            if winnerTeam[0].total_score == total_score and int(over) == int(x) or teamPlayersCount == w:
                score.status = "ends"
                matchteam.status = "completed"
            if winnerTeam[0].total_score < total_score:
                score.status = "ends"
                matchteam.status = "completed"
        except:
            pass
    
    score.total_score = total_score
    score.current_over = current_over
    score.save()
    matchteam.save()

    context = {"score":score, "overs":over, "wicket":w, "current_over":current_over,"total_balls":total_balls, "extra_runs":extra_runs, "scoreadd":scoreadd}
    return render(request, "score.html",context)

def scoreAdd(request,pk2,pk):
    score = Score.objects.get(id=pk2)
    if pk == "0" or pk == "1" or pk == "2" or pk == "3" or pk == "4" or pk == "6":
        ball = 1
        run = int(pk)
        comment = str(pk)
    elif pk == "noball" or pk == "wide":
        ball = 0
        run = 1
        comment = str(pk)
    elif pk == "wicket":
        ball = 1
        run = 0
        comment = str(pk)
    else:
        return redirect(f'/score/{pk2}')

    scoreAdd = ScoreAdd(score=score, ball=ball, run=run,comment=comment)
    scoreAdd.save()

    return redirect(f'/score/{pk2}')