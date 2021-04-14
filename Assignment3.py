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
        if not self.Actions(state):
            return True
        else:
            return False
    

    def Utility(self,state):
        if self.isTerminal(state):
            if self.ToMove(state) == "max": return 1.0
            if self.ToMove(state) == "min": return -1.0
        else:
            if state.numTakenTokens == 0: return 0
            if state.lastTakenToken == 1: return # count the number of the possible successors (i.e., legal moves). If the count is odd, return 0.5; otherwise, return-0.5.
            # If last move is a prime, count the multiples of that prime in all possible successors. If the count is odd, return 0.7; otherwise, return-0.7.
            # If the last move is a composite number (i.e., not prime), find the largest prime that can divide last move, count the multiples of that prime, including the prime number itself if it
            #   hasn’t already been taken, in all the possible successors. If the count is odd, return 0.6; otherwise, return-0.6.


        return
    

    def AlphaBetaSearch(self,state):
        player = self.ToMove(state)
        value, move = MaxValue(state,float('-inf'),float('inf'))
        return move

    def MaxValue(self,state,alpha,beta):
        if state.depth == 0 or self.IsTerminal(state):
            return self.Utility(state,self.ToMove(state)), None
        
        v = float('-inf')

        for action in self.Actions(state):
            v2,a2 = MinValue(self.Result(state,action),alpha,beta)
            if v2 > v:
                v, move = v2,action
                alpha = max(alpha,v)
            if v >= beta: return v, move
        return v, move

    def MinValue(self,state,alpha,beta):
        if self.IsTerminal(state): return self.Utility(state,self.ToMove(state)), None
        v = float('inf')
        for action in self.Actions(self):
            v2,a2 = MaxValue(self.Result(state,action),alpha,beta)
            if v2 < v:
                v,move = v2,action
                beta = min(beta,v)
            if v <= alpha: return v,move
        return v,move
    
    

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
        newState = State(self.numTokens,self.numTakenTokens, self.takenTokens, self.depth)

        newState.tokens.remove(value)
        newState.takenTokens.append(value)
        newState.lastTakenToken = value
        newState.depth += 1
        newState.numTokens -= 1
        newState.numTakenTokens += 1
        return newState
    


state = State(7,0)