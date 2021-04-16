class State():

    numTokens = 0
    numTakenTokens = 0
    takenTokens = []
    depth = 0
    tokens = []
    lastTakenToken = 0
    parentState = None

    def __init__(self, numTokens, numTakenTokens, takenTokens, depth):
        self.numTokens = numTokens
        self.numTakenTokens = numTakenTokens
        self.takenTokens = takenTokens
        for i in self.takenTokens:
            self.TakeToken(i)
        self.depth = depth

        for i in range(self.numTokens):
            self.tokens.append(i+1)
        
    
    
    def TakeToken(self,value):
        newState = State(self.numTokens,self.numTakenTokens, self.takenTokens, self.depth)

        newState.tokens.remove(value)
        newState.takenTokens.append(value)
        newState.lastTakenToken = value
        newState.depth += 1
        newState.numTokens -= 1
        newState.numTakenTokens += 1
        newState.parentState = self
        return newState
    

class Game():


    initialState = None
    actions = []
    isTerminal = False
    
    def __init__(self,state):
        self.initialState = state
        self.actions = self.Actions(self.initialState)
        self.isTerminal = self.IsTerminal(self.initialState)


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
            print("taking token:" + str(action))
            return state.TakeToken(action)
        
    
    def IsTerminal(self,state):
        if not self.Actions(state):
            return True
        else:
            return False
    

    def Utility(self,state):
        if self.IsTerminal(state):
            if self.ToMove(state) == "max": return 1.0
            if self.ToMove(state) == "min": return -1.0
        else:
            polarity = 1 if self.ToMove(state) == "max" else -1
            utility = 0
            if 1 in state.tokens: utility = 0
            if state.lastTakenToken == 1: utility = 0.5 if len(self.Actions(state))%2 !=0 else -0.5 # count the number of the possible successors (i.e., legal moves). If the count is odd, return 0.5; otherwise, return-0.5.
            if self.IsPrime(state.lastTakenToken): # If last move is a prime, count the multiples of that prime in all possible successors. If the count is odd, return 0.7; otherwise, return-0.7.
                count = 0
                for successor in self.Successors(state):
                    #check multiples of last token in successor
                    for i in successor.tokens:
                        if i%state.lastTakenToken == 0: count += 1
                if count%2 == 0: utility = -0.7
                else: utility = 0.7 
            else: # If the last move is a composite number (i.e., not prime), find the largest prime that can divide last move
                lp = self.LargestPrime(state.lastTakenToken)
                count = 0
                # count the multiples of that prime, including the prime number itself if it hasn’t already been taken
                for successor in self.Successors(state):
                # in all the possible successors. If the count is odd, return 0.6; otherwise, return-0.6.
                    for i in successor.tokens:
                        if i%lp == 0: count += 1
                if count%2 == 0: utility = -0.6
                else: utility = 0.6 
            
        return polarity * utility
    
    def IsPrime(self,num):
        if num > 1:
        # Iterate from 2 to n / 2
            for i in range(2, int(num/2)+1):
 
        # If num is divisible by any number between
        # 2 and n / 2, it is not prime
                if (num % i) == 0:
                    return False
                break
            else:
                return True
        else: return False

    def LargestPrime(self,n):
        #Returns all the prime factors of a positive integer
        factors = []
        d = 2
        while n > 1:
            while n % d == 0:
                factors.append(d)
                n /= d
            d = d + 1
            if d*d > n:
                if n > 1: factors.append(n)
                break
            
        if len(factors) >=1: return max(factors)
        else: return 1
       
    def Successors(self,state):
        actions = self.Actions(state)
        successors = []
        for action in actions:
            successors.append(self.Result(state,action))
        return successors

    def AlphaBetaSearch(self,state):
        player = self.ToMove(state)
        value, move = self.MaxValue(state,float('-inf'),float('inf'))
        return move

    def MaxValue(self,state,alpha,beta):
        if state.depth == 0 or self.IsTerminal(state):
            return self.Utility(state), None
        
        v = float('-inf')

        for action in self.Actions(state):
            v2,a2 = self.MinValue(self.Result(state,action),alpha,beta)
            if v2 > v:
                v, move = v2,action
                alpha = max(alpha,v)
            if v >= beta: return v, move
        return v, move

    def MinValue(self,state,alpha,beta):
        if self.IsTerminal(state): return self.Utility(state), None
        v = float('inf')
        for action in self.Actions(self):
            v2,a2 = MaxValue(self.Result(state,action),alpha,beta)
            if v2 < v:
                v,move = v2,action
                beta = min(beta,v)
            if v <= alpha: return v,move
        return v,move
    
state = State(7,0,[],0)
game = Game(state)
AlphaBetaSearch(game.initialState)