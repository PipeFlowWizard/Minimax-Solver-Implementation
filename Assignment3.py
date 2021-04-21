class State():

    numTokens = 0
    numTakenTokens = 0
    takenTokens = []
    tokens = []
    lastTakenToken = None


    def __init__(self, numTokens, numTakenTokens, takenTokens):
        self.tokens = []
        self.numTokens = numTokens
        self.numTakenTokens = numTakenTokens
        self.takenTokens = takenTokens.copy()

        if(len(self.takenTokens) > 0):
            self.lastTakenToken = self.takenTokens[-1]
        for i in range(self.numTokens):
            self.tokens.append(i+1)
        for i in self.takenTokens:
            self.tokens.remove(i)


        
    def TakeToken(self,value):
        newNumTakenTokens = self.numTakenTokens + 1
        newTakenTokens = self.takenTokens.copy()
        newTakenTokens.append(value)
        newState = State(self.numTokens,newNumTakenTokens, newTakenTokens)
        return newState
    
    def print(self):
        print("state: " + str(self.tokens) + " || takenTokens : " + str(self.takenTokens) + " || depth : " + str(self.numTakenTokens))

    

class Game():


    initialState = None
    searchDepth = 0
    numNodesEvaluated = 0
    maxDepthReached = 0
    numNodesVisited = 0
    
    def __init__(self,state,searchDepth):
        print("Initializing Game")
        self.initialState = state
        self.searchDepth = searchDepth



    def ToMove(self,state):
        #print("Checking player turn:")
        if state.numTakenTokens % 2 == 0:
            print("Max's turn")
            return "max"
        else: 
            print("Min's turn")
            return "min"
    
    def Actions(self,state):
        print("Checking for possible actions")
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
            print()
            print("--------------------------------------------------------------------")
            print("taking token:" + str(action) + " at depth:" + str(state.numTakenTokens))
            resultState = state.TakeToken(action)
            print(str(action) + " removed from State: " + str(state.tokens))
            print("Result: ", end = '')
            resultState.print()
            print("--------------------------------------------------------------------")
            print()
            self.numNodesVisited += 1
            return resultState
        
    
    def IsTerminal(self,state):
        print("checking for terminal state:")
        if not self.Actions(state):
            print("state is terminal")
            return True
        else:
            print("state is not terminal")
            return False
    
    def IsCutOff(self,state,depth):
        if self.searchDepth == 0: 
            print("no cut off depth")
            return self.IsTerminal(state)
        elif depth > self.searchDepth or self.IsTerminal(state):
            print("state depth is greater than cutoff depth")
            return True
        else: 
            print("state depth is less than cutoff depth")
            return False


    def Utility(self,state):
        self.numNodesEvaluated += 1
        print("Determining utility of state:")
        turn = self.ToMove(state)
        utility = 0
        polarity = 1
        if self.IsTerminal(state):
            print("terminal utility")
            if turn == "max": utility = -1.0
            if turn == "min": utility = 1.0
        else:
            print("other utility")
            polarity = 1 if turn == "max" else -1
            print("polarity set")
            if 1 in state.tokens: utility = 0
            elif state.lastTakenToken == 1: 
                utility = 0.5 if len(self.Actions(state))%2 !=0 else -0.5 # count the number of the possible successors (i.e., legal moves). If the count is odd, return 0.5; otherwise, return-0.5.
            elif self.IsPrime(state.lastTakenToken): # If last move is a prime, count the multiples of that prime in all possible successors. If the count is odd, return 0.7; otherwise, return-0.7.
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
            
        print("UTILITY = " + str(polarity * utility) + " turn: " + str(turn))
        return polarity * utility
    
    def IsPrime(self,num):
        print("-Checking if: " + str(num) + " is prime-")
        if num > 1:
        # Iterate from 2 to n / 2
            for i in range(2, int(num/2)+1):
            # If num is divisible by any number between
            # 2 and n / 2, it is not prime
                if (num % i) == 0:
                    print(str(num) + " is not prime")
                    return False
                break
            else:
                print(str(num) + " is prime")
                return True
        else: 
            print(str(num) + " is not prime")
            return False

    def LargestPrime(self,n):
        #Returns all the prime factors of a positive integer
        print("-Finding largest prime factor-")
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
            
        if len(factors) >=1: 
            lp = max(factors)
            print("largest prime factor of " + str(n) + " is " + str(lp))
            return lp
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
        value, move = self.MaxValue(state,float('-inf'),float('inf'),len(state.takenTokens))
        print("Best move for player: " + str(player) + " is " + str(move))
        print("Value: " + str(value))
        print("Number of Nodes Visited: " + str(self.numNodesVisited))
        print("Number of Nodes Evaluated: " + str(self.numNodesEvaluated))
        print("Max Depth Reached: " + str(self.maxDepthReached))
        return move

    def MaxValue(self,state,alpha,beta,depth):
        if depth > self.maxDepthReached: self.maxDepthReached = depth
        print("CALCULATING MAX VALUE OF STATE: " + str(state.tokens) + " at depth " + str(state.numTakenTokens))
        print("Checking if state above cutoff | alpha: " + str(alpha) + " | beta: " + str(beta))
        if self.IsCutOff(state,depth):
            return self.Utility(state), None
        print("Searching children of state: " + str(state.tokens))
        
        v = float('-inf')

        actions = self.Actions(state)
        for action in actions:
            v2,a2 = self.MinValue(self.Result(state,action),alpha,beta,depth+1)
            if v2 > v:
                v, move = v2,action
                alpha = max(alpha,v)
            if v >= beta:
                return v, move
            
        return v, move

    def MinValue(self,state,alpha,beta,depth):
        if depth > self.maxDepthReached: self.maxDepthReached = depth
        print("CALCULATING MIN VALUE OF STATE: " + str(state.tokens) + " at depth " + str(state.numTakenTokens))
        print("Checking if state is above cutoff | alpha: " + str(alpha) + " | beta: " + str(beta))
        if self.IsCutOff(state,depth): 
            return self.Utility(state), None
        print("Searching children of state: " + str(state.tokens))
        
        v = float('inf')
        
        for action in self.Actions(state):
            v2,a2 = self.MaxValue(self.Result(state,action),alpha,beta,depth+1)
            if v2 < v:
                v,move = v2,action
                beta = min(beta,v)
            if v <= alpha:
                return v,move
        
        return v,move



state = State(7,1,[1])
game = Game(state,2)
game.AlphaBetaSearch(game.initialState)

# #Parse the string formatted state
# def parse_string(line):
#     features = line[1:].strip().split()
#     if len(features) > 3:
#         my_list = list()

#         for i in features[3:-1]:
#             my_list.append(int(i))

#         print( int(features[1]), int(features[2]), my_list, int(features[-1]) )


# #Grab all testcases from a file
# def get_testcases(filename):
#     testcases = list()
#     try:
#         with open(filename, encoding='utf-8') as f:
#             for line in f:
#                 if line.strip().startswith(keyword):
#                     testcases.append(parse_string(line))
#     except FileNotFoundError:
#         print("File does not exist!")
#         sys.exit()
#     return testcases


    
# keyword = 'TakeTokens'
# cases = get_testcases('testcase.txt')
# # cases = get_testcases('testcase_more.txt')

# # change case_num to choose the testcase
# case_num = 1
# state = cases[case_num][0]
# depth = cases[case_num][1]
