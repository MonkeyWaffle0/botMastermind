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


def result(guess, ai=False):
    if "*" not in guess:
        global currentGuess, xGuess, holeOnePos, holeTwoPos, holeThreePos, holeFourPos, holeDict, xCow, attempts
        if not ai:
            guessingCombination = list(playerCombination)
        else:
            guessingCombination = list(aiCombination)
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
        if not ai:
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
        else:
            if bulls > 0:
                for bull in range(bulls):
                    i += 1
                    if i == 1:
                        putImage(bullImage, [xCow, 713])
                    elif i == 2:
                        putImage(bullImage, [xCow + 22, 713])
                    elif i == 3:
                        putImage(bullImage, [xCow, 735])
                    elif i == 4:
                        putImage(bullImage, [xCow + 22, 735])
            if cows > 0:
                for cow in range(cows):
                    i += 1
                    if i == 1:
                        putImage(cowImage, (xCow, 713))
                    elif i == 2:
                        putImage(cowImage, (xCow + 22, 713))
                    elif i == 3:
                        putImage(cowImage, (xCow, 735))
                    elif i == 4:
                        putImage(cowImage, (xCow + 22, 735))

        if not ai:
            if currentGuess == playerCombination:
                font = pygame.font.Font('freesansbold.ttf', 128)
                text = font.render("YOU WIN !", True, black)
                display.blit(text, (500, 300))
            elif attempts == 13:
                font = pygame.font.Font('freesansbold.ttf', 116)
                text = font.render("YOU LOST BITCH !", True, black)
                display.blit(text, (450, 300))
            currentGuess = "****"
            return aiGuess()
        else:
            if bulls == 4:
                font = pygame.font.Font('freesansbold.ttf', 128)
                text = font.render("YOU LOST BITCH !", True, black)
                display.blit(text, (500, 300))
            attempts += 1
            xGuess += 61
            xCow += 61
            holeOnePos = [xGuess, 95]
            holeTwoPos = [xGuess, 152]
            holeThreePos = [xGuess, 208]
            holeFourPos = [xGuess, 262]
            holeDict = {0: holeOnePos, 1: holeTwoPos, 2: holeThreePos, 3: holeFourPos}
            currentGuess = "****"
            return aiAnalyse(guess, cows, bulls)



possibleNumbers = ["1", "2", "3", "4", "5", "6", "7"]
aiAnswers = []
excludedPosition = []
threeDigitsTest = False
threeDigits = []
correctNumbers = []
abandonnedNumber = ""


def aiGuess():
    """Ai will generate a random combination, choosing digits one by one, taking account of the excludedPositions
    and the possibleNumbers."""
    global threeDigits, threeDigitsTest
    looptest = 0
    infiniteLoop = False
    searchLoop = True
    while searchLoop:
        looptest += 1
        if looptest == 500:
            infiniteLoop = True
        fail = False
        i = 0
        takenNumbers = []  # Digits already chosen by the AI
        answer = ""
        test = 0  # Amount of times the function looped
        while i < 4:
            ind = i  # Current index
            impossibleNumber = []  # Numbers that can't be at this index.
            # This loop will look at the next indexes and check if there is only one possibility for
            # each index, if it's the case, it will add the digit to impossibleNumber for the current
            # index to prevent going on an infinite loop.
            while ind < 3:
                futureBlock = []  # List of future impossible choices.
                # Append every excluded positions that match the current index to futureBlock
                for position in excludedPosition:
                    if position[0] == ind + 1 and position[1] not in futureBlock:
                        futureBlock.append(position[1])
                # Append the takenNumbers to futureBlock.
                for y in takenNumbers:
                    if y not in futureBlock:
                        futureBlock.append(y)
                # If futureBlock shows there is only 1 possible number left for a specific index, will
                # add it to impossibleNumber so it can be kept for the correct index.
                if len(futureBlock) >= len(possibleNumbers) - 1:
                    for x in possibleNumbers:
                        if x not in futureBlock and x not in impossibleNumber:
                            impossibleNumber.append(x)
                ind += 1
            # Append takenNumbers to impossibleNumber.
            for z in takenNumbers:
                if z not in impossibleNumber:
                    impossibleNumber.append(z)
            # Choose a number from possibleNumbers, if this number is an excludedPosition or
            # impossibleNumber, will choose another one.
            chosenNumber = random.choice(possibleNumbers)
            if (i, chosenNumber
                ) in excludedPosition or chosenNumber in impossibleNumber:
                test += 1
                # In the rare cases where this is stuck on an infinite loop, after 30 loops, will call
                # the function again.
                if test == 30:
                    break
                else:
                    continue
            else:
                i += 1
                takenNumbers.append(chosenNumber)
                answer += chosenNumber
        if threeDigitsTest:
            for number in threeDigits:
                if number not in answer:
                    fail = True
                    break

        for number in correctNumbers:
            if number not in answer:
                fail = True
                break
        if infiniteLoop:
            threeDigitsTest = False
            threeDigits = []
        if len(answer) < 4 or (answer in aiAnswers) or fail:
            continue
        else:
            searchLoop = False
            threeDigits = []
            # Append the current answer to aiAnswer so it won't call this answer again.
            aiAnswers.append(answer)
            return aiPlay(answer)


def aiPlay(answer):
    global xGuess, xCow
    y = 483
    answer = list(answer)
    for digit in answer:
        for pin, value in pinValue.items():
            if digit == value:
                putImage(pin, (xGuess - 4, y))
                y += 56
    return result(answer, ai=True)


def aiAnalyse(answer, cows, bulls):
    global threeDigitsTest, abandonnedNumber, threeDigits, correctNumbers, possibleNumbers
    if threeDigitsTest:
        if cows + bulls == 2:
            if abandonnedNumber not in correctNumbers:
                correctNumbers.append(abandonnedNumber)
        threeDigitsTest = False
        threeDigits = []
        abandonnedNumber = ""

    if bulls == 0:
        for i, number in enumerate(answer):
            excludedPosition.append((i, number))

    if cows + bulls == len(correctNumbers):
        allCorrect = True
        for number in correctNumbers:
            if number not in answer:
                allCorrect = False
        if allCorrect:
            for number in answer:
                if number not in correctNumbers:
                    possibleNumbers.remove(number)
                    for position in excludedPosition:
                        if position[1] == number:
                            excludedPosition.remove(position)

    if cows + bulls == 3:
        threeDigitsTest = True
        for number in answer:
            if number in correctNumbers:
                threeDigits.append(number)
                if len(threeDigits) > 3:
                    break

        if len(threeDigits) < 3:
            for number in answer:
                if number not in threeDigits:
                    threeDigits.append(number)
                    if len(threeDigits) == 3:
                        break
        for number in answer:
            if number not in threeDigits:
                abandonnedNumber = number
    elif cows + bulls == 4:
        if threeDigitsTest:
            threeDigits = []
            threeDigitsTest = False
        possibleNumbers = []
        correctNumbers = []
        for number in answer:
            possibleNumbers.append(number)
            correctNumbers.append(number)

    for number in range(1, 8):
        number = str(number)
        if number not in possibleNumbers:
            for position in excludedPosition:
                if position[1] == number:
                    excludedPosition.remove(position)
    # Returns the guess function until the answer matches the combination.



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