def bestOfFiles(listOfFiles):
    newNameList = []
    finalList1 = [[] for i in range(len(listOfFiles))]

    finalFinalList = []

    for lis in listOfFiles:
        if lis[0] not in newNameList:
            newNameList.append(lis[0])
        finalList1[newNameList.index(lis[0])].append(lis)
    finalList1=finalList1[:len(newNameList)]

    for lesson in finalList1:
        accuracyWeight = .6
        wpmWeight = 1 - accuracyWeight
        accuracyList = [int(x)*accuracyWeight for file,x,wpm in lesson]
        wpmList = [int(x)*wpmWeight for file,accuracy,x in lesson]
        nameList = [x for x,accuracy,wpm in lesson]

        best = 0
        bestPosition = 0
        for i in range(len(lesson)):
             total = accuracyList[i]+wpmList[i]
             if total > best:
                best = total
                bestPosition = i
        finalFinalList.append(lesson[bestPosition])
        
        
    return finalFinalList
        

def worstFile(listOfFiles):
    listOfFiles = bestOfFiles(listOfFiles)
    accuracyWeight = .6
    wpmWeight = 1 - accuracyWeight
    accuracyList = [int(x)*accuracyWeight for file,x,wpm in listOfFiles]
    wpmList = [int(x)*wpmWeight for file,accuracy,x in listOfFiles]
    nameList = [x for x,accuracy,wpm in listOfFiles]


    smallest = 101
    worst = 0
    for i in range(len(listOfFiles)):
        total = accuracyList[i]+wpmList[i]
        if total < smallest:
            smallest = total
            worst = i


    return worst

if __name__ == '__main__':
    data = [['lesson1',70,60],['lesson2',89,31],['lesson3',80,50],['lesson1',70,50],['lesson2',89,30],['lesson3',80,49]]
    worstFile(data)
    
