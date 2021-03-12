from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

import copy

thing = '┴ ┐ └ ┬ ├ ─ ┼ │ ┤ ┘ ┌ ╞ ╪ ═ ╡'

def makeAsciiArtRow(date, day, accuracy, wpm, idleTime, sizes, lastOne=False):
    sideL, t, sideR = ('├','┼','┤') if not lastOne else ('└','┴','┘')
    bottom = sideL+'─'*sizes[0]+t+'─'*sizes[1]+t+'─'*sizes[2]+t+'─'*sizes[3]+t+'─'*sizes[4]+sideR
    mid = '│{0}│{1}│{2}│{3}│{4}│'.format(date+' '*(sizes[0]-len(date)),
                                   day+' '*(sizes[1]-len(day)),
                                   accuracy+' '*(sizes[2]-len(accuracy)),
                                   wpm+' '*(sizes[3]-len(wpm)),
                                   idleTime+' '*(sizes[4]-len(idleTime)))
    return mid+'\n'+bottom

def makeAsciiArtTop(sizes):
    return '┌{0}┬{1}┬{2}┬{3}┬{4}┐'.format(
        '─'*sizes[0],
        '─'*sizes[1],
        '─'*sizes[2],
        '─'*sizes[3],
        '─'*sizes[4])

def makeAsciiArtHeader(sizes):
    labels = ('Date','Day','Accuracy','Wpm','Idle Time')
    mid = '│'
    for label,size in map(lambda x,y:(x,y),labels,sizes):
        mid += label + ' '*(size-len(label)) + '│'
    bottom = '╞'
    for size in sizes:
        bottom += '═'*size + '╪'
    bottom = bottom[:-1] + '╡'
    return makeAsciiArtTop(sizes) + '\n' + mid + '\n' + bottom

def getBiggestSizes(stuff):
    copyOfStuff = copy.copy(stuff)
    returning = []
    for thing in copyOfStuff:
        thing.sort(key=len,reverse=True)
        returning += [len(thing[0])]
    return returning


def getSizes(data):
    header = ['Date','Day','Accuracy','Wpm','Idle Time']
    lists = []
    for i in range(5):
        newList = [header[i]]
        for lis in data:
            newList+=[lis[i]]
        lists+=[newList]
    return getBiggestSizes(lists)

def makeTheChart(data):
    sizes = getSizes(data)
    header = makeAsciiArtHeader(sizes)
    on = 0
    last = len(data)-1
    body = ''
    for a,b,c,d,e in data:
        body += makeAsciiArtRow(a,b,c,d,e,sizes,lastOne=(on==last))+'\n'
        on+=1
    return header+'\n'+body
    

test = [['a','a','a','a','a'],['b','b','b','b','b']]
print(makeTheChart(test))


class TypingHistory(GridLayout):

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        print(user.historyDict)
        print(type(self))
        print(type(GridLayout))


print(type(TypingHistory))
