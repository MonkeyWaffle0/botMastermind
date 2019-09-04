import pygame
from pygame.locals import *
import random


pygame.init()

black = (0, 0, 0)
transparent = (0, 0, 0, 0)

cowImage = "Images/cow.png"
bullImage = "Images/bull.png"
xCow = 378

red = "Images/red.png"
blue = "Images/blue.png"
green = "Images/green.png"
pink = "Images/pink.png"
cyan = "Images/cyan.png"
orange = "Images/orange.png"
white = "Images/white.png"

redPos = [290, 30]
bluePos = [290, 80]
greenPos = [290, 130]
pinkPos = [290, 180]
cyanPos = [290, 230]
orangePos = [290, 280]
whitePos = [290, 330]
pinDict = {red: redPos, blue: bluePos, green: greenPos, pink: pinkPos, cyan: cyanPos,
           orange: orangePos, white: whitePos}
pinValue = {red: "1", blue: "2", green: "3", pink: "4", cyan: "5", orange: "6", white: "7"}

xGuess = 380
holeOnePos = [xGuess, 95]
holeTwoPos = [xGuess, 152]
holeThreePos = [xGuess, 209]
holeFourPos = [xGuess, 263]
holeDict = {0: holeOnePos, 1: holeTwoPos, 2: holeThreePos, 3: holeFourPos}

currentChoice = ""
currentGuess = "****"
attempts = 0

onGo = 0


def generateCombination():
    combination = ""
    while len(combination) < 4:
        rand = random.randrange(1, 8)
        rand = str(rand)
        if rand not in combination:
            combination = combination + rand
        else:
            continue
    return combination


def mousePosition():
    pos = pygame.mouse.get_pos()
    return pos


def trackMouse():
    position = mousePosition()
    for pin, pinPos in pinDict.items():
        if pinPos[1] < position[1] < pinPos[1] + 41 and pinPos[0] < position[0] < pinPos[0] + 41:
            if "selected" not in pin:
                putImage("Images/light" + pin[7: len(pin)], pinPos)
        else:
            putImage(pin, pinPos)

    global onGo
    if 730 < position[0] < 821 and 320 < position[1] < 382:
        onGo += 1
        if onGo <= 5:
            putImage("images/lightgobutton.png", (730, 320))
    else:
        onGo = 0
        putImage("images/gobutton.png", (730, 320))


def selectPin(color):
    for pin, pinPos in pinDict.items():
        if color == pin:
            if "selected" not in pin:
                pinDict["Images/selected" + pin[7: len(pin)]] = pinDict.pop(pin)

        else:
            if "selected" in pin:
                pinDict["Images/" + pin[15: len(pin)]] = pinDict.pop(pin)
            putImage(pin, pinPos)


def placePin(currentChoice, i, x, y):
    if currentChoice == "":
        return None

    putImage(currentChoice, (x, y))

    global currentGuess
    currentGuess = list(currentGuess)
    for pin, value in pinValue.items():
        if pin == currentChoice:
            currentGuess[i] = value

    currentGuess = "".join(currentGuess)


def result(guess):
    if "*" not in guess:
        global currentGuess, xGuess, holeOnePos, holeTwoPos, holeThreePos, holeFourPos, holeDict, xCow, attempts
        guessingCombination = list(playerCombination)
        cows = 0
        bulls = 0
        # Looking for a matching number.
        for i, number in enumerate(guessingCombination):
            if number in guess:
                # If the number has the same index as in the combination, adds a bull, otherwise, adds a cow.
                if guess[i] == guessingCombination[i]:
                    bulls += 1
                else:
                    cows += 1
                # Change the matching number so that it won't be analysed again.
                guessingCombination[i] = "*"
        i = 0
        if bulls > 0:
            for bull in range(bulls):
                i += 1
                if i == 1:
                    putImage(bullImage, [xCow, 31])
                elif i == 2:
                    putImage(bullImage, [xCow + 22, 31])
                elif i == 3:
                    putImage(bullImage, [xCow, 53])
                elif i == 4:
                    putImage(bullImage, [xCow + 22, 53])
        if cows > 0:
            for cow in range(cows):
                i += 1
                if i == 1:
                    putImage(cowImage, (xCow, 31))
                elif i == 2:
                    putImage(cowImage, (xCow + 22, 31))
                elif i == 3:
                    putImage(cowImage, (xCow, 53))
                elif i == 4:
                    putImage(cowImage, (xCow + 22, 53))

        xCow += 61
        xGuess += 61
        attempts += 1
        holeOnePos = [xGuess, 95]
        holeTwoPos = [xGuess, 152]
        holeThreePos = [xGuess, 208]
        holeFourPos = [xGuess, 262]
        holeDict = {0: holeOnePos, 1: holeTwoPos, 2: holeThreePos, 3: holeFourPos}

        if currentGuess == playerCombination:
            font = pygame.font.Font('freesansbold.ttf', 128)
            text = font.render("YOU WIN !", True, black)
            display.blit(text, (500, 300))
        elif attempts == 14:
            font = pygame.font.Font('freesansbold.ttf', 116)
            text = font.render("YOU LOST BITCH !", True, black)
            display.blit(text, (450, 300))
        currentGuess = "****"



def putImage(img, pos):
    loadedImg = pygame.image.load(img)
    display.blit(loadedImg, pos)
    return loadedImg


display = pygame.display.set_mode((1550, 900), RESIZABLE)
pygame.display.set_caption("Mastermind")
display.fill([120, 200, 200])
picture = putImage("Images/board.png", (230, 0))
clock = pygame.time.Clock()
playerCombination = generateCombination()
aiCombination = generateCombination()
running = True

print('picture', picture.get_bitsize())
print('screen', display.get_bitsize())

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            position = mousePosition()
            for pin, pinPos in pinDict.items():
                if pinPos[1] < position[1] < pinPos[1] + 41 and pinPos[0] < position[0] < pinPos[0] + 41:
                    currentChoice = pin
                    selectPin(currentChoice)
            for index, hole in holeDict.items():
                if hole[0] < position[0] < hole[0] + 45 and hole[1] < position[1] < hole[1] + 45:
                    placePin(currentChoice, index, hole[0] - 4, hole[1] - 6)

            if 730 < position[0] < 821 and 320 < position[1] < 382:
                putImage("images/clickedgobutton.png", (730, 320))
                result(currentGuess)

    trackMouse()

    pygame.display.update()
    clock.tick(30)

pygame.display.quit()
pygame.quit()