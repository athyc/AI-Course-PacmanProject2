# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util, math

from game import Agent

def euclidian(x1,x2):
    return math.sqrt((x1[0] - x2[0])*(x1[0] - x2[0]) + (x1[1] - x2[1])*(x1[1] - x2[1]))
def isWithinRange(ghostpos, pacpos, range):
    return euclidian(ghostpos, pacpos) <=range
def getClosestFood(pacpos, gameState):
    foods = gameState.getFood()
    foodList = foods.asList()
    all = list()
    for i in foodList:
        all.append(euclidian(i,pacpos))
    return foodList[all.index(min(all))]
def getClosestFoodWithList(pacpos, foodList):

    all = list()
    for i in foodList:
        all.append(util.manhattanDistance(i,pacpos))
    return foodList[all.index(min(all))],min(all)
class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        #print gameState
        #print "legalmoves",legalMoves
        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        #print "scores!!",scores
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
		
        "Add more of your code here if you want to"
        #print "scores!!",scores.index(max(scores))
        #print "legalmoves",legalMoves
        #athineyatsbds=raw_input()

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)

        successorGameState = currentGameState.generatePacmanSuccessor(action)
        currPos = currentGameState.getPacmanPosition()
        if(successorGameState.isWin()):
            return 999999
        if(successorGameState.isLose()):
            return -999999
        #print "1\n",successorGameState
        newPos = successorGameState.getPacmanPosition()
        #print "2",newPos
        newFood = successorGameState.getFood()
        #print "3",newFood
        foods = newFood.asList()
        ghosts = successorGameState.getGhostPositions()
        width,length = util.getDimensions(newFood)
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        #add euclidean distance somehow
        # if this action brings you in range two of ghost- and ghost timer is off - return low score - prioritizes avoiding ghosts and not losing
        sum = 0
        flag = 0
        for i in ghosts:
            if(isWithinRange(currPos, i, 3) and euclidian(currPos, i) > euclidian(newPos,i)):
                flag=1
                sum = sum -200
            elif (isWithinRange(currPos, i,2) and euclidian(currPos, i) <= euclidian(newPos, i)):
                sum = sum + 200
                flag=1

        if (flag):
            return sum

        #if this action brings you closer to ghost, return low score
        for i in range(0, len(ghosts)):

            if(isWithinRange(ghosts[i], newPos, 2) and newScaredTimes[i]):
                return 500
            elif(isWithinRange(ghosts[i], newPos, 3) and not newScaredTimes[i]):
                return -1000
        #if increases distance from ghost - return high-ish
        #if this move gets food, return high
        if(newPos in foods):
            return 1000
        #if dist(prevpac, closest food) > dist(thispac, closestfood) return high

        prevclos = getClosestFood(currentGameState.getPacmanPosition(),currentGameState)
        if ( euclidian(prevclos, currentGameState.getPacmanPosition()) > euclidian(prevclos, newPos)):
            return 550
        return 100

        # else if thsi action brings you near ghost and ghost timer is off - return high score - prioritize hunting ghosts
        # if this action brings you closer to food, return high score something stable / len of foods - gravitates toward  food

        """
        rvalue=0
        distancesFromGhost=list()
        distancesFromFood=list()

        for i in range(0,len(newGhostStates)):
        	print newGhostStates[i],',',newScaredTimes[i]
        	print manhattanDistance(newGhostStates[i].getPosition(),newPos)
        	distancesFromGhost.append(manhattanDistance(newGhostStates[i].getPosition(),newPos))
        	print "rvalue ghosts",rvalue
        
        rvalue=rvalue+(width*length - len(newFood.asList()))*min(distancesFromGhost)
        for i in newFood.asList():
        	print i
        	distancesFromFood.append(manhattanDistance(i,newPos))
        	print "rvalue food",rvalue
        rvalue=rvalue-(width*length - len(newFood.asList()))*min(distancesFromFood)
        "*** YOUR CODE HERE ***"

        return rvalue
        """

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    
    
    
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def minimax(depth, player, gameState, counter):
            
            #print "[playing",player
            #print "state\n",gameState
            #print "depth",depth
            #print 'node',counter
            #raw_input()
            if(gameState.isWin() or gameState.isLose() or depth==0):
               #print 'reached finale]',depth,gameState.isWin() , gameState.isLose(),'\n',gameState
               #raw_input()
               return self.evaluationFunction(gameState)
            successors=list()
            minimaxValues=list()
            if player == 0:
                #print 'now playing pacman'
                
                value = - float("inf")
                actions= gameState.getLegalActions()
                for i in actions:
                  #  print i #printactions
                    temp = gameState.generateSuccessor(player, i)
                 #   print temp
                    successors.append(temp)
                for i in successors:
                    minimaxValues.append(minimax(depth  , (player+1)%gameState.getNumAgents(),i,counter+1))
                #print 'minimaxvalues for node',counter
                #print minimaxValues
                value=max(value,max(minimaxValues))
                if(counter == 0):
               #     print minimaxValues
              #      print "to befinally returned",actions[minimaxValues.index(value)]
                    #raw_input()
                    return actions[minimaxValues.index(value)]
                return value
            if player!= 0:
                newdepth = depth
                if player == gameState.getNumAgents()-1:
                    newdepth = depth - 1
             #   print 'now playing ghost', player
                value = float("inf")

                for i in gameState.getLegalActions(player):
			#		print i
					temp=gameState.generateSuccessor(player,i)
			#		print temp
					successors.append(temp)

                for i in successors:
            #        print "calling minimax in depth",depth,"from player",player,"for successor",i
                    minimaxValues.append(minimax(newdepth, (player+1)%gameState.getNumAgents(), i,counter+1))
           #     print 'minimaxvalues for node',counter
          #      print minimaxValues
                value = min(value,min(minimaxValues))
         #       print value,']'
                return value
		
        #print 'finished a call'
        #raw_input()
        #print self.depth
        ndepth = (self.depth)
        rvalue = minimax(ndepth, 0, gameState, 0)
        #print rvalue
        return rvalue
        #print gameState.isWin(), gameState.isLose() 
        #a = raw_input()
        #return a
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    
        
        
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alphabeta(depth, player, gameState, a, b, counter):
            #print "caling abeta"
            if(gameState.isWin() or gameState.isLose() or depth==0):
                #print 'reached finale]',depth,self.evaluationFunction(gameState)
                return self.evaluationFunction(gameState)
            successors=list()
            abetaValues=list()
            if player == 0:
                actions= gameState.getLegalActions()
                value = - float("inf")
                #for i in actions:
                    #print i #printactions
                    #print gameState.generateSuccessor(player,i)
                    #successors.append(gameState.generateSuccessor(player,i))
                for i in actions:
                    succ = gameState.generateSuccessor(player, i)
                    #print "calling abeta in depth",depth,"from player",player,"for successor",i
                    value=max(value,alphabeta(depth  , (player+1)%gameState.getNumAgents(),succ,a,b,counter+1))
                    abetaValues.append(value)

                    if value> b:
                        #print 'a is greater or eq to b'
                        #raw_input()
                        return value
                        break
                    a = max(a, value)
                if counter == 0:

                    #print abetaValues
                    #print "to befinally returned",actions[abetaValues.index(value)]
                    return actions[abetaValues.index(value)]
                    #raw_input()
                    
                return value
            if player != 0:
                newdepth = depth
                if player == gameState.getNumAgents() - 1:
                    newdepth = depth - 1
                #print "now playing ghost"
                actions= gameState.getLegalActions(player)
                value =  float("inf")
                #for i in actions:
                    #print i #printactions
                    #print gameState.generateSuccessor(player,i)
                    #raw_input()
                    #successors.append(gameState.generateSuccessor(player,i))
                for i in actions:
                    succ = gameState.generateSuccessor(player, i)
                    #print "calling abeta in depth",depth,"from player",player,"for successor",i
                    value=min(value,alphabeta(newdepth  , (player+1)%gameState.getNumAgents(),succ,a,b,counter+1))

                    if a> value:
                        #print 'a is greater or eq to b'
                        return value
                        #raw_input()
                        break
                    b = min(b, value)

                return value
        res=alphabeta(self.depth, 0, gameState, - float("inf"), float("inf"), 0)
        #print 'final abeta res', res
        #raw_input()
        return res
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(depth , player , gameState , counter):
            #print "calling expectimax"

            if(gameState.isWin() or gameState.isLose() or depth==0):
                #print 'reached finale]',depth,self.evaluationFunction(gameState)
                rvalue = self.evaluationFunction(gameState)
                return rvalue
            successors=list()
            exmaxValues=list()
            if player ==0:

                actions= gameState.getLegalActions()
                
                
                #for i in actions:
                    #print i #printactions
                    #print gameState.generateSuccessor(player,i)
                    #successors.append(gameState.generateSuccessor(player,i))
                for i in actions:
                    succ = gameState.generateSuccessor(player,i)
                    exmaxValues.append(expectimax(depth,(player+1)%gameState.getNumAgents(), succ , counter+1))
                value=max(exmaxValues)
                if(counter == 0):
                    #print exmaxValues
                    #print "to befinally returned",actions[exmaxValues.index(value)]
                    #raw_input()
                    return actions[exmaxValues.index(value)]
                #print value,']'
                return value
            if player !=0:
                #print "now playing ghost"
                actions= gameState.getLegalActions(player)
                newdepth = depth
                if player == gameState.getNumAgents() - 1:
                    newdepth = depth - 1
                #for i in actions:
                    #print i #printactions
                    #print
                    #successors.append(gameState.generateSuccessor(player,i))
                    #raw_input()
                for i in actions:
                    succ = gameState.generateSuccessor(player,i)
                    #print "calling exmax in depth",depth,"from player",player,"for successor",i
                    exmaxValues.append(expectimax(newdepth,(player+1)%gameState.getNumAgents(), succ , counter+1))
                #print exmaxValues
                value =0
                for i in exmaxValues:
                    value =  value + i
                #print value  * 1.0/float(len(actions))
                return value * 1.0/float(len(actions))
        return expectimax(self.depth,0,gameState,0)
        util.raiseNotDefined()


def mediumOfGhostDistances(currPos, ghostPos):
    rvalue = 0.0
    for  i in ghostPos:
        rvalue = rvalue + manhattanDistance(currPos,i)
    return rvalue/len(ghostPos)


def isTooCloseToAGhost(currPos, ghostPos, range):
    for i in ghostPos:
        if euclidian(i, currPos) < range:
            return True
    return False


def noFoodNearby(currPos, foodList):
    for i in foodList:
        if euclidian(i,currPos) < 3:
            return False
    return True


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    currPos = currentGameState.getPacmanPosition()
    if (currentGameState.isWin()):
        return 999999
    if (currentGameState.isLose()):
        return -999999
    newFood = currentGameState.getFood().asList()
    foodDist = []
    for i in newFood:
        foodDist.append(manhattanDistance(i,currPos))

    ghostPos = currentGameState.getGhostPositions()
    if isTooCloseToAGhost(currPos, ghostPos, 1.1):
        return -1000
    food, dist = getClosestFoodWithList(currPos, newFood)
    return currentGameState.getScore() + (1.0 / dist)
    return  1.0/(len(newFood) + 1.0)
    foodList = currentGameState.getFood().asList()
    width, length = util.getDimensions(newFood)
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    foodPos, foodDist = getClosestFoodWithList(currPos, foodList)


# Abbreviation
better = betterEvaluationFunction

