'''
modules.py - multiple functions for cano.py simulations

Student Name - Miguel Pereira
Student ID   - 22646169

Version History:
    - 6/10/24 - original version created
    - 6/10/24 - final version finished

'''
import random
import numpy as np
import matplotlib.pyplot as plt
import tkinter.messagebox
import os
import math

from tkinter import *
from tkinter import ttk
from classes import *
from noise import snoise3





#runs the starting window of the program
def startWindow():
    #runs when start button is clicked
    def clicked1():
        error = False
        #check if entries are empty
        if len(mapEntry1.get()) == 0 or len(mapEntry2.get()) == 0:
            if error != True: tkinter.messagebox.showinfo("Empty Value",  "One of your Map entries are empty. Please re-enter!")
            error = True
        if len(blockEntry.get()) == 0:
            if error != True: tkinter.messagebox.showinfo("Empty Value",  "Block entry is empty. Please re-enter!")
            error = True


        #check if entries are intergers
        try:
            int(mapEntry1.get())
        except ValueError:
            if error != True: tkinter.messagebox.showinfo("Invalid Value",  "One of your Map entries is not an intiger")
            error = True
        try:
            int(mapEntry2.get())
        except ValueError:
            if error != True: tkinter.messagebox.showinfo("Invalid Value",  "One of your Map entries is not an intiger")
            error = True
        try:
            int(blockEntry.get())
        except ValueError:
            if error != True: tkinter.messagebox.showinfo("Invalid Value",  "Block entry is not an intiger")
            error = True


        if error == False:
            #intigers
            mapShape, blockSize, mapSeed = [int(mapEntry1.get()), int(mapEntry2.get())], int(blockEntry.get()), int(seedEntry.get())
            #strings
            season = seasonConvert(seasonSelect.get())

            #check if entries are valid
            if not 1 <= mapShape[0] <= 7 or not 1 <= mapShape[1] <= 7:
                if error != True: tkinter.messagebox.showinfo("Invalid Value",  "One of your Map Shape entries are invalid. Please re-enter!")
                error = True
            if not 50 <= blockSize <= 100:
                if error != True: tkinter.messagebox.showinfo("Invalid Value",  "Block Size entry is invalid. Please re-enter!")
                error = True

            #if no errors continue
            if error == False:
                StartWindow.destroy()
                simDataEdit(1, [season, 0, -1])
                random.seed(258) #247

                noise = convertColour(noiseMap(blockSize * max(mapShape[0], mapShape[1]), blockSize/100 * max(mapShape[0], mapShape[1]), mapSeed))
                grid = np.zeros([mapShape[0]*blockSize, mapShape[1]*blockSize]) #make grid
                grid = np.dstack([grid, grid, grid])                            #convert grid to rgb
                grid = noise[0:mapShape[0]*blockSize, 0:mapShape[1]*blockSize]  #make grid the noise

                blocks = appendboxes(blockSize, mapShape)
                place(mapShape, blockSize, blocks, grid)                        #place houses and trees

                mainWindow(mapShape, blockSize, blocks, grid)

    def clicked2():
        #runs if random seed button is clicked
        seedEntry.config(state="normal")
        seedEntry.delete(0, END)
        seedEntry.insert(END, random.randint(0, 1000))
        seedEntry.config(state="readonly")

    #defines starting windows parameters
    StartWindow = Tk()
    StartWindow.title("Start Simulation")
    StartWindow.geometry("300x125")

    #defines starting windows objects
    Label(StartWindow, text="Map Shape: (1-7)").grid(row=0)
    mapEntry1 = Entry(StartWindow, width=10)
    mapEntry2 = Entry(StartWindow, width=10)
    mapEntry1.insert(END, "2")
    mapEntry2.insert(END, "3")
    mapEntry1.grid(row=0, column=1)
    mapEntry2.grid(row=0, column=2)

    Label(StartWindow, text="Block Size: (50-100)").grid(row=1)
    blockEntry = Entry(StartWindow, width=10)
    blockEntry.insert(END, "50")
    blockEntry.grid(row=1, column=1)

    Label(StartWindow, text="Seed:").grid(row=3)
    seedEntry = Entry(StartWindow, width=10)
    seedEntry.insert(END, 232)
    seedEntry.config(state="readonly")
    seedEntry.grid(row=3, column=1)

    Label(StartWindow, text="Starting Season").grid(row=2)
    seasonSelect = ttk.Combobox(StartWindow, width=10, state="readonly", values=["Summer", "Autumn", "Winter", "Spring"])
    seasonSelect.set("Summer")
    seasonSelect.grid(row=2,column=1)

    Button(StartWindow, text = "Start Simulation", command = clicked1).grid(row=4,column=0)
    Button(StartWindow, text="Randomize Seed", command = clicked2).grid(row=4, column=1)

    #runs the starting window
    mainloop()





#runs the main window of the program
def mainWindow(mapShape, blockSize, blocks, grid):


    #runs when step button is clicked
    def clicked1():
        plt.clf()
        plot(HeatCheckBox.get(), LineCheckBox.get(), mapShape, blockSize, blocks, (seasonL, dayL, hourL, airTempL), grid)

    #runs when auto step button is clicked
    def clicked2():
        error = False

        #check if entries are intergers
        try:
            int(autoEntry.get())
        except ValueError:
            if error != True: tkinter.messagebox.showinfo("Invalid Value",  "Your AutoStep entry is not an intiger")
            error = True

        if error == False:
            #check if entries are valid
            if int(autoEntry.get()) > 90:
                if error != True: tkinter.messagebox.showinfo("Invalid Value",  "Your AutoStep entry is larger than 90. Please re-enter!")
                error = True

            #if no errors continue
            if error == False:
                for i in range(int(autoEntry.get())):
                    plt.clf()
                    plot(HeatCheckBox.get(), LineCheckBox.get(), mapShape, blockSize, blocks, (seasonL, dayL, hourL, airTempL), grid)

    #defines main windows parameters
    MainWindow = Tk()
    MainWindow.title("Manage Simulation")
    MainWindow.geometry("325x150")

    #defines main windows objects
    HeatCheckBox = IntVar()
    Checkbutton(MainWindow, text = "Heat View", variable = HeatCheckBox, onvalue=1, offvalue=0).grid(row=1, sticky=W)
    LineCheckBox = IntVar()
    Checkbutton(MainWindow, text = "Block Border", variable = LineCheckBox, onvalue=1, offvalue=0).grid(row=2, sticky=W)

    seasonL = Label(MainWindow, text= "Season: null")
    seasonL.grid(row=0, column=2)
    dayL = Label(MainWindow, text= "Day: null")
    dayL.grid(row=1, column=2)
    hourL = Label(MainWindow, text= "Hour: null")
    hourL.grid(row=2, column=2)
    airTempL = Label(MainWindow, text= "Air Temp: null")
    airTempL.grid(row=3, column=2)

    Label(MainWindow, text="AutoStep Amount:").grid(row=0)
    autoEntry = Entry(MainWindow, width=10)
    autoEntry.insert(END, "6")
    autoEntry.grid(row=0, column=1)

    Button(MainWindow, text = "Step Simulation", command = clicked1).grid(row=4, column=0)
    Button(MainWindow, text = "Auto Step Simulation", command = clicked2).grid(row=4, column=1)

    #runs the main window
    mainloop()



#generates the biomes size/orientation and placement of trees/houses in the blocks
def place(mapShape, blockSize, blocks, grid):
    for row in range(mapShape[0]):
        for col in range(mapShape[1]):
            blockX, blockY, biome = col * blockSize, row * blockSize, random.randint(0, 1)
            block = row * mapShape[1] + col
            newGrid = grid[blockY: blockY + blockSize, blockX: blockX + blockSize]

            if biome == 0:
                for i in range(random.randint(3, 12)):
                    treeSize = random.randint(0, 1)
                    if treeSize == 0:
                        hw = 3
                    else:
                        hw = 5

                    x, y = find(blockSize, newGrid, hw, hw) #find a free space on the map
                    plotTree(x, y, newGrid, treeSize) #set the x, y to a tree like structure
            else:
                for i in range(random.randint(1, 3)):
                    orientation = random.randint(0, 1)
                    if orientation == 0:
                        h = 5
                        w = 10
                    else:
                        h = 10
                        w = 5

                    x, y = find(blockSize, newGrid, h, w)   #find a free space on the map
                    plotHouse(x, y, newGrid, orientation)   #set the x, y to a house like structure
                    blocks[block].add_item(House((x, y), (0, 0), orientation)) #send house position to blockclass
                pass



#returns a valid position for a specified object
def find(blockSize, newGrid, height, width):
    x, y = random.randint(5, blockSize - 5), random.randint(5, blockSize - 5)
    count = 0
    data = np.ones(height * width)

    size = newGrid[y - int(round(height/2, 0)):y + int(round(height/2 + 1, 0)), x - int(round(width/2, 0)):x + int(round(width/2 + 1, 0))]  #get the data to be checked

    for row in range(height):   #format the data to be checked
        for col in range(width):
            i = row * width + col
            data[i] = size[row][col][2] * 255


    while check(data): #check if the x, y is in water or structures
        if count < 200:
            count += 1

            x, y = random.randint(5, blockSize - 5), random.randint(5, blockSize - 5)
            size = newGrid[y - int(round(height/2, 0)):y + int(round(height/2 + 1, 0)), x - int(round(width/2, 0)):x + int(round(width/2 + 1, 0))]

            for row in range(height):   #format the data to be checked
                for col in range(width):
                    i = row * width + col
                    data[i] = size[row][col][2] * 255
        else:
            data = np.ones(height * width)
    else:   #return data
        return x, y



def check(data):   #function checks data if it is in water or colliding
    colours = np.array([237, 236, 153, 81, 52, 18, 34])

    for b in data:
        for c in colours:
            if c == b:
                return True


def appendboxes(blockSize, mapShape):   #adds items to the block class for the total amount of blocks in the map
    blocks = []

    for row in range(mapShape[0]):
        for col in range(mapShape[1]):
            blocks.append(Block(blockSize, (blockSize * col, blockSize * row)))

    return blocks



def plotboxlines(mapShape, blockSize, colours, heatView):   #plots lines over the border of all blocks
    for i in range(mapShape[0]):
        plt.plot([0, blockSize * mapShape[1] - 0.5], [blockSize * i, blockSize * i], c = colours[heatView])
    for i in range(mapShape[1]):
        plt.plot([blockSize * i, blockSize * i], [0, blockSize * mapShape[0] - 0.5], c = colours[heatView])



def convertHeat(temps, grid):   #converts the rgb grid to its temperature values (therefore a heat view using cmap)
    blank = np.ones([len(grid), len(grid[0])])

    for block in range(len(grid)): #convert noise to rgb form
        for row in range(len(grid[0])):
            g = grid[block][row][2]

            if g == 237/255: blank[block][row] = temps[0] #water
            elif g == 236/255: blank[block][row] = temps[1] #sand
            elif g == 153/255: blank[block][row] = temps[2] #low grass
            elif g == 128/255: blank[block][row] = temps[3] #medium grass
            elif g == 117/255: blank[block][row] = temps[4] #high grass
            elif g == 92/255: blank[block][row] = temps[5] #mountain

            elif g == 81/255 or g == 52/255: blank[block][row] = temps[6] #tree
            elif g == 18/255 or g == 34/255: blank[block][row] = temps[7] #house

    return blank



#plots simulation
def plot(heatView, blockBorder, mapShape, blockSize, blocks, labels, grid):
    #variables
    data = simDataEdit(0, 0)
    lines = ["RED", "GREEN"]

    #steps simulation
    data, temps = step(labels, data)

    if blockBorder == 1:    #if block border is ticked
        plotboxlines(mapShape, blockSize, lines, heatView)

    if heatView == 1:   #if heat view is ticked
        grid = convertHeat(temps, grid)

    #add items
    plotPath(mapShape, blocks, blockSize, heatView)

    #sets simulation grid size
    plt.imshow(grid, vmin=0, vmax=40, cmap="rainbow")

    #update data
    simDataEdit(1, data)

    #defines simulatin ui parameters
    plt.title("Temperature Simulation")
    plt.show()



#steps the simulation logic once
def step(label, data):
    #DATA: [0] = season, [1] = day, [2] = hour
    #LABELS: [0] = season, [1] = day, [2] = hour, [3] = airTemp

    #variables
    seasons = ["Summer", "Autumn", "Winter", "Spring"]

    #time
    data[1] = [data[1] + 1 if data[2] == 23 else data[1]][0]    #increment the day
    data[2] = [data[2] + 1 if data[2] != 23 else 0][0]          #increment the hour

    #heat
    data[0] = [data[0] - data[0] if data[0] == 3 else data[0]][0]   #reset to summer past spring
    data[0] = [data[0] + 1 if data[1] == 90 else data[0]][0]        #increment the season
    data[1] = [data[1] - data[1] if data[1] == 90 else data[1]][0]  #reset the day counter

    airTemp = getAirTemp(data[2], data[0])
    waterTemp = getWaterTemp(data[2], data[0])
    houseTemp = getHouseTemp(data[2])

    temps = [
        waterTemp,
        airTemp + 6,
        airTemp + 3,
        airTemp,
        airTemp - 3,
        airTemp - 6,
        airTemp - 5,
        houseTemp,
        airTemp + 10]

    #update labels
    label[0].config(text=f"Season: {seasons[data[0]]}")
    label[1].config(text=f"Day: {data[1]}")
    label[2].config(text=f"Hour: {data[2]}")
    label[3].config(text=f"Air Temp: {airTemp}")

    return data, temps



#can be used to read or write to the simData.txt file
def simDataEdit(rw, data):

    if rw == 0:
        file = open(os.path.join(os.path.dirname(__file__), 'simData.txt'), "r")
        data = file.readlines()

        for i in range(len(data)): data[i] = int(data[i].strip())
        file.close()

        return data

    elif rw == 1:
        open(os.path.join(os.path.dirname(__file__), 'simData.txt'), 'w').close()   #clears current file
        file = open(os.path.join(os.path.dirname(__file__), 'simData.txt'), "a")    #opens file
        
        for i in range(len(data)): file.write(f"{data[i]}\n")
        file.close()

    else:
        pass



#converts rgb colour value to a usable value in the code
def RGB(r, g, b):
    colour = [r/255, g/255, b/255]
    return colour



#generates perlin noise for the map (not yet RGB)
def noiseMap(mapShape, blockScale, seed):
    scale = mapShape/blockScale
    noise = np.array([[snoise3((x + 0.1) / scale, y / scale, seed, octaves=1, persistence=0.5, lacunarity=2) for x in range(mapShape)] for y in range(mapShape)])

    return noise



#converts perlin noise to RGB
def convertColour(noise):
    for row in range(len(noise)):   #convert noise form -1,1 to 0,1 and to landscape colors
        for col in range(len(noise[0])):
            noise[row][col] = ((noise[row][col] + 1) * 1) / 2

    blank = np.ones([len(noise[0]), len(noise[0]), 3])

    for block in range(len(noise)): #convert noise to rgb form
        for row in range(len(noise[0])):
            n = noise[block][row]

            if 0 <= n <= 0.15: blank[block][row] = np.array([RGB(146, 197, 237)])
            elif 0.15 <= n <= 0.2: blank[block][row] = np.array([RGB(252, 250, 236)])
            elif 0.2 <= n <= 0.3: blank[block][row] = np.array([RGB(224, 231, 153)])
            elif 0.3 <= n <= 0.7: blank[block][row] = np.array([RGB(164, 203, 128)])
            elif 0.7 <= n <= 0.9: blank[block][row] = np.array([RGB(108, 182, 117)])
            elif 0.9 <= n <= 1.0: blank[block][row] = np.array([RGB(88, 144, 92)])

    return blank



#converts season from string to int value
def seasonConvert(season):
    seasons = np.array(["Summer", "Autumn", "Winter", "Spring"])
    season = np.where(seasons == str(season))[0][0]

    return season



#calculates the air temp based on hour and season
def getAirTemp(hour, season):
    temps = [30.8, 16.4, 23.6, 25.1, 14.3, 19.7, 18.4, 8.4, 13.4, 22.9, 10.6, 16.8] #max,min,mean temps of seasons in perth

    seasonmean = temps[season * 3 + 2]
    seasondif = seasonmean - temps[season * 3 + 1]

    output = np.arange(0, 24)
    output = [round(math.sin(output[i]/3.7) * seasondif + seasonmean, 2) for i in range(len(output))]

    return output[hour]



#calculates water temp based on hour and season
def getWaterTemp(hour, season):
    temps = [30.8, 16.4, 23.6, 25.1, 14.3, 19.7, 18.4, 8.4, 13.4, 22.9, 10.6, 16.8] #max,min,mean temps of seasons in perth

    seasonmean = temps[season * 3 + 2]
    seasondif = (seasonmean - temps[season * 3 + 1]) / 2

    output = np.arange(0, 24)
    output = [round(math.sin(output[i]/3.7) * seasondif + seasonmean, 2) for i in range(len(output))]

    return output[hour]



#calculates indoor house temp based on hour and season
def getHouseTemp(hour):
    temps = [23, 19, 21]

    seasonmean = temps[2]
    seasondif = (seasonmean - temps[1])

    output = np.arange(0, 24)
    output = [round(math.sin(output[i]/3.7) * seasondif + seasonmean, 2) for i in range(len(output))]

    return output[hour]



#draws the tree sprites on the given grid
def plotTree(x, y, newGrid, size):
    if size == 0:
        newGrid[y:y + 1, x - 1:x + 2] = np.array([RGB(4,63,52)])
        newGrid[y - 1:y + 2, x:x + 1] = np.array([RGB(4,63,52)])
        newGrid[y:y + 1, x:x + 1] = np.array([RGB(15, 118, 81)])
    if size == 1:
        newGrid[y:y + 1, x - 2:x + 3] = np.array([RGB(4,63,52)])
        newGrid[y - 2:y + 3, x:x + 1] = np.array([RGB(4,63,52)])
        newGrid[y - 1:y + 2, x - 1:x + 2] = np.array([RGB(4,63,52)])

        newGrid[y:y + 1, x - 1:x + 2] = np.array([RGB(15, 118, 81)])
        newGrid[y - 1:y + 2, x:x + 1] = np.array([RGB(15, 118, 81)])



#draws the house sprites on the given grid
def plotHouse(x, y, newGrid, orientation):
    if orientation == 0:
        newGrid[y - 2:y + 3, x - 4:x + 5] = np.array([RGB(146, 60, 18)])
        newGrid[y - 1:y + 2, x - 3:x + 4] = np.array([RGB(231, 139, 34)])
    if orientation == 1:
        newGrid[y - 4:y + 5, x - 2:x + 3] = np.array([RGB(146, 60, 18)])
        newGrid[y - 3:y + 4, x - 1:x + 2] = np.array([RGB(231, 139, 34)])



#plots the path between the houses
def plotPath(mapShape, blocks, blockSize, heatView):
    colourTemp = ["#e78b22", "#ff9d53"]

    for row in range(mapShape[0]):
        for col in range(mapShape[1]):
            block = row * mapShape[1] + col

            if len(blocks[block].items) >= 2:   #checks the blocks class to see which blocks have enough houses to path between
                house1, house2 = blocks[block].items[0].pos, blocks[block].items[1].pos
                relPos = [blockSize * row, blockSize *  col]

                plt.plot([house1[0] + relPos[1], house2[0] + relPos[1]], [house1[1] + relPos[0], house2[1] + relPos[0]], colourTemp[heatView], lw=2)