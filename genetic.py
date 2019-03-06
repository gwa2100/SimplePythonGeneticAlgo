from math import *
import random
import itertools
import time
import datetime


def math_string(s):
    s_len = len(s)
    m = [[None for i in range(s_len)] for j in range(s_len)]
    output_val = None
    for i in range(s_len):
        for j in range(len(s)):
            try:
                val = eval(s[i:j].strip())
                if len(s[i:j].strip()) > 1 and len(s[i:j]) - len(s[i:j].strip()) == 0:
                    output_val = val
                    m[i][j] = val

            except:
                val = None
    last_i = -1
    last_j = -1
    max_j = -1
    indexlist = []
    for i in range(s_len):
        for j in range(s_len):
            if m[i][j] and j > max_j:
                max_j = j
        if i > last_i and max_j > last_j:
            last_i = i
            last_j = max_j
            indexlist.append([last_i, last_j])

    os = ''
    if len(indexlist) > 0:
        os = 'str(s[0:'
        for a in indexlist:
            os = '%s%s])+str(m[%s][%s])+str(s[%s:' % (os, str(a[0]), str(a[0]), str(a[1]), a[1])
        os = '%slen(s)])' % os
    # print os
    out = eval(os)
    return float(eval(out))


def computeChoices(startingNumber):
    total = 0
    for x in range(startingNumber, 1, -1):
        total += x
    return total


class chromosome:
    def __init__(self, number, operator):
        self.number = number
        self.operator = operator


class creature:
    def __init__(self, numberOfChromosomes, chromosomes):
        self.numberOfChromosomes = numberOfChromosomes
        self.chromosomes = []
        self.chromosomes = chromosomes
        self.creatureScore = 0
        self.living = True
        self.chromoString = ""
        for x in self.chromosomes:
            self.chromoString += str(x.number)
            self.chromoString += x.operator
        self.chromoString = self.chromoString[:-1]
        self.creatureAnswer = 0;

    def generateChromoString(self):
        chromoString = ''
        for x in self.chromosomes:
            chromoString += str(x.number)
            chromoString += x.operator
        return chromoString


class world:
    def __init__(self, maxNumberOfCreatures, roundsToRun, numbers=[], targetAnswer=25, mutationPercentage=5):
        self.round = 0
        self.run = True
        self.maxNumberOfCreatures = maxNumberOfCreatures
        self.roundsToRun = roundsToRun
        self.creatures = []
        self.deadCreatures = []
        self.bestCreature = ""
        self.bestCreatureScore = 0
        self.numbers = []
        self.numbers = numbers
        self.chromosomes = []
        self.possibleOperators = ["*", "+", "-", "/"]
        self.targetAnswer = targetAnswer
        self.killedLastRound = 0
        self.totalKilled = 0
        self.average = 0
        self.mutatedLastRound = 0
        self.totalMutated = 0
        self.mutationRatio = mutationPercentage / 100
        self.startTime = 0
        self.endTime = 0
        self.avgElapsedTimeRnd = 0
        self.totalTime = 0
        self.lastRoundTime = 0
        # Generate Random Chromosomes
        for x in self.numbers:
            for o in self.possibleOperators:
                chromo = chromosome(x, o)
                self.chromosomes.append(chromo)
        print(str(len(self.chromosomes)) + " chromosomes have been created")
        for x in self.chromosomes:
            print(str(x.number) + x.operator)

    def generateCreatures(self, numberToGenerate):
        secure_random = random.SystemRandom()
        for creatureNum in range(0, numberToGenerate):
            chromoLoad = []
            for x in range(0, len(self.numbers)):
                foundUniqueChromo = False
                while not foundUniqueChromo:
                    tryChromo = secure_random.choice(self.chromosomes)
                    foundUniqueChromo = True
                    for y in chromoLoad:
                        tryChromoNum = tryChromo.number
                        chromoLoadNum = str(y.number)
                        if tryChromoNum == chromoLoadNum:
                            foundUniqueChromo == False
                    if foundUniqueChromo == True:
                        chromoLoad.append(tryChromo)
            creat = creature(len(self.numbers), chromoLoad)
            self.creatures.append(creat)

    def birthCreatures(self, numberToBirth):
        secure_random = random.SystemRandom()
        for x in numberToBirth:
            chromoLoad = []
            parent1 = secure_random.choice(self.creatures)
            parent2 = secure_random.choice(self.creatures)
            for y in len(self.numbers):
                tryChromoOne = secure_random.choice(parent1.chromosomes)
                tryChromoTwo = secure_random.choice(parent2.chromosomes)
                chromoLoad.append(tryChromoOne)
                chromoLoad.append(tryChromoTwo)
            newCreature = creature(len(self.numbers, chromoLoad))
            self.creatures.append(newCreature)

    def mutateCreatures(self, numberToMutate):
        secure_random = random.SystemRandom()
        self.mutatedLastRound = numberToMutate
        for creatureNum in range(0, numberToMutate):
            chromoLoad = []
            for x in range(0, len(self.numbers)):
                foundUniqueChromo = False
                while not foundUniqueChromo:
                    tryChromo = secure_random.choice(self.chromosomes)
                    if tryChromo in chromoLoad:
                        continue
                    else:
                        chromoLoad.append(tryChromo)
                        foundUniqueChromo = True
            creat = creature(len(self.numbers), chromoLoad)
            self.creatures.append(creat)

    def start(self):
        self.generateCreatures(self.maxNumberOfCreatures)
        self.loop()

    def loop(self):
        while (self.run == True) and (self.round <= self.roundsToRun):
            self.startTime = time.time()
            self.round += 1
            self.totalKilled += self.killedLastRound
            self.killedLastRound = 0
            self.totalMutated += self.mutatedLastRound
            self.mutatedLastRound = 0
            self.score()
            self.update()
            self.endTime = time.time()
            self.lastRoundTime = self.endTime - self.startTime
            self.totalTime += self.lastRoundTime
            self.avgElapsedTimeRnd = self.totalTime / self.round
            self.render()
        self.outputResults()

    def score(self):
        for x in self.creatures:
            x.creatureAnswer = answer = math_string(x.chromoString)
            # print(x.chromoString + "=" + str(answer))
            x.creatureScore = 100 - abs(int(self.targetAnswer) - answer)
            if x.creatureScore < 0:
                x.creatureScore = 0
            # print(x.creatureScore)
            if x.creatureScore > self.bestCreatureScore:
                self.bestCreature = x
                self.bestCreatureScore = x.creatureScore
                print("~~~ Found New Best Creature With Score: " + str(self.bestCreature.creatureScore) + "~~~")
                if self.bestCreatureScore == 100:
                    self.run = False

    def update(self):
        # get average score
        self.average = 0.00
        totals = 0
        for x in self.creatures:
            totals += x.creatureScore
        self.average = totals / len(self.creatures)
        # print ("AVG b4 purge:" + str(self.average))
        for x in self.creatures:
            if x.creatureScore == 0:
                self.creatures.remove(x)
                self.killedLastRound += 1
            if x.creatureScore < self.average:
                try:
                    self.creatures.remove(x)
                    self.killedLastRound += 1
                except:
                    pass
            if len(x.chromosomes) < len(self.numbers):
                try:
                    self.creatures.remove(x)
                    self.killedLastRound += 1
                except:
                    pass
        # get average score
        self.average = 0.00
        totals = 0
        for x in self.creatures:
            totals += x.creatureScore
        self.average = totals / len(self.creatures)
        # print("AVG After purge:" + str(self.average))
        numberToMutate = int(self.killedLastRound * self.mutationRatio)
        self.mutateCreatures(numberToMutate)
        self.generateCreatures(self.killedLastRound - numberToMutate)

    def render(self):
        print("=======================ROUND #" + str(self.round) + "===========================")
        print("Time Elapsed: Total: " + str(self.totalTime) + " Last Rnd: " + str(self.lastRoundTime) + " Ave/Rnd: " + str(self.avgElapsedTimeRnd) + " Est Rem Time: " + str((self.avgElapsedTimeRnd * (self.roundsToRun - self.round))/60) + " min")
        print("Killed: " + str(self.killedLastRound) + " Creatures Last Round")
        print("Mutated: " + str(self.mutatedLastRound) + " Creatures Last Round")
        print("Population: " + str(len(self.creatures)))
        print("Average Score: " + str(self.average))
        print("Best Creature Score: " + str(self.bestCreatureScore))
        print("Best Creature Chromo: " + self.bestCreature.chromoString)
        print("Best Creature Answer: " + str(self.bestCreature.creatureAnswer))
        print("===========================================================")

    def outputResults(self):
        print("===========================================================")
        print("=======================RESULTS=============================")
        print("===========================================================")
        print("Rounds Ran : +" + str(self.round) + " of target " + str(self.roundsToRun))
        print("Ending Average: " + str(self.average))
        print("Best Creature Score: " + str(self.bestCreatureScore))
        print("Best Creature Chromo: " + self.bestCreature.chromoString)
        print("Best Creature Answer: " + str(self.bestCreature.creatureAnswer))
        print("Total Population: " + str(self.totalKilled + len(self.creatures)))
        print("Total Killed:     " + str(self.totalKilled))
        print("Total Mutated:     " + str(self.totalMutated))
        print("=========================END===============================")
        self.writeResults()

    def writeResults(self):
        file = open("results.txt", "a")
        file.write("===========================================================\n")
        file.write("=======================RESULTS=============================\n")
        file.write("=======================DATE:" + str(datetime.datetime.now()) + "======================\n")
        file.write("Rounds Ran : +" + str(self.round) + " of target " + str(self.roundsToRun))
        file.write("\nEnding Average: " + str(self.average))
        file.write("\nBest Creature Score: " + str(self.bestCreatureScore))
        file.write("\nBest Creature Chromo: " + self.bestCreature.chromoString)
        file.write("\nBest Creature Answer: " + str(self.bestCreature.creatureAnswer))
        file.write("\nTotal Population: " + str(self.totalKilled + len(self.creatures)))
        file.write("\nTotal Killed:     " + str(self.totalKilled))
        file.write("\nTotal Mutated:     " + str(self.totalMutated))
        file.write("\n=========================END===============================\n")
        file.write("===========================================================\n")
        file.write("=======================CREATURE DUMP=======================\n")
        for x in self.creatures:
            file.write("===========================================================\n")
            file.write("Creature Chromo: " + x.chromoString)
            file.write("\nCreature Answer: " + str(x.creatureAnswer))
            file.write("\n===========================================================\n")

        file.write("=========================END===============================\n")
        file.write("===========================================================\n")
        file.write("=======================CHROMO DUMP=========================\n")
        for x in self.chromosomes:
            file.write(str(x.number) + x.operator + " | ")
        file.write("\n=========================END===============================\n")
        file.write("===========================================================\n")
        file.write("=======================RUN SPECS===========================\n")
        file.write("ROUNDS TO BE RUN: " + str(self.roundsToRun))
        file.write("\nMAX POPULATION SIZE: " + str(self.maxNumberOfCreatures))
        file.write("\nNUMBER PAYLOAD: " + str(self.numbers))
        file.write("\nTARGET ANSWER: " + str(self.targetAnswer))
        file.write("\nMUTATION RATIO: " + str(self.mutationRatio))
        file.write("\n=========================END===============================\n")
        file.write("=========================END OF ENTRY======================\n")

# creatures, rounds, numbers[], answer
#world = world(75, 10, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29], 31, 25)
world = world(100, 50, [3,5,7,9,11,13,17,23], 25, 20)
world.start()
