#[attack, block, energy cost, [effects]]
#effects: [type, magnitude, duration]
class Player:
    def __init__(self, health, sharpness, smite):
        self.health = health
        self.attack = 0
        self.block = 0
        self.energy = 8
        self.ownEffects = []
        self.effectsDealt = []
        self.sharpness = sharpness
        self.smite = smite

    def calcHealth(self, damageReceived):
        healthLost = damageReceived - self.block
        if healthLost <= 0:
            healthLost = 0
        self.health -= healthLost
        self.block = 0

    def receiveEffects(self, effect):
        #receive effects dealth from enemy
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
            #dragon's breath
            if i[0] == "dragon's breath":
                self.health -= i[1]
                i[2] -= 1
            #regeneration
            if i[0] == "regeneration":
                self.health += i[1]
                i[2] -= 1
            #fatigue
            if i[0] == "fatigue":
                self.energy -= i[1]
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

    def playerAction(self, card):
        self.attack = 0
        self.block = 0
        for i in card:
            #swords
            if i.name == "Netherite sword":
                self.attack += 8
                self.energy -= 2
                if self.sharpness:
                    self.attack += 2
            if i.name == "Diamond sword":
                self.attack += 7
                self.energy -= 2
                if self.sharpness:
                    self.attack += 2
            if i.name == "Iron sword":
                self.attack += 6
                self.energy -= 2
                if self.sharpness:
                    self.attack += 2
            if i.name == "Stone sword":
                self.attack += 5
                self.energy -= 2
                if self.sharpness:
                    self.attack += 2
            #axes
            if i.name == "Netherite axe":
                self.attack += 10
                self.energy -= 3
                self.effectsDealt.append(["weakness", 75 ,3])
                if self.smite:
                    self.attack += 3
            if i.name == "Diamond axe":
                self.attack += 9
                self.energy -= 3
                self.effectsDealt.append(["weakness", 75 ,2])
                if self.smite:
                    self.attack += 3
            if i.name == "Iron axe":
                self.attack += 8
                self.energy -= 3
                self.effectsDealt.append(["weakness", 50, 3])
                if self.smite:
                    self.attack += 3
            if i.name == "Stone axe":
                self.attack += 7
                self.energy -= 3
                self.effectsDealt.append(["weakness", 50, 2])
                if self.smite:
                    self.attack += 3
            #potions
            if i.name == "Splash potion of poison":
                self.energy -= 2
                self.effectsDealt.append(["poison", 3, 3])
            if i.name == "Potion of strength":
                self.energy -= 2
                self.ownEffectsAdd(["strength", 50, 3])
            if i.name == "Potion of regeneration":
                self.energy -= 3
                self.ownEffectsAdd(["regeneration", 2, 7])
            if i.name == "Potion of healing":
                self.energy -= 3
                if self.health+12 > 100:
                    self.health = 100
                else:
                    self.health += 12
            #bows
            if i.name == "Bow":
                self.attack += 3
                self.energy -= 1
            if i.name == "Crossbow":
                self.attack += 12
                self.energy -= 3
            #others
            if i.name == "Shield":
                self.block += 7
                self.energy -= 2
            if i.name == "Flint and steel":
                self.energy -= 1
                self.effectsDealt.append(["fire", 1, 5])
            if i.name == "Nether bed":
                self.attack += 20
                self.energy -= 4
                self.ownEffectsAdd(["fire", 1, 12])
            if i.name == "Milk bucket":
                self.ownEffects = []
                self.energy -= 2

        return[self.attack, self.block, self.energy, self.effectsDealt]
