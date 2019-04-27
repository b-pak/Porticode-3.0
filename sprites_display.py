import pygame
pygame.init()       #initialize pygame

win = pygame.display.set_mode((640,359))   #create window of 500x500
pygame.display.set_caption("Donation Game")       #name the window to "string"

#Loading images
bg = pygame.image.load("background.png")         #Background image
charSprite = pygame.image.load("sprites.png")    #Sprites image
buttonUp = pygame.image.load("buttonup.png")     #Buttonup image
ScaledButUp = pygame.transform.scale(buttonUp, (75,75))
buttonDown = pygame.image.load("buttondown.png") #Buttondown image
ScaledButDown = pygame.transform.scale(buttonDown,(75,75))
monsterorigin = pygame.image.load("monster01.png")
monster = pygame.transform.flip(monsterorigin, True, False)
#Create array of walking direction sprites
walkRight = []
walkLeft = []
walkUp = []
walkDown = []
for i in range(3):
    walkRight.append(charSprite.subsurface(i*64,128,64,64))
    walkLeft.append(charSprite.subsurface(i*64,64,64,64))
    walkUp.append(charSprite.subsurface(i*64,192,64,64))
    walkDown.append(charSprite.subsurface(i*64,0,64,64))
#Create array of monster idle sprites
monsterIdle = []
for i in range(3):
    monsterIdle.append(monster.subsurface(i*267,0,267,178))


#Ingame clock
clock = pygame.time.Clock()

#Character geometry and physics
x = 50      #position
y = 50
width = 32  #size
height = 32
vel = 5     #Movespeed

#Character attributes
exp = 0
level = 1

#Initiate movespeed variables
left = False
right = False
up = False
down = False
walkCount = 0
idleCount = 1

# Drawing character
def redrawGameWindow():     #Function of character update
    global walkCount    #Take walkCount as global variable
    global idleCount    #Take idleCount as global variable

    #Rookie test
    #win.fill((0, 0, 0))  # fill the window with black so that character doesnt duplicate
    #pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))  # Character as a rectangle (placed in window, colour of rectangle, position and size)

    #Putting images in window
    win.blit(bg,(0,0))  #Background
    win.blit(ScaledButUp,(300,150)) #Buttonup

    #Cycling walking sprites
    if walkCount + 1 >= 4:
        walkCount = 0

    #Cycling idling sprites
    if idleCount + 1 >= 4:
        idleCount = 1

    #Call walking sprites
    if left:
        win.blit(walkLeft[walkCount],(x,y))
        walkCount += 1

    elif right:
        win.blit(walkRight[walkCount],(x,y))
        walkCount += 1
    elif up:
        win.blit(walkUp[walkCount],(x,y))
        walkCount += 1
    elif down:
        win.blit(walkDown[walkCount],(x,y))
        walkCount += 1
    else:
        win.blit(charSprite, (x,y), (64,0,64,64))   #Default sprit into window (image, (position), (starting crop, end crop)

    #Hold mouse down to click button
    if event.type == pygame.MOUSEBUTTONDOWN:
        win.blit(ScaledButDown, (300, 150))

    #Experience bar
    pygame.draw.rect(win, (255,255,25), (x+9, y-11, 50, 10))      #draw rectangle, (in window, colour, position, size)
    pygame.draw.rect(win, (179,149,0),  (x+9, y-11, 50, 10))

    #Level counter
    text = font.render('Lv. ' + str(level), 1, (0,0,0))
    win.blit(text, (x+9,y-13))

    #Monster sprite
    win.blit(monsterIdle[idleCount],(380,100))

    pygame.display.update()  # Update game

#Main loop
font = pygame.font.SysFont('Arial', 12, True)   #Define font type, size, bold, italics
run = True
while run:
    #pygame.time.delay(100)  #ingame clock, in milliseconds
    clock.tick(9)

    #MonsterIdle Loop
    idleCount += 1

    #Checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()    #create list of keys, origin in top left corner

    if keys [pygame.K_LEFT] or keys [pygame.K_a]:
        x -= vel
        left = True
        right = False
        up = False
        down = False
    elif keys [pygame.K_RIGHT] or keys [pygame.K_d]:
        x += vel
        left = False
        right = True
        up = False
        down = False
    elif keys[pygame.K_DOWN] or keys [pygame.K_s]:
        y += vel
        left = False
        right = False
        up = False
        down = True
    elif keys[pygame.K_UP] or keys [pygame.K_w]:
        y -= vel
        left = False
        right = False
        up = True
        down = False
    else:
     #   right = False
     # left = False
     # up = False
        #down = False
        walkCount = 0

    redrawGameWindow()  #Call func for character update


pygame.quit()