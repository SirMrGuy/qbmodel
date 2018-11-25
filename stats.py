import time
start = time.time()

import os

rankdates = ['10-29']
ranklst = []
for date in rankdates:
    with open('ranks'+date+'.txt') as f:
        ranklst.append({})
        for line in f:
            lst = line.strip('\n').split('\t')
            ranklst[-1][' '.join(lst[1].split(' ')[:-1])] = float(lst[2])

tournaments = []
with open('tourneys.txt') as f:
    for line in f:
        tournaments.append(line.strip('\n').split(','))

logitpoints = []
marginpoints = []
games = 0
for tournament in tournaments:
    print 'Analyzing',tournament[0]
    ranks = ranklst[rankdates.index(tournament[1])]
    with open(os.path.join('./tournaments',tournament[0]+'.txt')) as scores:
        aliases = {}
        try:
            with open(os.path.join('./aliases',tournament[0]+'.txt')) as alias:
                for a in alias:
                    lst = a.strip('\n').split(',')
                    aliases[lst[0]] = lst[1]
        except:
            pass
        for game in scores:
            if ':' not in game and ',' in game:
                s = game.strip('\n')
                if s[-3:] == ' OT': s = s[:-3]
                if s[-4:] == ' Tie': s = s[:-4]
                lst = [' '.join(x.split(' ')[:-1]) for x in s.split(', ')]
                pts = [int(x.split(' ')[-1]) for x in s.split(', ')]
                lst = [x+' A' if len(x.split(' ')[-1]) > 1 else x for x in lst]
                lst = [aliases[' '.join(x.split(' ')[:-1])]+' '+x.split(' ')[-1] if ' '.join(x.split(' ')[:-1]) in aliases else x for x in lst]
                if lst[0] in ranks and lst[1] in ranks:
                    diff = ranks[lst[0]]-ranks[lst[1]]
                    margin = pts[0]-pts[1]
                    logitpoints += [(1,diff),(0,-diff)]
                    marginpoints += [(margin,diff),(-margin,-diff)]
                games += 1

with open('logit.csv','w') as out:
    out.write('win,diff\n')
    for p in logitpoints:
        out.write(str(p[0])+','+str(p[1])+'\n')
with open('logit2.csv','w') as out:
    out.write('win,diff\n')
    for p in logitpoints:
        if p[1]>=0: out.write(str(p[0])+','+str(p[1])+'\n')
with open('margin.csv','w') as out:
    out.write('margin,diff\n')
    for p in marginpoints:
        out.write(str(p[0])+','+str(p[1])+'\n')
with open('margin2.csv','w') as out:
    out.write('margin,diff\n')
    for p in marginpoints:
        if p[1]>=0: out.write(str(p[0])+','+str(p[1])+'\n')

print 'Analyzed',len(logitpoints)/2,'of',games,'game(s) in',len(tournaments),'tournament(s) in',round(time.time()-start,3),'second(s)'
