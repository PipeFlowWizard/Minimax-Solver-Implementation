class Game():


    
    initialState = State()


    def ToMove(self,state):

        if state.depth % 2 == 0:
            return "max"
        else: return "min"
    
    def Actions(self,state):
        if state.numTakenTokens == 0:
            return [i for i in range(1, (state.numTokens+1)//2, 2)]
        else: 
            actions = []
            for i in state.tokens:
                if state.tokens[i] % state.lastTakenToken == 0 or state.lastTakenToken % state.tokens[i] == 0:
                    actions.append(state.tokens[i])
            return actions
                    
    
    def Result(self,state,action):
        if action in self.Actions(state):
            return state.takenToken(action)
        
    
    def IsTerminal(self,state):
        return
    

    def Utility(self,state,position):
        return
    
    

class State():

    numTokens = 0
    numTakenTokens = 0
    takenTokens = []
    depth = 0
    tokens = [1,2,3,4,5]
    lastTakenToken = None
    

    def __init__(self, numTokens, numTakenTokens, takenTokens, depth):
        self.numTokens = numTokens
        self.numTakenTokens = numTakenTokens
        self.takenTokens = takenTokens
        self.depth = depth

        for i in range(numTokens):
            tokens.append(i+1)
        

    
    def takeToken(self,value):
        if not canTakeToken(value):
            print("cannot take that token")
            return
        
        newState = State(self.numTokens,self.numTakenTokens, self.takenTokens, self.depth)

        newState.tokens.remove(value)
        newState.takenTokens.append(value)
        newState.lastTakenToken = value
        newState.depth += 1
        newState.numTokens -= 1
        newState.numTakenTokens += 1
        return newState
    




def AlphaBetaSearch():


    return action