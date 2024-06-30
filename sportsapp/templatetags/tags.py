from django import template
from sportsapp.models import Match, TeamPlayer, Team, Score, ScoreAdd
register = template.Library()


@register.filter(name="matchTeamPlayer")
def matchTeamPlayer(pk2, pk):
    team = Team.objects.get(id=pk)
    match = Match.objects.get(id=pk2)
    teamPlayers = TeamPlayer.objects.filter(match=match, team=team)
    return teamPlayers


@register.filter(name="matchTeamScore")
def matchTeamScore(pk2, pk):
    # for i in match:
    # try:
    teamA = Team.objects.get(id=pk)
    matchteam = Match.objects.get(id=pk2,team=teamA)
    score = Score.objects.get(match=matchteam)
    scoreadd = ScoreAdd.objects.filter(score=score)
    r,b,w,ex=0,0,0,0
    for i in scoreadd:
        r = r + int(i.run)
        b = b + int(i.ball)
        if i.comment == "wicket":
            w = w + 1
        elif i.comment == "noball" or i.comment == "wide":
            ex = ex + 1
    extra_runs = ex
    total_score = r
    total_balls = b
    current_over = total_balls
    over = score.over
    x,y=0,0
    # if over % 6 == 0:
    x = int(current_over/6)
    if current_over % 6 != 0:
        y = current_over-x*6
    current_over = f"{x}.{y}"
    # except:
    #     score={"id":0,"total_score":0,"over":0}
    #     over=0
    #     w=0
    #     current_over=0
    #     total_balls=0
    #     extra_runs=0
    #     scoreadd=0

    context = [{
        "score":score,
        "overs":over,
        "wicket":w,
        "current_over":current_over,
        "total_balls":total_balls,
        "extra_runs":extra_runs,
        "scoreadd":scoreadd,
    }]

    return context

@register.filter(name="winLossStatus")
def winLossStatus(pk2, pk):
    try:
        teamA = Team.objects.get(id=pk)
        matchteam = Match.objects.get(id=pk2,team=teamA)
        score = Score.objects.get(match=matchteam)
        return [score.win_loss]
    except:
        return []