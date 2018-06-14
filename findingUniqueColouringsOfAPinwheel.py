#Testing a theory of an easier/faster way for me to brute force all possible
#colouring of a pinwheel
import copy
colours = ['A', 'B', 'C']

used_colours = []
curr_index = {0:None}


# numSpokes
#colours = string array of possible colours used in a colouring
# currIndexColArr, dictionary[0] is the current index of the "new colour for this iteration"
#uniqueColsArr, array of arrays, each of which is possible distinct colouring of the pinwheel
#currCol = current possible colouring array that is being modified
#unique Cols Arr has 1 FEWER colours that allowed for. The center is ignored for obvious reasons

def createTuplesOfPinwheel(numSpokes, colours, currIndexColArr, uniqueColsArr, currCol):
    if(len(currCol) == 0):
        currCol = [colours[0]]
        currIndexColArr[0] = 1

    if(len(currCol) == numSpokes):
        
        uniqueColsArr.append(currCol)
        #print("currCol is:", currCol)
        #print("uniqueColsArr are:",  uniqueColsArr)
        return uniqueColsArr

    

    deepCopy = copy.deepcopy(currCol)
    if(deepCopy is currCol):
        print("problem: deepCopy is currCol")
    #print("currCol: ", currCol)
    #print("currIndexColArr:", currIndexColArr[0])
    #add new if possible
    if(currIndexColArr[0] < (len(colours))):
        currCol.append(colours[currIndexColArr[0]])
        #needs to be the same for add all olds
        #currIndexColArr[0] = currIndexColArr[0] + 1
        newCurrIndexColArr = {0:0}
        newCurrIndexColArr[0] = currIndexColArr[0] + 1
        createTuplesOfPinwheel(numSpokes, colours, newCurrIndexColArr, uniqueColsArr, currCol)
    
    #add all olds possible
    currSpoke =  len(deepCopy)
    spokeBehind = currSpoke - 1
    spokeAhead = spokeBehind
    #account for end spokes
    if(len(deepCopy) == numSpokes - 1):
        spokeAhead = 0
    if(currIndexColArr[0] > len(colours)):
        currIndexColArr[0] = len(colours)
    for i in range (0, currIndexColArr[0]):
        if ((deepCopy[spokeBehind] != colours[i]) and (deepCopy[spokeAhead] != colours[i])):
            temp = {0:0}
            temp[0] = currIndexColArr[0] + 1
            tempDeepCopy = copy.deepcopy(deepCopy)
            tempDeepCopy.append(colours[i])
            #print(tempDeepCopy)
            createTuplesOfPinwheel(numSpokes, colours, temp, uniqueColsArr, tempDeepCopy)
    
    return uniqueColsArr


answer = createTuplesOfPinwheel(6, colours, curr_index, [0],[])

print(answer)
print("length of answer: ", len(answer))
for i in range (0, 13):
    print(answer[i])
