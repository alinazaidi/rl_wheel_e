import numpy as np

def randPair(s,e):
    return np.random.randint(s,e), np.random.randint(s,e)

#finds an array in the "depth" dimension of the grid
def findLoc(state, obj):
    for i in range(0,4):
        for j in range(0,4):
            if (state[i,j] == obj).all():
                return i,j

#Initialize stationary grid, all items are placed deterministically
def initGrid():
    state = np.zeros((4,4,4))
    #place player
    state[2,0] = np.array([0,0,0,1])
    #place pit
    state[0,0] = np.array([0,1,0,0])
    state[0,1] = np.array([0,1,0,0])
    state[1,0] = np.array([0,1,0,0])
    state[2,2] = np.array([0,1,0,0])
    state[3,0] = np.array([0,1,0,0])
    state[3,1] = np.array([0,1,0,0])
    state[3,2] = np.array([0,1,0,0])
    #place goal
    state[0,2] = np.array([1,0,0,0])
    return state

def makeMove(state, action):
##    print(dispGrid(state))
    #need to locate player in grid
    #need to determine what object (if any) is in the new grid spot the player is moving to
    player_loc = findLoc(state, np.array([0,0,0,1]))
    goal = findLoc(state, np.array([1,0,0,0]))
##    pit = findLoc(state, np.array([0,1,0,0]))
    pits = getLocPits(state,1)
##    print(pit)
    state = np.zeros((4,4,4))

    actions = [[-1,0],[1,0],[0,-1],[0,1]]
    #e.g. up => (player row - 1, player column + 0)
##    print(player_loc)
##    print(actions[action][0])

    new_loc = (player_loc[0] + actions[action][0], player_loc[1] + actions[action][1])

    if ((np.array(new_loc) <= (3,3)).all() and (np.array(new_loc) >= (0,0)).all()):
        state[new_loc][3] = 1

    new_player_loc = findLoc(state, np.array([0,0,0,1]))
    if (not new_player_loc):
        state[player_loc] = np.array([0,0,0,1])
    #re-place pit
    for p in pits:
        state[p][1] = 1
    #re-place goal
    state[goal][0] = 1
    return state

def getLoc(state, level):
    for i in range(0,4):
        for j in range(0,4):
            if (state[i,j][level] == 1):
                return i,j
def getLocPits(state, level):
    a =[]
    for i in range(0,4):
        for j in range(0,4):
            if (state[i,j][level] == 1):
                b=(i,j)
                a.append(b)
    return a

def getReward(state):
    player_loc = getLoc(state, 3)
    pits = getLocPits(state, 1)
    goal = getLoc(state, 0)
    a= 0 
    for p in pits:
        if (player_loc == p):
            a = 1
    if (a == 1):
        return -10 
    elif (player_loc == goal):
        return 10
    else:
        return -1
    
def dispGrid(state):
    grid = np.zeros((4,4), dtype=np.str)
    player_loc = findLoc(state, np.array([0,0,0,1]))
    goal = findLoc(state, np.array([1,0,0,0]))
    
    for i in range(0,4):
        for j in range(0,4):
            grid[i,j] = ' '
            
    if player_loc:
        grid[player_loc] = 'P' #player where no overlap
    if goal:
        grid[goal] = '+' #goal where no overlap

    for i in range(0,4):
        for j in range(0,4):
            if (state[i,j] == np.array([0,1,0,0])).all():
                grid[i,j] = '-' #pit where no overlap
    
    return grid

##state = initGrid()

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop
model = Sequential()
model.add(Dense(164, init='lecun_uniform', input_shape=(64,)))
model.add(Activation('relu'))
#model.add(Dropout(0.2)) I'm not using dropout, but maybe you wanna give it a try?

model.add(Dense(150, init='lecun_uniform'))
model.add(Activation('relu'))
#model.add(Dropout(0.2))

model.add(Dense(4, init='lecun_uniform'))
model.add(Activation('linear')) #linear output so we can have range of real-valued outputs

rms = RMSprop()
model.compile(loss='mse', optimizer=rms)

##model.predict(state.reshape(1,64), batch_size=1)
#just to show an example output; read outputs left to right: up/down/left/right

from IPython.display import clear_output
import random

epochs = 500
gamma = 0.9 #since it may take several moves to goal, making gamma high
epsilon = 1
for i in range(epochs):
    
    state = initGrid()
    status = 1
    #while game still in progress
    while(status == 1):
        print("Restart")
        #We are in state S
        #Let's run our Q function on S to get Q values for all possible actions
        qval = model.predict(state.reshape(1,64), batch_size=1)
        if (random.random() < epsilon): #choose random action
            action = np.random.randint(0,4)
        else: #choose best action from Q(s,a) values
            action = (np.argmax(qval))
        print(action)
        #Take action, observe new state S'
        new_state = makeMove(state, action)
        #Observe reward
        reward = getReward(new_state)
        #Get max_Q(S',a)
        newQ = model.predict(new_state.reshape(1,64), batch_size=1)
        maxQ = np.max(newQ)
        y = np.zeros((1,4))
        y[:] = qval[:]
        if reward == -1: #non-terminal state
            print("Normal")
            update = (reward + (gamma * maxQ))
        else: #terminal state
            update = reward
            print("TerminalState")
        y[0][action] = update #target output
        print("Game #: %s" % (i,))
        model.fit(state.reshape(1,64), y, batch_size=1, nb_epoch=1, verbose=1)
        state = new_state
        if reward != -1:
            status = 0
        clear_output(wait=True)
    if epsilon > 0.1:
        epsilon -= (1/epochs)

def testAlgo(init=0):
    i = 0
    if init==0:
        state = initGrid()
    elif init==1:
        state = initGridPlayer()
    elif init==2:
        state = initGridRand()
        
    print("Initial State:")
    print(dispGrid(state))
    status = 1
    #while game still in progress
    while(status == 1):
        qval = model.predict(state.reshape(1,64), batch_size=1)
        action = (np.argmax(qval)) #take action with highest Q-value
        print('Move #: %s; Taking action: %s' % (i, action))
        state = makeMove(state, action)
        print(dispGrid(state))
        reward = getReward(state)
        if reward != -1:
            status = 0
            print("Reward: %s" % (reward,))
        i += 1 #If we're taking more than 10 actions, just stop, we probably can't win this game
        if (i > 10):
            print("Game lost; too many moves.")
            break
testAlgo(init=0)
##testAlgo(init=0)
##testAlgo(init=0)
##testAlgo(init=0)
##testAlgo(init=0)
##testAlgo(init=0)
