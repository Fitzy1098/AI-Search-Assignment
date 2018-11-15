import random
import math
import time

def readFile(filename):
    file = open(filename, 'r')          #Opens the file
    data=file.readlines()               #Reads all the lines in the file
    stringdata="".join(data)            #Concatenates the data
    return(stringdata)

def getName(stringdata):                #Reads the name from the file
    stringdata=stringdata.split("=")
    name=stringdata[1].lstrip(" ")                    
    name=name.split(",")[0]
    return(name)

def getSize(stringdata):                #Reads the size from the file
    stringdata=stringdata.split("=")
    size=""
    size=stringdata[2][1:2]
    i=3
    while stringdata[2][1:i].isdigit():     #Iterates through all digits of the size
        size=stringdata[2][1:i]
        i+=1
    stringdata=stringdata[2][i:]
    return int(size)

def generateMatrix(size):                       #Generates a size*size matrix
    size=int(size)
    matrix = [[0]*size for i in range(size)]
    return matrix

def populateMatrix(stringdata, size, matrix):   #Fills the matrix with the distances from the file
    stringdata=stringdata.split("=")
    size=""
    size=stringdata[2][1:2]
    i=3
    while stringdata[2][1:i].isdigit():
        size=stringdata[2][1:i]
        i+=1
    stringdata=stringdata[2][i:]
    stringdata=stringdata.split(",")        #Splits all the numbers separated by commas
    size=int(size)
    length=size-1
    rowNum=1
    while length!=0:                        #Iterates trhough until all numbers processed
        row=stringdata[:length]
        stringdata=stringdata[length:]    
        colNum=size
        for i in range(0,len(row)):         #Iterates through each row
            num=""
            for j in range (0,len(row[i])): #Iterates through each number and reads all digits
                if row[i][j].isdigit:
                    num+=row[i][j]        
            num=int(num)
            matrix[rowNum-1][size-colNum+rowNum]=num    #Inserts the number into the correct cell in both halves of the matrix
            matrix[size-colNum+rowNum][rowNum-1]=num
            colNum-=1
        length-=1
        rowNum+=1
    return(matrix)

def printMatrix(size, matrix):      #Iterates through the rows of the matrix to print a correct matrix layout
    for i in range(size):
        print(matrix[i])
    
def work(x):                        #Runs simulated annealing on a given file
    start=time.time()               #Stores start time
    ultimateTour=[]                 #Tracks the best tour and distance
    ultimateDist=0
    file=readFile(x)
    name=getName(file)
    size=getSize(file)
    matrix=generateMatrix(size)
    matrix=populateMatrix(file,size,matrix)
    info=greedy(matrix,size)
    for j in range(1,100):                          #Repeats the algorithm 100 times
        tour=simAnnealing(matrix,size,name,info)    
        if ultimateDist==0 or ultimateDist>tour[1]: #Stores the tour and distance, if it is better than the current best
            ultimateDist=tour[1]
            ultimateTour=tour[0][:]
    end=time.time()                                 #Stores end time
    print(end-start)                                #Prints the duration
    print(ultimateTour)
    print(ultimateDist)
    writeFile(name,size,ultimateTour,ultimateDist)  #Writes the tour and distance to the output file


def simAnnealing(matrix,size,name,info):
    maxTemp=100000                          #Sets the maximum temperature
    temp=maxTemp                            
    bestTour=[]
    currentTour=[]
    currentTotal=0
    newTour1=[]
    newTotal=0
    currentTour=info[0]                     #Sets the current tour to the starting gready tour
    currentTotal=info[1]
    bestTour=[currentTour[:],currentTotal]  #Tracks the current best tour
    loop=1                                  #Counts the number of iterations of the while loop
    while (temp>0.0001):                    #Repeats until temperature drops below a minimum
        newInfo=neighbour(currentTour,size,matrix)      #Swaps two of the cities in the tour and calcualtes the new distance
        newTour1=newInfo[0][:]
        newTotal=newInfo[1]
        acceptanceProbability=probability(temp, newTotal, currentTotal)     #Calcualtes the probability the new tour will be accepted
        rand=random.random()
        if acceptanceProbability>rand:  #Accepts new tour of the proability is greater than a ranodm number between 0 and 1
            currentTour=newTour1[:]
            currentTotal=newTotal   
            if currentTotal<bestTour[1]:        #Stores the tour if it is the shortest tour found so far
                bestTour[1]=currentTotal
                bestTour[0]=currentTour[:]
        temp=maxTemp/(1+(10*math.pow(loop,2)))  #Decreases the temperature
        loop+=1
    return(bestTour)

def greedy(matrix,size):        #Generates the initial tour
    shortestTour=[]
    shortestDist=0
    for j in range(1,size):     #Iterates through all of the cities, starting the tour from each
        currentCity=j
        nextCity=0
        unvisited=[]
        visited=[j]
        total=0
        for i in range(1,size+1):   #Creates a list of unvisted cities
            unvisited.append(i)
        unvisited.remove(j)
        while len(unvisited)!=0:        #Iterates through until all cities have been visited
            shortest=0
            for i in range(0,len(unvisited)):   #Iterates through all the unvisited cities, calucalting the distance from the current city to each one
                city=unvisited[i]
                dist=matrix[currentCity-1][city-1]
                if shortest==0 or dist<shortest:    #Stores the city that is closest
                    nextCity=city
                    shortest=dist
            total+=shortest                 #Adds distance to total
            currentCity=nextCity
            visited.append(nextCity)        #Adds city to the tour
            unvisited.remove(nextCity)      #Removes city from the list of unvisited cities
        total+=matrix[nextCity-1][j-1]
        visited.append(j)                   #Adds the start city to the end of the tour
        if total<=shortestDist or shortestDist==0:      #Stores the current tour if it is the shortest
            shortestDist=total
            shortestTour=visited
    tour=[shortestTour,shortestDist]
    return tour


def neighbour(current,size,matrix):                 #Randomly swaps two cities in the tour
    newTour=current[:]
    location1=random.randint(0,size)                #Randomly chooses two positions in the tour list
    location2=random.randint(0,size)
    newDistance=0
    while location1==location2:                     #Picks different positions if they are the same
        location2=random.randint(1,size)
    city1=newTour[location1]                        #Identifies the city at the list positions
    city2=newTour[location2]
    newTour[location1]=city2                        #Swaps the two cities
    newTour[location2]=city1
    if location1==0:                                #Changes the start city if one of the swapped cities was the end city and vice versa
        newTour[size]=city2
    if location1==size:
        newTour[0]=city2
    if location2==0:
        newTour[size]=city1
    if location2==size:
        newTour[0]=city1
    for i in range(0,size):                         #Calculates the new tour length
        dist=matrix[newTour[i]-1][newTour[i+1]-1]
        newDistance+=dist
    info=[newTour,newDistance]
    return info
    
def probability(temperature, newTot, currentTot):   #Calcualtes the probability a new tour will be accepted      
    if newTot<=currentTot:                          #Highest probability if the tour is shorter
        return 1.0
    else:
        power=((currentTot-newTot)/temperature)     #Calcualtes the probability for longer tours
        prob=(math.exp(power))
        return prob       
            
def writeFile(name,size,tour,distance):         #Writes the output file
    filename="tourNEW"+name
    filename=filename+".txt"
    f= open(filename,"w+")                      #Opens/Creates the file in write mode
    name="NAME = "+name+",\n"
    f.write(name)                               
    size="TOURSIZE = "+str(size)+",\n"
    f.write(size)
    distance="LENGTH = "+str(distance)+",\n"
    f.write(distance)
    for i in range(0,len(tour)-1):              #Iterates through tour list and writes the tour 
        f.write(str(tour[i])+",")
    f.write(str(tour[len(tour)-1]))
    f.close()

#work("NEWAISearchfile012.txt")
