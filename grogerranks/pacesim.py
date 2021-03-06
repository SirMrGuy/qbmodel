import random
import time

def calcmargin(diff):
    return random.normalvariate(18.2743+6.4399*diff,164.4)

def genbracket(brackets,teams):
    lst = []
    for i in range(teams): lst.append(range(i*brackets,(i+1)*brackets))
    for i in range(1,len(lst),2): lst[i] = lst[i][::-1]

    ret = []
    for i in range(brackets):
        ret.append([])
        for j in lst: ret[-1].append(j[i])
    return ret

def roundrobin(bracket):
    scores = [0]*len(bracket)
    wins = [0]*len(bracket)
    for a in range(len(bracket)):
        for b in range(a+1,len(bracket)):
            diff = ranks[bracket[a]]-ranks[bracket[b]]
            margin = calcmargin(diff)
            scores[a] += margin
            scores[b] -= margin
            if margin > 0: wins[a] += 1
            else: wins[b] += 1
    return [x for x in sorted(zip(wins,scores,bracket),reverse=True)]

date = '11-22'
ranks = {}
teams = []
finishes = {}
with open('ranks'+date+'.txt') as f:
    for i in range(96):
        lst = f.readline().strip('\n').split('\t')
        team = ' '.join(lst[1].split(' ')[:-1])
        ranks[team] = float(lst[2])
        teams.append(team)
        finishes[team] = []
        for j in range(96): finishes[team].append(0)

prelimbrackets = [[teams[n] for n in x] for x in genbracket(12,8)]

trials = 100000.0
count = 0
start = time.time()
while count < trials:
    count += 1
    if count%1000 == 0: print count,round((time.time()-start)*(trials-count)/count,1)

    prelimresults = []
    for b in prelimbrackets: prelimresults.append(roundrobin(b))

    tiers = [[],[],[],[]]
    for i in range(8):
        for p in prelimresults: tiers[i/2].append(p[i])

    tiers = [[y[2] for y in sorted(x,reverse=True)] for x in tiers]

    playoffbrackets = []
    for i in range(4):
        playoffbrackets.append([[tiers[i][n] for n in x] for x in genbracket(4,6)])

    playoffresults = []
    for tier in playoffbrackets:
        tierresults = []
        for b in tier: tierresults.append(roundrobin(b))
        playoffresults.append(tierresults)

    tierI = [[],[]]
    for i in range(4):
        for p in playoffresults[0]: tierI[i/2].append(p[i][2])

    tierIcross = []
    for i in range(4,6):
        for p in playoffresults[0]: tierIcross.append(p[i])
    tierIcross = [x[2] for x in sorted(tierIcross,reverse=True)]
    
    tierIIcross = []
    for p in playoffresults[1]: tierIIcross.append(p[0])
    tierIIcross = [x[2] for x in sorted(tierIIcross,reverse=True)]

    cross = tierIcross+tierIIcross
    
    superplayoffs = []
    for i in range(1,4):
        for j in range(6):
            if i == 1 and j == 0: continue
            superplayoffs.append([])
            for p in playoffresults[i]: superplayoffs[-1].append(p[j][2])

    results = []
    for b in tierI: results += [x[2] for x in roundrobin(b)]
    
    crossbrackets = [[cross[n] for n in x] for x in genbracket(2,6)]
    crossresults = []
    for b in crossbrackets: crossresults.append([x[2] for x in roundrobin(b)])
    for i in range(6):
        a = crossresults[0][i]
        b = crossresults[1][i]
        if calcmargin(ranks[a]-ranks[b]) > 0: results += [a,b]
        else: results += [b,a]

    for b in superplayoffs: results += [x[2] for x in roundrobin(b)]

    for i in range(96):
        finishes[results[i]][i] += 1
        
'''
with open('pacesimfull.csv','w') as f:
    for team in teams:
        s = team
        for i in finishes[team]: s += ','+str(i)
        s += '\n'
        f.write(s)
with open('pacesimsummary.csv','w') as f:
    for team in teams:
        lst = [team,
               str(round(100*finishes[team][0]/trials,1)),
               str(round(100*sum(finishes[team][0:8])/trials,1)),
               str(round(100*sum(finishes[team][0:16])/trials,1)),
               str(round(100*sum(finishes[team][0:24])/trials,1))]
        s = ','.join(lst)+'\n'
        f.write(s)
'''

with open('../docs/pace.js','w') as f:
    teamlst = teams[:24]
    f.write('function fillTable() {\n')
    f.write('\tvar table = document.getElementById("paceTable");\n')
    for team in teamlst:
        lst = [team,
               "{:.2f}".format(sum([i*finishes[team][i] for i in range(96)])/trials+1),
               "{:.1f}".format(round(100*sum(finishes[team][0:24])/trials,1))+'%',
               "{:.1f}".format(round(100*sum(finishes[team][0:16])/trials,1))+'%',
               "{:.1f}".format(round(100*sum(finishes[team][0:8])/trials,1))+'%',
               "{:.1f}".format(round(100*finishes[team][0]/trials,1))+'%']
        f.write('\tvar row = table.insertRow()\n')
        for i in range(len(lst)):
            f.write('\tvar cell = row.insertCell();\n')
            f.write('\tcell.innerHTML = "'+lst[i]+'";\n')
    f.write('}\n')
    
    f.write('function teamSelect() {\n')
    f.write('\tvar div = document.getElementById("main");\n')
    f.write('\tvar arr = [\'Select a team\','+str(teamlst)[1:]+';\n')
    f.write('\tvar s = document.createElement("select");\n')
    f.write('\ts.setAttribute("onchange","graph(this.value)");\n')
    f.write('\tdiv.appendChild(s);\n')
    f.write('\tfor (var i = 0; i < arr.length; i++) {\n')
    f.write('\t\tvar option = document.createElement("option");\n')
    f.write('\t\toption.value = arr[i];\n')
    f.write('\t\toption.text = arr[i];\n')
    f.write('\t\ts.appendChild(option);\n')
    f.write('\t}\n')
    f.write('}\n')

    f.write('function graph(s) {\n')
    f.write('\tvar trials = '+str(trials)+';\n')
    f.write('\tvar c = document.getElementById("graph");\n')
    f.write('\tvar ctx = c.getContext("2d");\n')
    f.write('\tctx.clearRect(40, 0, c.width-40, c.height-51);\n')
    f.write('\tif(s=="Select a team")return;\n')
    f.write('\tfunction bar(size,place) {\n')
    f.write('\t\tif(place<1) ctx.fillStyle="#33FFFF";\n')
    f.write('\t\telse if(place<8) ctx.fillStyle="#FFDD11";\n')
    f.write('\t\telse if(place<16) ctx.fillStyle="#BBBBBB";\n')
    f.write('\t\telse if(place<24) ctx.fillStyle="#CC8033";\n')
    f.write('\t\telse ctx.fillStyle="#AA3333";\n')
    f.write('\t\tctx.fillRect(10*place+40,449-1000*size/trials,10,1000*size/trials)\n')
    f.write('\t}\n')
    f.write('\tvar places = {};\n')
    for t in teamlst: f.write('\tplaces["'+t+'"] = '+str(finishes[t])+';\n')
    f.write('\tfor(var i = 0; i < places[s].length; i++) {\n')
    f.write('\t\tbar(places[s][i],i);\n')
    f.write('\t}\n')
    f.write('}\n')
