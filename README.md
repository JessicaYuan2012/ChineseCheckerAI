# ChineseCheckerAI
CS221 Autumn 2016 project by Yang Yuan and Jiafu Wu.<br>
An AI agent to play Chinese Checkers in python 2.7.

## Code Organization
* runGame.py<br>
  Main entrance for the project. Simulation of several Chinese Checkers games
   with results and statistics output. See Usage Section for more details.
* board.py<br>
  Definition of a simplified board for Chinese Checkers.
* game.py<br>
  Definition of the MDP for Chinese Checkers.
* agent.py<br>
  Several agent classes, including HumanAgent, SimpleGreedyAgent, RandomAgent,
  MiniMaxAgent and MiniMaxAlphaBetaAgent.
* features.py<br>
  Different feature extraction function given a state in game.
* learning.py<br>
  TD-learning Algorithm and corresponding auxiliary functions.

## Usage
In runGame.py, there're examples of usage of this program.
Basically, you should choose 2 agents to play against each other.<br>
`1.` Instantiate a game.
```python
ccgame = SimplifiedChineseChecker(5, 3)
```
`2.` Get your agents.
```python
# 0. human agent
humanAgent = HumanAgent(ccgame)
# 1. baseline - simple greedy agent
simpleGreedyAgent = SimpleGreedyAgent(ccgame)
# 2. minimax agent with naive evaluation function
minimaxAgent = MiniMaxAlphaBetaAgent(ccgame, depth=2)
```
For TD learning agents, you can provide a dictionary object of
feature extraction functions and their weights directly, get the evaluation function
using the dictionary and then create a minimax agent using the evaluation function.
```python
feature_weight_dict1 = {diffOfAvgSquaredVerDistToGoalVertex: 0.00328899184996,
                            diffOfAvgVerDistToGoalVertex: 0.0238213005841}
evalFunction1 = getEvalFunctionGivenWeights(feature_weight_dict1)
tdAgent1 = MiniMaxAlphaBetaAgent(ccgame, depth=2, evalFunction=evalFunction1)
```
Or you can use a list of feature extraction functions, and get the weights via training process.
```python
featureFuctionList1 = [diffOfAvgVerDistToGoalVertex, diffOfAvgSquaredVerDistToGoalVertex]
featureExtractor1 = getFeatureExtractor(featureFuctionList1)
evalFunction1 = getEvalFunctionViaTDlearning(ccgame, featureExtractor1, num_trials=1000)
tdAgent1 = MiniMaxAlphaBetaAgent(ccgame, depth=2, evalFunction=evalFunction1)
```
`3.` Let your agents play against each other, and see the results and statistics output to the console.
Note that player 1 goes first as the agent, player 2 is the opponent.
```python
simulateMultipleGames({1: minimaxAgent, 2: tdAgent1}, 50, ccgame)
```