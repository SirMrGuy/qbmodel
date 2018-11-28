# -*- coding: cp1252 -*-
import time
start = time.time()

import os

years = ['2016-17','2017-18']
ranklst = {}
for year in years:
    with open('ranks'+year+'.txt') as f:
        ranks = {}
        for line in f:
            if line == '\n': continue
            lst = line.strip('\n').split(' – ')
            team = lst[0].split('. ')[1].split(')')[0]+')'
            if ',' in lst[1]: appb = float(lst[1].split(',')[0].strip('*'))
            else: appb = float(lst[1].strip('*'))
            ranks[team] = appb
        ranklst[year] = ranks
            
logitpoints = []
marginpoints = []
games = 0
for year in years:
    print 'Analyzing PACE',year
    ranks = ranklst[year]
    with open('../data/'+year+'/tournaments/PACE.txt') as scores:
        aliases = {}
        try:
            with open('../data/'+year+'/aliases/PACE.txt') as alias:
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
                lst = [' '.join(x.split(' ')[:-1])+' A '+x.split(' ')[-1] if len(x.split(' ')[-2]) > 1 else x for x in lst]
                lst = [aliases[' '.join(x.split(' ')[:-2])]+' '+' '.join(x.split(' ')[-2:]) if ' '.join(x.split(' ')[:-2]) in aliases else x for x in lst]
                if lst[0] in ranks and lst[1] in ranks:
                    diff = ranks[lst[0]]-ranks[lst[1]]
                    margin = pts[0]-pts[1]
                    logitpoints += [(1,diff),(0,-diff)]
                    marginpoints += [(margin,diff),(-margin,-diff)]
                games += 1

with open('logit.csv','w') as out:
    out.write('win,diff\n')
    for p in logitpoints:
        if p[1]>=0: out.write(str(p[0])+','+str(p[1])+'\n')
        out.write(str(p[0])+','+str(p[1])+'\n')
with open('margin.csv','w') as out:
    out.write('margin,diff\n')
    for p in marginpoints:
        if p[1]>=0: out.write(str(p[0])+','+str(p[1])+'\n')

print 'Analyzed',len(logitpoints)/2,'of',games,'game(s) in',len(years),'tournament(s) in',round(time.time()-start,3),'second(s)'
