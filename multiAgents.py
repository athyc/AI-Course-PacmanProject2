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
        print gameState
        print "legalmoves",legalMoves
        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        print "scores!!",scores
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
		
        "Add more of your code here if you want to"
        print "scores!!",scores.index(max(scores))
        print "legalmoves",legalMoves	
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
        print "1\n",successorGameState
        newPos = successorGameState.getPacmanPosition()
        print "2",newPos
        newFood = successorGameState.getFood()
        print "3",newFood
        width,length = util.getDimensions(newFood)
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
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
            
            print "[playing",player
            #print "state\n",gameState
            print "depth",depth
            print 'node',counter
            #raw_input()
            if(gameState.isWin() or gameState.isLose() or depth==0):
               print 'reached finale]',depth,gameState.isWin() , gameState.isLose(),'\n',gameState
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
        print self.depth
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
            print "caling abeta"
            if(gameState.isWin() or gameState.isLose() or depth==0):
                #print 'reached finale]',depth,self.evaluationFunction(gameState)
                return self.evaluationFunction(gameState)
            successors=list()
            abetaValues=list()
            if player == 0:
                actions= gameState.getLegalActions()
                value = - float("inf")
                for i in actions:
                    print i #printactions
                    #print gameState.generateSuccessor(player,i)
                    #successors.append(gameState.generateSuccessor(player,i))
                for i in actions:
                    succ = gameState.generateSuccessor(player, i)
                    print "calling abeta in depth",depth,"from player",player,"for successor",i
                    value=max(value,alphabeta(depth  , (player+1)%gameState.getNumAgents(),succ,a,b,counter+1))
                    abetaValues.append(value)

                    if value> b:
                        print 'a is greater or eq to b'
                        #raw_input()
                        return value
                        break
                    a = max(a, value)
                if counter == 0:

                    print abetaValues
                    print "to befinally returned",actions[abetaValues.index(value)]
                    return actions[abetaValues.index(value)]
                    #raw_input()
                    
                return value
            if player != 0:
                newdepth = depth
                if player == gameState.getNumAgents() - 1:
                    newdepth = depth - 1
                print "now playing ghost"
                actions= gameState.getLegalActions(player)
                value =  float("inf")
                #for i in actions:
                    #print i #printactions
                    #print gameState.generateSuccessor(player,i)
                    #raw_input()
                    #successors.append(gameState.generateSuccessor(player,i))
                for i in actions:
                    succ = gameState.generateSuccessor(player, i)
                    print "calling abeta in depth",depth,"from player",player,"for successor",i
                    value=min(value,alphabeta(newdepth  , (player+1)%gameState.getNumAgents(),succ,a,b,counter+1))

                    if a> value:
                        print 'a is greater or eq to b'
                        return value
                        #raw_input()
                        break
                    b = min(b, value)

                return value
        res=alphabeta(self.depth, 0, gameState, - float("inf"), float("inf"), 0)
        print 'final abeta res', res
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
            if(gameState.isWin() or gameState.isLose() or depth==0):
                #print 'reached finale]',depth,self.evaluationFunction(gameState)
                return self.evaluationFunction(gameState)
            successors=list()
            exmaxValues=list()
            if player ==0:
                actions= gameState.getLegalActions()
                
                
                for i in actions:
                    print i #printactions
                    #print gameState.generateSuccessor(player,i)
                    #successors.append(gameState.generateSuccessor(player,i))
                for i in actions:
                    succ = gameState.generateSuccessor(player,i)
                    exmaxValues.append(expectimax(depth,(player+1)%gameState.getNumAgents(), succ , counter+1))
                value=max(exmaxValues)
                if(counter == 0):
                    print exmaxValues
                    print "to befinally returned",actions[exmaxValues.index(value)]
                    #raw_input()
                    return actions[exmaxValues.index(value)]
                print value,']'
                return value
            if player !=0:
                print "now playing ghost"
                actions= gameState.getLegalActions(player)
                newdepth = depth
                if player == gameState.getNumAgents() - 1:
                    newdepth = depth - 1
                for i in actions:
                    print i #printactions
                    #print
                    #successors.append(gameState.generateSuccessor(player,i))
                    #raw_input()
                for i in actions:
                    succ = gameState.generateSuccessor(player,i)
                    print "calling exmax in depth",depth,"from player",player,"for successor",i
                    exmaxValues.append(expectimax(newdepth,(player+1)%gameState.getNumAgents(), succ , counter+1))
                print exmaxValues
                value = 0
                for i in exmaxValues:
                    value = value + i
                print value
                return value/len(exmaxValues)
        return expectimax(self.depth,0,gameState,0)
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

