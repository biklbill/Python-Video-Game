#[attack, block, energy cost, [effects]]
#effects: [type, magnitude, duration]
import random

class Enemy:
    def __init__ (self, health):
        self.health = health
        self.attack = 0
        self.block = 0
        self.ownEffects = []
        self.effectsDealt = []
        self.actionMessage = ""

    def calcHealth(self, damageReceived):
        healthLost = damageReceived - self.block
        if healthLost <= 0:
            healthLost = 0
        self.health -= healthLost
        self.block = 0

    def receiveEffects(self, effect):
        #receive effects dealt by players
        refreshed = False
        if effect != []:
            for i in self.ownEffects:
                if i[0] == effect[0]:
                    i[2] = effect[2]
                    refreshed = True
            if refreshed == False:
                for j in effect:
                    self.ownEffects.append(j)

    def removeEffectsDealt(self):
        self.effectsDealt = []

    def calcOwnEffectsBefore(self):
        for i in self.ownEffects:
            #fire
            if i[0] == "fire":
                self.health -= i[1]
                i[2] -= 1
            #poison
            if i[0] == "poison":
                self.health -= i[1]
                i[2] -= 1
            #wither
            if i[0] == "wither":
                self.health -= i[1]
                i[2] -= 1
            #regeneration
            if i[0] == "regeneration":
                self.health += i[1]
                i[2] -= 1
            #remove effect from the list when it runs out
            if i[2] <= 0:
                self.ownEffects.remove(i)

    def calcOwnEffectsAfter(self):
        for i in self.ownEffects:
            #strength
            if i[0] == "strength":
                #calculate damage
                self.attack += int(self.attack * (int(i[1]) / 100))
                i[2] -= 1
            #weakness
            if i[0] == "weakness":
                #calculate damage
                self.attack = int(self.attack * ((100 - int(i[1])) / 100))
                i[2] -= 1
            #laser charge
            if i[0] == "laser":
                i[2] -= 1
                if i[2] <= 0:
                    self.attack += i[1]
            #remove effect from the list when it runs out
            if i[2] <= 0:
                self.ownEffects.remove(i)

    def ownEffectsAdd(self, effect):
        #add effect if effects not already exist
        #refresh effect to maximum duration if one already exist
        refreshed = False
        for i in self.ownEffects:
            if i[0] == effect[0]:
                if i[0] != "laser":
                    i[2] = effect[2]
                refreshed = True
        if refreshed == False:
            self.ownEffects.append(effect)

class Zombie(Enemy):
    def zombieActions(self):
        self.attack = 0
        self.block = 0
        zombieAction = random.randint(1, 5)
        if zombieAction == 1 or zombieAction == 2 or zombieAction == 3:
            self.attack += 3
            self.actionMessage = "Zombie will attack you for 3 damage"
        else:
            self.block += 3
            self.actionMessage = "Zombie will block for 3 damage"

class CaveSpider(Enemy):
    #immune to poison
    def caveSpiderActions(self):
        self.attack = 0
        self.block = 0
        caveSpiderAction = random.randint(1, 5)
        if caveSpiderAction == 1 or caveSpiderAction == 2:
            self.attack += 3
            self.actionMessage = "Cave spider will bite you for 3 damage"
        elif caveSpiderAction == 3 or caveSpiderAction == 4:
            self.block += 4
            self.actionMessage = "Cave spider will block for 4 damage"
        else:
            self.effectsDealt.append(["poison", 2, 3])
            self.actionMessage = "Cave spider will poison you for 3 rounds"

class Skeleton(Enemy):
    def skeletonActions(self):
        self.attack = 0
        self.block = 0
        skeletonAction = random.randint(1, 5)
        if skeletonAction == 1 or skeletonAction == 2 or skeletonAction == 3:
            self.attack += 4
            self.actionMessage = "Skeleton will shoot you for 4 damage"
        elif skeletonAction == 4:
            self.block += 2
            self.actionMessage = "Skeleton will block for 2 damage"
        else:
            self.ownEffectsAdd(["strength", 50, 3])
            self.actionMessage = "Skeleton will gain strength effect for 3 rounds"

class ZombifiedPiglin(Enemy):
    #immune to fire
    def zombifiedPiglinActions(self):
        self.attack = 0
        self.block = 0
        zombifiedPiglinAction = random.randint(1, 5)
        if zombifiedPiglinAction == 1 or zombifiedPiglinAction == 2 or zombifiedPiglinAction == 3:
            self.attack += 6
            self.actionMessage = "Zombified piglin will attack you for 6 damage"
        else:
            self.block += 4
            self.actionMessage = "Zombified piglin will block for 4 damage"

class WitherSkeleton(Enemy):
    #immune to wither effect
    def witherSkeletonActions(self):
        self.attack = 0
        self.block = 0
        witherSkeletonAction = random.randint(1, 5)
        if witherSkeletonAction == 1 or witherSkeletonAction == 2:
            self.attack += 4
            self.effectsDealt.append(["wither", 3, 2])
            self.actionMessage = "Wither skeleton will attack you for 4 damage and inflict wither effect for 2 rounds"
        else:
            self.block += 2
            self.actionMessage = "Wither skeleton will block for 2 damage"

class ElderGuardian(Enemy):
    #thorns
    #heal 2 health each round
    def elderGuardianActions(self):
        self.attack = 0
        self.block = 0
        self.health += 2
        elderGuardianAction = random.randint(1, 5)
        if elderGuardianAction == 1 or elderGuardianAction == 2:
            #check if laser is already active
            self.ownEffectsAdd(["laser", 10, 4])
            self.actionMessage = "Elder guardian is charging its laser which will deal 10 damage 4 rounds later"
        elif elderGuardianAction == 3:
            self.effectsDealt.append(["fatigue", 1, 2])
            self.actionMessage = "Elder guardian will inflict fatigue effect for 2 rounds"
        else:
            self.block += 10
            self.actionMessage = "Elder guardian will block for 10 damage"

class Wither(Enemy):
    #immune to wither effect
    #heal 2 health each round
    def witherActions(self):
        self.attack = 0
        self.block = 0
        self.health += 2
        witherAction = random.randint(1, 5)
        if witherAction == 1:
            self.attack += 3
            self.effectsDealt.append(["wither", 3, 3])
            self.actionMessage = "Wither will attack you for 3 damage and inflict wither effect for 3 rounds"
        elif witherAction == 2:
            self.attack += 5
            self.actionMessage = "Wither will charge at you for 5 damage"
        else:
            self.block += 4
            self.actionMessage = "Wither will block for 4 damage"

class Creeper(Enemy):
    def creeperActions(self):
        self.attack = 0
        self.block = 0
        creeperAction = random.randint(1, 5)
        if creeperAction == 1 or creeperAction == 2:
            self.attack += 10
            self.actionMessage = "Creeper will explode and dealt 10 damage to you"
        else:
            self.block += 5
            self.actionMessage = "Creeper will block for 5 damage"

class Blaze(Enemy):
    #immune to fire
    def blazeActions(self):
        self.attack = 0
        self.block = 0
        blazeAction = random.randint(1, 5)
        if blazeAction == 1 or blazeAction == 2:
            self.effectsDealt.append(["fire", 1, 7])
            self.actionMessage = "Blaze will set you on fire for 7 rounds"
        elif blazeAction == 3:
            self.attack += 4
            self.actionMessage = "Blaze will attack you for 4 damage"
        else:
            self.block += 3
            self.actionMessage = "Blaze will block for 3 damage"

class IronGolem(Enemy):
    #2 natural block each round
    def ironGolemActions(self):
        self.attack = 0
        self.block = 2
        ironGolemAction = random.randint(1, 5)
        if ironGolemAction == 1 or ironGolemAction == 2:
            self.attack += 8
            self.actionMessage = "Iron golem will attack you for 8 damage"
        else:
            self.block += 7
            self.actionMessage = "Iron golem will block for 7 damage"

class Witch(Enemy):
    def witchActions(self):
        self.attack = 0
        self.block = 0
        witchAction = random.randint(1, 5)
        if witchAction == 1:
            self.effectsDealt.append(["poison", 2, 4])
            self.actionMessage = "Witch will throw a splash potion of poison"
        elif witchAction == 2:
            self.effectsDealt.append(["weakness", 75, 3])
            self.actionMessage = "Witch will throw a splash potion of weakness"
        elif witchAction == 3:
            self.attack += 5
            self.actionMessage = "Witch will throw a splash potion of harming"
        elif witchAction == 4:
            self.ownEffectsAdd(["regeneration", 3, 4])
            self.actionMessage = "Witch drank a potion of regeneration"
        else:
            self.health += 5
            self.actionMessage = "Witch will drink a potion of healing"

class EnderDragon(Enemy):
    #heal 4 health each round
    def enderDragonActions(self):
        self.attack = 0
        self.block = 0
        self.health += 4
        enderDragonAction = random.randint(1, 10)
        if enderDragonAction == 1 or enderDragonAction == 2:
            self.attack = 10
            self.actionMessage = "Ender dragon will attack you for 10 damage"
        elif enderDragonAction == 3 or enderDragonAction == 4:
            self.block += 10
            self.actionMessage = "Ender dragon will block for 10 damage"
        elif enderDragonAction == 5 or enderDragonAction == 6:
            self.effectsDealt.append(["dragon's breath", 4, 4])
            self.actionMessage = "Ender dragon will release dragon's breath"
        elif enderDragonAction == 7 or enderDragonAction == 8:
            self.health += 8
            self.actionMessage = "Ender dragon healed itself for 8 health via the crystals"
        else:
            self.ownEffects = []
            self.actionMessage = "Ender dragon cleansed itself of all effects"
