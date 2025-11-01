import pygame
from pygame.locals import *
import interaction
import deck

pygame.init()
width = 1000
height = 750
title = "minecraft"
FPS = 60
newGame = False
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
lightBlue = (135, 206, 235)
green = (0, 255, 0)
red = (255, 0, 0)

screen = pygame.display.set_mode((width, height))

class Button:
    def __init__ (self, image, x_pos, y_pos, textInput, normalColour, hoverColour, fontSize):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.normalColour = normalColour
        self.hoverColour = hoverColour
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.textInput = textInput
        self.buttonFont = pygame.font.SysFont("aria", fontSize)
        self.text = self.buttonFont.render(self.textInput, True, "white")
        self.textRect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.textRect)

    def checkForInput(self, position):
        if pygame.Rect.collidepoint(self.rect, position):
            return True

    def changeColour(self, position):
        if pygame.Rect.collidepoint(self.rect, position):
            self.text = self.buttonFont.render(self.textInput, True, self.hoverColour)
        else:
            self.text = self.buttonFont.render(self.textInput, True, self.normalColour)

class Card:
    def __init__ (self, list, x_pos, y_pos):
        self.clicked = False
        self.contentInput = list[0]
        self.energyCost = list[1]
        self.action = list[2]
        self.name = list[3]
        self.colour = list[4]
        self.fontSize = list[5]
        self.x_pos = x_pos
        self.y_pos = y_pos
        #load font for cards
        self.font = pygame.font.SysFont("aria", self.fontSize)
        #card template
        cardTemplate = pygame.image.load("images\\card template.png")
        self.template = pygame.transform.scale(cardTemplate, (100, 150))
        self.templateRect = self.template.get_rect(center=(self.x_pos, self.y_pos))    
        #image of card
        self.content = pygame.transform.scale(self.contentInput, (50, 50))
        self.contentRect = self.content.get_rect(center=(self.x_pos, self.y_pos))
        #energy of card
        energyImg = pygame.image.load("images\\water drop.png")
        self.energyImage = pygame.transform.scale(energyImg, (20, 30))
        self.energyImageRect = self.energyImage.get_rect(center=(self.x_pos+50, self.y_pos-70))
        self.energyText = self.font.render(self.energyCost, True, self.colour)
        self.energyRect = self.energyText.get_rect(center=(self.x_pos+51, self.y_pos-65))
        #function of card
        self.actionText = self.font.render(self.action, True, self.colour)
        self.actionRect = self.actionText.get_rect(center=(self.x_pos, self.y_pos+40))
        #name of card
        self.nameText = self.font.render(self.name, True, self.colour)
        self.nameRect = self.nameText.get_rect(center=(self.x_pos, self.y_pos-40))
        #create "use" box
        self.box = pygame.draw.rect(screen, white, (825, 575, 150, 150), 3)
        self.useFont = pygame.font.SysFont("cambria", 50)
        #if card is placed
        self.hovered = False

    def update(self):
        screen.blit(self.template, self.templateRect)
        screen.blit(self.content, self.contentRect)
        screen.blit(self.energyImage, self.energyImageRect)
        screen.blit(self.energyText, self.energyRect)
        screen.blit(self.actionText, self.actionRect)
        screen.blit(self.nameText, self.nameRect)

    def checkForInput(self, position):
        if pygame.Rect.collidepoint(self.templateRect, position):
            return True

    def changePosition(self, position):
        if pygame.Rect.collidepoint(self.templateRect, position):
            #change position of card
            self.templateRect = self.template.get_rect(center=(self.x_pos, self.y_pos-20))
            self.contentRect = self.content.get_rect(center=(self.x_pos, self.y_pos-20))
            self.energyImageRect = self.energyImage.get_rect(center=(self.x_pos+50, self.y_pos-90))
            self.energyRect = self.energyText.get_rect(center=(self.x_pos+51, self.y_pos-85))
            self.actionRect = self.actionText.get_rect(center=(self.x_pos, self.y_pos+20))
            self.nameRect = self.nameText.get_rect(center=(self.x_pos, self.y_pos-60))
        else:
            #change back
            self.templateRect = self.template.get_rect(center=(self.x_pos, self.y_pos))
            self.contentRect = self.content.get_rect(center=(self.x_pos, self.y_pos)) 
            self.energyImageRect = self.energyImage.get_rect(center=(self.x_pos+50, self.y_pos-70))
            self.energyRect = self.energyText.get_rect(center=(self.x_pos+51, self.y_pos-65))
            self.actionRect = self.actionText.get_rect(center=(self.x_pos, self.y_pos+40))
            self.nameRect = self.nameText.get_rect(center=(self.x_pos, self.y_pos-40))
    
    def followCursor(self, position):
        if self.clicked:
            if pygame.Rect.collidepoint(self.box, position):
                self.useText = self.useFont.render("use", True, "green")
                pygame.draw.rect(screen, green, (825, 575, 150, 150), 3)
                self.hovered = True
            else:
                self.useText = self.useFont.render("use", True, "white")
                pygame.draw.rect(screen, white, (825, 575, 150, 150), 3)
                self.hovered = False
            screen.blit(self.useText, (865, 615))
            self.templateRect = self.template.get_rect(center=(position[0], position[1]))
            self.contentRect = self.content.get_rect(center=(position[0], position[1]))
            self.energyImageRect = self.energyImage.get_rect(center=(position[0]+50, position[1]-70))
            self.energyRect = self.energyText.get_rect(center=(position[0]+51, position[1]-65))
            self.actionRect = self.actionText.get_rect(center=(position[0], position[1]+40))
            self.nameRect = self.nameText.get_rect(center=(position[0], position[1]-40))

class MiniCard:
    def __init__(self):
        self.position1 = False
        self.position1Card = ""
        self.position2 = False
        self.position2Card = ""
        self.position3 = False
        self.position3Card = ""
        self.position4 = False
        self.position4Card = ""
        self.position5 = False
        self.position5Card = ""
        self.position6 = False
        self.position6Card = ""
        self.position7 = False
        self.position7Card = ""
        self.position8 = False
        self.position8Card = ""
        self.position9 = False
        self.position9Card = ""
        self.position10 = False
        self.position10Card = ""

    def display(self, card):
        #assign cards going to be played
        if card != [] and self.position1 == False:
            self.position1 = True
            self.position1Card = card.pop()
        elif card != [] and self.position2 == False:
            self.position2 = True
            self.position2Card = card.pop()
        elif card != [] and self.position3 == False:
            self.position3 = True
            self.position3Card = card.pop()
        elif card != [] and self.position4 == False:
            self.position4 = True
            self.position4Card = card.pop()
        elif card != [] and self.position5 == False:
            self.position5 = True
            self.position5Card = card.pop()
        elif card != [] and self.position6 == False:
            self.position6 = True
            self.position6Card = card.pop()
        elif card != [] and self.position7 == False:
            self.position7 = True
            self.position7Card = card.pop()
        elif card != [] and self.position8 == False:
            self.position8 = True
            self.position8Card = card.pop()
        elif card != [] and self.position9 == False:
            self.position9 = True
            self.position9Card = card.pop()
        elif card != [] and self.position10 == False:
            self.position10 = True
            self.position10Card = card.pop()

    def reset(self):
        #clear the displayed cards after being played
        self.position1 = False
        self.position2 = False
        self.position3 = False
        self.position4 = False
        self.position5 = False
        self.position6 = False
        self.position7 = False
        self.position8 = False
        self.position9 = False
        self.position10 = False

    def loadMiniCard(self):
        #load cards going to be played
        if self.position1:
            screen.blit(pygame.transform.scale(self.position1Card.contentInput, (30, 30)), (90, 50))
        if self.position2:
            screen.blit(pygame.transform.scale(self.position2Card.contentInput, (30, 30)), (120, 50))
        if self.position3:
            screen.blit(pygame.transform.scale(self.position3Card.contentInput, (30, 30)), (150, 50))
        if self.position4:
            screen.blit(pygame.transform.scale(self.position4Card.contentInput, (30, 30)), (180, 50))
        if self.position5:
            screen.blit(pygame.transform.scale(self.position5Card.contentInput, (30, 30)), (210, 50))
        if self.position6:
            screen.blit(pygame.transform.scale(self.position6Card.contentInput, (30, 30)), (240, 50))
        if self.position7:
            screen.blit(pygame.transform.scale(self.position7Card.contentInput, (30, 30)), (270, 50))
        if self.position8:
            screen.blit(pygame.transform.scale(self.position8Card.contentInput, (30, 30)), (300, 50))
        if self.position9:
            screen.blit(pygame.transform.scale(self.position9Card.contentInput, (30, 30)), (330, 50))
        if self.position10:
            screen.blit(pygame.transform.scale(self.position10Card.contentInput, (30, 30)), (360, 50))

class Effect:
    def __init__ (self):
        self.enterPressed = False
        self.counter = 0
        self.playerEffects = []
        self.enemyEffects = []
        #load image icons
        self.strengthIconImg = pygame.image.load("images\\strength icon.png")
        self.weaknessIconImg = pygame.image.load("images\\weakness icon.png")
        self.regenerationIconImg = pygame.image.load("images\\regeneration icon.png")
        self.fireIconImg = pygame.image.load("images\\fire icon.png")
        self.poisonIconImg = pygame.image.load("images\\poison icon.png")
        self.witherIconImg = pygame.image.load("images\\wither icon.png")
        self.laserImg = pygame.image.load("images\\laser icon.png")
        self.dragonsBreathImg = pygame.image.load("images\\dragon's breath icon.png")
        self.fatigueImg = pygame.image.load("images\\mining fatigue icon.png")

    def display(self, effect, object):
        #store player effects and enemy effects in 2 lists
        if object == "player":
            if self.enterPressed:
                self.playerEffects = []
                for i in effect:
                    self.playerEffects.append(i[0])
        if object == "enemy":
            if self.enterPressed:
                self.enemyEffects = []
                for i in effect:
                    self.enemyEffects.append(i[0])

    def loadEffects(self):
        self.counter = 0
        for i in self.playerEffects:
            self.counter += 1
            #display the effect based on what is applied
            if self.counter < 6:
                if i == "strength":
                    screen.blit(pygame.transform.scale(self.strengthIconImg, (30, 30)), (self.counter*30+20, 500))
                elif i == "weakness":
                    screen.blit(pygame.transform.scale(self.weaknessIconImg, (30, 30)), (self.counter*30+20, 500))
                elif i == "regeneration":
                    screen.blit(pygame.transform.scale(self.regenerationIconImg, (30, 30)), (self.counter*30+20, 500))
                elif i == "fire":
                    screen.blit(pygame.transform.scale(self.fireIconImg, (30, 30)), (self.counter*30+20, 500))
                elif i == "poison":
                    screen.blit(pygame.transform.scale(self.poisonIconImg, (30, 30)), (self.counter*30+20, 500))
                elif i == "wither":
                    screen.blit(pygame.transform.scale(self.witherIconImg, (30, 30)), (self.counter*30+20, 500))
                elif i == "laser":
                    screen.blit(pygame.transform.scale(self.laserImg, (30, 30)), (self.counter*30+20, 500))
                elif i == "dragon's breath":
                    screen.blit(pygame.transform.scale(self.dragonsBreathImg, (30, 30)), (self.counter*30+20, 500))
                elif i == "fatigue":
                    screen.blit(pygame.transform.scale(self.fatigueImg, (30, 30)), (self.counter*30+20, 500))
            else:
                if i == "strength":
                    screen.blit(pygame.transform.scale(self.strengthIconImg, (30, 30)), ((self.counter-5)*30+20, 530))
                elif i == "weakness":
                    screen.blit(pygame.transform.scale(self.weaknessIconImg, (30, 30)), ((self.counter-5)*30+20, 530))
                elif i == "regeneration":
                    screen.blit(pygame.transform.scale(self.regenerationIconImg, (30, 30)), ((self.counter-5)*30+20, 530))
                elif i == "fire":
                    screen.blit(pygame.transform.scale(self.fireIconImg, (30, 30)), ((self.counter-5)*30+20, 530))
                elif i == "poison":
                    screen.blit(pygame.transform.scale(self.poisonIconImg, (30, 30)), ((self.counter-5)*30+20, 530))
                elif i == "wither":
                    screen.blit(pygame.transform.scale(self.witherIconImg, (30, 30)), ((self.counter-5)*30+20, 530))
                elif i == "laser":
                    screen.blit(pygame.transform.scale(self.laserImg, (30, 30)), ((self.counter-5)*30+20, 530))
                elif i == "dragon's breath":
                    screen.blit(pygame.transform.scale(self.dragonsBreathImg, (30, 30)), ((self.counter-5)*30+20, 530))
                elif i == "fatigue":
                    screen.blit(pygame.transform.scale(self.fatigueImg, (30, 30)), ((self.counter-5)*30+20, 530))
        self.counter = 0
        for i in self.enemyEffects:
            self.counter += 1
            if self.counter < 6:
                if i == "strength":
                    screen.blit(pygame.transform.scale(self.strengthIconImg, (30, 30)), (self.counter*30+690, 500))
                elif i == "weakness":
                    screen.blit(pygame.transform.scale(self.weaknessIconImg, (30, 30)), (self.counter*30+690, 500))
                elif i == "regeneration":
                    screen.blit(pygame.transform.scale(self.regenerationIconImg, (30, 30)), (self.counter*30+690, 500))
                elif i == "fire":
                    screen.blit(pygame.transform.scale(self.fireIconImg, (30, 30)), (self.counter*30+690, 500))
                elif i == "poison":
                    screen.blit(pygame.transform.scale(self.poisonIconImg, (30, 30)), (self.counter*30+690, 500))
                elif i == "wither":
                    screen.blit(pygame.transform.scale(self.witherIconImg, (30, 30)), (self.counter*30+690, 500))
                elif i == "laser":
                    screen.blit(pygame.transform.scale(self.laserImg, (30, 30)), (self.counter*30+690, 500))
                elif i == "dragon's breath":
                    screen.blit(pygame.transform.scale(self.dragonsBreathImg, (30, 30)), (self.counter*30+690, 500))
                elif i == "fatigue":
                    screen.blit(pygame.transform.scale(self.fatigueImg, (30, 30)), (self.counter*30+690, 500))
            else:
                if i == "strength":
                    screen.blit(pygame.transform.scale(self.strengthIconImg, (30, 30)), ((self.counter-5)*30+690, 530))
                elif i == "weakness":
                    screen.blit(pygame.transform.scale(self.weaknessIconImg, (30, 30)), ((self.counter-5)*30+690, 530))
                elif i == "regeneration":
                    screen.blit(pygame.transform.scale(self.regenerationIconImg, (30, 30)), ((self.counter-5)*30+690, 530))
                elif i == "fire":
                    screen.blit(pygame.transform.scale(self.fireIconImg, (30, 30)), ((self.counter-5)*30+690, 530))
                elif i == "poison":
                    screen.blit(pygame.transform.scale(self.poisonIconImg, (30, 30)), ((self.counter-5)*30+690, 530))
                elif i == "wither":
                    screen.blit(pygame.transform.scale(self.witherIconImg, (30, 30)), ((self.counter-5)*30+690, 530))
                elif i == "laser":
                    screen.blit(pygame.transform.scale(self.laserImg, (30, 30)), ((self.counter-5)*30+690, 530))
                elif i == "dragon's breath":
                    screen.blit(pygame.transform.scale(self.dragonsBreathImg, (30, 30)), ((self.counter-5)*30+690, 530))
                elif i == "fatigue":
                    screen.blit(pygame.transform.scale(self.fatigueImg, (30, 30)), ((self.counter-5)*30+690, 530))

class Bar:
    def __init__(self):
        self.font = pygame.font.SysFont("aria", 25)

    def healthBar(self, maxHealth, health, object):
        if health < 0:
            health = 0
        if object == "player":
            pygame.draw.rect(screen, white, (75, 100, 250, 25), 1)
            pygame.draw.rect(screen, red, (75, 100, (250/maxHealth)*health, 25))
            text = self.font.render(str(health)+"/"+str(maxHealth), True, "white")
            screen.blit(text, (75, 105))
        else:
            pygame.draw.rect(screen, white, (700, 100, 250, 25), 1)
            pygame.draw.rect(screen, red, (700, 100, (250/maxHealth)*health, 25))
            text = self.font.render(str(health)+"/"+str(maxHealth), True, "white")
            screen.blit(text, (700, 105))        

    def energyBar(self, energy):
        pygame.draw.rect(screen, white, (75, 125, 80, 25), 1)
        pygame.draw.rect(screen, blue, (75, 125, 10*energy, 25))
        text = self.font.render(str(energy)+"/8", True, "white")
        screen.blit(text, (75, 130))

    def energyUsedBar(self, energy):
        pygame.draw.rect(screen, lightBlue, (75, 150, 10*energy, 25))
        text = self.font.render(str(energy), True, "white")
        if energy != 0:
            screen.blit(text, (75, 155))

class Window:
    def __init__(self, title, framerate):
        self.result = "no result"
        self.displayEffect = Effect()
        self.playerWin = False
        self.playerLose = False
        self.remainHealth = 100
        #load health bar
        self.bar = Bar()
        #load background images
        self.menuImg = pygame.image.load('images\\menu.png')
        self.mapImg = pygame.image.load('images\\map.png')
        #load button images
        self.blueRectImg = pygame.image.load("images\\blue rect button.png")
        self.yellowRoundImg = pygame.image.load("images\\yellow round button.png")
        self.blueRoundImg = pygame.image.load("images\\blue round button.png")
        self.redRoundImg = pygame.image.load("images\\red round button.png")
        self.orangeRoundImg = pygame.image.load("images\\orange round button.png")
        self.greyRectImg = pygame.image.load("images\\grey rect button.png")
        #load character images
        self.playerImg = pygame.image.load("images\\steve.png")
        self.zombieImg = pygame.image.load("images\\zombie.png")
        self.caveSpiderImg = pygame.image.load("images\\cave spider.png")
        self.skeletonImg = pygame.image.load("images\\skeleton.png")
        self.zombifiedPiglinImg = pygame.image.load("images\\zombified piglin.png")
        self.witherSkeletonImg = pygame.image.load("images\\wither skeleton.png")
        self.elderGuardianImg = pygame.image.load("images\\elder guardian.png")
        self.witherImg = pygame.image.load("images\\wither.png")
        self.creeperImg = pygame.image.load("images\\creeper.png")
        self.blazeImg = pygame.image.load("images\\blaze.png")
        self.ironGolemImg = pygame.image.load("images\\iron golem.png")
        self.witchImg = pygame.image.load("images\\witch.png")
        self.enderDragonImg = pygame.image.load("images\\ender dragon.png")
        self.villagerImg = pygame.image.load("images\\villager.png")
        #load enemy background images
        self.zombieBackgroundImg = pygame.image.load("images\\zombie background.png")
        self.caveSpiderBackgroundImg = pygame.image.load("images\\cave spider background.png")
        self.skeletonBackgroundImg = pygame.image.load("images\\skeleton background.png")
        self.zombifiedPiglinBackgroundImg = pygame.image.load("images\\zombified piglin background.png")
        self.witherSkeletonBackgroundImg = pygame.image.load("images\\wither skeleton background.png")
        self.elderGuardianBackgroundImg = pygame.image.load("images\\elder guardian background.png")
        self.witherBackgroundImg = pygame.image.load("images\\wither background.png")
        self.creeperBackgroundImg = pygame.image.load("images\\creeper background.png")
        self.blazeBackgroundImg = pygame.image.load("images\\blaze background.png")
        self.ironGolemBackgroundImg = pygame.image.load("images\\iron golem background.png")
        self.witchBackgroundImg = pygame.image.load("images\\witch background.png")
        self.enderDragonBackgroundImg = pygame.image.load("images\\ender dragon background.png")
        #load card images
        self.cardBackgroundImg = pygame.image.load("images\\cards background.png")
        self.netheriteSwordImg = pygame.image.load("images\\netherite sword.png")
        self.diamondSwordImg = pygame.image.load("images\\diamond sword.png")
        self.ironSwordImg = pygame.image.load("images\\iron sword.png")
        self.stoneSwordImg = pygame.image.load("images\\stone sword.png")
        self.netheriteAxeImg = pygame.image.load("images\\netherite axe.png")
        self.diamondAxeImg = pygame.image.load("images\\diamond axe.png")
        self.ironAxeImg = pygame.image.load("images\\iron axe.png")
        self.stoneAxeImg = pygame.image.load("images\\stone axe.png")
        self.potionOfHealingImg = pygame.image.load("images\\potion of healing.png")
        self.potionOfRegenerationImg = pygame.image.load("images\\potion of regeneration.png")
        self.potionOfStrengthImg = pygame.image.load("images\\potion of strength.png")
        self.splashPotionOfPoisonImg = pygame.image.load("images\\splash potion of poison.png")
        self.bowImg = pygame.image.load("images\\bow.png")
        self.crossbowImg = pygame.image.load("images\\crossbow.png")
        self.shieldImg = pygame.image.load("images\\shield.png")
        self.flintAndSteelImg = pygame.image.load("images\\flint and steel.png")
        self.bedImg = pygame.image.load("images\\bed.png")
        self.milkBucketImg = pygame.image.load("images\\milk bucket.png")
        self.enchantedBookImg = pygame.image.load("images\\enchanted book.png")
        #load effect icons
        self.resistanceIconImg = pygame.image.load("images\\resistance icon.png")
        self.fireResistanceIconImg = pygame.image.load("images\\fire resistance icon.png")
        self.regenerationIconImg = pygame.image.load("images\\regeneration icon.png")
        self.poisonIconImg = pygame.image.load("images\\poison icon.png")
        self.witherIconImg = pygame.image.load("images\\wither icon.png")
        self.thornsIconImg = pygame.image.load("images\\cactus.png")
        #load emerald
        self.emeraldImg = pygame.image.load("images\\emerald.png")
        #load fonts
        self.titleFont = pygame.font.Font("fonts\\chalkduster.ttf", 75)
        self.creditsFont = pygame.font.SysFont("aria", 50)
        self.displayFont = pygame.font.SysFont("aria", 30)
        self.shopFont = pygame.font.SysFont("cambria", 12)
        self.gameFont = pygame.font.SysFont("cambria", 20)
        self.winconFont = pygame.font.Font("fonts\\ARCADECLASSIC.TTF", 100)
        #card stats
        self.netheriteSwordStats = [self.netheriteSwordImg, "2", "+8 attack", "Netherite sword", "black", 15]
        self.diamondSwordStats = [self.diamondSwordImg, "2", "+7 attack", "Diamond sword", "black", 15]
        self.ironSwordStats = [self.ironSwordImg, "2", "+6 attack", "Iron sword", "black", 15]
        self.stoneSwordStats = [self.stoneSwordImg, "2", "+5 attack", "Stone sword", "black", 15]
        self.netheriteAxeStats = [self.netheriteAxeImg, "3", "+10 attack, weakness", "Netherite axe", "black", 15]
        self.diamondAxeStats = [self.diamondAxeImg, "3", "+9 attack, weakness", "Diamond axe", "black", 15]
        self.ironAxeStats = [self.ironAxeImg, "3", "+8 attack, weakness", "Iron axe", "black", 15]
        self.stoneAxeStats = [self.stoneAxeImg, "3", "+7 attack, weakness", "Stone axe", "black", 15]
        self.potionOfHealingStats = [self.potionOfHealingImg, "3", "+12 health", "Potion of healing", "black", 13]
        self.potionOfRegenerationStats = [self.potionOfRegenerationImg, "3", "+2x7 health", "Potion of regeneration", "black", 13]
        self.potionOfStrengthStats = [self.potionOfStrengthImg, "2", "+50% attack", "Potion of strength", "black", 13]
        self.splashPotionOfPoisonStats = [self.splashPotionOfPoisonImg, "2", "3x3 attack", "Splash potion of poison", "black", 13]
        self.bowStats = [self.bowImg, "1", "+3 attack", "Bow", "black", 15]
        self.crossbowStats = [self.crossbowImg, "3", "+12 attack", "Crossbow", "black", 15]
        self.shieldStats = [self.shieldImg, "2", "+7 block", "Shield", "black", 15]
        self.flintAndSteelStats = [self.flintAndSteelImg, "1", "+1x5 attack", "Flint and steel", "black", 15]
        self.bedStats = [self.bedImg, "4", "+20 attack, -1x12 attack", "Nether bed", "black", 13]
        self.milkBucketStats = [self.milkBucketImg, "2", "remove effects", "Milk bucket", "black", 15]
        allCards = [self.ironAxeStats, self.ironSwordStats, self.shieldStats, self.shieldStats, self.potionOfStrengthStats, self.splashPotionOfPoisonStats,
        self.flintAndSteelStats, self.stoneAxeStats, self.stoneSwordStats, self.diamondSwordStats, self.potionOfStrengthStats, self.bowStats, self.bowStats, self.crossbowStats]
        #deck
        self.deck = deck.Deck()
        self.deck.discardPile = allCards
        #time
        self.fps = framerate
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.tick = 0
        self.running = True
        #create main menu buttons
        menuButton = pygame.transform.scale(self.blueRectImg, (400, 50))
        self.newGameButton = Button(menuButton, 500, 400, "New game", "white", "green", 27)
        self.credits = Button(menuButton, 500, 460, "Credits", "white", "green", 27)
        #create return buttons
        returnButton = pygame.transform.scale(self.yellowRoundImg, (50, 50))
        self.returnMenuButton = Button(returnButton, 50, 50, "return", "white", "green", 20)
        self.returnMapButton = Button(returnButton, 50, 50, "return", "white", "green", 20)
        #create shop buttons
        shopButton = pygame.transform.scale(self.orangeRoundImg, (50, 50))
        self.shopButton = Button(shopButton, 950, 50, "shop", "white", "green", 20)
        purchaseButton = pygame.transform.scale(self.greyRectImg, (100, 50))
        self.price1 = Button(purchaseButton, 400, 190, "3 emeralds", "black", "green", 20)
        self.price2 = Button(purchaseButton, 525, 190, "3 emeralds", "black", "green", 20)
        self.price3 = Button(purchaseButton, 650, 190, "4 emeralds", "black", "green", 20)
        self.price4 = Button(purchaseButton, 775, 190, "4 emeralds", "black", "green", 20)
        self.price5 = Button(purchaseButton, 900, 190, "5 emeralds", "black", "green", 20)
        self.price6 = Button(purchaseButton, 400, 540, "5 emeralds", "black", "green", 20)
        self.price7 = Button(purchaseButton, 525, 540, "5 emeralds", "black", "green", 20)
        self.price8 = Button(purchaseButton, 650, 540, "5 emeralds", "black", "green", 20)
        self.price9 = Button(purchaseButton, 775, 540, "8 emeralds", "black", "green", 20)
        self.price10 = Button(purchaseButton, 900, 540, "8 emeralds", "black", "green", 20)
        #create map buttons
        normalGameButton = pygame.transform.scale(self.blueRoundImg, (50, 50))
        bossButton = pygame.transform.scale(self.redRoundImg, (75, 75))
        finalBossButton = pygame.transform.scale(self.redRoundImg, (100, 100))
        self.game1 = Button(normalGameButton, 500, 675, "1", "white", "green", 25)
        self.gameLeft2 = Button(normalGameButton, 365, 585, "L2", "white", "green", 25)
        self.gameRight2 = Button(normalGameButton, 635, 585, "R2", "white", "green", 25)
        self.gameLeft3 = Button(normalGameButton, 230, 495, "L3", "white", "green", 25)
        self.gameRight3 = Button(normalGameButton, 770, 495, "R3", "white", "green", 25)
        self.leftBoss = Button(bossButton, 95, 405, "Boss", "white", "green", 25)
        self.rightBoss = Button(bossButton, 905, 405, "Boss", "white", "green", 25)
        self.gameLeft5 = Button(normalGameButton, 230, 315, "L5", "white", "green", 25)
        self.gameRight5 = Button(normalGameButton, 770, 315, "R5", "white", "green", 25)
        self.gameLeft6 = Button(normalGameButton, 365, 225, "L6", "white", "green", 25)
        self.gameRight6 = Button(normalGameButton, 635, 225, "R6", "white", "green", 25)
        self.finalBoss = Button(finalBossButton, 500, 115, "Final Boss", "white", "green", 22)
        #game results
        self.game1Result = False
        self.gameLeft2Result = False
        self.gameRight2Result = False
        self.gameLeft3Result = False
        self.gameRight3Result = False
        self.leftBossResult = False
        self.rightBossResult = False
        self.gameLeft5Result = False
        self.gameRight5Result = False
        self.gameLeft6Result = False
        self.gameRight6Result = False
        self.finalBossResult = False
        #path chosen
        self.leftPath = True
        self.rightPath = True
        #messages
        self.centreMessage = ""
        self.toDisplay = False
        self.displayMessage = False
        #cards used
        self.miniCard = MiniCard()
        self.miniCardsUsed = []
        #shop items
        self.item1 = Card([self.netheriteSwordImg, "2", "", "", "black", 15], 400, 100)
        self.item2 = Card([self.netheriteAxeImg, "3", "", "", "black", 15], 525, 100)
        self.item3 = Card([self.potionOfRegenerationImg, "3", "", "", "black", 15], 650, 100)
        self.item4 = Card([self.potionOfHealingImg, "3", "", "", "black", 15], 775, 100)
        self.item5 = Card([self.bedImg, "4", "", "", "black", 15], 900, 100)
        self.item6 = Card([self.milkBucketImg, "2", "", "", "black", 15], 400, 450)
        self.item7 = Card([self.stoneSwordImg, "2", "", "", "black", 15], 525, 450)
        self.item8 = Card([self.stoneAxeImg, "3", "", "", "black", 15], 650, 450)
        self.item9 = Card([self.enchantedBookImg, "", "", "", "black", 15], 775, 450)
        self.item10 = Card([self.enchantedBookImg, "", "", "", "black", 15], 900, 450)
        #enchants
        self.sharpness = False
        self.smite = False
        #purchase detection
        self.swordRemove = False
        self.axeRemove = False
        self.sharpnessApplied = False
        self.smiteApplied = False
        #emeralds
        self.emeralds = 2
        self.emeraldsApplied = False
        #if enter key is pressed
        self.enterPressed = False
        #interface user's currently in
        self.inMenu = False
        self.inMap = False
        self.inCredits = False
        self.inBattle = False
        self.inShop = False
        self.mainMenu()

    def event_queue(self):
        for event in pygame.event.get():
            #if the user clicked "x"
            if event.type == pygame.QUIT:
                self.running = False
                return self.running
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.inMenu:
                    if self.running:
                        if self.newGameButton.checkForInput(pygame.mouse.get_pos()):
                            self.map()
                    if self.running:
                        if self.credits.checkForInput(pygame.mouse.get_pos()):
                            self.creditsScreen()
                if self.inMap:
                    if self.running:
                        if self.returnMenuButton.checkForInput(pygame.mouse.get_pos()):
                            self.mainMenu()
                    if self.running:
                        if self.shopButton.checkForInput(pygame.mouse.get_pos()):
                            self.shop()
                    if self.running:
                        if self.game1.checkForInput(pygame.mouse.get_pos()):
                            if self.game1Result == False:
                                self.playerWin = False
                                self.playerLose = False
                                self.interactionData = interaction.Interactions(self.remainHealth, "zombie", self.sharpness, self.smite)
                                self.playerData = self.interactionData.playerData
                                self.enemyData = self.interactionData.enemyData
                                #create cards
                                self.deck.drawToHand()
                                self.card1 = Card(self.deck.hand[0], 280, 650)
                                self.card2 = Card(self.deck.hand[1], 390, 650)
                                self.card3 = Card(self.deck.hand[2], 500, 650)
                                self.card4 = Card(self.deck.hand[3], 610, 650)
                                self.card5 = Card(self.deck.hand[4], 720, 650)
                                self.battle("1")
                            else:
                                self.toDisplay = True
                                self.centreMessage = "You have already completed this level"
                    if self.running:
                        if self.gameLeft2.checkForInput(pygame.mouse.get_pos()):
                            if self.leftPath:
                                if self.game1Result:
                                    if self.gameLeft2Result == False:
                                        self.emeraldsApplied = False
                                        self.rightPath = False
                                        self.playerWin = False
                                        self.playerLose = False
                                        self.interactionData = interaction.Interactions(self.remainHealth, "cave spider", self.sharpness, self.smite)
                                        self.playerData = self.interactionData.playerData
                                        self.enemyData = self.interactionData.enemyData
                                        #reset
                                        for i in range (0, 5):
                                            self.deck.handToDiscard(i)
                                        self.displayEffect.playerEffects = []
                                        self.displayEffect.enemyEffects = []
                                        #create cards
                                        self.deck.drawToHand()
                                        self.card1 = Card(self.deck.hand[0], 280, 650)
                                        self.card2 = Card(self.deck.hand[1], 390, 650)
                                        self.card3 = Card(self.deck.hand[2], 500, 650)
                                        self.card4 = Card(self.deck.hand[3], 610, 650)
                                        self.card5 = Card(self.deck.hand[4], 720, 650)
                                        self.battle("L2")
                                    else:
                                        self.toDisplay = True
                                        self.centreMessage = "You have already completed this level"
                                else:
                                    self.toDisplay = True
                                    self.centreMessage = "Please complete level 1 first"
                            else:
                                self.toDisplay = True
                                self.centreMessage = "You have chosen the right path, you can't play the left path"
                    if self.running:
                        if self.gameRight2.checkForInput(pygame.mouse.get_pos()):
                            if self.rightPath:
                                if self.game1Result:
                                    if self.gameRight2Result == False:
                                        self.emeraldsApplied = False
                                        self.leftPath = False
                                        self.playerWin = False
                                        self.playerLose = False
                                        self.interactionData = interaction.Interactions(self.remainHealth, "skeleton", self.sharpness, self.smite)
                                        self.playerData = self.interactionData.playerData
                                        self.enemyData = self.interactionData.enemyData
                                        #reset
                                        for i in range (0, 5):
                                            self.deck.handToDiscard(i)
                                        self.displayEffect.playerEffects = []
                                        self.displayEffect.enemyEffects = []
                                        #create cards
                                        self.deck.drawToHand()
                                        self.card1 = Card(self.deck.hand[0], 280, 650)
                                        self.card2 = Card(self.deck.hand[1], 390, 650)
                                        self.card3 = Card(self.deck.hand[2], 500, 650)
                                        self.card4 = Card(self.deck.hand[3], 610, 650)
                                        self.card5 = Card(self.deck.hand[4], 720, 650)
                                        self.battle("R2")
                                    else:
                                        self.toDisplay = True
                                        self.centreMessage = "You have already completed this level"
                                else:
                                    self.toDisplay = True
                                    self.centreMessage = "Please complete level 1 first"
                            else:
                                self.toDisplay = True
                                self.centreMessage = "You have chosen the left path, you can't play the right path"
                    if self.running:
                        if self.gameLeft3.checkForInput(pygame.mouse.get_pos()):
                            if self.leftPath:
                                if self.gameLeft2Result:
                                    if self.gameLeft3Result == False:
                                        self.emeraldsApplied = False
                                        self.playerWin = False
                                        self.playerLose = False
                                        self.interactionData = interaction.Interactions(self.remainHealth, "zombified piglin", self.sharpness, self.smite)
                                        self.playerData = self.interactionData.playerData
                                        self.enemyData = self.interactionData.enemyData
                                        #reset
                                        for i in range (0, 5):
                                            self.deck.handToDiscard(i)
                                        self.displayEffect.playerEffects = []
                                        self.displayEffect.enemyEffects = []
                                        #create cards
                                        self.deck.drawToHand()
                                        self.card1 = Card(self.deck.hand[0], 280, 650)
                                        self.card2 = Card(self.deck.hand[1], 390, 650)
                                        self.card3 = Card(self.deck.hand[2], 500, 650)
                                        self.card4 = Card(self.deck.hand[3], 610, 650)
                                        self.card5 = Card(self.deck.hand[4], 720, 650)
                                        self.battle("L3")
                                    else:
                                        self.toDisplay = True
                                        self.centreMessage = "You have already completed this level"
                                else:
                                    self.toDisplay = True
                                    self.centreMessage = "Please complete level L2 first"
                            else:
                                self.toDisplay = True
                                self.centreMessage = "You have chosen the right path, you can't play the left path"
                    if self.running:
                        if self.gameRight3.checkForInput(pygame.mouse.get_pos()):
                            if self.rightPath:
                                if self.gameRight2Result:
                                    if self.gameRight3Result == False:
                                        self.emeraldsApplied = False
                                        self.playerWin = False
                                        self.playerLose = False
                                        self.interactionData = interaction.Interactions(self.remainHealth, "wither skeleton", self.sharpness, self.smite)
                                        self.playerData = self.interactionData.playerData
                                        self.enemyData = self.interactionData.enemyData
                                        #reset
                                        for i in range (0, 5):
                                            self.deck.handToDiscard(i)
                                        self.displayEffect.playerEffects = []
                                        self.displayEffect.enemyEffects = []
                                        #create cards
                                        self.deck.drawToHand()
                                        self.card1 = Card(self.deck.hand[0], 280, 650)
                                        self.card2 = Card(self.deck.hand[1], 390, 650)
                                        self.card3 = Card(self.deck.hand[2], 500, 650)
                                        self.card4 = Card(self.deck.hand[3], 610, 650)
                                        self.card5 = Card(self.deck.hand[4], 720, 650)
                                        self.battle("R3")
                                    else:
                                        self.toDisplay = True
                                        self.centreMessage = "You have already completed this level"
                                else:
                                    self.toDisplay = True
                                    self.centreMessage = "Please complete level R2 first"
                            else:
                                self.toDisplay = True
                                self.centreMessage = "You have chosen the left path, you can't play the right path"
                    if self.running:
                        if self.leftBoss.checkForInput(pygame.mouse.get_pos()):
                            if self.leftPath:
                                if self.gameLeft3Result:
                                    if self.leftBossResult == False:
                                        self.emeraldsApplied = False
                                        self.playerWin = False
                                        self.playerLose = False
                                        self.interactionData = interaction.Interactions(self.remainHealth, "elder guardian", self.sharpness, self.smite)
                                        self.playerData = self.interactionData.playerData
                                        self.enemyData = self.interactionData.enemyData
                                        #reset
                                        for i in range (0, 5):
                                            self.deck.handToDiscard(i)
                                        self.displayEffect.playerEffects = []
                                        self.displayEffect.enemyEffects = []
                                        #create cards
                                        self.deck.drawToHand()
                                        self.card1 = Card(self.deck.hand[0], 280, 650)
                                        self.card2 = Card(self.deck.hand[1], 390, 650)
                                        self.card3 = Card(self.deck.hand[2], 500, 650)
                                        self.card4 = Card(self.deck.hand[3], 610, 650)
                                        self.card5 = Card(self.deck.hand[4], 720, 650)
                                        self.battle("LB")
                                    else:
                                        self.toDisplay = True
                                        self.centreMessage = "You have already completed this level"
                                else:
                                    self.toDisplay = True
                                    self.centreMessage = "Please complete level L3 first"
                            else:
                                self.toDisplay = True
                                self.centreMessage = "You have chosen the right path, you can't play the left path"
                    if self.running:
                        if self.rightBoss.checkForInput(pygame.mouse.get_pos()):
                            if self.rightPath:
                                if self.gameRight3Result:
                                    if self.rightBossResult == False:
                                        self.emeraldsApplied = False
                                        self.playerWin = False
                                        self.playerLose = False
                                        self.interactionData = interaction.Interactions(self.remainHealth, "wither", self.sharpness, self.smite)
                                        self.playerData = self.interactionData.playerData
                                        self.enemyData = self.interactionData.enemyData
                                        #reset
                                        for i in range (0, 5):
                                            self.deck.handToDiscard(i)
                                        self.displayEffect.playerEffects = []
                                        self.displayEffect.enemyEffects = []
                                        #create cards
                                        self.deck.drawToHand()
                                        self.card1 = Card(self.deck.hand[0], 280, 650)
                                        self.card2 = Card(self.deck.hand[1], 390, 650)
                                        self.card3 = Card(self.deck.hand[2], 500, 650)
                                        self.card4 = Card(self.deck.hand[3], 610, 650)
                                        self.card5 = Card(self.deck.hand[4], 720, 650)
                                        self.battle("RB")
                                    else:
                                        self.toDisplay = True
                                        self.centreMessage = "You have already completed this level"
                                else:
                                    self.toDisplay = True
                                    self.centreMessage = "Please complete level R3 first"
                            else:
                                self.toDisplay = True
                                self.centreMessage = "You have chosen the left path, you can't play the right path"
                    if self.running:
                        if self.gameLeft5.checkForInput(pygame.mouse.get_pos()):
                            if self.leftPath:
                                if self.leftBossResult:
                                    if self.gameLeft5Result == False:
                                        self.emeraldsApplied = False
                                        self.playerWin = False
                                        self.playerLose = False
                                        self.interactionData = interaction.Interactions(self.remainHealth, "creeper", self.sharpness, self.smite)
                                        self.playerData = self.interactionData.playerData
                                        self.enemyData = self.interactionData.enemyData
                                        #reset
                                        for i in range (0, 5):
                                            self.deck.handToDiscard(i)
                                        self.displayEffect.playerEffects = []
                                        self.displayEffect.enemyEffects = []
                                        #create cards
                                        self.deck.drawToHand()
                                        self.card1 = Card(self.deck.hand[0], 280, 650)
                                        self.card2 = Card(self.deck.hand[1], 390, 650)
                                        self.card3 = Card(self.deck.hand[2], 500, 650)
                                        self.card4 = Card(self.deck.hand[3], 610, 650)
                                        self.card5 = Card(self.deck.hand[4], 720, 650)
                                        self.battle("L5")
                                    else:
                                        self.toDisplay = True
                                        self.centreMessage = "You have already completed this level"
                                else:
                                    self.toDisplay = True
                                    self.centreMessage = "Please complete level Left Boss first"
                            else:
                                self.toDisplay = True
                                self.centreMessage = "You have chosen the right path, you can't play the left path"
                    if self.running:
                        if self.gameRight5.checkForInput(pygame.mouse.get_pos()):
                            if self.rightPath:
                                if self.rightBossResult:
                                    if self.gameRight5Result == False:
                                        self.emeraldsApplied = False
                                        self.playerWin = False
                                        self.playerLose = False
                                        self.interactionData = interaction.Interactions(self.remainHealth, "blaze", self.sharpness, self.smite)
                                        self.playerData = self.interactionData.playerData
                                        self.enemyData = self.interactionData.enemyData
                                        #reset
                                        for i in range (0, 5):
                                            self.deck.handToDiscard(i)
                                        self.displayEffect.playerEffects = []
                                        self.displayEffect.enemyEffects = []
                                        #create cards
                                        self.deck.drawToHand()
                                        self.card1 = Card(self.deck.hand[0], 280, 650)
                                        self.card2 = Card(self.deck.hand[1], 390, 650)
                                        self.card3 = Card(self.deck.hand[2], 500, 650)
                                        self.card4 = Card(self.deck.hand[3], 610, 650)
                                        self.card5 = Card(self.deck.hand[4], 720, 650)
                                        self.battle("R5")
                                    else:
                                        self.toDisplay = True
                                        self.centreMessage = "You have already completed this level"
                                else:
                                    self.toDisplay = True
                                    self.centreMessage = "Please complete level Right Boss first"
                            else:
                                self.toDisplay = True
                                self.centreMessage = "You have chosen the left path, you can't play the right path"
                    if self.running:
                        if self.gameLeft6.checkForInput(pygame.mouse.get_pos()):
                            if self.leftPath:
                                if self.gameLeft5Result:
                                    if self.gameLeft6Result == False:
                                        self.emeraldsApplied = False
                                        self.playerWin = False
                                        self.playerLose = False
                                        self.interactionData = interaction.Interactions(self.remainHealth, "iron golem", self.sharpness, self.smite)
                                        self.playerData = self.interactionData.playerData
                                        self.enemyData = self.interactionData.enemyData
                                        #reset
                                        for i in range (0, 5):
                                            self.deck.handToDiscard(i)
                                        self.displayEffect.playerEffects = []
                                        self.displayEffect.enemyEffects = []
                                        #create cards
                                        self.deck.drawToHand()
                                        self.card1 = Card(self.deck.hand[0], 280, 650)
                                        self.card2 = Card(self.deck.hand[1], 390, 650)
                                        self.card3 = Card(self.deck.hand[2], 500, 650)
                                        self.card4 = Card(self.deck.hand[3], 610, 650)
                                        self.card5 = Card(self.deck.hand[4], 720, 650)
                                        self.battle("L6")
                                    else:
                                        self.toDisplay = True
                                        self.centreMessage = "You have already completed this level"
                                else:
                                    self.toDisplay = True
                                    self.centreMessage = "Please complete level L5 first"
                            else:
                                self.toDisplay = True
                                self.centreMessage = "You have chosen the right path, you can't play the left path"
                    if self.running:
                        if self.gameRight6.checkForInput(pygame.mouse.get_pos()):
                            if self.rightPath:
                                if self.gameRight5Result:
                                    if self.gameRight6Result == False:
                                        self.emeraldsApplied = False
                                        self.playerWin = False
                                        self.playerLose = False
                                        self.interactionData = interaction.Interactions(self.remainHealth, "witch", self.sharpness, self.smite)
                                        self.playerData = self.interactionData.playerData
                                        self.enemyData = self.interactionData.enemyData
                                        #reset
                                        for i in range (0, 5):
                                            self.deck.handToDiscard(i)
                                        self.displayEffect.playerEffects = []
                                        self.displayEffect.enemyEffects = []
                                        #create cards
                                        self.deck.drawToHand()
                                        self.card1 = Card(self.deck.hand[0], 280, 650)
                                        self.card2 = Card(self.deck.hand[1], 390, 650)
                                        self.card3 = Card(self.deck.hand[2], 500, 650)
                                        self.card4 = Card(self.deck.hand[3], 610, 650)
                                        self.card5 = Card(self.deck.hand[4], 720, 650)
                                        self.battle("R6")
                                    else:
                                        self.toDisplay = True
                                        self.centreMessage = "You have already completed this level"
                                else:
                                    self.toDisplay = True
                                    self.centreMessage = "Please complete level R5 first"
                            else:
                                self.toDisplay = True
                                self.centreMessage = "You have chosen the left path, you can't play the right path"
                    if self.running:
                        if self.finalBoss.checkForInput(pygame.mouse.get_pos()):
                            if self.gameLeft6Result or self.gameRight6Result:
                                self.playerWin = False
                                self.playerLose = False
                                self.interactionData = interaction.Interactions(self.remainHealth, "ender dragon", self.sharpness, self.smite)
                                self.playerData = self.interactionData.playerData
                                self.enemyData = self.interactionData.enemyData
                                #reset
                                for i in range (0, 5):
                                    self.deck.handToDiscard(i)
                                self.displayEffect.playerEffects = []
                                self.displayEffect.enemyEffects = []
                                #create cards
                                self.deck.drawToHand()
                                self.card1 = Card(self.deck.hand[0], 280, 650)
                                self.card2 = Card(self.deck.hand[1], 390, 650)
                                self.card3 = Card(self.deck.hand[2], 500, 650)
                                self.card4 = Card(self.deck.hand[3], 610, 650)
                                self.card5 = Card(self.deck.hand[4], 720, 650)
                                self.battle("B")
                            else:
                                self.toDisplay = True
                                self.centreMessage = "Please complete level L6 or R6 first"
                if self.inBattle:
                    if self.running:
                        if self.playerWin or self.playerLose:
                            if self.returnMapButton.checkForInput(pygame.mouse.get_pos()):
                                self.map()
                    if self.running:
                        if pygame.Rect.collidepoint(self.card1.templateRect, pygame.mouse.get_pos()):
                            self.card1.clicked = True
                    if self.running:
                        if pygame.Rect.collidepoint(self.card2.templateRect, pygame.mouse.get_pos()):
                            self.card2.clicked = True
                    if self.running:
                        if pygame.Rect.collidepoint(self.card3.templateRect, pygame.mouse.get_pos()):
                            self.card3.clicked = True
                    if self.running:
                        if pygame.Rect.collidepoint(self.card4.templateRect, pygame.mouse.get_pos()):
                            self.card4.clicked = True
                    if self.running:
                        if pygame.Rect.collidepoint(self.card5.templateRect, pygame.mouse.get_pos()):
                            self.card5.clicked = True
                if self.inShop:
                    if self.running:
                        if self.price1.checkForInput(pygame.mouse.get_pos()):
                            if self.emeralds >= 3:
                                self.deck.discardPile.append(self.netheriteSwordStats)
                                self.emeralds -= 3
                                self.toDisplay = True
                                self.centreMessage = "Netherite sword purchased"
                            else:
                                self.toDisplay = True
                                self.centreMessage = "Not enough emeralds"
                        if self.price2.checkForInput(pygame.mouse.get_pos()):
                            if self.emeralds >= 3:
                                self.deck.discardPile.append(self.netheriteAxeStats)
                                self.emeralds -= 3
                                self.toDisplay = True
                                self.centreMessage = "Netherite axe purchased"
                            else:
                                self.toDisplay = True
                                self.centreMessage = "Not enough emeralds"
                        if self.price3.checkForInput(pygame.mouse.get_pos()):
                            if self.emeralds >= 4:
                                self.deck.discardPile.append(self.potionOfRegenerationStats)
                                self.emeralds -= 4
                                self.toDisplay = True
                                self.centreMessage = "Potion of regeneration purchased"
                            else:
                                self.toDisplay = True
                                self.centreMessage = "Not enough emeralds"
                        if self.price4.checkForInput(pygame.mouse.get_pos()):
                            if self.emeralds >= 4:
                                self.deck.discardPile.append(self.potionOfHealingStats)
                                self.emeralds -= 4
                                self.toDisplay = True
                                self.centreMessage = "Potion of healing purchased"
                            else:
                                self.toDisplay = True
                                self.centreMessage = "Not enough emeralds"
                        if self.price5.checkForInput(pygame.mouse.get_pos()):
                            if self.emeralds >= 5:
                                self.deck.discardPile.append(self.bedStats)
                                self.emeralds -= 5
                                self.toDisplay = True
                                self.centreMessage = "Nether bed purchased"
                            else:
                                self.toDisplay = True
                                self.centreMessage = "Not enough emeralds"
                        if self.price6.checkForInput(pygame.mouse.get_pos()):
                            if self.emeralds >= 5:
                                self.deck.discardPile.append(self.milkBucketStats)
                                self.emeralds -= 5
                                self.toDisplay = True
                                self.centreMessage = "Milk bucket purchased"
                            else:
                                self.toDisplay = True
                                self.centreMessage = "Not enough emeralds"
                        if self.price7.checkForInput(pygame.mouse.get_pos()):
                            if self.swordRemove == False:
                                if self.emeralds >= 5:
                                    self.swordRemove = True
                                    inDiscard = False
                                    inDraw = False
                                    inHand = False
                                    for i in self.deck.discardPile:
                                        if i == self.stoneSwordStats:
                                            inDiscard = True
                                    for i in self.deck.drawPile:
                                        if i == self.stoneSwordStats:
                                            inDraw = True
                                    for i in self.deck.hand:
                                        if i == self.stoneSwordStats:
                                            inHand = True
                                    if inDiscard:
                                        self.deck.discardPile.remove(self.stoneSwordStats)
                                    if inDraw:
                                        self.deck.drawPile.remove(self.stoneSwordStats)
                                    if inHand:
                                        for i in range(0, 4):
                                            if self.deck.hand[i] == self.stoneSwordStats:
                                                self.deck.hand[i] = "PH"
                                    self.emeralds -= 5
                                    self.toDisplay = True
                                    self.centreMessage = "Stone swords removed"
                                else:
                                    self.toDisplay = True
                                    self.centreMessage = "Not enough emeralds"
                            else:
                                self.toDisplay = True
                                self.centreMessage = "This item can only be purchased once"
                        if self.price8.checkForInput(pygame.mouse.get_pos()):
                            if self.axeRemove == False:
                                if self.emeralds >= 5:
                                    self.axeRemove = True
                                    inDiscard = False
                                    inDraw = False
                                    inHand = False
                                    for i in self.deck.discardPile:
                                        if i == self.stoneAxeStats:
                                            inDiscard = True
                                    for i in self.deck.drawPile:
                                        if i == self.stoneAxeStats:
                                            inDraw = True
                                    for i in self.deck.hand:
                                        if i == self.stoneAxeStats:
                                            inHand = True
                                    if inDiscard:
                                        self.deck.discardPile.remove(self.stoneAxeStats)
                                    if inDraw:
                                        self.deck.drawPile.remove(self.stoneAxeStats)
                                    if inHand:
                                        for i in range(0, 4):
                                            if self.deck.hand[i] == self.stoneAxeStats:
                                                self.deck.hand[i] = "PH"
                                    self.emeralds -= 5
                                    self.toDisplay = True
                                    self.centreMessage = "Stone axes removed"
                                else:
                                    self.toDisplay = True
                                    self.centreMessage = "Not enough emeralds"
                            else:
                                self.toDisplay = True
                                self.centreMessage = "This item can only be purchased once"
                        if self.price9.checkForInput(pygame.mouse.get_pos()):
                            if self.sharpnessApplied == False:
                                if self.emeralds >= 8:
                                    self.sharpnessApplied = True
                                    self.sharpness = True
                                    self.emeralds -= 8
                                    self.toDisplay = True
                                    self.centreMessage = "Sharpness enchantment purchased"
                                else:
                                    self.toDisplay = True
                                    self.centreMessage = "Not enough emeralds"
                            else:
                                self.toDisplay = True
                                self.centreMessage = "This item can only be purchased once"
                        if self.price10.checkForInput(pygame.mouse.get_pos()):
                            if self.smiteApplied == False:
                                if self.emeralds >= 8:
                                    self.smiteApplied = True
                                    self.smite = True
                                    self.emeralds -= 8
                                    self.toDisplay = True
                                    self.centreMessage = "Smite enchantment purchased"
                                else:
                                    self.toDisplay = True
                                    self.centreMessage = "Not enough emeralds"
                            else:
                                self.toDisplay = True
                                self.centreMessage = "This item can only be purchased once"
                        if self.returnMapButton.checkForInput(pygame.mouse.get_pos()):
                            self.map()
                if self.inCredits:
                    if self.running:
                        if self.returnMenuButton.checkForInput(pygame.mouse.get_pos()):
                            self.mainMenu()
            if event.type == pygame.MOUSEBUTTONUP:
                if self.inBattle:
                    self.card1.clicked = False
                    self.card2.clicked = False
                    self.card3.clicked = False
                    self.card4.clicked = False
                    self.card5.clicked = False
                    if self.card1.hovered:
                        self.card1.hovered = False
                        self.interactionData.energyCard.append(self.card1)
                        #update deck
                        self.deck.handToDiscard(0)
                        self.deck.drawToHand()
                        #check energy limit
                        self.interactionData.calcEnergyUsed()
                        if self.interactionData.energyExceed:
                            self.deck.pushBack(0)
                        else:
                            self.miniCardsUsed.append(self.card1)
                            self.interactionData.card.append(self.card1)
                        self.card1 = Card(self.deck.hand[0], 280, 650)
                    if self.card2.hovered:
                        self.card2.hovered = False
                        self.interactionData.energyCard.append(self.card2)
                        #update deck
                        self.deck.handToDiscard(1)
                        self.deck.drawToHand()
                        #check energy limit
                        self.interactionData.calcEnergyUsed()
                        if self.interactionData.energyExceed:
                            self.deck.pushBack(1)
                        else:
                            self.miniCardsUsed.append(self.card2)
                            self.interactionData.card.append(self.card2)
                        self.card2 = Card(self.deck.hand[1], 390, 650)
                    if self.card3.hovered:
                        self.card3.hovered = False
                        self.interactionData.energyCard.append(self.card3)
                        #update deck
                        self.deck.handToDiscard(2)
                        self.deck.drawToHand()
                        #check energy limit
                        self.interactionData.calcEnergyUsed()
                        if self.interactionData.energyExceed:
                            self.deck.pushBack(2)
                        else:
                            self.miniCardsUsed.append(self.card3)
                            self.interactionData.card.append(self.card3)
                        self.card3 = Card(self.deck.hand[2], 500, 650)
                    if self.card4.hovered:
                        self.card4.hovered = False
                        self.interactionData.energyCard.append(self.card4)
                        #update deck
                        self.deck.handToDiscard(3)
                        self.deck.drawToHand()
                        #check energy limit
                        self.interactionData.calcEnergyUsed()
                        if self.interactionData.energyExceed:
                            self.deck.pushBack(3)
                        else:
                            self.miniCardsUsed.append(self.card4)
                            self.interactionData.card.append(self.card4)
                        self.card4 = Card(self.deck.hand[3], 610, 650)
                    if self.card5.hovered:
                        self.card5.hovered = False
                        self.interactionData.energyCard.append(self.card5)
                        #update deck
                        self.deck.handToDiscard(4)
                        self.deck.drawToHand()
                        #check energy limit
                        self.interactionData.calcEnergyUsed()
                        if self.interactionData.energyExceed:
                            self.deck.pushBack(4)
                        else:
                            self.miniCardsUsed.append(self.card5)
                            self.interactionData.card.append(self.card5)
                        self.card5 = Card(self.deck.hand[4], 720, 650)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.enterPressed = True
                    self.displayEffect.enterPressed = True

    def mainMenu(self):
        while self.running:
            self.inMenu = True
            self.inMap = False
            self.inCredits = False
            self.inBattle = False
            self.inShop = False
            #load the background image
            menuImg = pygame.transform.scale(self.menuImg, (width, height))
            screen.blit(menuImg, (0,0))
            #load the title
            gameTitle = self.titleFont.render("Minecraft the Spire", True, blue)
            screen.blit(gameTitle, gameTitle.get_rect(center=(500, 200)))
            #load the "New game" button
            self.newGameButton.update()
            self.newGameButton.changeColour(pygame.mouse.get_pos())
            #load the "Credits" button
            self.credits.update()
            self.credits.changeColour(pygame.mouse.get_pos()) 
            #update the window
            pygame.display.flip()
            self.clock.tick(self.fps)
            self.event_queue()
        pygame.display.quit()
        return pygame.quit()

    def map(self):
        while self.running:
            self.inMenu = False
            self.inMap = True
            self.inCredits = False
            self.inBattle = False
            self.inShop = False
            #load the background image
            screen.blit(pygame.transform.scale(self.mapImg, (width, height)), (0,0))
            #load return button
            self.returnMenuButton.update()
            self.returnMenuButton.changeColour(pygame.mouse.get_pos())
            #load game buttons
            self.game1.update()
            self.game1.changeColour(pygame.mouse.get_pos())
            self.gameLeft2.update()
            self.gameLeft2.changeColour(pygame.mouse.get_pos())
            self.gameRight2.update()
            self.gameRight2.changeColour(pygame.mouse.get_pos())
            self.gameLeft3.update()
            self.gameLeft3.changeColour(pygame.mouse.get_pos())
            self.gameRight3.update()
            self.gameRight3.changeColour(pygame.mouse.get_pos())
            self.leftBoss.update()
            self.leftBoss.changeColour(pygame.mouse.get_pos())
            self.rightBoss.update()
            self.rightBoss.changeColour(pygame.mouse.get_pos())
            self.gameLeft5.update()
            self.gameLeft5.changeColour(pygame.mouse.get_pos())
            self.gameRight5.update()
            self.gameRight5.changeColour(pygame.mouse.get_pos())
            self.gameLeft6.update()
            self.gameLeft6.changeColour(pygame.mouse.get_pos())
            self.gameRight6.update()
            self.gameRight6.changeColour(pygame.mouse.get_pos())
            self.finalBoss.update()
            self.finalBoss.changeColour(pygame.mouse.get_pos())
            #load shop button
            self.shopButton.update()
            self.shopButton.changeColour(pygame.mouse.get_pos())
            #load number of emeralds
            screen.blit(self.creditsFont.render(str(self.emeralds), True, "white"), (920, 710))
            screen.blit(pygame.transform.scale(self.emeraldImg, (50, 50)), (950, 700))
            #display message
            if self.toDisplay:
                self.tick += 1
                if self.tick < 100:
                    toDisplayText = self.displayFont.render(self.centreMessage, True, "red")
                    screen.blit(toDisplayText, toDisplayText.get_rect(center=(500, 375)))
                else:
                    self.tick = 0
                    self.toDisplay = False
            #update the window
            pygame.display.flip()
            self.clock.tick(self.fps)
            self.event_queue()
        pygame.display.quit()
        return pygame.quit()

    def battle(self, battle):
        while self.running:
            self.inMenu = False
            self.inMap = False
            self.inCredits = False
            self.inBattle = True
            self.inShop = False
            #game choice
            if battle == "1":
                #load background
                screen.blit(pygame.transform.scale(self.zombieBackgroundImg, (width, height)), (0, 0))
                #load enemy
                screen.blit(pygame.transform.scale(self.zombieImg, (150, 300)), (750, 175))
                #load health bar
                self.bar.healthBar(100, self.playerData.health, "player")
                self.bar.healthBar(50, self.enemyData.health, "enemy")
                #load energy
                self.bar.energyBar(self.playerData.energy)
                self.bar.energyUsedBar(self.interactionData.energyUsed)
                #load cards played by player
                screen.blit(self.gameFont.render("Cards used:", True, white), (100, 25))
                self.miniCard.display(self.miniCardsUsed)
                self.miniCard.loadMiniCard()
                #when player confirms play
                if self.enterPressed:
                    self.result = interaction.Interactions.playerToEnemy(self.interactionData)
                    if self.result == "player lose":
                        self.playerLose = True
                    self.result = interaction.Interactions.enemyToPlayer(self.interactionData, "zombie")
                    if self.result == "player win":
                        self.playerWin = True
                        if self.emeraldsApplied == False:
                            self.emeralds += 2
                            self.emeraldsApplied = True
                    self.remainHealth = self.playerData.health
                    self.miniCard.reset()
                    self.interactionData.card = []
                    self.enterPressed = False
                    self.interactionData.energyUsed = 0
                    self.displayMessage = True
                #display result message
                if self.playerLose:
                    screen.blit(self.winconFont.render("YOU   LOST!", True, blue), (300, 200))
                elif self.playerWin:
                    screen.blit(self.winconFont.render("YOU   WIN!", True, blue), (300, 200))
                    self.game1Result = True
            if battle == "L2":
                #load background
                screen.blit(pygame.transform.scale(self.caveSpiderBackgroundImg, (width, height)), (0, 0))
                #load enemy
                screen.blit(pygame.transform.scale(self.caveSpiderImg, (250, 250)), (650, 200))
                #load health bar
                self.bar.healthBar(100, self.playerData.health, "player")
                self.bar.healthBar(50, self.enemyData.health, "enemy")
                #load energy
                self.bar.energyBar(self.playerData.energy)
                self.bar.energyUsedBar(self.interactionData.energyUsed)
                #load cards played by player
                screen.blit(self.gameFont.render("Cards used:", True, white), (100, 25))
                self.miniCard.display(self.miniCardsUsed)
                self.miniCard.loadMiniCard()
                #when player confirms play
                if self.enterPressed:
                    self.result = interaction.Interactions.playerToEnemy(self.interactionData)
                    if self.result == "player lose":
                        self.playerLose = True
                    self.result = interaction.Interactions.enemyToPlayer(self.interactionData, "cave spider")
                    if self.result == "player win":
                        self.playerWin = True
                        if self.emeraldsApplied == False:
                            self.emeralds += 2
                            self.emeraldsApplied = True
                    self.remainHealth = self.playerData.health
                    self.miniCard.reset()
                    self.interactionData.card = []
                    self.enterPressed = False
                    self.interactionData.energyUsed = 0
                    self.displayMessage = True
                #passive abilities
                screen.blit(self.gameFont.render("Passive abilities:", True, white), (700, 25))
                screen.blit(pygame.transform.scale(self.poisonIconImg, (30, 30)), (850, 25))
                pygame.draw.line(screen, red, (850, 25), (880, 55), 2)
                pygame.draw.line(screen, red, (880, 25), (850, 55), 2)
                #display result message
                if self.playerLose:
                    screen.blit(self.winconFont.render("YOU   LOST!", True, blue), (300, 200))
                elif self.playerWin:
                    screen.blit(self.winconFont.render("YOU   WIN!", True, blue), (300, 200))
                    self.gameLeft2Result = True
            if battle == "R2":
                #load background
                screen.blit(pygame.transform.scale(self.skeletonBackgroundImg, (width, height)), (0, 0))
                #load enemy
                screen.blit(pygame.transform.scale(self.skeletonImg, (150, 300)), (700, 175))
                #load health bar
                self.bar.healthBar(100, self.playerData.health, "player")
                self.bar.healthBar(50, self.enemyData.health, "enemy")
                #load energy
                self.bar.energyBar(self.playerData.energy)
                self.bar.energyUsedBar(self.interactionData.energyUsed)
                #load cards played by player
                screen.blit(self.gameFont.render("Cards used:", True, white), (100, 25))
                self.miniCard.display(self.miniCardsUsed)
                self.miniCard.loadMiniCard()
                #when player confirms play
                if self.enterPressed:
                    self.result = interaction.Interactions.playerToEnemy(self.interactionData)
                    if self.result == "player lose":
                        self.playerLose = True
                    self.result = interaction.Interactions.enemyToPlayer(self.interactionData, "skeleton")
                    if self.result == "player win":
                        self.playerWin = True
                        if self.emeraldsApplied == False:
                            self.emeralds += 2
                            self.emeraldsApplied = True
                    self.remainHealth = self.playerData.health
                    self.miniCard.reset()
                    self.interactionData.card = []
                    self.enterPressed = False
                    self.interactionData.energyUsed = 0
                    self.displayMessage = True
                #display result message
                if self.playerLose:
                    screen.blit(self.winconFont.render("YOU   LOST!", True, blue), (300, 200))
                elif self.playerWin:
                    screen.blit(self.winconFont.render("YOU   WIN!", True, blue), (300, 200))
                    self.gameRight2Result = True
            if battle == "L3":
                #load background
                screen.blit(pygame.transform.scale(self.zombifiedPiglinBackgroundImg, (width, height)), (0, 0))
                #load enemy
                screen.blit(pygame.transform.scale(self.zombifiedPiglinImg, (150, 325)), (700, 150))
                #load health bar
                self.bar.healthBar(100, self.playerData.health, "player")
                self.bar.healthBar(75, self.enemyData.health, "enemy")
                #load energy
                self.bar.energyBar(self.playerData.energy)
                self.bar.energyUsedBar(self.interactionData.energyUsed)
                #load cards played by player
                screen.blit(self.gameFont.render("Cards used:", True, white), (100, 25))
                self.miniCard.display(self.miniCardsUsed)
                self.miniCard.loadMiniCard()
                #when player confirms play
                if self.enterPressed:
                    self.result = interaction.Interactions.playerToEnemy(self.interactionData)
                    if self.result == "player lose":
                        self.playerLose = True
                    self.result = interaction.Interactions.enemyToPlayer(self.interactionData, "zombified piglin")
                    if self.result == "player win":
                        self.playerWin = True
                        if self.emeraldsApplied == False:
                            self.emeralds += 2
                            self.emeraldsApplied = True
                    self.remainHealth = self.playerData.health
                    self.miniCard.reset()
                    self.interactionData.card = []
                    self.enterPressed = False
                    self.interactionData.energyUsed = 0
                    self.displayMessage = True
                #passive abilities
                screen.blit(self.gameFont.render("Passive abilities:", True, white), (700, 25))
                screen.blit(pygame.transform.scale(self.fireResistanceIconImg, (30, 30)), (850, 25))
                #display result message
                if self.playerLose:
                    screen.blit(self.winconFont.render("YOU   LOST!", True, blue), (300, 200))
                elif self.playerWin:
                    screen.blit(self.winconFont.render("YOU   WIN!", True, blue), (300, 200))
                    self.gameLeft3Result = True
            if battle == "R3":
                #load background
                screen.blit(pygame.transform.scale(self.witherSkeletonBackgroundImg, (width, height)), (0, 0))
                #load enemy
                screen.blit(pygame.transform.scale(self.witherSkeletonImg, (150, 300)), (700, 175))
                #load health bar
                self.bar.healthBar(100, self.playerData.health, "player")
                self.bar.healthBar(75, self.enemyData.health, "enemy")
                #load energy
                self.bar.energyBar(self.playerData.energy)
                self.bar.energyUsedBar(self.interactionData.energyUsed)
                #load cards played by player
                screen.blit(self.gameFont.render("Cards used:", True, white), (100, 25))
                self.miniCard.display(self.miniCardsUsed)
                self.miniCard.loadMiniCard()
                #when player confirms play
                if self.enterPressed:
                    self.result = interaction.Interactions.playerToEnemy(self.interactionData)
                    if self.result == "player lose":
                        self.playerLose = True
                    self.result = interaction.Interactions.enemyToPlayer(self.interactionData, "wither skeleton")
                    if self.result == "player win":
                        self.playerWin = True
                        if self.emeraldsApplied == False:
                            self.emeralds += 2
                            self.emeraldsApplied = True
                    self.remainHealth = self.playerData.health
                    self.miniCard.reset()
                    self.interactionData.card = []
                    self.enterPressed = False
                    self.interactionData.energyUsed = 0
                    self.displayMessage = True
                #passive abilities
                screen.blit(self.gameFont.render("Passive abilities:", True, white), (700, 25))
                screen.blit(pygame.transform.scale(self.witherIconImg, (30, 30)), (850, 25))
                pygame.draw.line(screen, red, (850, 25), (880, 55), 2)
                pygame.draw.line(screen, red, (880, 25), (850, 55), 2)
                #display result message
                if self.playerLose:
                    screen.blit(self.winconFont.render("YOU   LOST!", True, blue), (300, 200))
                elif self.playerWin:
                    screen.blit(self.winconFont.render("YOU   WIN!", True, blue), (300, 200))
                    self.gameRight3Result = True
            if battle == "LB":
                #load background
                screen.blit(pygame.transform.scale(self.elderGuardianBackgroundImg, (width, height)), (0, 0))
                #load enemy
                screen.blit(pygame.transform.scale(self.elderGuardianImg, (350, 300)), (600, 200))
                #load health bar
                self.bar.healthBar(100, self.playerData.health, "player")
                self.bar.healthBar(150, self.enemyData.health, "enemy")
                #load energy
                self.bar.energyBar(self.playerData.energy)
                self.bar.energyUsedBar(self.interactionData.energyUsed)
                #load cards played by player
                screen.blit(self.gameFont.render("Cards used:", True, white), (100, 25))
                self.miniCard.display(self.miniCardsUsed)
                self.miniCard.loadMiniCard()
                #when player confirms play
                if self.enterPressed:
                    self.result = interaction.Interactions.playerToEnemy(self.interactionData)
                    if self.result == "player lose":
                        self.playerLose = True
                    self.result = interaction.Interactions.enemyToPlayer(self.interactionData, "elder guardian")
                    if self.result == "player win":
                        self.playerWin = True
                        if self.emeraldsApplied == False:
                            self.emeralds += 10
                            self.emeraldsApplied = True
                    self.remainHealth = self.playerData.health
                    self.miniCard.reset()
                    self.interactionData.card = []
                    self.enterPressed = False
                    self.interactionData.energyUsed = 0
                    self.displayMessage = True
                #passive abilities
                screen.blit(self.gameFont.render("Passive abilities:", True, white), (700, 25))
                screen.blit(pygame.transform.scale(self.thornsIconImg, (30, 30)), (850, 25))
                screen.blit(pygame.transform.scale(self.regenerationIconImg, (30, 30)), (880, 25))
                #display result message
                if self.playerLose:
                    screen.blit(self.winconFont.render("YOU   LOST!", True, blue), (300, 200))
                elif self.playerWin:
                    screen.blit(self.winconFont.render("YOU   WIN!", True, blue), (300, 200))
                    self.leftBossResult = True
            if battle == "RB":
                #load background
                screen.blit(pygame.transform.scale(self.witherBackgroundImg, (width, height)), (0, 0))
                #load enemy
                screen.blit(pygame.transform.scale(self.witherImg, (350, 350)), (600, 150))
                #load health bar
                self.bar.healthBar(100, self.playerData.health, "player")
                self.bar.healthBar(150, self.enemyData.health, "enemy")
                #load energy
                self.bar.energyBar(self.playerData.energy)
                self.bar.energyUsedBar(self.interactionData.energyUsed)
                #load cards played by player
                screen.blit(self.gameFont.render("Cards used:", True, white), (100, 25))
                self.miniCard.display(self.miniCardsUsed)
                self.miniCard.loadMiniCard()
                #when player confirms play
                if self.enterPressed:
                    self.result = interaction.Interactions.playerToEnemy(self.interactionData)
                    if self.result == "player lose":
                        self.playerLose = True
                    self.result = interaction.Interactions.enemyToPlayer(self.interactionData, "wither")
                    if self.result == "player win":
                        self.playerWin = True
                        if self.emeraldsApplied == False:
                            self.emeralds += 10
                            self.emeraldsApplied = True
                    self.remainHealth = self.playerData.health
                    self.miniCard.reset()
                    self.interactionData.card = []
                    self.enterPressed = False
                    self.interactionData.energyUsed = 0
                    self.displayMessage = True
                #passive abilities
                screen.blit(self.gameFont.render("Passive abilities:", True, white), (700, 25))
                screen.blit(pygame.transform.scale(self.witherIconImg, (30, 30)), (850, 25))
                pygame.draw.line(screen, red, (850, 25), (880, 55), 2)
                pygame.draw.line(screen, red, (880, 25), (850, 55), 2)
                screen.blit(pygame.transform.scale(self.regenerationIconImg, (30, 30)), (880, 25))
                #display result message
                if self.playerLose:
                    screen.blit(self.winconFont.render("YOU   LOST!", True, blue), (300, 200))
                elif self.playerWin:
                    screen.blit(self.winconFont.render("YOU   WIN!", True, blue), (300, 200))
                    self.rightBossResult = True
            if battle == "L5":
                #load background
                screen.blit(pygame.transform.scale(self.creeperBackgroundImg, (width, height)), (0, 0))
                #load enemy
                screen.blit(pygame.transform.scale(self.creeperImg, (125, 300)), (700, 175))
                #load health bar
                self.bar.healthBar(100, self.playerData.health, "player")
                self.bar.healthBar(100, self.enemyData.health, "enemy")
                #load energy
                self.bar.energyBar(self.playerData.energy)
                self.bar.energyUsedBar(self.interactionData.energyUsed)
                #load cards played by player
                screen.blit(self.gameFont.render("Cards used:", True, white), (100, 25))
                self.miniCard.display(self.miniCardsUsed)
                self.miniCard.loadMiniCard()
                #when player confirms play
                if self.enterPressed:
                    self.result = interaction.Interactions.playerToEnemy(self.interactionData)
                    if self.result == "player lose":
                        self.playerLose = True
                    self.result = interaction.Interactions.enemyToPlayer(self.interactionData, "creeper")
                    if self.result == "player win":
                        self.playerWin = True
                        if self.emeraldsApplied == False:
                            self.emeralds += 4
                            self.emeraldsApplied = True
                    self.remainHealth = self.playerData.health
                    self.miniCard.reset()
                    self.interactionData.card = []
                    self.enterPressed = False
                    self.interactionData.energyUsed = 0
                    self.displayMessage = True
                #display result message
                if self.playerLose:
                    screen.blit(self.winconFont.render("YOU   LOST!", True, blue), (300, 200))
                elif self.playerWin:
                    screen.blit(self.winconFont.render("YOU   WIN!", True, blue), (300, 200))
                    self.gameLeft5Result = True
            if battle == "R5":
                #load background
                screen.blit(pygame.transform.scale(self.blazeBackgroundImg, (width, height)), (0, 0))
                #load enemy
                screen.blit(pygame.transform.scale(self.blazeImg, (150, 275)), (700, 150))
                #load health bar
                self.bar.healthBar(100, self.playerData.health, "player")
                self.bar.healthBar(100, self.enemyData.health, "enemy")
                #load energy
                self.bar.energyBar(self.playerData.energy)
                self.bar.energyUsedBar(self.interactionData.energyUsed)
                #load cards played by player
                screen.blit(self.gameFont.render("Cards used:", True, white), (100, 25))
                self.miniCard.display(self.miniCardsUsed)
                self.miniCard.loadMiniCard()
                #when player confirms play
                if self.enterPressed:
                    self.result = interaction.Interactions.playerToEnemy(self.interactionData)
                    if self.result == "player lose":
                        self.playerLose = True
                    self.result = interaction.Interactions.enemyToPlayer(self.interactionData, "blaze")
                    if self.result == "player win":
                        self.playerWin = True
                        if self.emeraldsApplied == False:
                            self.emeralds += 4
                            self.emeraldsApplied = True
                    self.remainHealth = self.playerData.health
                    self.miniCard.reset()
                    self.interactionData.card = []
                    self.enterPressed = False
                    self.interactionData.energyUsed = 0
                    self.displayMessage = True
                #passive abilities
                screen.blit(self.gameFont.render("Passive abilities:", True, white), (700, 25))
                screen.blit(pygame.transform.scale(self.fireResistanceIconImg, (30, 30)), (850, 25))
                #display result message
                if self.playerLose:
                    screen.blit(self.winconFont.render("YOU   LOST!", True, blue), (300, 200))
                elif self.playerWin:
                    screen.blit(self.winconFont.render("YOU   WIN!", True, blue), (300, 200))
                    self.gameRight5Result = True
            if battle == "L6":
                #load background
                screen.blit(pygame.transform.scale(self.ironGolemBackgroundImg, (width, height)), (0, 0))
                #load enemy
                screen.blit(pygame.transform.scale(self.ironGolemImg, (150, 300)), (700, 175))
                #load health bar
                self.bar.healthBar(100, self.playerData.health, "player")
                self.bar.healthBar(125, self.enemyData.health, "enemy")
                #load energy
                self.bar.energyBar(self.playerData.energy)
                self.bar.energyUsedBar(self.interactionData.energyUsed)
                #load cards played by player
                screen.blit(self.gameFont.render("Cards used:", True, white), (100, 25))
                self.miniCard.display(self.miniCardsUsed)
                self.miniCard.loadMiniCard()
                #when player confirms play
                if self.enterPressed:
                    self.result = interaction.Interactions.playerToEnemy(self.interactionData)
                    if self.result == "player lose":
                        self.playerLose = True
                    self.result = interaction.Interactions.enemyToPlayer(self.interactionData, "iron golem")
                    if self.result == "player win":
                        self.playerWin = True
                        if self.emeraldsApplied == False:
                            self.emeralds += 4
                            self.emeraldsApplied = True
                    self.remainHealth = self.playerData.health
                    self.miniCard.reset()
                    self.interactionData.card = []
                    self.enterPressed = False
                    self.interactionData.energyUsed = 0
                    self.displayMessage = True
                #passive abilities
                screen.blit(self.gameFont.render("Passive abilities:", True, white), (700, 25))
                screen.blit(pygame.transform.scale(self.resistanceIconImg, (30, 30)), (850, 25))
                #display result message
                if self.playerLose:
                    screen.blit(self.winconFont.render("YOU   LOST!", True, blue), (300, 200))
                elif self.playerWin:
                    screen.blit(self.winconFont.render("YOU   WIN!", True, blue), (300, 200))
                    self.gameLeft6Result = True
            if battle == "R6":
                #load background
                screen.blit(pygame.transform.scale(self.witchBackgroundImg, (width, height)), (0, 0))
                #load enemy
                screen.blit(pygame.transform.scale(self.witchImg, (150, 300)), (700, 200))
                #load health bar
                self.bar.healthBar(100, self.playerData.health, "player")
                self.bar.healthBar(125, self.enemyData.health, "enemy")
                #load energy
                self.bar.energyBar(self.playerData.energy)
                self.bar.energyUsedBar(self.interactionData.energyUsed)
                #load cards played by player
                screen.blit(self.gameFont.render("Cards used:", True, white), (100, 25))
                self.miniCard.display(self.miniCardsUsed)
                self.miniCard.loadMiniCard()
                #when player confirms play
                if self.enterPressed:
                    self.result = interaction.Interactions.playerToEnemy(self.interactionData)
                    if self.result == "player lose":
                        self.playerLose = True
                    self.result = interaction.Interactions.enemyToPlayer(self.interactionData, "witch")
                    if self.result == "player win":
                        self.playerWin = True
                        if self.emeraldsApplied == False:
                            self.emeralds += 4
                            self.emeraldsApplied = True
                    self.remainHealth = self.playerData.health
                    self.miniCard.reset()
                    self.interactionData.card = []
                    self.enterPressed = False
                    self.interactionData.energyUsed = 0
                    self.displayMessage = True
                #display result message
                if self.playerLose:
                    screen.blit(self.winconFont.render("YOU   LOST!", True, blue), (300, 200))
                elif self.playerWin:
                    screen.blit(self.winconFont.render("YOU   WIN!", True, blue), (300, 200))
                    self.gameRight6Result = True
            if battle == "B":
                #load background
                screen.blit(pygame.transform.scale(self.enderDragonBackgroundImg, (width, height)), (0, 0))
                #load enemy
                screen.blit(pygame.transform.scale(self.enderDragonImg, (450, 300)), (500, 200))
                #load health bar
                self.bar.healthBar(100, self.playerData.health, "player")
                self.bar.healthBar(200, self.enemyData.health, "enemy")
                #load energy
                self.bar.energyBar(self.playerData.energy)
                self.bar.energyUsedBar(self.interactionData.energyUsed)
                #load cards played by player
                screen.blit(self.gameFont.render("Cards used:", True, white), (100, 25))
                self.miniCard.display(self.miniCardsUsed)
                self.miniCard.loadMiniCard()
                #when player confirms play
                if self.enterPressed:
                    self.result = interaction.Interactions.playerToEnemy(self.interactionData)
                    if self.result == "player lose":
                        self.playerLose = True
                    self.result = interaction.Interactions.enemyToPlayer(self.interactionData, "ender dragon")
                    if self.result == "player win":
                        self.playerWin = True
                    self.remainHealth = self.playerData.health
                    self.miniCard.reset()
                    self.interactionData.card = []
                    self.enterPressed = False
                    self.interactionData.energyUsed = 0
                    self.displayMessage = True
                #passive abilities
                screen.blit(self.gameFont.render("Passive abilities:", True, white), (700, 25))
                screen.blit(pygame.transform.scale(self.regenerationIconImg, (30, 30)), (850, 25))
                #display result message
                if self.playerLose:
                    screen.blit(self.winconFont.render("YOU   LOST!", True, blue), (300, 200))
                elif self.playerWin:
                    screen.blit(self.winconFont.render("YOU   WIN!", True, blue), (300, 200))
                    self.finalBossResult = True
            #player effects
            screen.blit(self.gameFont.render("Effects:", True, white), (50, 475))
            self.displayEffect.display(self.interactionData.playerData.ownEffects, "player")
            self.displayEffect.loadEffects()
            #enemy effects
            screen.blit(self.gameFont.render("Effects:", True, white), (720, 475))
            self.displayEffect.display(self.interactionData.enemyData.ownEffects, "enemy")
            self.displayEffect.loadEffects()
            self.displayEffect.enterPressed = False
            #load player
            screen.blit(pygame.transform.scale(self.playerImg, (200, 300)), (75, 175))
            #load enemy action message
            if self.displayMessage:
                actionText = self.displayFont.render(self.interactionData.enemyData.actionMessage, True, "blue")
                screen.blit(actionText, actionText.get_rect(center=(500, 200)))
            #load cards background
            screen.blit(pygame.transform.scale(self.cardBackgroundImg, (620, 200)), (190, 550))
            #load cards
            self.card1.update()
            self.card1.changePosition(pygame.mouse.get_pos())
            self.card1.followCursor(pygame.mouse.get_pos())
            self.card2.update()
            self.card2.changePosition(pygame.mouse.get_pos())
            self.card2.followCursor(pygame.mouse.get_pos())
            self.card3.update()
            self.card3.changePosition(pygame.mouse.get_pos())
            self.card3.followCursor(pygame.mouse.get_pos())
            self.card4.update()
            self.card4.changePosition(pygame.mouse.get_pos())
            self.card4.followCursor(pygame.mouse.get_pos())
            self.card5.update()
            self.card5.changePosition(pygame.mouse.get_pos())
            self.card5.followCursor(pygame.mouse.get_pos())
            #load number of cards
            numOfCards1 = self.gameFont.render("Number of cards", True, white)
            numOfCards2 = self.gameFont.render(f"before reshuffle: {len(self.deck.drawPile)}", True, white)
            screen.blit(numOfCards1, numOfCards1.get_rect(center=(100, 650)))
            screen.blit(numOfCards2, numOfCards2.get_rect(center=(100, 675)))
            #guide for user
            enterToPlay1 = self.gameFont.render("Press enter", True, white)
            screen.blit(enterToPlay1, enterToPlay1.get_rect(center=(100, 575)))
            enterToPlay2 = self.gameFont.render("to play cards", True, white)
            screen.blit(enterToPlay2, enterToPlay2.get_rect(center=(100, 600)))
            #load return button
            if self.playerWin or self.playerLose:
                self.returnMapButton.update()
                self.returnMapButton.changeColour(pygame.mouse.get_pos())
            pygame.display.flip()
            self.clock.tick(self.fps)
            self.event_queue()
        pygame.display.quit()
        return pygame.quit()

    def shop(self):
        while self.running:
            self.inMenu = False
            self.inMap = False
            self.inCredits = False
            self.inBattle = False
            self.inShop = True
            pygame.Surface.fill(screen, lightBlue)
            #load items
            self.item1.update()
            self.item2.update()
            self.item3.update()
            self.item4.update()
            self.item5.update()
            self.item6.update()
            self.item7.update()
            self.item8.update()
            self.item9.update()
            self.item10.update()
            #load prices
            self.price1.update()
            self.price1.changeColour(pygame.mouse.get_pos())
            self.price2.update()
            self.price2.changeColour(pygame.mouse.get_pos())
            self.price3.update()
            self.price3.changeColour(pygame.mouse.get_pos())
            self.price4.update()
            self.price4.changeColour(pygame.mouse.get_pos())
            self.price5.update()
            self.price5.changeColour(pygame.mouse.get_pos())
            self.price6.update()
            self.price6.changeColour(pygame.mouse.get_pos())
            self.price7.update()
            self.price7.changeColour(pygame.mouse.get_pos())
            self.price8.update()
            self.price8.changeColour(pygame.mouse.get_pos())
            self.price9.update()
            self.price9.changeColour(pygame.mouse.get_pos())
            self.price10.update()
            self.price10.changeColour(pygame.mouse.get_pos())
            #load card details
            screen.blit(self.shopFont.render("Netherite sword", True, black), (350, 220))
            screen.blit(self.shopFont.render("Energy cost: 2", True, black), (350, 240))
            screen.blit(self.shopFont.render("+8 attack", True, black), (350, 260))
            screen.blit(self.shopFont.render("Netherite axe", True, black), (475, 220))
            screen.blit(self.shopFont.render("Energy cost: 3", True, black), (475, 240))
            screen.blit(self.shopFont.render("+10 attack", True, black), (475, 260))
            screen.blit(self.shopFont.render("50% weakness", True, black), (475, 280))
            screen.blit(self.shopFont.render("Potion of regeneration", True, black), (600, 220))
            screen.blit(self.shopFont.render("Energy cost: 3", True, black), (600, 240))
            screen.blit(self.shopFont.render("+2x7 health", True, black), (600, 260))
            screen.blit(self.shopFont.render("Potion of Healing", True, black), (725, 220))
            screen.blit(self.shopFont.render("Energy cost: 3", True, black), (725, 240))
            screen.blit(self.shopFont.render("+12 health", True, black), (725, 260))
            screen.blit(self.shopFont.render("Nether bed", True, black), (850, 220))
            screen.blit(self.shopFont.render("Energy cost: 4", True, black), (850, 240))
            screen.blit(self.shopFont.render("+20 attack", True, black), (850, 260))
            screen.blit(self.shopFont.render("-1x12 health(fire)", True, black), (850, 280))
            screen.blit(self.shopFont.render("Milk bucket", True, black), (350, 570))
            screen.blit(self.shopFont.render("Energy cost: 2", True, black), (350, 590))
            screen.blit(self.shopFont.render("Clear player's effects", True, black), (350, 610))
            screen.blit(self.shopFont.render("Remove stone swords", True, black), (475, 570))
            screen.blit(self.shopFont.render("Remove stone axes", True, black), (600, 570))
            screen.blit(self.shopFont.render("Sharpness", True, black), (725, 570))
            screen.blit(self.shopFont.render("All sword damage +2", True, black), (725, 590))
            screen.blit(self.shopFont.render("Smite", True, black), (850, 570))
            screen.blit(self.shopFont.render("All axe damage +3", True, black), (850, 590))
            #load number of emeralds
            screen.blit(self.creditsFont.render(str(self.emeralds), True, "white"), (920, 710))
            screen.blit(pygame.transform.scale(self.emeraldImg, (50, 50)), (950, 700))
            #load villager
            screen.blit(pygame.transform.scale(self.villagerImg, (150, 300)), (75, 200))
            #display message
            if self.toDisplay:
                self.tick += 1
                if self.tick < 100:
                    toDisplayText = self.displayFont.render(self.centreMessage, True, "green")
                    screen.blit(toDisplayText, toDisplayText.get_rect(center=(500, 375)))
                else:
                    self.tick = 0
                    self.toDisplay = False
            #load return button
            self.returnMapButton.update()
            self.returnMapButton.changeColour(pygame.mouse.get_pos())
            #update the window
            pygame.display.flip()
            self.clock.tick(self.fps)
            self.event_queue()
        pygame.display.quit()
        return pygame.quit()

    def creditsScreen(self):
        while self.running:
            self.inMenu = False
            self.inMap = False
            self.inCredits = True
            self.inBattle = False
            self.inShop = False
            pygame.Surface.fill(screen, black)
            #load credit messages
            creditsContent = self.creditsFont.render("I_Think_Im", True, white)
            screen.blit(creditsContent, creditsContent.get_rect(center=(500, 200)))
            creditsContent = self.creditsFont.render("The epic noob", True, white)
            screen.blit(creditsContent, creditsContent.get_rect(center=(500, 250)))
            creditsContent = self.creditsFont.render("PDF", True, white)
            screen.blit(creditsContent, creditsContent.get_rect(center=(500, 300)))
            creditsContent = self.creditsFont.render("Special thanks to:", True, white)
            screen.blit(creditsContent, creditsContent.get_rect(center=(500, 400)))
            creditsContent = self.creditsFont.render("Mojang's Minecraft", True, white)
            screen.blit(creditsContent, creditsContent.get_rect(center=(500, 450)))
            creditsContent = self.creditsFont.render("MegaCrit's Slay the Spire", True, white)
            screen.blit(creditsContent, creditsContent.get_rect(center=(500, 500)))
            #load return button
            self.returnMenuButton.update()
            self.returnMenuButton.changeColour(pygame.mouse.get_pos())
            #update the window
            pygame.display.flip()
            self.clock.tick(self.fps)
            self.event_queue()
        pygame.display.quit()
        return pygame.quit()

if __name__ == "__main__":
    main = Window(title, FPS)
