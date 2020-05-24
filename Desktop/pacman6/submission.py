from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):

    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions()
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) 
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
	newPos = successorGameState.getPacmanPosition()
	currentpos= currentGameState.getPacmanPosition()
	newFood = successorGameState.getFood()
	newGhostStates = successorGameState.getGhostStates()
	newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
	score=successorGameState.getScore()
	foodArray=newFood.asList()
	for i in foodArray:
		foodDist = util.manhattanDistance(i,newPos)
		if (foodDist)!=0:
        		score=score+(1.0/foodDist)
	for ghost in newGhostStates:
		ghostpos=ghost.getPosition()
		ghostDist = util.manhattanDistance(ghostpos,newPos)
		if (abs(newPos[0]-ghostpos[0])+abs(newPos[1]-ghostpos[1]))>1:	
			score=score+(1.0/ghostDist)
		
	
	return score

def scoreEvaluationFunction(currentGameState):
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    
    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '4'):
        self.index = 0 
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
	self.action1 = Directions.STOP
	self.value_max = -99999
	self.value_min = 99999
	self.value_avg = 99999

class MinimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
	num_of_agents = gameState.getNumAgents()
	depth1 = self.depth * num_of_agents	

	self.getAction1(gameState,depth1,num_of_agents)
	return self.action1		
	util.raiseNotDefined()

    def maxvalue(self ,state, agentIndex, currentdepth):
      v = (float("-inf"), "Stop")
      for action in state.getLegalActions(agentIndex):
        v = max([v, (self.value(state.generateSuccessor(agentIndex, action), \
          (currentdepth+1) % self.number_of_agents, currentdepth+1), action)], key=lambda item:item[0])
      return v

    def minvalue(self, state, agentIndex, currentdepth):
      v = (float("inf"), "Stop")
      for action in state.getLegalActions(agentIndex):
        v = min([v, (self.value(state.generateSuccessor(agentIndex, action), \
          (currentdepth+1) % self.number_of_agents, currentdepth+1), action)], key=lambda item:item[0])
      return v
    def value(self, state, agentIndex, currentdepth):
      if state.isLose() or state.isWin() or currentdepth >= self.depth*self.number_of_agents:
        return self.evaluationFunction(state)
      if (agentIndex == 0):
        return self.maxvalue(state, agentIndex, currentdepth)[0]  
      else:
        return self.minvalue(state, agentIndex, currentdepth)[0]
    
    def getAction1(self,gameState,depth1,num_of_agents):
	maxvalues = list()
	minvalues = list()
	if gameState.isWin() or gameState.isLose():
		return self.evaluationFunction(gameState)
			
	if depth1 > 0:
		if depth1%num_of_agents ==0:
			agentNumber = 0
				
		else: 
			agentNumber = num_of_agents-(depth1%num_of_agents)
		
		actions = gameState.getLegalActions(agentNumber)
		for action in actions:
			successorGameState = gameState.generateSuccessor(agentNumber,action)
			 
			if agentNumber == 0: 
				maxvalues.append((self.getAction1(successorGameState,depth1-1,num_of_agents), action))			
				maximum = max(maxvalues) 
				self.value_max = maximum[0]
				self.action1=maximum[1]				
				
			else:	
				minvalues.append((self.getAction1(successorGameState,depth1-1,num_of_agents), action))			
				minimum = min(minvalues)
				self.value_min = minimum[0]
			
		if agentNumber == 0:
			return self.value_max
		else:
			return self.value_min
	
	else:
		return self.evaluationFunction(gameState) 

