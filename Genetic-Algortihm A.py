import time
import random

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
    stringdata=stringdata[2][i:]            #Removes size from the remaining file
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
        for i in range(0, len(row)):         #Iterates through each row
            num=""
            for j in range (0, len(row[i])): #Iterates through each number and reads all digits
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
    
def work(x):                 #Runs the Genetic Algorithm on a given file 'x'
    bestTour=[]
    bestDist=0
    filename=x
    start=time.time()               #Stores the start time
    file=readFile(filename)         #Reads the data from the file
    name=getName(file)              #Gets the name of the file
    size=getSize(file)              #Gets the number of cities
    matrix=generateMatrix(size)     #Generates a matrix of the correct size
    matrix=populateMatrix(file, size, matrix) #Populates the matrix with data from the 
    initial=greedy(matrix, size)
    tour=genetic(initial, matrix, size)
    end=time.time()                 #Stores the end time
    print(end-start)                #Prints the time taken
    writeFile(name, size, tour[0], tour[1])

def greedy(matrix, size):        #Generates the initial population of all greedy tours
    population=[]
    for j in range(1, size+1):     #Iterates through all of the cities, starting the tour from each
        currentCity=j
        nextCity=0
        unvisited=[]
        visited=[j]
        total=0
        for i in range(1, size+1):   #Creates a list of unvisted cities
            unvisited.append(i)
        unvisited.remove(j)
        while len(unvisited)!=0:        #Iterates through until all cities have been visited
            shortest=0
            for i in range(0, len(unvisited)):   #Iterates through all the unvisited cities, calucalting the distance from the current city to each one
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
        tour=[visited,total]
        population.append(tour)             #Adds tour and its distance to the population
        
        
    return population



def mutate(current, size, matrix, mutateProb):                 #Randomly reverses a section of the tour
    rand=random.random()
    if mutateProb<rand:          #Returns the original tour if probability not high enough
        return current
    elif mutateProb>rand:
        newTour=current[:]                  #Makes a shallow copy of the current tour
        location1=random.randint(0, size)                #Randomly chooses two positions in the tour list
        location2=random.randint(0, size)
        newDistance=0
        while location1==location2:                     #Picks different positions if they are the same
            location2=random.randint(1, size)
        split2=max(location1, location2)                #Finds the larger of the two positions
        split1=min(location1, location2)                #Finds the smaller of the two positions
        reverse=newTour[split1:split2]                  #Copies the section to be reversed
        reverse=reverse[::-1]                           #Reverses the section
        for i in range(0, len(reverse)):                #Iterates through the new tour and replaces the reveresed values
            newTour[split1+i]=reverse[i]
        if location1==0 or location2==0:                #Changes the start city if one of the reversed cities was the end city and vice versa, ensuring it remains a tour
            newTour[size]=newTour[0]
        if location1==size or location2==size:
            newTour[0]=newTour[size]
        return newTour


def genetic(currentPop, matrix, size):              #Perfroms the genetic algorithm
    bestDist=0                                      #Stores the best distance and tour
    bestTour=[]
    for i in range(0, len(currentPop)):             #stores the best tour from the initial population
        currentDist=currentPop[i][1]
        currentTour=currentPop[i][0]
        if bestDist==0 or bestDist>=currentDist:
            bestTour=currentTour
            bestDist=currentDist
    for x in range(0,1250):                         #Repeats for the given number of generations
        popFitness=[]
        breedingPool=[]
        popFitness=fitness(currentPop)              #Calculates the fitness for each tour in the population
        breedingPool=selection(popFitness, int(size/10))  #Generates the breeding pool
        newPop=[]
        for i in range(0, len(breedingPool)-1):         #Iterates through the breeding pool
            children=[]
            children=breed(breedingPool[i], breedingPool[i+1], size, matrix)    #Mates two parents from the breeding pool to produce two children
            newPop.append(children[0])                  #Adds the children to the new population
            newPop.append(children[1])        
        currentPop=newPop[:]                            #Sets the new population to be the current population
        for i in range(0, len(currentPop)):             #Checks if any of the new population are a better tour
            currentDist=currentPop[i][1]
            currentTour=currentPop[i][0]
            if bestDist==0 or bestDist>=currentDist:
                bestTour=currentTour
                bestDist=currentDist
    print(bestTour)
    print(bestDist)
    return([bestTour,bestDist])                         #Returns the best tour

def fitness(population):            #Calcualtes the fitness of every member of a population
    fitness=[]
    for i in range(0, len(population)):         #Iterates trhough the population
        fitness.append([1/population[i][1], population[i][0]])  #Sets their fitness to be 1/tour length
    fitness.sort(key=lambda x: x[1])            #Sorts the tours in ascending order
    return fitness

def selection(fitness, elite):              #Selects which of the population will be used for breeding
    total=0
    breedingPool=[]
    for k in range(1, elite):               #Keeps the specified number of most fit tours
        breedingPool.append(fitness[len(fitness)-k][1])
    for i in range(0, len(fitness)):        #Calcualtes the total of all fitnesses
        total+=fitness[i][0]
    while True:                             #Repeats until the breeding pool is the correct size
        for j in range(0, len(fitness)):        #Iterates through the population
            currentFitness=(360*fitness[j][0])/total    #Calculates the probability a tour will be accepted
            pick=360*random.random()
            if currentFitness>=pick:                    #Adds tour to breeding pool if the probability is large enough
                breedingPool.append(fitness[j][1])
                if len(breedingPool)==int(len(fitness)/2+1):    #Returns the breeding pool if it is large enough
                    return breedingPool
            
def breed(parent1, parent2, size, matrix):      #Breeds two parents to produce two children using order crossover operator
    info=[]
    newDistance=0
    child1=[0]*size         #Generates the two empty children
    child2=[0]*size
    p1=[]
    p2=[] 
    geneA=int(random.random()*len(parent1))         #Randomly selects two positions to split the parents
    geneB=int(random.random()*len(parent1))
    while geneB==geneA:                             #Generates new position if they are the same
        geneB=int(random.random()*len(parent1))
    startGene=min(geneA, geneB)                     #Finds the smaller of the two positions
    endGene=max(geneA, geneB)                       #Finds the larger of the two positions
    for i in range(startGene, endGene):             #Copies the sections between the splits to the two children
        child1[i]=parent1[i]
        child2[i]=parent2[i]
    for j in range(endGene, size):                  #Iterates through the parents after the second split and appends to list of cities
        p1.append(parent1[j])
        p2.append(parent2[j])
    for j in range(0,endGene):                      #Iterates through the parents before the second split and appends to list of cities
        p1.append(parent1[j])
        p2.append(parent2[j])
    p1 = [item for item in p1 if item not in child2]    #Removes the cities already in the child from the corresponding list of cities
    p2 = [item for item in p2 if item not in child1]
    for i in range(endGene, size):                      #Iterates through the children after the second split and appends the cities from the corresponding list
        if child1[i]==0:
            child1[i]=p2[0]
            p2.pop(0)
        if child2[i]==0:
            child2[i]=p1[0]
            p1.pop(0)
    for i in range(0, endGene):         #Iterates through the children before the first split and appends the cities from the corresponding list
        if child1[i]==0:
            child1[i]=p2[0]
            p2.pop(0)
        if child2[i]==0:
            child2[i]=p1[0]
            p1.pop(0)
    child1.append(child1[0])            #Apends the start node to the end of the tour
    child2.append(child2[0])
    child1=mutate(child1,size, matrix, 0.01)     #Mutates the children with a given probability
    child2=mutate(child2,size, matrix, 0.01)
    
    for i in range(0, size):                         #Calculates the new tour length
        dist=matrix[child1[i]-1][child1[i+1]-1]
        newDistance+=dist
    info.append([child1, newDistance])              #Appends the child to the list of children
    newDistance=0
    for i in range(0,size):                         #Calculates the new tour length
        dist=matrix[child2[i]-1][child2[i+1]-1]
        newDistance+=dist
    info.append([child2, newDistance])              #Appends the child to the list of children
    return info

def writeFile(name, size, tour, distance):         #Writes the output file
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





    
