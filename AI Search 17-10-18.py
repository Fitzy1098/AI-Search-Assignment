def readFile(filename):
    #filename = "AISearchtestcase.txt" #"NEWAISearchfile012.txt" #
    file = open(filename, 'r')
    data=file.readlines()
    stringdata="".join(data)
    return(stringdata)

def getName(stringdata):
    stringdata=stringdata.split("=")
    name=stringdata[1].lstrip(" ")                    
    name=name.split(",")[0]
    return(name)

def getSize(stringdata):
    stringdata=stringdata.split("=")
    size=""
    size=stringdata[2][1:2]
    i=3
    while stringdata[2][1:i].isdigit():
        size=stringdata[2][1:i]
        i+=1
    stringdata=stringdata[2][i:]

    return int(size)

def generateMatrix(size):
    size=int(size)
    matrix = [[0]*size for i in range(size)]
    return matrix

def populateMatrix(stringdata, size, matrix):
    stringdata=stringdata.split("=")
    size=""
    size=stringdata[2][1:2]
    i=3
    while stringdata[2][1:i].isdigit():
        size=stringdata[2][1:i]
        i+=1
    stringdata=stringdata[2][i:]
    
    stringdata=stringdata.split(",")
    size=int(size)
    length=size-1
    rowNum=1


    while length!=0:
        row=stringdata[:length]
        stringdata=stringdata[length:]    
        colNum=size


        for cell in row:
            num=""
            i=0
            foundInt=0
            while foundInt!=2:
                if cell[i].isdigit():
                    num+=cell[i]
                    foundInt=1
                else:
                    if foundInt == 1:
                        foundInt=2
                if cell[i]==cell[-1]:
                    foundInt=2
                i+=1    
            num=int(num)

            

            matrix[rowNum-1][size-colNum+rowNum]=num
            matrix[size-colNum+rowNum][rowNum-1]=num
            colNum-=1
        length-=1
        rowNum+=1
    return(matrix)

def printMatrix(size, matrix):
    for i in range(size):
        print(matrix[i])
    
def work(x):
    s=readFile(x)
    n=getName(s)
    si=getSize(s)
    m=generateMatrix(si)
    n=populateMatrix(s,si,m)
    printMatrix(si,n)
