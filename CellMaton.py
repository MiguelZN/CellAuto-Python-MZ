import pygame,os,sys,random,math,time

#file path of folder
path = os.path.dirname(os.path.realpath(sys.argv[0]))
#iconpath = path+r"\cellautoicon.ico"
iconpath = path+r"/cellautoicon.ico"
icon = pygame.image.load(iconpath)

seconds = 0

pygame.init()

pygame.display.set_caption("CellAuto - Miguel Zavala")
pygame.display.set_icon(icon)

displayres = [320,320]

white = (250,250,250)
black = (0,0,0)
display = pygame.display.set_mode(displayres)
display.fill(black)
boundaryamount1 = 15
boundaryamount2 = 5




pixarray = pygame.PixelArray(display)
#pixarray[300][300] = (250,0,0)   -> creates a pixel as red in [300][300]

#gameattributes
displayx = displayres[0]
displayy = displayres[1]
displaysize = displayres[0] #does not matter either x or y
startinglivingcells = 40
cellidstart = startinglivingcells+1 #adds 1 to this everytime a new cell is created
listoflivingcells = []
gameRunning = True
listofspecies = ["blue","white","red","green","purple","orange","pink","yellow"] # types of species; 4 for now
strengthrange = (1,5)
reproducepercentage = 50
reproduceamount = 2
changeofreproduce = 10000 #out of 10000
chanceofdying = 1 #5/100

#COLORS
blue = (0,0,250)
green = (0,250,0)
red = (250,0,0)
black = (0,0,0)

#classes
class Cell():
    def __init__(self,id, posnx, posny, species,strength):
        global seconds
        self.cellid = id+1 #changes
        self.posnx = 0 #DEFAULT: 0
        self.posny = 0 #DEFAULT: 0
        self.color = [0,0,0]
        self.isalive = True
        self.canReproduce = False
        self.HasReproduced = False
        self.timealive = seconds+1
        self.species = "" #DEFAULT: ""
        self.strength = 0 #DEFAULT: 0
        self.speed = 1 #all cells are pixel speed 1 for now

        self.newcell(posnx,posny,species,strength)
        self.determinecolor()

    def checkCellSpeed(self):
        if(self.speed>2):
            self.speed = 2

    def increaseTimeAlive(self):
        global seconds
        self.timealive = seconds - self.timealive

        if(self.timealive>10):
            self.canReproduce = True

    def changeofdying(self):
        chance = random.randrange(0,1000)
        if(chanceofdying>=chance and seconds%10==0):
            self.strength-=1

    def determinecolor(self):
        strengthcolorincrease = self.strength * 30

        if(self.color[0]<=250 and self.color[1]<=250 and self.color[2]<=250):
            ""
        else:
            return None

        #SPECIES
        if(self.species=="red"):
            self.color = (250,0,0)
            #self.color[0] = self.color[0]+strengthcolorincrease
        elif(self.species=="blue"):
            self.color = (0,0,250)
            #self.color[2] = self.color[2] + strengthcolorincrease
        elif(self.species=="green"):
            self.color = (0,250,0)
            #self.color[1] = self.color[1] + strengthcolorincrease
        elif(self.species=="white"):
            self.color= (250,250,250)
        elif(self.species=="orange"):
            self.color = (255, 140, 0)
        elif (self.species == "purple"):
            self.color = (216, 118, 252)
        elif(self.species=="pink"):
            self.color= (255, 0, 238)
        elif(self.species=="yellow"):
            self.color= (255, 204, 0)









    def reproduce(self):
        #print(self.timealive)
        if(self.canReproduce==False and self.timealive<10 and self.HasReproduced==False):
            print("CANNOT REPRODUCE: TIMEALIVE:"+str(self.timealive))
            return None

        global cellidstart
        randx = random.choice((-10,10))
        randy = random.choice((-10, 10))
        print("TIMEALIVE:"+str(self.timealive))
        try:
            for i in range(reproduceamount):
                listoflivingcells.append(Cell(cellidstart,self.posnx+randx,self.posny+randy,self.species,random.randrange(strengthrange[0],strengthrange[1])))
                cellidstart=+1
        except:
            print("REPRODUCE ERROR")
        self.HasReproduced = True
        self.canReproduce = False



    def newcell(self,posnx,posny,species, strength):
        if(species=="newcell"):
            self.posnx = random.randrange(boundaryamount1,displayx-boundaryamount1)
            self.posny = random.randrange(boundaryamount1,displayy-boundaryamount1)
            self.species = random.choice(listofspecies)
            self.strength = random.randrange(strengthrange[0],strengthrange[1])
        else:
            self.posnx = posnx
            self.posny = posny
            self.species = species
            self.strength = strength

    def __str__(self):
        string = "Cell#"+str(self.cellid)\
                 +"\nSPECIES:"+self.species+"\n"\
                 "POSNX:"+str(self.posnx)+\
                 "\nPOSNY:"+str(self.posny)+\
                 "\nALIVE?:" + str(self.isalive)\
                 +"\nREPRODUCING?:"+str(self.reproducing)+\
                 "\nSTRENGTH:"+str(self.strength)+"\n"
        return string


#methods

#adds livingcells to the game, takes in an empty list of cells
def createLivingCells(list):
    for i in range(startinglivingcells):
        list.append(Cell(i,species="newcell",
                         posny= 0,
                         posnx= 0,
                         strength=0))  #appends a "Cell" to living cells list



def drawCells(celllist):
    print(len(celllist))
    for cell in celllist:

        """
        # drawing cells
        if (cell.species == "blue"):
            pixarray[cell.posnx][cell.posny] = blue
        elif (cell.species == "green"):
            pixarray[cell.posnx][cell.posny] = green
        elif (cell.species == "red"):
            pixarray[cell.posnx][cell.posny] = red
        elif (cell.species == "white"):
            pixarray[cell.posnx][cell.posny] = white
        """
        try:
            pixarray[cell.posnx][cell.posny] = cell.color
        except:
            print("COLORERROR")


#needs improvements
def movedrawCells(celllist):
    try:
        for cell in celllist:
            #keeps cells within display
            if(cell.posnx<=boundaryamount2):
                cell.posnx = displayx-boundaryamount1
            if(cell.posnx>=displayx-boundaryamount2):
                cell.posnx = boundaryamount1
            if(cell.posny>=displayy-boundaryamount2):
                cell.posny = boundaryamount1
            if(cell.posny<=boundaryamount2):
                cell.posny = displayy-boundaryamount1

            movex = random.choice((-1*cell.speed,cell.speed)) #either moves -1 back, 1 forward, 0 stays
            movey = random.choice((-1*cell.speed,cell.speed)) #either moves -1 back, 1 forward, 0 stays

            pixarray[cell.posnx][cell.posnx] = black

            #MOVEMENT
            cell.posnx = cell.posnx +movex
            cell.posny = cell.posny + movey

            """
            #comparing the cells with one another
            for othercell in celllist:
                #if the cell has a different cellid (not the same cell)
                #and is a different species and on the same spot
                if othercell.cellid!= cell.cellid and cell.posnx == othercell.posnx and cell.posny == othercell.posny and cell.species!= othercell.species:
                    if(cell.strength> othercell.strength):
                        othercell.isalive = False #other cell died
                    elif(othercell.strength>cell.strength):
                        cell.isalive = False
                    elif(cell.strength==othercell.strength):
                        whichcelldies = random.choice(("thiscell","othercell"))
                        if(whichcelldies=="thiscell"):
                            cell.isalive = False
                        elif(whichcelldies=="othercell"):
                            othercell.isalive = False
                            
            
    
                #if the cells are the same species and on the same spot
                #then create a new cell of same species in spot
    
                
                if cell.species == othercell.species and cell.posnx == othercell.posnx and cell.posny == othercell.posny:
                    global cellidstart
                    cellidstart =cellidstart+1
    
                    #adds a new cell in the same tile of the same species
                    listoflivingcells.append(Cell(id=cellidstart,
                                                  species=cell.species,
                                                  strength= random.randrange(strengthrange[0],strengthrange[1]),
                                                  posnx = random.randrange(0,displayx),
                                                  posny= random.randrange(0,displayy)))
            """
    except:
        print("MOVECELLS ERROR")
celltoremove = random.choice(("thiscell", "othercell"))
def checkCells():
    radius = 3 #if cells are within a 3 pixel radius

    try:
        id = 0
        for cell in listoflivingcells:
            id +=1

            cell.cellid = id
            cell.changeofdying()
            cell.checkCellSpeed()
            cell.increaseTimeAlive()

            #remove the cell once its strength is low
            if(cell.strength<=0 or cell.isalive==False):
                listoflivingcells.remove(cell)



            for othercell in listoflivingcells:

                if(cell.cellid==othercell.cellid and cell.species!=othercell.species):
                    print("CELLID ERROR")
                distance = math.sqrt(math.pow((othercell.posnx-cell.posnx),2)+math.pow((othercell.posny-cell.posny),2))
                if(othercell.cellid!=cell.cellid and distance<=3):
                        print("STILLWORKING")

                        if (cell.cellid != othercell.cellid and cell.species == othercell.species):  # creates a new cell
                            chance = random.randrange(0, changeofreproduce)

                            if (chance <= reproducepercentage):
                                cell.reproduce()
                            # print(len(listoflivingcells))
                            print("NEWCELL")

                        if(cell.strength> othercell.strength and cell.species!=othercell.species):
                            othercell.isalive = False
                            cell.speed+=1
                            cell.strength+=1
                            print("CELL DEFEATED OTHERCELL")
                            chance = random.randrange(0,100)

                            if(chance<=30):
                                cell.reproduce()

                        elif(othercell.strength>cell.strength and cell.species!=othercell.species):
                            cell.isalive = False
                            othercell.speed += 1
                            othercell.strength += 1
                            print("OTHERCELL DEFEATED CELL")
                            chance = random.randrange(0, 100)

                            if (chance <= 30):
                                othercell.reproduce()

                        elif(cell.strength==othercell.strength and cell.species!=othercell.species):
                            print("EVENMATCH")
                            if(celltoremove=="thiscell"):
                                cell.isalive = False
                                chance = random.randrange(0, 100)

                                if (chance <= 30):
                                    othercell.reproduce()










    except:
        print("CHECKCELLS ERROR")








#GAME
createLivingCells(listoflivingcells) #creates the living cells
clock = pygame.time.Clock()

"""
#TEXT
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 10)

populationinfo = myfont.render("Populations:",True,(0,0,0))
redspecies = myfont.render("blank",True,(250,0,0))
bluespecies = myfont.render("blank",True,(0,0,250))
greenspecies = myfont.render("blank",True,(0,250,0))

    #draws a rectangle box (unusable)
    #pygame.draw.rect(display,white,(400,0,500,500))

display.blit(populationinfo,(450,15))
"""
start = time.time()
end = ""
seconds = ""

while gameRunning:
    end = time.time()

    seconds = int(end-start)+1
    print(seconds)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    display.fill(black)



    movedrawCells(listoflivingcells)
    checkCells()

    #time.sleep(.02)

    try:
        drawCells(listoflivingcells)
    except:
        "DRAW ERROR"



    pygame.display.update()
    clock.tick(50)

