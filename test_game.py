import pygame



run = True
while run:
    #pygame.time.delay(100)  #ingame clock, in milliseconds
    clock.tick(10)
    #Checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    redrawGameWindow()  #Call func for character update