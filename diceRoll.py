# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 13:36:32 2020

@author: joseph.crutchley
"""

from random import randint

def rollDice(sides,adv_string = ''):
    if adv_string.lower()[:3] == 'adv':
        return max(randint(1,sides),randint(1,sides))
    if adv_string.lower()[:3] == 'dis':
        return min(randint(1,sides),randint(1,sides))
    else:
        return randint(1,sides)


class dicePool:
    def __init__(self,diceList = []):
        self.diceList = diceList
        
    def roll(self,description = '', bonus = 0, critChance = 0, crit = False):
        '''
        Return the result of a pool of dice being rolled
        Dice input as strings of the form '<number of dice>d<number of sides>
        Bonus value added on
        Critical hit determined either by crit boolean or by critChance (entered as integer percentage)
        '''
        self.rollSum = 0
        self.diceString = 'Rolled : {diceList}'.format(diceList = ', '.join(map(str,self.diceList)))
        critRoll = randint(1,100)
        self.resultDict = {}
        if critRoll < critChance:
            crit = True
            
        if description != '':
                print(description)
                
        for diceSet in self.diceList: 
            try:
                if diceSet.split('d')[0] == '':
                    number_of_dice = 1
                else:
                    number_of_dice = int(diceSet.split('d')[0])
                sides = int(diceSet.split('d')[-1])
                if sides not in self.resultDict:
                    self.resultDict[sides] = []
                if crit:
                    number_of_dice *= 2
            except ValueError:
                number_of_dice = 0
                sides = diceSet
            try:
                for i in range(number_of_dice):
                    rolledValue = rollDice(sides)
                    self.resultDict[sides].append(rolledValue)
                    self.rollSum += rolledValue
                #self.diceString += str(number_of_dice) + 'd' + str(sides) + ', '
            except (TypeError, UnboundLocalError):
                self.resultDict[sides].append('Error with d{sides}'.format(sides))
        self.rollSum += bonus
        return self.rollSum, self.diceString[:-2],self.resultDict
            
def rollDicePool(description = '',diceList = [],bonus = 0,critChance = 0, crit = False):
    '''
    Return the result of a pool of dice being rolled
    Dice input as strings of the form '<number of dice>d<number of sides>
    Bonus value added on
    Critical hit determined either by crit boolean or by critChance (entered as integer percentage)
    '''
    rollSum = 0
#    diceString = 'These dice were rolled : '
    diceString = 'Rolled : '
    critRoll = randint(1,100)
    resultDict = {}
    if critRoll < critChance:
        crit = True
        
    if description != '':
            print(description)
            
    for diceSet in diceList: 
        try:
            if diceSet.split('d')[0] == '':
                number_of_dice = 1
            else:
                number_of_dice = int(diceSet.split('d')[0])
            sides = int(diceSet.split('d')[-1])
            if sides not in resultDict:
                resultDict[sides] = []
            if crit:
                number_of_dice *= 2
        except ValueError:
            number_of_dice = 0
            sides = diceSet
        try:
            for i in range(number_of_dice):
                rolledValue = rollDice(sides)
                resultDict[sides].append(rolledValue)
                rollSum += rolledValue
            diceString += str(number_of_dice) + 'd' + str(sides) + ', '
        except (TypeError, UnboundLocalError):
            resultDict[sides].append('Error with d{sides}'.format(sides))
    rollSum += bonus
    #if crit:
        #print('Critical Hit!')
    #print(diceString[:-2] + '\nWith a bonus of ' + str(bonus) + '\nThe result was ' + str(rollSum) + '\n')
    return rollSum, diceString[:-2],resultDict
            
def getDiceSides(dice = 'd6'):
    try:
        diceSides = int(dice.split('d')[1]  )
    except TypeError:
        diceSides = dice   
    return diceSides


def rollStats(number_of_stats):
    '''
    For each stat, roll 4d6, drop the lowest
    '''
    statList = []
    for stat in range(number_of_stats):
    
        statRoll = [rollDice(6) , rollDice(6) , rollDice(6) , rollDice(6)]
        
        statResult = sum(statRoll) - min(statRoll)
        
        statList.append(statResult)

        
    return statList

if __name__ == "__main__":
    
    rollDicePool(diceList = ['20d4'],description = 'Air elemental flyby')
    rollDicePool('Rogue Sneak Attack',['5d6','2d8'],bonus = 5, critChance = 15)