import pygame
from pygame.locals import *
import random
from time import sleep


pygame.init()

black = (0, 0, 0)


# Pins that will be placed on the game board.
class Pin:
    def __init__(self, color, pos):
        self.color = color
        # Path to the pin's image.
        self.path = "images/" + color + ".png"
        # Position of the pin on the GUI.
        self.pos = pos
        # If the pin is currently selected or not.
        self.selected = False

    def select(self):
        """Change the pin path to the image of the selected pin,
        deselect every other pins."""
        if not self.selected:
            self.selected = True
            global pinList
            pinList.remove(self)
            self.path = "images/selected" + self.color + ".png"
            pinList.append(self)

        for pin in pinList:
            if pin.color != self.color:
                if pin.selected:
                    pin.deselect()

    def deselect(self):
        """Change the pin path to the image of the deselected pin."""
        if self.selected:
            self.selected = False
            global pinList
            pinList.remove(self)
            self.path = "images/" + self.color + ".png"
            pinList.append(self)


# Creating the seven pins that player will use to select and place.
red = Pin("red", (290, 30))
blue = Pin("blue", (290, 80))
green = Pin("green", (290, 130))
pink = Pin("pink", (290, 180))
cyan = Pin("cyan", (290, 230))
orange = Pin("orange", (290, 280))
white = Pin("white", (290, 330))

pinList = [red, blue, green, pink, cyan, orange, white]
# Values of the pins (could also be in the Pin class but I chose a dictionary.
pinValue = {red: "1", blue: "2", green: "3", pink: "4", cyan: "5", orange: "6", white: "7"}

# Path to the cow and bull images.
cowImage = "Images/cow.png"
bullImage = "Images/bull.png"
# Starting x value of the position of the cow and bull image.
xCow = 378
# Starting x value of the position of the pins images.
xGuess = 380
# List of all the pins images on the board, used to replace them when switching to colorblind mode.
imgList = []
# Position of the 4 holes where the player has to place the pins.
holeOnePos = [xGuess, 95]
holeTwoPos = [xGuess, 152]
holeThreePos = [xGuess, 209]
holeFourPos = [xGuess, 263]
holeDict = {0: holeOnePos, 1: holeTwoPos, 2: holeThreePos, 3: holeFourPos}
# Pin that is currently selected.
currentChoice = ""
# Player's answer, will be a 4 digits number.
currentGuess = "****"
# Attempts to guess the correct combination.
attempts = 0


def generateCombination():
    """Generate a random 4 digits combination containing figures between 1 and 7 (each corresponding to a pin)."""
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
    """Return a tuple corresponding to the position of the mouse."""
    pos = pygame.mouse.get_pos()
    return pos


onGo = 0
def trackMouse():
    """Get the position of the mouse, if the mouse is over a pin, will load a highlighted image of the pin,
    if the pin is selected, will load the selected image of the pin."""
    global imgList
    position = mousePosition()
    for pin in pinList:
        # Checks if the mouse position is on a pin position.
        if pin.pos[1] < position[1] < pin.pos[1] + 41 and pin.pos[0] < position[0] < pin.pos[0] + 41:
            # If the pin is not selected, will load the highlighted image of the pin.
            if not pin.selected:
                if not colorblindMode:
                    putImage("Images/light" + pin.color + ".png", pin.pos)
                else:
                    putImage("Images/light" + pin.color + "cb.png", pin.pos)
            else:
               if not colorblindMode:
                   putImage(pin.path, pin.pos)
               else:
                   putImage("Images/selected" + pin.color + "cb.png", pin.pos)

        # Loads every other pin images.
        else:
            if not colorblindMode:
                putImage(pin.path, pin.pos)
            elif colorblindMode:
                if pin.selected:
                    putImage("images/selected" + pin.color + "cb.png", pin.pos)
                else:
                    putImage("images/" + pin.color + "cb.png", pin.pos)
            # If the tuple (image path, image position) is not in imgList, will add it to the list.
            if (pin.path, pin.pos) not in imgList:
                imgList.append((pin.path, pin.pos))

    # If the mouse if over the go button, will highlight it.
    global onGo
    if 730 < position[0] < 821 and 415 < position[1] < 477:
        onGo += 1
        if onGo <= 5:
            putImage("images/lightgobutton.png", (730, 415))
    else:
        onGo = 0
        putImage("images/gobutton.png", (730, 415))


def placePin(currentChoice, index, x, y):
    """Place the image of the selected pin on the hole the player clicked on.
    Then change the currentGuess according to what to player chose.
    index corresponds to the hole the player clicked on."""
    if currentChoice == "":
        return None
    # Puts the image of the pin on the hole.
    if not colorblindMode:
        putImage("images/" + currentChoice.color + ".png", (x, y))
    elif colorblindMode:
        putImage("images/" + currentChoice.color + "cb.png", (x, y))
    global imgList
    if ("images/" + currentChoice.color + ".png", (x, y)) not in imgList:
        imgList.append(("images/" + currentChoice.color + ".png", (x, y)))

    # Replace the index value in currentGuess with the pin value of the selected pin.
    global currentGuess
    currentGuess = list(currentGuess)
    for pin, value in pinValue.items():
        if pin == currentChoice:
            currentGuess[index] = value

    currentGuess = "".join(currentGuess)


def result(guess, ai=False):
    """Analyse how many cows and bulls the player got, then put the cows and bulls images according to the result.
    Then return aiGuess function so the AI will generate a combination.
    If ai = True then it will analyse the AI's guess."""
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

        # Put the cows and bulls images.
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

        # If the player or the AI got the right combination (4 bulls), will display a winning/losing text and stop
        # the current game loop.
        global endGame
        if not ai:
            if currentGuess == playerCombination:
                font = pygame.font.Font('freesansbold.ttf', 128)
                text = font.render("YOU WIN !", True, black)
                display.blit(text, (500, 300))
                endGame = True
            elif attempts == 13:
                font = pygame.font.Font('freesansbold.ttf', 116)
                text = font.render("YOU LOST BITCH !", True, black)
                display.blit(text, (320, 300))
                endGame = True
            currentGuess = "****"
            return aiGuess()
        else:
            if bulls == 4:
                font = pygame.font.Font('freesansbold.ttf', 116)
                text = font.render("YOU LOST BITCH !", True, black)
                display.blit(text, (320, 300))
                endGame = True

            # If neither the player or the AI got the right combination, will increment xGuess and xCow so the player
            # can play on the next row of holes.
            if not endGame:
                putImage("images/bgfill.png", (xGuess - 5, 315))
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

# List of the possible digits the AI can choose.
possibleNumbers = ["1", "2", "3", "4", "5", "6", "7"]
# List of the answer tha AI already gave.
aiAnswers = []
# Contains tuples (index, value) of excluded positions for the AI.
excludedPosition = []
# If the AI gets a least 3 cows and bulls, will do a three digits test for the next guess.
threeDigitsTest = False
# List of the three digits the AI will test.
threeDigits = []
# List of the digits that are in the AI's combination.
correctNumbers = []
# Digit the AI abandonned during the three digits test.
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
    """Puts the images of the pins the AI chose, returns the result function for the AI."""
    global xGuess, xCow
    y = 483
    answer = list(answer)
    for digit in answer:
        for pin, value in pinValue.items():
            if digit == value:
                putImage("images/" + pin.color + ".png", (xGuess - 4, y))
                y += 56
    return result(answer, ai=True)


def aiAnalyse(answer, cows, bulls):
    """Make decisions according to the result the AI got."""
    global threeDigitsTest, abandonnedNumber, threeDigits, correctNumbers, possibleNumbers
    if threeDigitsTest:
        if cows + bulls == 2:
            if abandonnedNumber not in correctNumbers:
                correctNumbers.append(abandonnedNumber)
        threeDigitsTest = False
        threeDigits = []
        abandonnedNumber = ""

    # If there are no bulls, adds the current position to the excludedPosition list.
    if bulls == 0:
        for i, number in enumerate(answer):
            excludedPosition.append((i, number))

    # If there are as many cows and bulls as correct numbers, will remove the other digits from the possible numbers.
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

    # If cows + bulls == 3, will run a three digits test. Meaning it will put 3 of the current digits in the next
    # guess.
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


def putImage(img, pos):
    """Load an image and blit it to the display."""
    loadedImg = pygame.image.load(img)
    display.blit(loadedImg, pos)
    return loadedImg


# Setting up the display.
display = pygame.display.set_mode((1550, 900), RESIZABLE)
pygame.display.set_caption("Mastermind")
display.fill([120, 200, 200])
putImage("Images/board.png", (230, 0))
clock = pygame.time.Clock()
playerCombination = generateCombination()
aiCombination = generateCombination()
running = True
endGame = False
colorblindMode = False

# Running loop
while running:
    # Loop of a game, when the game is over, will reset the display and start the loop again.
    while not endGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                endGame = True
            elif event.type == pygame.MOUSEBUTTONUP:
                position = mousePosition()
                for pin in pinList:
                    if pin.pos[1] < position[1] < pin.pos[1] + 41 and pin.pos[0] < position[0] < pin.pos[0] + 41:
                        currentChoice = pin
                        pin.select()
                for index, hole in holeDict.items():
                    if hole[0] < position[0] < hole[0] + 45 and hole[1] < position[1] < hole[1] + 45:
                        placePin(currentChoice, index, hole[0] - 4, hole[1] - 6)

                if 730 < position[0] < 821 and 415 < position[1] < 477:
                    putImage("images/clickedgobutton.png", (730, 415))
                    result(currentGuess)
                elif 1485 < position[0] < 1525 and 40 < position[1] < 80:
                    if not colorblindMode:
                        putImage("images/ticked.png", (1487, 38))
                        colorblindMode = True
                        for image in imgList:
                            path = image[0]
                            putImage(path[:len(path) - 4] + "cb" + ".png", image[1])
                    else:
                        putImage("images/unticked.png", (1487, 38))
                        colorblindMode = False
                        for image in imgList:
                            putImage(image[0], image[1])

        if not endGame:
            putImage("images/arrow.png", (xGuess - 3, 315))
        putImage("images/colorblindmode.png", (1320, 30))
        trackMouse()
        pygame.display.update()
        clock.tick(30)

    # Resets the display and variables for a new game to start.
    if running:
        sleep(5)
    display = pygame.display.set_mode((1550, 900), RESIZABLE)
    pygame.display.set_caption("Mastermind")
    display.fill([120, 200, 200])
    putImage("Images/board.png", (230, 0))
    clock = pygame.time.Clock()
    playerCombination = generateCombination()
    aiCombination = generateCombination()
    endGame = False
    possibleNumbers = ["1", "2", "3", "4", "5", "6", "7"]
    aiAnswers = []
    excludedPosition = []
    threeDigitsTest = False
    threeDigits = []
    correctNumbers = []
    abandonnedNumber = ""
    xGuess = 380
    xCow = 378
    holeOnePos = [xGuess, 95]
    holeTwoPos = [xGuess, 152]
    holeThreePos = [xGuess, 209]
    holeFourPos = [xGuess, 263]
    holeDict = {0: holeOnePos, 1: holeTwoPos, 2: holeThreePos, 3: holeFourPos}
    currentChoice = ""
    currentGuess = "****"
    attempts = 0
    imgList = []
    if colorblindMode:
        putImage("images/ticked.png", (1487, 38))


pygame.display.quit()
pygame.quit()

