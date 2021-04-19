class State():

    numTokens = 0
    numTakenTokens = 0
    takenTokens = []
    depth = 0
    tokens = []
    lastTakenToken = None
    parentState = None

    def __init__(self, numTokens, numTakenTokens, takenTokens, depth):
        self.tokens = []
        self.numTokens = numTokens
        self.numTakenTokens = numTakenTokens
        self.takenTokens = takenTokens.copy()
        self.depth = depth
        if(len(self.takenTokens) > 0):
            self.lastTakenToken = self.takenTokens[-1]
        for i in range(self.numTokens):
            self.tokens.append(i+1)
        

        for i in self.takenTokens:
            self.tokens.remove(i)

        print("state initialized: " + str(self.tokens) + " || depth : " + str(self.depth) + " || takenTokens : " + str(self.takenTokens))

        
        
    
    
    def TakeToken(self,value):
        newNumTakenTokens = self.numTakenTokens +1
        newTakenTokens = self.takenTokens.copy()
        newTakenTokens.append(value)
        newState = State(self.numTokens,newNumTakenTokens, newTakenTokens, self.depth + 1)
        newState.parentState = self
        return newState
    

class Game():


    initialState = None
    actions = []
    isTerminal = False
    
    def __init__(self,state):
        print("Initializing Game")
        self.initialState = state
        self.actions = self.Actions(state)
        self.isTerminal = self.IsTerminal(state)


    def ToMove(self,state):
        #print("Checking player turn:")
        if state.depth % 2 == 0:
            print("Max's turn")
            return "max"
        else: 
            print("Min's turn")
            return "min"
    
    def Actions(self,state):
        #print("Checking for possible actions")
        if state.numTakenTokens == 0:
            print("First move: valid actions are " + str([i for i in range(1, (state.numTokens+1)//2, 2)]))
            return [i for i in range(1, (state.numTokens+1)//2, 2)]
        else: 
            actions = []
            #print("Actions: tokens: " + str(state.tokens))
            #print("Actions: last taken token: " + str(state.lastTakenToken))
            #print("Actions: num taken tokens: " + str(state.numTakenTokens))
            for i in state.tokens:
                if i % state.lastTakenToken == 0 or state.lastTakenToken % i == 0:
                    actions.append(i)
            print("valid actions are: " + str(actions))
            return actions
                    
    

    def Result(self,state,action):
        if action in self.Actions(state):
            print("taking token:" + str(action))
            return state.TakeToken(action)
        
    
    def IsTerminal(self,state):
        #print("checking for terminal state:")
        if not self.Actions(state):
            print("state is terminal")
            return True
        else:
            print("state is not terminal")
            return False
    

    def Utility(self,state):
        #print("Determining utility of state:")
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
            
        #print("utility = " + str(polarity * utility))
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
        #print("Generating successor states")
        actions = self.Actions(state)
        successors = []
        for action in actions:
            successors.append(self.Result(state,action))
        return successors

    def AlphaBetaSearch(self,state):
        player = self.ToMove(state)
        value, move = self.MaxValue(state,float('-inf'),float('inf'))
        print("Best move for player: " + str(player) + " is " + str(move))
        return move

    def MaxValue(self,state,alpha,beta):
        #print("Calculating max value")
        if self.IsTerminal(state):
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
        #print("Calculating min value")
        if self.IsTerminal(state): return self.Utility(state), None
        v = float('inf')
        for action in self.Actions(state):
            v2,a2 = self.MaxValue(self.Result(state,action),alpha,beta)
            if v2 < v:
                v,move = v2,action
                beta = min(beta,v)
            if v <= alpha: return v,move
        return v,move
    
state = State(8,3,[3,1,2],0)

game = Game(state)
game.AlphaBetaSearch(game.initialState)

keyword = 'TakeTokens'


# Parse the string formatted state
def parse_string(line):
    features = line[1:].strip().split()
    if len(features) > 3:
        my_list = list()

        for i in features[3:-1]:
            my_list.append(int(i))

        print( int(features[1]), int(features[2]), my_list, int(features[-1]) )


#Grab all testcases from a file
def get_testcases(filename):
    testcases = list()
    try:
        with open(filename, encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith(keyword):
                    testcases.append(parse_string(line))
    except FileNotFoundError:
        print("File does not exist!")
        sys.exit()
    return testcases