import enemy
import player

class Interactions:
    def __init__ (self, health, enemyChoice, sharpness, smite):
        self.playerData = player.Player(health, sharpness, smite)
        self.enemyChoice = enemyChoice
        self.card = []
        self.energyCard = []
        self.energyExceed = False
        self.energyUsed = 0
        self.lastEnergyUsed = 0
        if self.enemyChoice == "zombie":
            self.enemyData = enemy.Enemy(50)
        elif self.enemyChoice == "cave spider":
            self.enemyData = enemy.Enemy(50)
        elif self.enemyChoice == "skeleton":
            self.enemyData = enemy.Enemy(50)
        elif self.enemyChoice == "zombified piglin":
            self.enemyData = enemy.Enemy(75)
        elif self.enemyChoice == "wither skeleton":
            self.enemyData = enemy.Enemy(75)
        elif self.enemyChoice == "elder guardian":
            self.enemyData = enemy.Enemy(150)
        elif self.enemyChoice == "wither":
            self.enemyData = enemy.Enemy(150)
        elif self.enemyChoice == "creeper":
            self.enemyData = enemy.Enemy(100)
        elif self.enemyChoice == "blaze":
            self.enemyData = enemy.Enemy(100)
        elif self.enemyChoice == "iron golem":
            self.enemyData = enemy.Enemy(125)
        elif self.enemyChoice == "witch":
            self.enemyData = enemy.Enemy(125)
        else:
            self.enemyData = enemy.Enemy(200)

    def playerToEnemy(self):
        #clear previous effects dealt to enemy
        player.Player.removeEffectsDealt(self.playerData)
        #receive effects dealt from enemy
        player.Player.receiveEffects(self.playerData, self.enemyData.effectsDealt)
        #calculate effects at the start
        player.Player.calcOwnEffectsBefore(self.playerData)
        if self.playerData.health > 0:
            player.Player.playerAction(self.playerData, self.card)
            player.Player.calcOwnEffectsAfter(self.playerData)
        #calculate health
        player.Player.calcHealth(self.playerData, self.enemyData.attack)
        #win condition
        if self.playerData.health <= 0:
            return "player lose"
        #calculate energy
        self.playerData.energy += 4
        if self.playerData.energy > 8:
            self.playerData.energy = 8
        #win condition
        return "no result"

    def enemyToPlayer(self, object):
        #calculate health
        enemy.Enemy.calcHealth(self.enemyData, self.playerData.attack)
        #thorns
        if object == "elder guardian":
            if self.playerData.attack != 0:
                self.playerData.health -= 2
        #clear previous effects dealt to player
        enemy.Enemy.removeEffectsDealt(self.enemyData)
        #remove effects
        if object == "cave spider":
            for i in self.playerData.effectsDealt:
                if i[0] == "poison":
                    self.playerData.effectsDealt.remove(i)
        elif object == "zombified piglin" or object == "blaze":
            for i in self.playerData.effectsDealt:
                if i[0] == "fire":
                    self.playerData.effectsDealt.remove(i)
        elif object == "wither skeleton" or object == "wither":
            for i in self.playerData.effectsDealt:
                if i[0] == "wither":
                    self.playerData.effectsDealt.remove(i)
        #receive effects dealt from player
        enemy.Enemy.receiveEffects(self.enemyData, self.playerData.effectsDealt)
        #calculate effects at the start
        enemy.Enemy.calcOwnEffectsBefore(self.enemyData)
        if self.enemyData.health > 0:
            if object == "zombie":
                enemy.Zombie.zombieActions(self.enemyData)
            elif object == "cave spider":
                enemy.CaveSpider.caveSpiderActions(self.enemyData)
            elif object == "skeleton":
                enemy.Skeleton.skeletonActions(self.enemyData)
            elif object == "zombified piglin":
                enemy.ZombifiedPiglin.zombifiedPiglinActions(self.enemyData)
            elif object == "wither skeleton":
                enemy.WitherSkeleton.witherSkeletonActions(self.enemyData)
            elif object == "elder guardian":
                enemy.ElderGuardian.elderGuardianActions(self.enemyData)
            elif object == "wither":
                enemy.Wither.witherActions(self.enemyData)
            elif object == "creeper":
                enemy.Creeper.creeperActions(self.enemyData)
            elif object == "blaze":
                enemy.Blaze.blazeActions(self.enemyData)
            elif object == "iron golem":
                enemy.IronGolem.ironGolemActions(self.enemyData)
            elif object == "witch":
                enemy.Witch.witchActions(self.enemyData)
            elif object == "ender dragon":
                enemy.EnderDragon.enderDragonActions(self.enemyData)
            enemy.Enemy.calcOwnEffectsAfter(self.enemyData)
        else:
            return "player win"
        return "no result"

    def calcEnergyUsed(self):
        for i in self.energyCard:
            #energy cost 1
            if i.name == "Bow" or i.name == "Flint and steel":
                self.energyUsed += 1
                self.lastEnergyUsed = 1
            #energy cost 2
            if i.name == "Netherite sword" or i.name == "Diamond sword" or i.name == "Iron sword" or i.name == "Stone sword" or i.name == "Shield" or i.name == "Splash potion of poison" or i.name == "Potion of strength" or i.name == "Milk bucket":
                self.energyUsed += 2
                self.lastEnergyUsed = 2
            #energy cost 3
            if i.name == "Netherite axe" or i.name == "Diamond axe" or i.name == "Iron axe" or i.name == "Stone axe" or i.name == "Potion of regeneration" or i.name == "Potion of healing" or i.name == "Crossbow":
                self.energyUsed += 3
                self.lastEnergyUsed = 3
            #energy cost 4
            if i.name == "Nether bed":
                self.energyUsed += 4
                self.lastEnergyUsed = 4
        self.energyCard.remove(i)
        #if energy exceeds limit
        if self.energyUsed > self.playerData.energy:
            self.energyExceed = True
            self.energyUsed -= self.lastEnergyUsed
            self.lastEnergyUsed = 0
        else:
            self.energyExceed = False
            self.lastEnergyUsed = 0
