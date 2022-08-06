import pygame
import random 
pygame.init()

worldx = 800
worldy = 550

DISPLAYSURF = pygame.display.set_mode((worldx, worldy))
pygame.display.set_caption("The Tale of Penumbria")

clock = pygame.time.Clock()
done = False
lvl = 1
grav  = 0
health = 140

tx = 40
ty = 40

shift_x = 5
pos = 0
changeLevel = False
gameOver = False
win = False
frameCount = 0
jumpCount = 0
displayTitlePage = True


# IMAGES ================================================================================
TITLE = pygame.transform.scale(pygame.image.load("THE TALE OF.png").convert_alpha(), (worldx, worldy))
BG1 = pygame.transform.scale(pygame.image.load("foresty.jpg").convert_alpha(), (worldx, worldy))
walkRight = [pygame.image.load('R1.png').convert_alpha(), pygame.image.load('R2.png').convert_alpha(), pygame.image.load('R3.png').convert_alpha(), pygame.image.load('R4.png').convert_alpha(), pygame.image.load('R5.png').convert_alpha(), pygame.image.load('R6.png').convert_alpha(), pygame.image.load('R7.png').convert_alpha(), pygame.image.load('R8.png').convert_alpha(), pygame.image.load('R9.png').convert_alpha()]
walkLeft = [pygame.image.load('L1.png').convert_alpha(), pygame.image.load('L2.png').convert_alpha(), pygame.image.load('L3.png').convert_alpha(), pygame.image.load('L4.png').convert_alpha(), pygame.image.load('L5.png').convert_alpha(), pygame.image.load('L6.png').convert_alpha(), pygame.image.load('L7.png').convert_alpha(), pygame.image.load('L8.png').convert_alpha(), pygame.image.load('L9.png').convert_alpha()]
groundblock = pygame.transform.scale(pygame.image.load('ground.png').convert_alpha(), (40, 40))
playerImg = pygame.image.load('standing.png')
energy = pygame.transform.scale(pygame.image.load('energy.png').convert_alpha(), (40, 40))
spike = pygame.transform.scale(pygame.image.load('spikes.png').convert_alpha(), (40, 40))
fires = pygame.transform.scale(pygame.image.load('fire.png').convert_alpha(), (80, 80))
doorway = pygame.transform.scale(pygame.image.load('doorway.jpg').convert_alpha(), (80, 80))
gameover = pygame.transform.scale(pygame.image.load('gameover.jpg').convert_alpha(), (800, 550))
youwin = pygame.transform.scale(pygame.image.load('winscreen.jpg').convert_alpha(), (800, 550))
instructions = pygame.transform.scale(pygame.image.load('arrowkeys2.png').convert_alpha(), (600, 150))
healthtext = pygame.transform.scale(pygame.image.load('healthtext.png').convert_alpha(), (200, 150))

# MUSIC ===================================================================================
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1) #music will play indefinitely

# COLOURS =================================================================================
BLACK = (0, 0, 0)
NAVY = (0, 0, 60)
DARK_BLUE = (0, 0, 90)
BLUE = (0, 0, 120)
GREEN = (0, 66, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
HEALTHBAR = (0, 200, 0)

# OBJECTS AND FUNCTIONS ===================================================================

class player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = image
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.image = image
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.on_ground = False
        self.on_plat = False
        self.under_plat = False
        self.plat = plat_list
        self.hitbox = (self.x + 20, self.y, 17, 42)
        self.pos = 0
        self.hitFire = False
        
    def draw(self, DISPLAYSURF, plat_list):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                playerImg = walkLeft[self.walkCount//3]
                self.walkCount += 1
                
            elif self.right:
                playerImg = walkRight[self.walkCount //3]
                self.walkCount += 1
            
        else:
            if self.right:
                playerImg = walkRight[0]           
                
            else:
                playerImg = walkLeft[0]

        self.y += grav

        DISPLAYSURF.blit(playerImg, (self.x, self.y))
        self.hitbox = (self.x + 22, self.y + 14, 15, 50)
                                     
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        self.rect = pygame.Rect(x, y, 40, 40)
        self.rect.y = y
        self.rect.x = x
        self.width = width
        self.height = height
    def platform(lvl, tx, ty):
        plat_list = pygame.sprite.Group()
        if lvl == 1:
            ploc = []
            ploc.append((200, 280, 3))
            ploc.append((400, 220, 3))
            ploc.append((600, 140,3))
            ploc.append((800, 80, 3))
            ploc.append((1000, 140, 1))
            ploc.append((1200, 220, 1))
            ploc.append((1400, 280, 1))
            ploc.append((1880, 280, 4))
            ploc.append((2400, 280, 2))
            ploc.append((2600, 220, 16))
            ploc.append((3300, 140, 3))
            ploc.append((3500, 180, 0))
            ploc.append((3700, 150, 0))
            ploc.append((3900, 210, 0))
            ploc.append((4100, 160, 0))
            ploc.append((4500, 280, 2))
            ploc.append((4660, 210, 4))
            ploc.append((4900, 140, 1))
            ploc.append((5100, 140, 3))
            
            i = 0
            while i < len(ploc):
                j=0
                while j <= ploc[i][2]:
                    plat = Platform((ploc[i][0]+(j*tx)),ploc[i][1],tx,ty, groundblock)
                    plat_list.add(plat)
                    j += 1
                #print('run' + str(i) + str(ploc[i]))
                i += 1
        if lvl == 2:
            ploc = []
            ploc.append((200, 280, 3))
        return plat_list

class Spikes(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        self.rect = pygame.Rect(x, y, 40, 40)
        self.rect.y = y
        self.rect.x = x
    def generateSpike(lvl, tx, ty):
        spike_list = pygame.sprite.Group()
        sloc = []
        if lvl == 1:
            sloc.append((800,320,3))
            sloc.append((1800, 320, 8))
            sloc.append((2640, 180, 1))
            sloc.append((2760, 180, 1))
            sloc.append((2940, 180, 0))
            sloc.append((3020, 180, 0))
            sloc.append((3100, 180, 1))
            sloc.append((3400, 320, 20))
            sloc.append((4740, 170, 1))
            i = 0
            while i < len(sloc):
                j=0
                while j <= sloc[i][2]:
                    s = Spikes((sloc[i][0]+(j*tx)),sloc[i][1],tx,ty, spike)
                    spike_list.add(s)
                    j += 1
                i += 1
        if lvl == 2:
            sloc.append((800,320,3))
            sloc.append((1800, 320, 8))
            sloc.append((2640, 180, 1))
            sloc.append((2760, 180, 1))
            sloc.append((2940, 180, 0))
            sloc.append((3020, 180, 0))
            sloc.append((3100, 180, 1))
            
            i = 0
            while i < len(sloc):
                j=0
                while j <= sloc[i][2]:
                    s = Spikes((sloc[i][0]+(j*tx)),sloc[i][1],tx,ty, spike)
                    spike_list.add(s)
                    j += 1
                i += 1
        return spike_list

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        self.rect = pygame.Rect(x, y, 40, 40)
        self.rect.y = y
        self.rect.x = x
    def generateGround(lvl, tx, ty):
        ground_list = pygame.sprite.Group()
        if lvl == 1:
            gloc = []
            gloc.append((0, 360, 150))
            i = 0
            while i < len(gloc):
                j=0
                while j <= gloc[i][2]:
                    ground = Ground((gloc[i][0]+(j*tx)),gloc[i][1],tx,ty, groundblock)
                    ground_list.add(ground)
                    j += 1
                i += 1
            return ground_list
        if lvl == 2:
            gloc = []
            gloc.append((0, 360, 90))
            i = 0
            while i < len(gloc):
                j=0
                while j <= gloc[i][2]:
                    ground = Ground((gloc[i][0]+(j*tx)),gloc[i][1],tx,ty, groundblock)
                    ground_list.add(ground)
                    j += 1
                i += 1
            return ground_list

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        self.rect = pygame.Rect(x + 5, y + 30, 20, 20)
        self.rect.y = y
        self.rect.x = x
    def generateFireball(lvl):
        fire_list = pygame.sprite.Group()
        floc = []
        if lvl == 1:
            floc.append((350, 0))
            i = 0
            while i < len(floc):
                fire = Fireball(floc[i][0], floc[i][1], 80, 80, fires)
                fire_list.add(fire)
                i += 1
            return fire_list
        if lvl == 2:
            floc.append((550, 0))
            i = 0
            while i < len(floc):
                fire = Fireball(floc[i][0], floc[i][1], 80, 80, fires)
                fire_list.add(fire)
                i += 1
            return fire_list

class Energy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        self.rect = pygame.Rect(x + 10, y + 10, 20, 20)
        self.rect.y = y
        self.rect.x = x
    def generateEnergy(lvl):
        energy_list = pygame.sprite.Group()
        eloc = []
        if lvl == 1:
            eloc.append((300, 200))
            eloc.append((1140, 120))
            eloc.append((1340, 180))
            eloc.append((1540, 240))
            eloc.append((1950, 180))
            eloc.append((2720, 180))
            eloc.append((2860, 180))
            eloc.append((2980, 180))
            eloc.append((3060, 180))
            eloc.append((3500, 140, 0))
            eloc.append((3700, 110, 0))
            eloc.append((3900, 170, 0))
            eloc.append((4100, 120, 0))
            i = 0
            while i < len(eloc):
                ener = Energy(eloc[i][0], eloc[i][1], 40, 40, energy)
                energy_list.add(ener)
                i += 1
        elif lvl == 2:
            eloc.append((300, 200))
            i = 0
            while i < len(eloc):
                ener = Energy(eloc[i][0], eloc[i][1], 40, 40, energy)
                energy_list.add(ener)
                i += 1
        return energy_list

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.y = y
        self.rect.x = x
    def generatePortal(lvl):
        portal_list = pygame.sprite.Group()
        poloc = []
        if lvl == 1:
            poloc.append((5140, 60))
            i = 0
            while i < len(poloc):
                portal = Portal(poloc[i][0], poloc[i][1], 80, 80, doorway)
                portal_list.add(portal)
                i += 1
        if lvl == 2:
            poloc.append((3340, 60))
            i = 0
            while i < len(poloc):
                portal = Portal(poloc[i][0], poloc[i][1], 80, 80, doorway)
                portal_list.add(portal)
                i += 1
        return portal_list

    
all_Sprites = pygame.sprite.Group()
    
def drawBottomPanel():
    pygame.draw.rect(DISPLAYSURF, NAVY,(0,410,600,200))
    pygame.draw.rect(DISPLAYSURF, DARK_BLUE, (600, 410, 300, 200))
    pygame.draw.rect(DISPLAYSURF, BLUE, (0, 400, 1000, 10))
    pygame.draw.rect(DISPLAYSURF, BLUE, (590, 400, 10, 200))
    pygame.draw.rect(DISPLAYSURF, RED, (630, 480, 140, 15))
    DISPLAYSURF.blit(instructions, (0, 410))
    DISPLAYSURF.blit(healthtext, (600, 400))

def redrawGameWindow(HEALTHBAR, health):
    DISPLAYSURF.fill(GREEN)
    ground_list.draw(DISPLAYSURF)
    energy_list.draw(DISPLAYSURF)
    portal_list.draw(DISPLAYSURF)
    char.draw(DISPLAYSURF, plat_list)
    plat_list.draw(DISPLAYSURF)
    spike_list.draw(DISPLAYSURF)
    fire_list.draw(DISPLAYSURF)
    drawBottomPanel()
    pygame.draw.rect(DISPLAYSURF, HEALTHBAR, (630, 480, health, 15))
    pygame.display.update()

def shiftWorld():
    if char.x >= 500 and char.right and not collideLeft and char.pos < 4500:
        char.x -= shift_x
        char.pos += shift_x
        for plat in plat_list:
            plat.rect.x -= shift_x
        for energy in energy_list:
            energy.rect.x -= shift_x
        for s in spike_list:
            s.rect.x -= shift_x
        for fire in fire_list:
            fire.rect.x -= shift_x
        for ground in ground_list:
            ground.rect.x -= shift_x
        for portal in portal_list:
            portal.rect.x -= shift_x
    elif char.x <= 100 and char.pos > 0 and char.left and not collideRight:
        char.x += shift_x
        char.pos -= shift_x
        for plat in plat_list:
            plat.rect.x += shift_x
        for energy in energy_list:
            energy.rect.x += shift_x
        for s in spike_list:
            s.rect.x += shift_x
        for fire in fire_list:
            fire.rect.x += shift_x
        for ground in ground_list:
            ground.rect.x += shift_x
        for portal in portal_list:
            portal.rect.x += shift_x  
           
# GENERATE ================================================================================
ground_list = Ground.generateGround(lvl , tx, ty)
plat_list = Platform.platform(lvl, tx, ty)
energy_list = Energy.generateEnergy(lvl)
fire_list = Fireball.generateFireball(lvl)
spike_list = Spikes.generateSpike(lvl, tx, ty)
char = player(0, 296, 64, 64, playerImg)
portal_list = Portal.generatePortal(lvl)

# TITLE PAGE LOOP ======================================================================
while not done and displayTitlePage:
    DISPLAYSURF.blit(TITLE, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            displayTitlePage = False
    clock.tick(60)
    pygame.display.update()

# MAIN GAME LOOP =========================================================================
while not done and not gameOver and not win:
    clock.tick(60) #this game runs at 60 FPS

    frameCount += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True           
#gravity
    if not char.on_ground:
        if grav < 2: #gravity capped so player doesn't accelerate through platforms
            grav += 0.35
        char.y += grav

#move the fireballs
    for fire in fire_list:
        fire.rect.x -= 8
        fire.rect.y += 5  

#movement
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP]:
                if char.left:
                    facing = -1
                else:
                    facing = 1
                    
    if keys[pygame.K_LEFT] and char.x > char.vel:
        char.x -= char.vel
        char.left = True
        char.right = False
        char.standing = False
    elif keys[pygame.K_RIGHT] and char.x < worldx - char.width:
        char.x += char.vel
        char.left = False
        char.right = True
        char.standing = False
    else:
        char.standing = True
        #char.left = False
        #char.right = False
        char.walkCount = 0
        
#jumping
    if not(char.isJump):
        if keys[pygame.K_UP] and jumpCount == 0 and (char.on_ground or char.on_plat):
            char.isJump = True
            if facing == 1:
                char.left = False
                char.right = True
            elif facing == -1:
                char.left = True
                char.right = False
                char.walkCount = 0
        elif jumpCount > 0:
            jumpCount -= 1  
    else:
        jumpCount = 15
        grav = -5
        char.y += grav
        char.isJump = False
        char.on_ground = False
        char.on_plat = False

    playerLeft = char.x - 15
    playerRight = char.x + 30
    playerTop = char.y + 15
    playerMiddle = char.y + 35
    playerBottom = char.y + 55

#player collision with ground
    for ground in ground_list:
        if ground.y - 5 >= char.y + 45 >= ground.y - 20:
                grav = 0
                char.on_ground = True

#player collision with platform
    collideLeft = False
    collideRight = False
    for plat in plat_list:
        #left side:
        if plat.rect.x - 4 <= playerRight <= plat.rect.x + 4 : #if player's right side is in the same place as the left side of the platform:
            if (plat.rect.y <= playerTop <= plat.rect.y + 40)  or (plat.rect.y <= playerBottom <= plat.rect.y + 45): #if the top or the bottom of the player is in contact with the platform:
                char.x -= char.vel
                collideLeft = True
                char.Right = False
        #right side
        elif plat.rect.x - 4 <= playerRight <= plat.rect.x + 4:
            if (plat.rect.y <= playerTop <= plat.rect.y + 40)  or (plat.rect.y <= playerTop <= plat.rect.y + 40):
                char.x += char.vel
                collideRight = True
                char.Left = False
     #top side
        if plat.rect.y - 8 <= playerBottom <= plat.rect.y + 8:
            if (plat.rect.x  <=  playerRight + 5  <= plat.rect.x + 40) or (plat.rect.x <= playerRight <= plat.rect.x + 45):
                grav = -0.1
                grav -= 0.1
                char.on_plat = True
    #bottom side
        if plat.rect.y <=  playerTop <= plat.rect.y + 42:
             if (plat.rect.x  <=  playerRight + 5  <= plat.rect.x + 40) or (plat.rect.x <= playerRight <= plat.rect.x + 45):
                grav = 0
                grav += 0.35
#collision with energy
    for energy in energy_list:
        #left side:
        if energy.rect.x <= playerRight <= energy.rect.x + 20 or energy.rect.x <= char.x <= energy.rect.x + 20: #if player's right side is in the same place as the left side of the platform:
            if (energy.rect.y <= playerTop <= energy.rect.y + 12)  or  (energy.rect.y <= playerMiddle <= energy.rect.y + 12) or (energy.rect.y <= playerBottom <= energy.rect.y + 12): #if the top or the bottom of the player is in contact with the platform:
                if health < 140 : health += 5
                else: health = 140
                energy_list.remove(energy) #you've collected it!
#collision with spikes
    for s in spike_list:
        if s.rect.y <= playerBottom <= s.rect.y + 40:
            if (s.rect.x  <=  playerRight + 5 <= s.rect.x + 40):
                health -= 1
#collision with fireball
    for fire in fire_list:
        if fire.rect.y <= playerTop <= fire.rect.y + 40 or fire.rect.y <= playerMiddle <= fire.rect.y + 40 or fire.rect.y <= char.y + 45 <= fire.rect.y + 40:
            if fire.rect.x  <=  playerRight + 5 <= fire.rect.x + 40 or fire.rect.x < char.x <= fire.rect.x + 40:
                health -= 40
                fire_list.remove(fire)
#collision with door
    for door in portal_list:
        if door.rect.x  <= char.x  <= door.rect.x + 80:
            if door.rect.y <= playerTop <= door.rect.y + 80:
                win = True
        
    '''if changeLevel:        #for future update purposes!
        char.x = 100
        char.y = 56
        for ground in ground_list:
            ground_list.remove(ground)
        for plat in plat_list:
            plat_list.remove(plat)
        for energy in energy_list:
            energy_list.remove(energy)
        for s in spike_list:
            spike_list.remove(s)
        for fire in fire_list:
            fire_list.remove(fire)
        for portal in portal_list:
            portal_list.remove(portal)
        lvl += 1
        ground_list = Ground.generateGround(lvl , tx, ty)
        plat_list = Platform.platform(lvl, tx, ty)
        #energy_list = Energy.generateEnergy(lvl)
        fire_list = Fireball.generateFireball(lvl)
        spike_list = Spikes.generateSpike(lvl, tx, ty)
        changeLevel = False'''

    if health < 0:
        gameOver = True

    if frameCount % 60 == 0:
        fire_list.add(Fireball(random.randint(400, 1200), -80, 80, 80, fires))
        
    shiftWorld()
    redrawGameWindow(HEALTHBAR, health)

#GAME OVER LOOP =====================================================================================================
while not done and gameOver:
    DISPLAYSURF.blit(gameover, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            displayTitlePage = False
    clock.tick(60)
    pygame.display.update()
    
#YOU WIN LOOP ========================================================================================================
while not done and win:
    DISPLAYSURF.blit(youwin, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            displayTitlePage = False
    clock.tick(60)
    pygame.display.update()
    
pygame.quit()


