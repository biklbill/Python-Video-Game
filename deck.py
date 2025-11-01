import random

class Deck:
    def __init__(self):
        self.drawPile = []
        self.discardPile = []
        #"PH" is place holder
        self.hand = ["PH", "PH", "PH", "PH", "PH"]

    def discardToDraw(self):
        for i in self.discardPile:
            #leave one card in discard pile to avoid popping from empty list
            if len(self.discardPile) > 1:
                self.drawPile.append(self.discardPile.pop(0))
        random.shuffle(self.drawPile)

    def drawToHand(self):
        for i in range (0, 5):
            #draw card to specific place
            if self.hand[i] == "PH":
                #when draw pile runs out
                if self.drawPile == []:
                    self.discardToDraw()
                self.hand[i] = self.drawPile.pop(0)

    def handToDiscard(self, cardPos):
        if self.hand[cardPos] != "PH":
            self.discardPile.append(self.hand[cardPos])
        #mark the specific card used
        self.hand[cardPos] = "PH"

    def pushBack(self, cardPos):
        self.drawPile.insert(0, self.hand[cardPos])
        self.hand[cardPos] = self.discardPile.pop()
