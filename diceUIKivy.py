# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 11:57:07 2020

@author: joseph.crutchley
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy_garden.graph import Graph, MeshLinePlot
import diceRoll
import numpy as np
import re

class numberInput(TextInput): #Extend TextInput class so that only numbers are accepted
    def on_parent(self,widget,parent):
        input_type = 'number'
        

class mainApp(App):
    def build(self):
        self.icon = 'diceSmall.png'
        mainPanel = TabbedPanel()
        mainPanel.default_tab_text = 'Dice Roll'
        
        mainPanel.add_widget(self.tabProbabilityTesting())
        mainPanel.default_tab_content = self.tabDiceRoll()
        return mainPanel
    
    def addButtons(self,buttonList,buttonFunctionList,layout):
        for rowIndex, rowButtons in enumerate(buttonList):
            rowLayout = BoxLayout(
                size_hint = (1,1),
                padding = [0,0.5,0,0.5],
                )
            for buttonIndex, buttonLabel in enumerate(rowButtons):
                button = Button(
                    text = buttonLabel,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    size_hint = (1,1),
                    )
                button.bind(on_press=buttonFunctionList[rowIndex][buttonIndex])
                rowLayout.add_widget(button)
            layout.add_widget(rowLayout)
        
    def tabDiceRoll(self):
        mainLayout = BoxLayout(orientation = 'vertical')
        fontSize = 35
        labelList = ['d4','d6','d8','d10','d12','d20','d100','custom']
        self.diceDict = {}
        buttons = [
            ['Roll Inputs','Clear Inputs'],
            ['D20','2d6'],
            ['Roll Stats', '(dis)Advantage'],
            ]
        buttonFunctionList = [
            [self.fireRollButton, self.fireClearButton],
            [self.fireD20Button,self.fireMonopolyButton],
            [self.fireStatsButton, self.fireAdvantageButton], 
            ]
        
        for label in labelList:
            rowLayout = BoxLayout()
            self.kivyLabel = TextInput(
                text = label if label != 'custom' else '',
                hint_text = 'Custom dice' if label == 'custom' else '',
                background_color = [0.75,0.75,0.75,1],
                font_size = '{size}sp'.format(size = int(fontSize/2)),
                readonly = True if label != 'custom' else False,
                input_filter = 'int',
                size_hint = (0.3,1))
            self.diceDict[label] = numberInput(
                multiline = False, 
                font_size = '{size}sp'.format(size = int(fontSize/2)), 
                hint_text = 'Enter number of dice here',
                input_filter = 'int',
                size_hint = (0.7,1))
            rowLayout.add_widget(self.kivyLabel)
            rowLayout.add_widget(self.diceDict[label])
            mainLayout.add_widget(rowLayout)
            
        self.addButtons(buttons,buttonFunctionList,mainLayout)
            
        self.resultTextBox = TextInput(
            text = '\n\n\n\n\n',
            multiline = True, 
            readonly = True, 
            font_size = '{size}sp'.format(size = int(fontSize/2)),
            halign = 'left',
            background_color = [109/255,162/255,1,1],
            background_active = 'd20Skeleton.png',
            background_normal = 'd20Skeleton.png',
            size_hint = (0.9,8),
            pos_hint = {'center_x': .5, 'center_y': .5}
            )
        mainLayout.add_widget(self.resultTextBox)
        
        return mainLayout
    
    def tabProbabilityTesting(self):
        '''
        tab containing plot of probability distributions from various user-specificed pools of dice
        '''
        self.plotColorMap = [
            [1,0,0,1],
            [0,1,0,1],
            [0,0,1,1],
            [1,1,0,1],
            [1,0,1,1],
            [0,1,1,1],
            [1,1,1,1],
            [0.75,0.75,0.75,1]]
        tabProb = TabbedPanelItem(text = 'Prob. Plots')
        self.statsMainLayout = BoxLayout(orientation = 'vertical')
        self.entryLayout =  BoxLayout(orientation = 'vertical',size_hint = (1,0.45))
        buttonLayout = BoxLayout(size_hint = (1,0.05))
        self.graphLayout = BoxLayout(size_hint = (1,0.5))
        self.graph = Graph(xlabel='Value', ylabel='Counts', 
            x_ticks_minor=1,x_ticks_major=2, y_ticks_minor = 100, y_ticks_major=500,
            y_grid_label=True, x_grid_label=True, padding=5,
            x_grid=True, y_grid=True, xmin=-0, xmax=15, ymin=0,ymax = 5000)
        self.graphLayout.add_widget(self.graph)
        self.plotList = []
        self.statsMainLayout.add_widget(self.entryLayout)
        self.statsMainLayout.add_widget(buttonLayout)
        self.statsMainLayout.add_widget(self.graphLayout)
        self.testList = []
        self.appendNewTest(self.entryLayout,readOnly = True) 
        self.testList.append(self.appendNewTest(self.entryLayout)) 
        buttonList = [['Add New Test','Plot Results','Reset']]
        buttonFunctionList = [[self.fireNewTestButton,self.firePlotButton,self.fireResetTestsButton]]
        self.addButtons(buttonList,buttonFunctionList,buttonLayout)
        tabProb.add_widget(self.statsMainLayout)
        return tabProb    
    
    def appendNewTest(self,layout,readOnly = False):
        '''
        Add new test to probability distribution tab
        readOnly should be true for the first line to give a header column, and false thereafter
        '''
        rowLayout = BoxLayout(orientation = 'horizontal',)
        testIndex = len(self.testList) if not readOnly else -1
        testDice = TextInput(
            hint_text = 'Dice', 
            text = 'Enter dice list' if readOnly else '',
            readonly = readOnly,
            background_color = self.plotColorMap[testIndex])
        testBonus = numberInput(
            hint_text = 'Bonus', 
            text = 'Enter fixed bonus' if readOnly else '',
            readonly = readOnly,
            background_color = self.plotColorMap[testIndex])
        testMode = numberInput(
            hint_text = 'Expected Value (output)', 
            text = 'Expected Value' if readOnly else '',
            readonly = True,
            background_color = self.plotColorMap[testIndex])
        rowLayout.add_widget(testDice)
        rowLayout.add_widget(testBonus)
        rowLayout.add_widget(testMode)
        layout.add_widget(rowLayout)
        return(testDice,testBonus,testMode,rowLayout)
    
        
    def createPlot(self):
        '''
        Clear existing plots, and add a plot for each specificed test to the graph.
        Each will be colour coded to match the background of the test rowButtons
        Could (should!) do actual stats stuff to get expected values of each dice pool, but 10k tests takes negligible time even on a phone
        '''
        for plot in self.plotList:
            self.graph.remove_plot(plot)
        self.plotList = []
        maxCount = [500]
        maxValue = [6]
        numberOfTests = 10000
        for index, test in enumerate(self.testList):
            outcomes = {}
            diceList = re.findall(r"[\w\d']+", test[0].text)
            if len(diceList) > 0:
                bonus = 0 if len(test[1].text) == 0 else int(test[1].text)
                for i in range(0,numberOfTests):
                    diceResult = diceRoll.rollDicePool(diceList = diceList, bonus = bonus)[0]
                    if diceResult in outcomes:
                        outcomes[diceResult]+=1
                    else:
                        outcomes[diceResult] = 1
                plot = MeshLinePlot(color=self.plotColorMap[index],mode = 'points')
                xList = [key for key in outcomes]
                xList.sort()
                plot.points = [(key, outcomes[key]) for key in xList]
                maxCount.append(max(outcomes[key] for key in outcomes))
                maxValue.append(max(key for key in outcomes))
                expectedValue = round(sum([key * outcomes[key] for key in outcomes])/numberOfTests,1)
                test[2].text = str(expectedValue) if expectedValue != 0 else 'Error with {diceList}'.format(diceList = diceList)
                self.results=outcomes
                self.graph.add_plot(plot)
                self.plotList.append(plot)
        #Pad graph axes to make maximum values clear and prevent them being lost over the edge of the visible space
        self.graph.xmax = max(maxValue) + 2
        self.graph.ymax = max(maxCount) + 500
    
    
    def diceRollOutput(self,diceList):
        dicePool =  diceRoll.dicePool(diceList = diceList)
        dicePool.roll()
        message = dicePool.diceString+ ' \n'
        for diceType in dicePool.resultDict:
            message += 'd{diceType} : {diceResults}\n'.format(
                diceType = diceType,
                diceResults = ', '.join(map(str,dicePool.resultDict[diceType])))
        message += 'Result: ' + str(dicePool.rollSum)
        return message
    
    def fireRollButton(self,instance):
        diceList = []
        for dice in self.diceDict:
            no_of_dice = self.diceDict[dice].text
            if dice == 'custom':
                dice = 'd' + self.kivyLabel.text.lower()
            if no_of_dice != '' and no_of_dice != 0:
                diceList.append(no_of_dice + dice)
        if len(diceList) > 0:
            message = self.diceRollOutput(diceList)
            self.resultTextBox.text = '\n' + message + '\n'
        
    def fireD20Button(self,instance):
        result = diceRoll.rollDice(20)
        self.resultTextBox.text = '\n\nRolled 1d20\nResult: ' + str(result) + '\n'
         
    def fireAdvantageButton(self,instance,sides=20):
        result1 = diceRoll.rollDice(sides)
        result2 = diceRoll.rollDice(sides)
        message = 'Rolled 2d{sides}\nResult: {r1} , {r2}'.format(sides = sides, r1 = result1, r2 = result2)
        self.resultTextBox.text = '\n\n' + message + '\n'
    
    def fireMonopolyButton(self,instance):
        message = self.diceRollOutput(['2d6'])
        self.resultTextBox.text = '\n' + message + '\n'
       
    def fireStatsButton(self,instance):
        stats = diceRoll.rollStats(6)
        outString = 'Stats rolled : \n' + str(stats[0]) + ' ' + str(stats[1]) + ' ' + str(stats[2]) +'\n' + str(stats[3]) + ' ' + str(stats[4]) + ' ' + str(stats[5])
        outString += '\nAverage of ' + str(np.round( sum(stats) / len(stats) , 2))
        self.resultTextBox.text = '\n' + outString + '\n'
        
    def fireClearButton(self,instance):
        for label in self.diceDict:
            self.diceDict[label].text = ''
        self.kivyLabel.text = ''
        
    def fireNewTestButton(self,instance):
        if len(self.testList) <7:
            self.testList.append(self.appendNewTest(self.entryLayout)) 
            
    def fireResetTestsButton(self,instance):
        while len(self.testList) >1:
            self.entryLayout.remove_widget(self.testList.pop()[-1])
        for textBox in self.testList[0]:
            textBox.text = ''
        for plot in self.plotList:
            self.graph.remove_plot(plot)
    
    def firePlotButton(self,instance):
        self.createPlot()
    
if __name__ == "__main__":
    app = mainApp()
    app.run()

