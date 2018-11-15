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
    
def work(filename):                 #Runs the A* search on a given file
    start=time.time()               #Stores the start time
    file=readFile(filename)   
    name=getName(file)
    size=getSize(file)
    matrix=generateMatrix(size)
    matrix=populateMatrix(file,size,matrix)
    aStar(size,matrix,name)
    end=time.time()                 #Stores the end time
    print(end-start)                #Prints the time taken


def greedy(matrix,start,end,toVisit):           #Calcualtes the shortest greedy route through all remaining cities back to the start. This is the heuristic H(z)
    toVisit1=toVisit[:]                         #List of cities yet to visit
    currentCity=start
    nextCity=0
    total=0
    toVisit1.remove(start)                      #Removes start city from list
    while len(toVisit1)!=0:                     #Iterates through until no more cities left to visit
        shortest=0
        row=matrix[currentCity-1]               #Stores appropriate row of matrix, so don't have to access two lists every time
        for i in range(0,len(toVisit1)):        #Iterates through all remaining cities
            city=toVisit1[i]
            dist=row[city-1]                    #Calculates distance from current city
            if shortest==0 or dist<shortest:    #Stores city and distance if shorter
                shortest=dist
                nextCity=city
        total+=shortest                         #Adds shortest length to total
        currentCity=nextCity                    #Changes the current city
        toVisit1.remove(nextCity)               #Removes city from list of unvisited
    total+=matrix[nextCity-1][end-1]            #Adds distance back to start to route
    return total    

def aStar(size,matrix,name):                    #Runs the A* search
    bestTour=[]
    bestDist=0
    if size>180:                                #Changes increments of i if number of cities too large, so it runs faster.
        x=int(size/2)
    else:
        x=1
    for i in range(1,size+1,x):                 #Iterates through all cities as the start
        toVisit=[]
        cities=[i]
        for k in range(0,size):                 #Creates a list of cities yet to visit
            toVisit.append(k+1)
        toVisit.remove(i)                       #Removes start city
        length=0
        lastcity=i
        currentDist=0
        while len(toVisit)!=0:                  #Iterates through until no cities left to visit
            row=matrix[lastcity-1]              #Stores row of matrix, so it only accesses one list in the for loop
            shortest=0
            nextCity=0
            for j in range (0,len(toVisit)):    #Iterates through all remaining cities
                city=toVisit[j]
                dist=row[city-1]               #Calculates distance between the last city and the one being checked
                f=greedy(matrix,city,i,toVisit)+length+dist         #Calculates f(z) using greedy, the total length so far and the distance between the current two cities
                if f<=shortest or shortest==0:                      #Stores the city and distance if f(z) is shorter
                    nextCity=city
                    shortest=f
                    currentDist=dist
            length+=currentDist                 #Adds distance to the total
            cities.append(nextCity)             #Adds city to the tour
            toVisit.remove(nextCity)            #Removes city from the list of unvisited cities
            lastcity=nextCity
        cities.append(i)                        #Adds the start city to the end of the tour
        length+=matrix[lastcity-1][i-1]
        if length<=bestDist or bestDist==0:     #Stores the current tour and distance if it is the best
            bestDist=length
            bestTour=cities
    print(bestTour)
    print(bestDist)
    writeFile(name,size,bestTour,bestDist)      #Writes the tour and distances to the output file

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
