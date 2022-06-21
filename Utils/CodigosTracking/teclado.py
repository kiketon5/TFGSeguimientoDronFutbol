import pygame

def init():
    pygame.init()
    win = pygame.display.set_mode((400, 400))

def getKey(keyName):
    ans = False
    for eve in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame,'K_{}'.format(keyName))
    #K_{LEFT}
    if keyInput[myKey]:
        ans = True
    pygame.display.update()

    return ans

def main():
    if getKey("LEFT"):
        print("LEFT KEY PRESSED")
    if getKey("RIGHT"):
        print("RIGHT KEY PRESSED")
    if getKey("UP"):
        print("UP KEY PRESSED")
    if getKey("DOWN"):
        print("DOWN KEY PRESSED")

if __name__ == '__main__':
    init()
    while True:
        main()