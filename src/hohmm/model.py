import itertools
import random

class HOHMM:
    def __init__(self, order, emissions = None, hidden = None, startProbability = None, emissionProbability = None, transitionProbability = None, corpus = None):
        if ( emissions is None and hidden is None and startProbability is None and emissionProbability is None and transitionProbability is None and corpus is None ):
            self.__read__(order)
        else:
            self.order = order
            self.emissions = emissions
            self.hiddens = hidden
            self.startProbabilities = startProbability
            self.emissionProbabilities = emissionProbability
            self.transitionProbabilities = transitionProbability
            self.corpus = corpus
            self.alphas = dict()
            self.betas = dict()
            self.gammas = dict()
            self.deltas = dict()

    def __read__(self, path):
        file = open(path, 'r')
        self.order = int(file.readline())

        emissionSize = int(file.readline())
        self.emissions = []
        for i in range(0, emissionSize):
            self.emissions.append(file.readline().strip())

        stateSize = int(file.readline())
        self.hiddens = []
        for i in range(0, stateSize):
            self.hiddens.append(file.readline().strip())

        self.startProbabilities = []
        for i in range(0, stateSize):
            self.startProbabilities.append(float(file.readline()))
        self.emissionProbabilities = []
        for i in range(0, stateSize):
            emissionSet = []
            for i in range(0, emissionSize):
                emissionSet.append(float(file.readline()))
            self.emissionProbabilities.append(emissionSet)
        self.transitionProbabilities = []
        for i in range(0, stateSize):
            transitionSet = []
            for i in range(0, stateSize):
                transitionSet.append(float(file.readline()))
            self.transitionProbabilities.append(transitionSet)

        corpusSize = int(file.readline())
        self.corpus = []
        for i in range(0, corpusSize):
            pair = []
            pair.append(file.readline().strip())
#            file.readline()
            val = file.readline()
            pair.append(int(val))
            self.corpus.append(pair)

    def __getEmissionIndex__(self, emission):
        for i in range(0, len(self.emissions)):
            if self.emissions[i] == emission:
                return i
        return -1

    def __getStateIndex__(self, state):
        for i in range(0, len(self.hiddens)):
            if self.hiddens[i] == state:
                return i
        return -1

    #y is an element of self.corpus and is the emission sequence to be analyzed
    #j is between 1 and the length of y
    #state is the hidden state to be analyzed
    #returns the probability that first j emissions of y result in ending on state
    def __alpha__(self, y, j, state):
        if (y, j, state) in self.alphas:
            return self.alphas[(y, j, state)]

        emissionIndex = self.__getEmissionIndex__(y[j - 1])
        stateIndex = self.__getStateIndex__(state)

        if j == 1:
            return self.startProbabilities[stateIndex] * self.emissionProbabilities[stateIndex][emissionIndex]

        sum = 0
        for hidden in self.hiddens:
            hiddenIndex = self.__getStateIndex__(hidden)
            alphas = 1
            for i in range(1, self.order + 1):
                if j - i < 0:
                    break
                alphas *= self.__alpha__(y, j - i, hidden)

            sum += alphas * self.transitionProbabilities[hiddenIndex][stateIndex] * self.emissionProbabilities[stateIndex][emissionIndex]

        self.alphas[(y, j, state)] = sum
        return sum

    #y is an element of self.corpus and is the emission sequence to be analyzed
    #j is between 1 and the length of y
    #state is the hidden state to be analyzed
    def __beta__(self, y, j, state):
        if (y, j, state) in self.betas:
            return self.betas[(y, j, state)]

        if j == len(y):
            return 1

        emissionIndex =self.__getEmissionIndex__(y[j])
        stateIndex = self.__getStateIndex__(state)

        sum = 0
        for hidden in self.hiddens:
            hiddenIndex = self.__getStateIndex__(hidden)
            betas = 1
            for i in range(j + 1, min(j + self.order, len(y)) + 1):
                betas *= self.__beta__(y, i, hidden)

            sum += self.transitionProbabilities[stateIndex][hiddenIndex] * self.emissionProbabilities[hiddenIndex][emissionIndex] * betas

        self.betas[(y, j, state)] = sum
        return sum

    #y is an element of self.corpus and is the emission sequence to be analyzed
    #j is between 1 and the length of y
    #state is a hidden state to be analyzed
    #nextState is a hidden state to be analyzed
    #returns the probability that state is the jth state and nextState is the j+1th state
    def __gamma__(self, y, j, state, nextState):
        if (y, j, state, nextState) in self.gammas:
            return self.gammas[(y, j, state, nextState)]

        emissionIndex = self.__getEmissionIndex__(y[j])
        stateIndex = self.__getStateIndex__(state)
        nextStateIndex = self.__getStateIndex__(nextState)

        value = self.__alpha__(y, j, state) * self.transitionProbabilities[stateIndex][nextStateIndex] * self.emissionProbabilities[nextStateIndex][emissionIndex] * self.__beta__(y, j + 1, nextState) / self.__probability__(y)
        self.gammas[(y, j, state, nextState)] = value
        return value

    #y is an element of self.corpus and is the emission sequence to be analyzed
    #j is between 1 and the length of y
    #state is the hidden state to be analyzed
    #returns the probability of an analyzed word that the jth state is state
    def __delta__(self, y, j, state):
        if (y, j, state) in self.deltas:
            return self.deltas[(y, j, state)]

        if j == len(y):
            return self.__alpha__(y, j, state) / self.__probability__(y)

        sum = 0
        for hidden in self.hiddens:
            sum += self.__gamma__(y, j, state, hidden)

        self.deltas[(y, j, state)] = sum
        return sum

    #y is the emission sequence to be analyzed
    #returns the probability that y is observed
    def __probability__(self, y):
        sum = 0
        for hidden in self.hiddens:
            sum += self.__alpha__(y, len(y), hidden)
        return sum

    #state is the state which we want the starting probability for
    #returns the numerator for the probability computations that we start at state
    def __startingNumerator__(self, state):
        sum = 0
        for observation in self.corpus:
            sum += self.__delta__(observation[0], 1, state) * observation[1]
        return sum

    #returns the denominator for the starting probability calculations
    def __startingDenominator__(self):
        sum = 0
        for hidden in self.hiddens:
            sum += self.__startingNumerator__(hidden)
        return sum

    #state is the state which we want the starting probability for
    #returns the probability that we start at state
    def __starting__(self, state):
        return self.__startingNumerator__(state) / self.__startingDenominator__()

    #startState is the hidden state to start at
    #endState is the hidden state to end at
    #returns the numerator of the probability calculation of transitioning from startState to endState
    def __transitionNumerator__(self, startState, endState):
        sum = 0
        for observation in self.corpus:
            obsSum = 0
            for i in range(1, len(observation[0])):
                obsSum += self.__gamma__(observation[0], i, startState, endState)
            sum += obsSum * observation[1]
        return sum 

    #startState is the state we wish to get the transition probabilities for
    #returns the denominator for the probability calculation of the transitions out of startState
    def __transitionDenominator__(self, startState):
        sum = 0
        for state in self.hiddens:
            sum += self.__transitionNumerator__(startState, state)
        return sum

    #state is the state we wish to get the output probability of
    #observation is the observation which we think that state will output
    #returns the numerator of the probability calculation that state will output observation
    def __outputNumerator__(self, state, observation):
        sum = 0
        for corpusValue in self.corpus:
            obsSum = 0
            for i in range(0, len(corpusValue[0])):
                if list(corpusValue[0])[i] == observation:
                    obsSum += self.__delta__(corpusValue[0], i + 1, state)
            sum += obsSum * corpusValue[1]
        return sum

    #state is the state which we are calculating output probabilities of
    #returns the denominator of the probability calculation for the outputs at state
    def __outputDenominator__(self, state):
        sum = 0
        for emission in self.emissions:
            sum += self.__outputNumerator__(state, emission)
        return sum

    def __baumWelchHelper__(self):
        newStartProbability = []
        newEmissionProbability = []
        newTransitionProbability = []

        startDenominator = self.__startingDenominator__()
        for i in range(0, len(self.hiddens)):
            print i
            newStartProbability.append(self.__startingNumerator__(self.hiddens[i]) / startDenominator)

            print "a"
            outputDenominator = self.__outputDenominator__(self.hiddens[i])
            print "b"
            tempEmission = []
            for emission in self.emissions:
                tempEmission.append(self.__outputNumerator__(self.hiddens[i], emission) / outputDenominator)
            print "c"
            newEmissionProbability.append(tempEmission)
            print "d"

            transitionDenominator = self.__transitionDenominator__(self.hiddens[i])
            print "e"
            tempTransition = []
            for hidden in self.hiddens:
                tempTransition.append(self.__transitionNumerator__(self.hiddens[i], hidden) / transitionDenominator)
            print "f"
            newTransitionProbability.append(tempTransition)
            print "g"

        self.alphas = dict()
        self.betas = dict()
        self.gammas = dict()
        self.deltas = dict()
        return HOHMM(self.order, self.emissions, self.hiddens, newStartProbability, newEmissionProbability, newTransitionProbability, self.corpus)

    #todo
    def baumWelch(self):
        ret = self.__baumWelchHelper__()
        for i in range(0,10):
            print i
            print ret
            ret = ret.__baumWelchHelper__()

        return ret

    def __arrayEqual__(self, first, second):
        for i in range(0, len(first)):
            if first[i] != second[i]:
                return False

        return True

    def __getPermutations__(self, size, base):
        result = []

        permutation = []
        final = []
        for i in range(0, size):
            permutation.append(0)
            final.append(base - 1)
        result.append(permutation)

        while not self.__arrayEqual__(permutation, final):
            newPermutation = []
            for i in range(0, size):
                newPermutation.append(permutation[i])

            newPermutation[0] += 1
            for i in range(0, size):
                if newPermutation[i] == base:
                    newPermutation[i] = 0
                    newPermutation[i + 1] += 1
            result.append(newPermutation)
            permutation = newPermutation

        return result

    def __helper__(self, observations, probabilities, start, length):
        if length == 1:
            for i in range(0, len(self.hiddens)):
                probabilities[i][0] = self.startProbabilities[i] * self.emissionProbabilities[i][self.__getEmissionIndex__(observations[i])]
            return

        max = 0
        for i in range(1, len(observations)):
            for transitions in self.__getPermutations__(length, len(self.hiddens)):
                value = self.__helper2__(observations, probabilities, transitions, i)
                if value > max:
                    max = value
            probabilities[transitions[len(transitions) - 1]][i] = max

    def __helper2__(self, observations, probabilities, transitions, index):
        value = probabilities[transitions[0]][index - 1]
        for i in range(1, len(transitions)):
            value *= self.transitionProbabilities[transitions[i - 1]][transitions[i]] * self.emissionProbabilities[transitions[i]][self.__getEmissionIndex__(observations[index])]

        return value


    #pulled from wikipedia.org http://en.wikipedia.org/wiki/Viterbi_algorithm
    def viterbi(self, observations):
        """t1 = []
        for i in range(0, len(self.hiddens)):
            t1Temp = []
            for j in range(0, len(observations)):
                t1Temp.append(0)
            t1.append(t1Temp)

        for i in range(0, self.order):
            self.__helper__(observations, t1, 0, i + 1)

        for i in range(self.order, len(observations) - self.order + 1):
            self.__helper__(observations, t1, i, self.order + 1)

        sequence = []
        for i in range(0, len(observations)):
            max = 0
            for j in range(1, len(self.hiddens)):
                if t1[j][i] > t1[max][i]:
                    max = j
            sequence.append(self.hiddens[max])

        print sequence"""
        t1 = []
        t2 = []
        for i in range(0, len(self.hiddens)):
            t1Temp = []
            t2Temp = []
            for j in range(0, len(observations)):
                t1Temp.append(0)
                t2Temp.append(0)
            t1.append(t1Temp)
            t2.append(t2Temp)

        for i in range(0, len(self.hiddens)):
            t1[i][0] = self.startProbabilities[i] * self.emissionProbabilities[i][self.__getEmissionIndex__(observations[0])]

#        print t1

        for i in range(1, len(observations)):
            for j in range(0, len(self.hiddens)):
                max = 0
                index = 0
                for k in range(0, len(self.hiddens)):
                    value = t1[k][i - 1] * self.transitionProbabilities[k][j] * self.emissionProbabilities[j][self.__getEmissionIndex__(observations[i])]
                    if value > max:
                        max = value
                        index = k
                t1[j][i] = max
                t2[j][i] = index

#        print t1
#        print t2

        z = []
        x = []
        for i in range(0, len(observations)):
            z.append(0)
            x.append('')

        index = 0
        for k in range(0, len(self.hiddens)):
            if t1[k][len(observations) - 1] > t1[index][len(observations) - 1]:
                index = k

        res = ""
        z[len(observations) - 1] = index
        x[len(observations) - 1] = self.hiddens[index]
        res += x[len(observations) - 1]

        for i in range(len(observations) - 1, 0, -1):
            z[i - 1] = t2[z[i]][i]
            x[i - 1] = self.hiddens[z[i - 1]]
            res = x[i - 1] + res

        return res

        """self.order = order
            self.emissions = emissions
                self.hiddens = hidden
            self.startProbabilities = startProbability
            self.emissionProbabilities = emissionProbability
            self.transitionProbabilities = transitionProbability
            self.corpus = corpus
"""

    def __eq__(self, other):
        if self.order != other.order:
            return False

        if len(self.emissions) != len(other.emissions):
            return False;
        for i in range(0, len(self.emissions)):
            if self.emissions[i] != other.emissions[i]:
                return False

        if len(self.hiddens) != len(other.hiddens):
            return False;
        for i in range(0, len(self.hiddens)):
            if self.hiddens[i] != other.hiddens[i]:
                return False

        if len(self.startProbabilities) != len(other.startProbabilities):
            return False
        for i in range(0, len(self.startProbabilities)):
            if not floats_equal(self.startProbabilities[i], other.startProbabilities[i], 0.00001):
                return False

        if len(self.emissionProbabilities) != len(other.emissionProbabilities):
            return False
        for i in range(0, len(self.emissionProbabilities)):
            if len(self.emissionProbabilities[i]) != len(other.emissionProbabilities[i]):
                return False
            for j in range(0, len(self.emissionProbabilities[i])):
                if not floats_equal(self.emissionProbabilities[i][j], other.emissionProbabilities[i][j], 0.00001):
                    return False

        if len(self.transitionProbabilities) != len(other.transitionProbabilities):
            return False
        for i in range(0, len(self.transitionProbabilities)):
            if len(self.transitionProbabilities[i]) != len(other.transitionProbabilities[i]):
                return False
            for j in range(0, len(self.transitionProbabilities[i])):
                if not floats_equal(self.transitionProbabilities[i][j], other.transitionProbabilities[i][j], 0.00001):
                    return False

        if len(self.corpus) != len(other.corpus):
            return False
        for i in range(0, len(self.corpus)):
            if len(self.corpus[i]) != len(other.corpus[i]):
                return False
            for j in range(0, len(self.corpus[i])):
                if self.corpus[i][j] != other.corpus[i][j]:
                    return False

        return True

    def write(self, path):
        file = open(path, 'w')

        file.write(str(self.order) + "\n")

        file.write(str(len(self.emissions)) + "\n")
        for emission in self.emissions:
            file.write(emission + "\n")

        file.write(str(len(self.hiddens)) + "\n")
        for hidden in self.hiddens:
            file.write(hidden + "\n")

        for starting in self.startProbabilities:
            file.write(str(starting) + "\n");
        for emissionSet in self.emissionProbabilities:
            for emission in emissionSet:
                file.write(str(emission) + "\n")
        for transitionSet in self.transitionProbabilities:
            for transition in transitionSet:
                file.write(str(transition) + "\n")

        file.write(str(len(self.corpus)) + "\n")
        for pair in self.corpus:
            file.write(pair[0] + "\n")
            file.write(str(pair[1]) + "\n")

    #size is the length of the desired emission, random if not specified
    #returns a sequence of random emissions of size size
    def getRandomSequence(self, size = 0):
        if size == 0:
            size = random.randint(0, 1000)

        choice = self.__getRandom__()
        observationSequence = str(choice[0])
        stateSequence = str(choice[1])
        current = choice[1]
        for i in range(0, size):
            choice = self.__getRandom__(self.__getStateIndex__(current))
            observationSequence += str(choice[0])
            stateSequence += str(choice[1])
            current = choice[1]

        return (observationSequence, stateSequence)

    #current is the current state in an observation sequence (-1 corresponds to not having started yet)
    #returns a random (emission, next state)
    def __getRandom__(self, current = -1):
        probabilities = []
        if current == -1:
            probabilities = self.startProbabilities
        else:
            probabilities = self.transitionProbabilities[current]

        nextState = ""
        emission = ""
        choice = random.random()
        probability = 0
        for i in range(0, len(probabilities)):
            probability += probabilities[i]
            if ( choice < probability ):
                nextState = self.hiddens[i]
                choice = random.random()
                probability = 0
                for j in range(0, len(self.emissionProbabilities[i])):
                    probability += self.emissionProbabilities[i][j]
                    if ( choice < probability ):
                        emission = self.emissions[j]
                        return (emission, nextState)
        return (emission, nextState)

    def __str__(self):
        ret = ""
        ret += "Order: " + str(self.order) + "\n"
        ret += "Emissions: " + str(self.emissions) + "\n"
        ret += "Hidden States: " + str(self.hiddens) + "\n"
        for i in range(0, len(self.startProbabilities)):
            ret += "Probability of starting at " + self.hiddens[i] + ": " + str(self.startProbabilities[i]) + "\n"

        for i in range(0, len(self.hiddens)):
            for j in range(0, len(self.emissionProbabilities[i])):
                ret += "Probability of observing " + self.emissions[j] + " at state " + self.hiddens[i] + ": " + str(self.emissionProbabilities[i][j]) + "\n"

        for i in range(0, len(self.hiddens)):
            for j in range(0, len(self.transitionProbabilities[i])):
                ret += "Probability of transitioning from state " + self.hiddens[i] + " to state " + self.hiddens[j] + ": " + str(self.transitionProbabilities[i][j]) + "\n"

        ret += "Corpus:\n"
        for pair in self.corpus:
            pass
#            ret += str(pair) + "\n"

        return ret

def initTest(order):
    emissions = ["A", "B"]
    hidden = ["s", "t"]
    startProbability = [0.85, 0.15]
    emissionProbability = [[0.4, 0.6], [0.5, 0.5]]
    transitionProbability = [[0.3, 0.7], [0.1, 0.9]]
    corpus = [["ABBA", 10], ["BAB", 20]]

    hmm = HOHMM(order, emissions, hidden, startProbability, emissionProbability, transitionProbability, corpus)
    return hmm

def initSanity(order):
    emissions = ["A", "B", "C", "D", "E"]
    hidden = ["s", "t"]
    startProbability = [0.85, 0.15]
    emissionProbability = [[0.1, 0.2, 0.3, 0.2, 0.2], [0.7, 0.1, 0.05, 0.05, 0.1]]
    transitionProbability = [[0.3, 0.7], [0.6, 0.4]]
    corpus = [["ABBA", 10], ["BAB", 20]]

    hmm = HOHMM(order, emissions, hidden, startProbability, emissionProbability, transitionProbability, corpus)
    return hmm

def initBlank(corpus, order):
    emissions = ["A", "B"]
    hidden = ["s", "t"]
    startProbability = [0.8, 0.2]
    emissionProbability = [[0.5, 0.5], [0.5, 0.5]]
    transitionProbability = [[0.35, 0.65], [0.05, 0.95]]

    hmm = HOHMM(order, emissions, hidden, startProbability, emissionProbability, transitionProbability, corpus)
    return hmm

def initClose(original, corpus, order, distance):
    emissions = original.emissions
    hidden = original.hiddens
    startProbability = []
    emissionProbability = []
    transitionProbability = []

    multiplier = -1
    for prob in original.startProbabilities:
        if prob < distance:
            multiplier = 1
        elif prob > 1 - distance:
            multiplier = -1
        startProbability.append(prob + multiplier * distance)
        multiplier *= -1

    for pair in original.emissionProbabilities:
        temp = []
        for prob in pair:
            if prob < distance:
                multiplier = 1
            elif prob > 1 - distance:
                multipler = -1
            temp.append(prob + multiplier * distance)
            multiplier *= -1
        emissionProbability.append(temp)

    for pair in original.transitionProbabilities:
        temp = []
        for prob in pair:
            if prob < distance:
                multiplier = 1
            elif prob > 1 - distance:
                multiplier = -1
            temp.append(prob + multiplier * distance)
            multiplier *= -1
        transitionProbability.append(temp)

    hmm = HOHMM(order, emissions, hidden, startProbability, emissionProbability, transitionProbability, corpus)
    print hmm
    return hmm

    """ self.order = order
            self.emissions = emissions
                self.hiddens = hidden
            self.startProbabilities = startProbability
            self.emissionProbabilities = emissionProbability
            self.transitionProbabilities = transitionProbability
            self.corpus = corpus"""

def alphaTest():
    cases = [["ABBA", 1, "s"],
             ["ABBA", 1, "t"],
             ["ABBA", 2, "s"],
             ["ABBA", 2, "t"],
             ["ABBA", 3, "s"],
             ["ABBA", 3, "t"],
             ["ABBA", 4, "s"],
             ["ABBA", 4, "t"],
             ["BAB", 1, "s"],
             ["BAB", 1, "t"],
             ["BAB", 2, "s"],
             ["BAB", 2, "t"],
             ["BAB", 3, "s"],
             ["BAB", 3, "t"]
             ]
    results = [0.34000,
               0.07500,
               0.06570,
               0.15275,
               0.02099,
               0.09173,
               0.00618,
               0.04862,
               0.51000,
               0.07500,
               0.06420,
               0.21225,
               0.02429,
               0.11798
               ]

    hmm = initTest(1)

    for i in range(0, len(cases)):
        value = hmm.__alpha__(cases[i][0], cases[i][1], cases[i][2])
        if floats_equal(results[i], value, 0.00001):
            print passed("__alpha__ order 1", i)
        else:
            print failed("__alpha__ order 1", i, value, results[i])

def betaTest():
    cases = [["ABBA", 4, "s"],
             ["ABBA", 4, "t"],
             ["ABBA", 3, "s"],
             ["ABBA", 3, "t"],
             ["ABBA", 2, "s"],
             ["ABBA", 2, "t"],
             ["ABBA", 1, "s"],
             ["ABBA", 1, "t"],
             ["BAB", 3, "s"],
             ["BAB", 3, "t"],
             ["BAB", 2, "s"],
             ["BAB", 2, "t"],
             ["BAB", 1, "s"],
             ["BAB", 1, "t"]
             ]
    results = [1,
               1,
               0.47000,
               0.49000,
               0.25610,
               0.24870,
               0.13315,
               0.12729,
               1,
               1,
               0.53000,
               0.51000,
               0.24210,
               0.25070
               ]

    hmm = initTest(1)

    for i in range(0, len(cases)):
        value = hmm.__beta__(cases[i][0], cases[i][1], cases[i][2])
        if floats_equal(results[i], value, 0.00001):
            print passed("__beta__ order 1", i)
        else:
            print failed("__beta__ order 1", i, value, results[i])

def gammaTest():
    cases = [["ABBA", 1, "s", "s"],
             ["ABBA", 1, "s", "t"],
             ["ABBA", 1, "t", "s"],
             ["ABBA", 1, "t", "t"],
             ["ABBA", 2, "s", "s"],
             ["ABBA", 2, "s", "t"],
             ["ABBA", 2, "t", "s"],
             ["ABBA", 2, "t", "t"],
             ["ABBA", 3, "s", "s"],
             ["ABBA", 3, "s", "t"],
             ["ABBA", 3, "t", "s"],
             ["ABBA", 3, "t", "t"],
             ["BAB", 1, "s", "s"],
             ["BAB", 1, "s", "t"],
             ["BAB", 1, "t", "s"],
             ["BAB", 1, "t", "t"],
             ["BAB", 2, "s", "s"],
             ["BAB", 2, "s", "t"],
             ["BAB", 2, "t", "s"],
             ["BAB", 2, "t", "t"]
             ]
    results = [0.28593,
               0.53991,
               0.02102,
               0.15312,
               0.10140,
               0.20555,
               0.07858,
               0.61445,
               0.04595,
               0.13403,
               0.06694,
               0.75307,
               0.22798,
               0.63985,
               0.01117,
               0.12098,
               0.08122,
               0.15793,
               0.08951,
               0.67133
               ]

    hmm = initTest(1)

    for i in range(0, len(cases)):
        value = hmm.__gamma__(cases[i][0], cases[i][1], cases[i][2], cases[i][3])
        if floats_equal(results[i], value, 0.00001):
            print passed("__gamma__ order 1", i)
        else:
            print failed("__gamma__ order 1", i, value, results[i])

def probabilityTest():
    cases = [["ABBA"],
             ["BAB"]
             ]
    results = [0.05481,
               0.14227
               ]

    hmm = initTest(1)

    for i in range(0, len(cases)):
        value = hmm.__probability__(cases[i][0])
        if floats_equal(results[i], value, 0.00001):
            print passed("__probability__ order 1", i)
        else:
            print failed("__probability__ order 1", i, value, results[i])

def deltaTest():
    cases = [["ABBA", 1, "s"],
             ["ABBA", 1, "t"],
             ["ABBA", 2, "s"],
             ["ABBA", 2, "t"],
             ["ABBA", 3, "s"],
             ["ABBA", 3, "t"],
             ["ABBA", 4, "s"],
             ["ABBA", 4, "t"],
             ["BAB", 1, "s"],
             ["BAB", 1, "t"],
             ["BAB", 2, "s"],
             ["BAB", 2, "t"],
             ["BAB", 3, "s"],
             ["BAB", 3, "t"]
             ]
    results = [0.82584,
               0.17415,
               0.30695,
               0.69304,
               0.17998,
               0.82001,
               0.11289,
               0.88710,
               0.86784,
               0.13215,
               0.23915,
               0.76084,
               0.17073,
               0.82926
               ]

    hmm = initTest(1)

    for i in range(0, len(cases)):
        value = hmm.__delta__(cases[i][0], cases[i][1], cases[i][2])
        if floats_equal(results[i], value, 0.00001):
            print passed("__delta__ order 1", i)
        else:
            print failed("__delta__ order 1", i, value, results[i])

def startingNumeratorTest():
    cases = [["s"],
             ["t"]
             ]
    results = [25.61533,
               4.38466
               ]

    hmm = initTest(1)

    for i in range(0, len(cases)):
        value = hmm.__startingNumerator__(cases[i][0])
        if floats_equal(results[i], value, 0.00001):
            print passed("__startingNumerator__ order 1", i)
        else:
                print failed("__startingNumerator__ order 1", i, value, results[i])

def startingDenominatorTest():
    cases = [[]
             ]
    results = [30.00000
               ]

    hmm = initTest(1)

    for i in range(0, len(cases)):
        value = hmm.__startingDenominator__()
        if floats_equal(results[i], value, 0.00001):
            print passed("__startingDenominator__ order 1", i)
        else:
            print failed("__startingDenominator__ order 1", i, value, results[i])

def transitionNumeratorTest():
    cases = [["s", "s"],
             ["s", "t"],
             ["t", "s"],
             ["t", "t"]
             ]
    results = [10.51700,
               24.75091,
               3.67921,
               31.05286
               ]

    hmm = initTest(1)

    for i in range(0, len(cases)):
        value = hmm.__transitionNumerator__(cases[i][0], cases[i][1])
        if floats_equal(results[i], value, 0.00001):
            print passed("__transitionNumerator__ order 1", i)
        else:
            print failed("__transitionNumerator__ order 1", i, value, results[i])

def transitionDenominatorTest():
    cases = ["s",
             "t"
             ]
    results = [35.26792,
               34.73207
               ]

    hmm = initTest(1)

    for i in range(0, len(cases)):
        value = hmm.__transitionDenominator__(cases[i][0])
        if floats_equal(results[i], value, 0.00001):
            print passed("__transitionDenominator__ order 1", i)
        else:
            print failed("__transitionDenominator__ order 1", i, value, results[i])

def outputNumeratorTest():
    cases = [["s", "A"],
             ["s", "B"],
             ["t", "A"],
             ["t", "B"]
             ]
    results = [14.17059,
               25.64095,
               25.82940,
               34.35904
               ]

    hmm = initTest(1)

    for i in range(0, len(cases)):
        value = hmm.__outputNumerator__(cases[i][0], cases[i][1])
        if floats_equal(results[i], value, 0.00001):
            print passed("__outputNumerator__ order 1", i)
        else:
            print failed("__outputNumerator__ order 1", i, value, results[i])

def outputDenominatorTest():
    cases = [["s"],
             ["t"]
             ]
    results = [39.81155,
               60.18844
               ]

    hmm = initTest(1)

    for i in range(0, len(cases)):
        value = hmm.__outputDenominator__(cases[i][0])
        if floats_equal(results[i], value, 0.00001):
            print passed("__outputDenominator__ order 1", i)
        else:
            print failed("__outputDenominator__ order 1", i, value, results[i])

def baumWelchHelperTest():
    cases = [[]
             ]
    results = []

    emissions = ["A", "B"]
    hidden = ["s", "t"]
    startProbability = [0.85384, 0.14615]
    emissionProbability = [[0.35594, 0.64405], [0.42914, 0.57085]]
    transitionProbability = [[0.29820, 0.70179], [0.10593, 0.89406]]
    corpus = [["ABBA", 10], ["BAB", 20]]

    results.append(HOHMM(1, emissions, hidden, startProbability, emissionProbability, transitionProbability, corpus))

    hmm = initTest(1)

    for i in range(0, len(cases)):
        value = hmm.__baumWelchHelper__()
        if results[i] == value:
            print passed("__baumWelchHelper__ order 1", i)
        else:
            print failed("__baumWelchHelper__ order 1", i, value, results[i])

#TODO
def baumWelchTest():
    hmm = initTest(1)
    hmm = hmm.baumWelch()

def readWriteTest():
    hmm = initTest(1)
    hmm.write('tmp.txt')
    new = HOHMM('tmp.txt')

    if hmm == new:
        print passed("write order 1", 0)
        print passed("read order 1", 0)
    else:
        print failed("write order 1", 0, "N/A", "N/A")
        print failed("read order 1", 0, "N/A", "N/A")

def viterbiTest():
    cases = [initTest(1),
             initSanity(1)
             ]
    results = ["stttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt",
               "tstssttststttstsstssstssttsttsstsststssttstststtststttsststtttsststtststttstststtsststtttststttsststs"
               ]
    random.seed(1)
    for i in range(0, len(cases)):
        sequences = cases[i].getRandomSequence(100)
        value = cases[i].viterbi(sequences[0])
        if value != results[i]:
            print failed("viterbi order 1", i, results[i], value)
        else:
            print passed("viterbi order 1", i)

def passed(function, case):
    return "HOHMM " + function + " Test " + str(case) + " passed"

def failed(function, case, real, expected):
    return "HOHMM " + function + " Test " + str(case) + " failed; Expected: " + str(expected) + "; Received: " + str(real)

def floats_equal(first, second, epsilon):
    return abs(first - second) < epsilon

def test():
    alphaTest()
    betaTest()
    probabilityTest()
    gammaTest()
    deltaTest()
    startingNumeratorTest()
    startingDenominatorTest()
    transitionNumeratorTest()
    transitionDenominatorTest()
    outputNumeratorTest()
    outputDenominatorTest()
    baumWelchHelperTest()
    readWriteTest()
    viterbiTest()

def sanityCheck():
    hmm = initSanity(1)
    random.seed(1)

    size = 1000
    average = 0.0
    for j in range(0, size):
        sequences = hmm.getRandomSequence(100)
        value = hmm.viterbi(sequences[0])
        result = 0
        for i in range(0, len(value)):
            if value[i] != sequences[1][i]:
                result = result + 1
        average += result
    print average / size

def sanityCheck2():
    originals = [initSanity(1)
                 ]

    random.seed(50000)
    for original in originals:
        corpus = dict()
        for i in range(0, 50):
            sequence = original.getRandomSequence(random.randint(1, 6))[0]
            if corpus.has_key(sequence):
                corpus[sequence] = corpus[sequence] + 1
            else:
                corpus[sequence] = 1

        print corpus.items()
#    learned = initBlank(corpus.items(), 1)
        learned = initClose(original, corpus.items(), 1, 0.1)
    #learned = HOHMM("test.txt2")
        test = learned.baumWelch()
        print test
        print original
        test.write("test.txt2")
    """hmm = initTest(1)
print original
    hmm = hmm.__baumWelchHelper__()
    print hmm
    hmm = hmm.__baumWelchHelper__()
    print hmm
    hmm = hmm.__baumWelchHelper__()
    print hmm"""
