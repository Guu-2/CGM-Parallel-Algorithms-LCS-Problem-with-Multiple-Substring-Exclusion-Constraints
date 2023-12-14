# Python program for implementation of
# Aho-Corasick algorithm for string matching

# defaultdict is used only for storing the final output
# We will return a dictionary where key is the matched word
# and value is the list of indexes of matched word
from collections import defaultdict

# For simplicity, Arrays and Queues have been implemented using lists. 
# If you want to improve performance try using them instead
class AhoCorasick:
    def __init__(self, words):

        # Max number of states in the matching machine.
        # Should be equal to the sum of the length of all keywords.
        self.max_states = sum([len(word) for word in words])

        # Maximum number of characters.
        # Currently supports only alphabets [a,z]
        self.max_characters = 26

        # OUTPUT FUNCTION IS IMPLEMENTED USING out []
        # Bit i in this mask is 1 if the word with
        # index i appears when the machine enters this state.
        # Lets say, a state outputs two words "he" and "she" and
        # in our provided words list, he has index 0 and she has index 3
        # so value of out[state] for this state will be 1001
        # It has been initialized to all 0.
        # We have taken one extra state for the root.
        self.out = [0]*(self.max_states+1)

        # FAILURE FUNCTION IS IMPLEMENTED USING fail []
        # There is one value for each state + 1 for the root
        # It has been initialized to all -1
        # This will contain the fail state value for each state
        self.fail = [-1]*(self.max_states+1)

        # GOTO FUNCTION (OR TRIE) IS IMPLEMENTED USING goto [[]]
        # Number of rows = max_states + 1
        # Number of columns = max_characters i.e 26 in our case
        # It has been initialized to all -1.
        self.goto = [[-1]*self.max_characters for _ in range(self.max_states+1)]

        # Convert all words to lowercase
        # so that our search is case insensitive
        for i in range(len(words)):
            words[i] = words[i].lower()

        # All the words in dictionary which will be used to create Trie
        # The index of each keyword is important:
        # "out[state] & (1 << i)" is > 0 if we just found word[i]
        # in the text.
        self.words = words

        # Once the Trie has been built, it will contain the number
        # of nodes in Trie which is total number of states required <= max_states
        self.states_count = self.__build_matching_machine()


	# Builds the String matching machine.
	# Returns the number of states that the built machine has.
    # States are numbered 0 up to the return value - 1, inclusive.
    def __build_matching_machine(self):
        k = len(self.words)

        # Initially, we just have the 0 state
        states = 1

        # Convalues for goto function, i.e., fill goto
        # This is same as building a Trie for words[]
        for i in range(k):
            word = self.words[i]
            current_state = 0

            # Process all the characters of the current word
            for character in word:
                ch = ord(character) - 97 # Ascii value of 'a' = 97

                # Allocate a new node (create a new state)
                # if a node for ch doesn't exist.
                if self.goto[current_state][ch] == -1:
                    self.goto[current_state][ch] = states
                    states += 1

                current_state = self.goto[current_state][ch]

            # Add current word in output function
            self.out[current_state] |= (1<<i)

        # For all characters which don't have
        # an edge from root (or state 0) in Trie,
        # add a goto edge to state 0 itself
        for ch in range(self.max_characters):
            if self.goto[0][ch] == -1:
                self.goto[0][ch] = 0
        
        # Failure function is computed in 
        # breadth first order using a queue
        queue = []

        # Iterate over every possible input
        for ch in range(self.max_characters):

            # All nodes of depth 1 have failure
            # function value as 0. For example,
            # in above diagram we move to 0
            
            if self.goto[0][ch] != 0:
                self.fail[self.goto[0][ch]] = 0
                queue.append(self.goto[0][ch])

        # Now queue has states 1 and 3
        while queue:
            # Remove the front state from queue
            state = queue.pop(0)
            # For the removed state, find failure
            # function for all those characters
            # for which goto function is not defined.
            for ch in range(self.max_characters):
                # If goto function is defined for
                # character 'ch' and 'state'
                if self.goto[state][ch] != -1:
                    # Find failure state of removed state
                    failure = self.fail[state]
                    # Find the deepest node labeled by proper
                    # suffix of String from root to current state.
                    while self.goto[failure][ch] == -1:
                        failure = self.fail[failure]
                    failure = self.goto[failure][ch]
                    self.fail[self.goto[state][ch]] = failure
                    # Merge output values
                    self.out[self.goto[state][ch]] |= self.out[failure]
                    # Insert the next level node (of Trie) in Queue
                    queue.append(self.goto[state][ch])
        
        return states




# dynamic programming algorithm to solve LCS With expluding constraint
def M_STR_EC_LCS(X, Y, P):
    n = len(X)
    m = len(Y)
    # t = len(P) 
    T = AhoCorasick(P)
    t = T.states_count
    print(t)
    # Khởi tạo ma trận f(i, j, k)
    f = [[[-1] * (t) for _ in range(m)] for _ in range(n)]
    # f = [[[0] * (t) for _ in range(m)] for _ in range(n)]
    # Gán giá trị f(i, 0, 0) và f(0, j, 0) bằng 0
    for i in range(n):
        f[i][0][0] = 0
    for j in range(m):
        f[0][j][0] = 0
        
    S = {0}  # Tập hợp các trạng thái


    print(f)
    # Tính toán giá trị f(i, j, k) cho tất cả các i, j, k
    for i in range(n):
        for j in range(m):
            # print('\nindex row: ' + str(i) + ' column : ' + str(j) );
            for k in S:
                if X[i] != Y[j]:
                    f[i][j][k] = max(f[i - 1][j][k], f[i][j - 1][k])
                    # print(f[i][j][k])
                else:
                    ch = ord(X[i].lower()) - 97
                    next_k = T.goto[k][ch] #same for X[i] , Y[i] 

                    out_k = T.out[next_k]
                    print("ouput : " + str(out_k))
                    # k = T[k].get(X[i - 1], 0)
                    if int(out_k) == 0:
                        f[i][j][next_k] = max(f[i - 1][j - 1][next_k], 1 + f[i - 1][j - 1][k])
                        # print(f[i][j][next_k])
                        # print(f[n-1][m-1][next_k])
                        S = S | {next_k}

    # # Tìm giá trị lớn nhất của f(n, m, k)
    print(f)
    print(S)
    # # print(LCS)
    # for k in range(t ):
    #     print(f[n][m][k])

    max_length = max(f[n -1 ][m -1][k] for k in range(t))
    return max_length

# running program
if __name__ == '__main__':
    # Example usage
    # X = "ACEGNK"
    # Y = "ABCMNO"
    # P = ["GT" , "ABC" , "LOP" , "AD"]
    # X = "ABCT"
    # Y = "ABCD"
    # P = ["GT" , "ABC" ]
    X = "ABCQWETX"
    Y = "ABCTXYOM"
    P = ["GT" , "ABCTX"]
    lcs_length = M_STR_EC_LCS(X, Y, P)
    print("Length of LCS excluding P:", lcs_length)