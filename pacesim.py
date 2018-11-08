import random
import time

ranks = {}
toptwo = {}
top = {}
total = {}
winner = {}
teams = []
with open('ranks.txt') as f:
    for i in range(28):
        lst = f.readline().strip('\n').split('\t')
        team = ' '.join(lst[1].split(' ')[:-1])
        ranks[team] = float(lst[2])
        toptwo[team] = 0
        top[team] = 0
        total[team] = 0
        winner[team] = 0
        teams.append(team)

brackets = [[1,8,9,16,17,24],
            [2,7,10,15,18,23],
            [3,6,11,14,19,22],
            [4,5,12,13,20,21]]
brackets = [[teams[n-1] for n in x] for x in brackets]

def roundrobin(bracket):
    scores = [0]*len(bracket)
    wins = [0]*len(bracket)
    for a in range(len(bracket)):
        for b in range(a+1,len(bracket)):
            diff = ranks[bracket[a]]-ranks[bracket[b]]
            margin = random.normalvariate(7.562*diff,152.7)
            scores[a] += margin
            scores[b] -= margin
            if margin > 0: wins[a] += 1
            else: wins[b] += 1
    return [x for _,_,x in sorted(zip(wins,scores,bracket),reverse=True)]

trials = 1000000.0
count = 0
start = time.time()
while count < trials:
    count += 1
    if count%1000 == 0: print count,round((time.time()-start)*(trials-count)/count)
    
    playoffs = []
    for b in brackets: playoffs.append(roundrobin(b))
    
    champ = []
    ninth = []
    for j in range(4):
        champ += [playoffs[j][0],playoffs[j][1]]
        ninth += [playoffs[j][2],playoffs[j][3]]
    for t in champ:
        toptwo[t] += 1
        top[t] += 1
    for t in ninth: toptwo[t] += 1
    crossa = [playoffs[0][4],playoffs[3][4],playoffs[2][5],playoffs[1][5],teams[24],teams[27]]
    crossb = [playoffs[1][4],playoffs[2][4],playoffs[3][5],playoffs[0][5],teams[25],teams[26]]

    champ = roundrobin(champ)
    winner[champ[0]] += 1
    for i in range(8): total[champ[i]] += i+1
    ninth = roundrobin(ninth)
    for i in range(8): total[ninth[i]] += i+9
    
    crossa = roundrobin(crossa)
    crossb = roundrobin(crossb)
    for i in range(6):
        diff = ranks[crossa[i]]-ranks[crossb[i]]
        if random.normalvariate(7.562*diff,152.7) > 0:
            total[crossa[i]] += 17+2*i
            total[crossb[i]] += 18+2*i
        else:
            total[crossb[i]] += 17+2*i
            total[crossa[i]] += 18+2*i
for t in teams[:24]: print t
print ''
for t in teams[:24]: print total[t]/trials
print ''
for t in teams[:24]: print toptwo[t]/trials
print ''
for t in teams[:24]: print top[t]/trials
print ''
for t in teams[:24]: print winner[t]/trials
