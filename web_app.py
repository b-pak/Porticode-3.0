from flask import Flask, render_template, redirect, url_for
import sys
from datetime import date
import _thread
import pygame


sys.path.append('/Users/PakBrian/Documents/GitHub/b-pak.github.io/Donation')

import moneymovement
from models import TransferType, TransferRequestStatus, TransferRequest

pygame.init()  # initialize pygame

win = pygame.display.set_mode((640, 359))  # create window of 500x500
pygame.display.set_caption("Donation Game")  # name the window to "string"

# rathian = monster(350, 150, 256, 256, 1, monster02, 10, 5, 2)

font = pygame.font.SysFont('Arial', 12, True)  # Define font type, size, bold, italics

# Ingame clock
clock = pygame.time.Clock()

# Loading images
bg = pygame.image.load("background2.png")  # Background image
scaled_bg = pygame.transform.scale(bg, (640, 359))
charSprite = pygame.image.load("sprites.png")  # Sprites image
buttonUp = pygame.image.load("buttonup.png")  # Buttonup image
ScaledButUp = pygame.transform.scale(buttonUp, (75, 75))
buttonDown = pygame.image.load("buttondown.png")  # Buttondown image
ScaledButDown = pygame.transform.scale(buttonDown, (75, 75))
monster01 = pygame.image.load("teostra.png")
monster01 = pygame.transform.scale(monster01, (1280, 576))
# player02 = pygame.image.load("player02.png")
# player02 = pygame.transform.scale(player02,(1020,426))
# monster02 = pygame.image.load('rathian.png')
# monster02 = pygame.transform.scale(monster02,(1280,512))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/donate/', methods=['POST'])
def one_click_donate():
    donate(user_account, charity_account_1, 1, "Unicef")
    return render_template('donate.html')

@app.route('/back/', methods=['POST'])
def back():
    return redirect(url_for('index'))

class monster():
    def __init__(self, x, y, width, height, level, monSprite, numSprites, numSpritesPerRow, numRows):
        #Geometry and physics
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        #Idle loop variables
        self.idleCount = 0
        #Monster attributes
        self.level = level
        #Idle sprites animation
        self.sprites = []
        self.numSprites = numSprites
        spriteCount = 0
        for i in range(numSpritesPerRow):
            for j in range(numRows):
                self.sprites.append(monSprite.subsurface(i*self.width, j*self.height, self.width, self.height))
                spriteCount += 1
                if spriteCount == numSprites:
                    break

    def draw(self,win):
        # Cycling idle sprites
        if self.idleCount >= self.numSprites :
            self.idleCount = 0

        win.blit(self.sprites[self.idleCount],(self.x, self.y))

class player():
    def __init__(self, x, y, width, height):
        #Geometry and physics
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        #Movespeed variables
        self.vel = 10
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.walkCount = 0
        #Character attributes
        self.exp = 0
        self.addEXP = False
        self.level = 1
        #Walking sprites animation
        self.walkRight = []
        self.walkLeft = []
        self.walkUp = []
        self.walkDown = []
        for i in range(3):
            self.walkRight.append(charSprite.subsurface(i * 64, 128, 64, 64))
            self.walkLeft.append(charSprite.subsurface(i * 64, 64, 64, 64))
            self.walkUp.append(charSprite.subsurface(i * 64, 192, 64, 64))
            self.walkDown.append(charSprite.subsurface(i * 64, 0, 64, 64))

    def draw(self, win):
        # Cycling walking sprites
        if self.walkCount + 1 >= 4:
            self.walkCount = 0
        # Call walking sprites
        if self.left:
            win.blit(self.walkLeft[self.walkCount], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(self.walkRight[self.walkCount], (self.x, self.y))
            self.walkCount += 1
        elif self.up:
            win.blit(self.walkUp[self.walkCount], (self.x, self.y))
            self.walkCount += 1
        elif self.down:
            win.blit(self.walkDown[self.walkCount], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(charSprite, (self.x, self.y), (64, 0, 64, 64))  # Default sprit into window (image, (position), (starting crop, end crop)

    #Donation gives exp
    def add_experience(self):
        self.exp += 60
        if self.exp > 100:
            self.exp = self.exp - 100
            self.level += 1


man = player(50, 180, 64, 64)
teostra = monster(350, 100, 256, 192, 1, monster01, 14, 5, 3)


# Drawing character
def redrawGameWindow():     #Function of character update

    #Rookie test
    #win.fill((0, 0, 0))  # fill the window with black so that character doesnt duplicate
    #pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))  # Character as a rectangle (placed in window, colour of rectangle, position and size)

    #Putting images in window
    win.blit(scaled_bg, (0, 0))  #Background
    # win.blit(ScaledButUp, (300, 150)) #Buttonup
    buttonArea = pygame.Rect(300, 150, 75, 75)

    #Putting characters in window
    man.draw(win)
    teostra.draw(win)
    #rathian.draw(win)

    #Hold mouse down to click button
    '''
    if pygame.event.type == pygame.MOUSEBUTTONDOWN and pygame.event.button == 1:  #Mousebutton down and is left mouse button
        pos = pygame.mouse.get_pos()    #Get mouse position
        if buttonArea.collidepoint(pos):
            pygame.draw.rect(win, (0, 0, 0), (10, 10, 100, 100))
            win.blit(ScaledButDown, (300, 150))
    '''


    #Experience bar
    pygame.draw.rect(win, (179, 149, 0),  (man.x+9, man.y-11, 50, 10))
    pygame.draw.rect(win, (255, 255, 25), (man.x+9, man.y-11, 0 + man.exp * 0.5, 10))      #draw rectangle, (in window, colour, position, size)

    #Level counter
    text = font.render('Lv. ' + str(man.level), 1, (0, 0, 0))
    win.blit(text, (man.x+9, man.y-10))

    pygame.display.update()  # Update game

# Main loop





base_url = 'https://api-sandbox.capitalone.com'
client_id = '83c59ee7d6a4479c8e142422cbe9022a'
client_secret = '6d5c0077c6d4e214c6850d5f1611689e'

moneymovement.setup_oauth(client_id, client_secret, base_url)

accounts = moneymovement.get_eligible_accounts()

user_account = accounts['accounts'][1]
charity_account_1 = accounts['accounts'][2]
charity_account_2 = accounts['accounts'][3]

'''
actors = [user_account, charity_account_1, charity_account_2]

for actor in actors:
    print(actor['accountNickname'])
'''

def donate(origin, destination, amount, name):

    today = str(date.today())

    transfer_request = TransferRequest()

    transfer_request.originMoneyMovementAccountReferenceId = origin["moneyMovementAccountReferenceId"]
    transfer_request.destinationMoneyMovementAccountReferenceId = destination["moneyMovementAccountReferenceId"]
    transfer_request.transferAmount = amount  # Upto 2 decimal places
    transfer_request.currencyCode = "USD"  # optional Default: USD
    transfer_request.transferDate = today
    transfer_request.memo = "Donation"  # optional
    transfer_request.transferType = TransferType.ACH.value
    transfer_request.frequency = "OneTime"  # optional Default: OneTime

    transfer_response = moneymovement.initiate_transfer(transfer_request)

    transfer_id = transfer_response['transferRequestId']

    transfer_request_receipt = moneymovement.get_transfer_request(transfer_id)

    #print(transfer_request_receipt)

    '''
    filters = {
        "fromDate": "2018-11-16",
        "toDate": "2018-11-18",
        "transferType": None,
        "transferRequestStatus": None
    }

    transfer_requests = moneymovement.get_transfer_requests(user_account["moneyMovementAccountReferenceId"],
                                                            filters)

    transfers = transfer_requests['transferRequests']

    for transfer in transfers:
        print(transfer['transferRequestId'] + " " + transfer['memo'])
    '''

    print("You Donated {} {} to {}!".format(amount, "USD", name))

    man.add_experience()


def loop_game():


    # Create array of walking direction sprites
    '''
    walkRight = []
    walkLeft = []
    walkUp = []
    walkDown = []
    for i in range(3):
        walkRight.append(charSprite.subsurface(i*64,128,64,64))
        walkLeft.append(charSprite.subsurface(i*64,64,64,64))
        walkUp.append(charSprite.subsurface(i*64,192,64,64))
        walkDown.append(charSprite.subsurface(i*64,0,64,64))
    '''



    run = True
    while run:
        #pygame.time.delay(100)  #ingame clock, in milliseconds
        clock.tick(10)

        #Monster idle loop
        teostra.idleCount += 1
        #rathian.idleCount += 1

        #Checking for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()    #create list of keys, origin in top left corner

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and man.x > man.vel:
            man.x -= man.vel
            man.left = True
            man.right = False
            man.up = False
            man.down = False
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and man.x < 640 - man.width - man.vel :
            man.x += man.vel
            man.left = False
            man.right = True
            man.up = False
            man.down = False
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and man.y < 270 - man.width - man.vel:
            man.y += man.vel
            man.left = False
            man.right = False
            man.up = False
            man.down = True
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and man.y > 230 - man.width - man.vel:
            man.y -= man.vel
            man.left = False
            man.right = False
            man.up = True
            man.down = False

        else:
            man.walkCount = 1
            '''
            man.right = False
            man.left = False
            man.up = False
            man.down = False
            '''

        redrawGameWindow()  #Call func for character update

    pygame.quit()


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, threaded=True)
    _thread.start_new_thread(loop_game(), ())
