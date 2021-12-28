import random
import copy
import numpy as np
import time

# def print_successors(succs):
#     for successor in succs:
#         for row in successor:
#             print(row)
#             print()


class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
   

    def succ(self, state, piece):
        #two cases 
        succ = []
        self.game_value(state)
        
        drop_phase = True   # TODO: detect drop phase
        rCounter = 0
        bCounter = 0
        for i in range(len(state)):
            for j in range(len(state)):
                if(state[i][j] == 'b'):
                    bCounter += 1
                if(state[i][j] == 'r'):
                    rCounter += 1
                if(bCounter == 4 and rCounter == 4):
                    drop_phase = False
        if(drop_phase):
            for i in range(len(state)):
                for j in range(len(state)):
                    if (state[i][j] == ' '):
                        deep_copy = copy.deepcopy(state)
                        deep_copy[i][j] = piece
                        succ.append(deep_copy)

            return list(filter(None, succ))


                    
        for i in range(len(state)):
            for j in range(len(state)):
                if (state[i][j] == piece):
                    succ.insert(0, self.move_up(state,i,j))
                    succ.insert(1, self.move_down(state,i,j))
                    succ.insert(2, self.move_left(state,i,j))
                    succ.insert(3, self.move_right(state,i,j))
                    succ.insert(4, self.move_leftup(state,i,j))
                    succ.insert(5, self.move_rightup(state,i,j))
                    succ.insert(6, self.move_leftdown(state,i,j))
                    succ.insert(7, self.move_rightdown(state,i,j))
        
       
        return list(filter(None, succ))

    def move_up(self,state, i, j):
        temp_state = copy.deepcopy(state)
        if i-1 >= 0 and temp_state[i-1][j] == ' ':
            temp_state[i][j], temp_state[i-1][j] = temp_state[i-1][j], temp_state[i][j]
        return temp_state
    def move_down(self,state, i, j):
        temp_state = copy.deepcopy(state)
        if i+1 < 5 and temp_state[i+1][j] == ' ':
            temp_state[i][j], temp_state[i+1][j] = temp_state[i+1][j], temp_state[i][j]
        return temp_state
    def move_left(self,state, i, j):
        temp_state = copy.deepcopy(state)
        if j-1 >= 0 and temp_state[i][j-1] == ' ':
            temp_state[i][j], temp_state[i][j-1] = temp_state[i][j-1], temp_state[i][j]
        return temp_state
    def move_right(self,state, i, j):
        temp_state = copy.deepcopy(state)
        if j+1 < len(state) and temp_state[i][j+1] == ' ':
            temp_state[i][j], temp_state[i][j+1] = temp_state[i][j+1], temp_state[i][j]
        return temp_state
    def move_leftup(self,state, i, j):
        temp_state = copy.deepcopy(state)
        if i-1 >= 0 and j-1 >=0 and temp_state[i-1][j-1] == ' ':
            temp_state[i][j], temp_state[i-1][j-1] = temp_state[i-1][j-1], temp_state[i][j]
        return temp_state
    def move_rightup(self,state, i, j):
        temp_state = copy.deepcopy(state)
        if i-1 >= 0 and j+1 < len(state) and temp_state[i-1][j+1] == ' ':
            temp_state[i][j], temp_state[i-1][j+1] = temp_state[i-1][j+1], temp_state[i][j]
        return temp_state
    def move_leftdown(self,state, i, j):
        temp_state = copy.deepcopy(state)
        if i+1 < len(state)  and j-1 >= 0 and temp_state[i+1][j-1] == ' ':
            temp_state[i][j], temp_state[i+1][j-1] = temp_state[i+1][j-1], temp_state[i][j]
        return temp_state
    def move_rightdown(self,state, i, j):
        temp_state = copy.deepcopy(state)
        if i+1 < len(state)  and j+1 < 5 and temp_state[i+1][j+1] == ' ':
            temp_state[i][j], temp_state[i+1][j+1] = temp_state[i+1][j+1], temp_state[i][j]
        return temp_state
    def get_location(self, state):
        blt = []
        rlt = []
        for i in range(5):
            for j in range(5):
                if state[i][j] == 'b':
                    blt.append((i,j))
                elif state[i][j] == 'r':
                    rlt.append((i,j))
        return blt,rlt

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
      
        
        #during drop phase just means adding another piece
        drop_phase = True   # TODO: detect drop phase
        rCounter = 0
        bCounter = 0
        for i in range(5):
            for j in range(5):
                if(state[i][j] == 'b'):
                    bCounter += 1
                if(state[i][j] == 'r'):
                    rCounter += 1
                if(bCounter == 4 and rCounter == 4):
                    drop_phase = False
               
        
        if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            move = []
            val, beta_state = self.max_value(state,0)
            orig = np.array(state) == np.array(beta_state)
            diff = np.where(orig ==False)
        

            if state[diff[0][0]][diff[1][0]] == ' ':
                (row,col) = (diff[0][1],diff[1][1])
                (i,j) = (diff[0][0], diff[1][0])
            else:
                (row,col) = (diff[0][0],diff[1][0])
                (i,j) = (diff[0][1], diff[1][1])
            move.insert(0,(i,j))
            move.insert(1,(row,col))
            return move
        
            
           

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better

        move = []
        val, beta_state = self.max_value(state,0)
        orig = np.array(state) == np.array(beta_state)
        diff = np.where(orig ==False)
        (i,j) = (diff[0][0],diff[1][0])
        while not state[i][j] == ' ':
            (i,j) = (diff[0][0],diff[1][0])
        move.insert(0,(i,j))

        # (row, col) = (random.randint(0,4), random.randint(0,4))
        # while not state[row][col] == ' ':
        #     (row, col) = (random.randint(0,4), random.randint(0,4))

        # ensure the destination (row,col) tuple is at the beginning of the move list
        # move.insert(0, (row, col))
        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and 3x3 square corners wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        for i in range(2):
            for j in range(2):
                    if state[i][j] != ' ' and state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
                        return 1 if state[i][col]==self.my_piece else -1

        # TODO: check / diagonal wins
        for i in range(3,5):
            for j in range(2):
                    if state[i][j] != ' ' and state[i][j] == state[i-1][j+1] == state[i-2][j+2] == state[i-3][j+3]:
                        return 1 if state[i][j]==self.my_piece else -1
        # TODO: check 3x3 square corners wins
        # x 0-3 y 0-3
        for i in range(3):
            for j in range(3):
                    if state[i][j] != ' ' and state[i+1][j+1]== ' ' and state[i][j] == state[i][j+2] == state[i+2][j] == state[i+2][j+2]:
                        return 1 if state[i][j]==self.my_piece else -1


        return 0 # no winner yet
    def heuristic_game_value(self, state, piece):

        # game_val = self.game_value(self, state, self.my_piece)
        b,r = self.get_location(state)
        # if game_val == 1:
        #     print("Terminal State")
        #     return 1

        if piece == 'b':
            player = 'b'
            ai = 'r'
        elif piece == 'r':
            player = 'r'
            ai = 'b'

        pmax = 0
        aimax = 0
        pcnt = 0
        aicnt = 0
        #row 
        for i in range(len(state)):
            for j in range(len(state)):
                if state[i][j] == player:
                    pcnt += 1
            if pcnt > pmax:
                pmax = pcnt
            pcnt = 0
    
        for i in range(len(state)):
            for j in range(len(state)):
                if state[i][j] == ai:
                    aicnt += 1
            if aicnt > aimax:
                aimax = aicnt
            aicnt = 0
        #col
        for i in range(len(state)):
            for j in range(len(state)):
                if state[j][i] == player:
                    pcnt += 1
            if pcnt > pmax:
                pmax = pcnt
            pcnt = 0
        
        for i in range(len(state)):
            for j in range(len(state)):
                if state[j][i] == ai:
                    aicnt += 1
            if aicnt > aimax:
                aimax = aicnt
            aicnt = 0

  
        pcnt = 0
        aicnt = 0
        #/
        for i in range(3, 5):
            for j in range(2):
                if state[i][j] == player:
                    pcnt += 1
                if state[i - 1][j + 1] == player:
                    pcnt += 1
                if state[i - 2][j + 2] == player:
                    pcnt += 1
                if state[i - 3][j + 3] == player:
                    pcnt += 1
                if pcnt > pmax:
                    pmax = pcnt
                pcnt = 0
        row = 0
        
        for i in range(3, 5):
            for j in range(2):
                if state[i][j] == ai:
                    aicnt += 1
                if state[i - 1][j + 1] == ai:
                    aicnt += 1
                if state[i - 2][j + 2] == ai:
                    aicnt += 1
                if state[i - 3][j + 3] == ai:
                    aicnt += 1
                if aicnt > aimax:
                    aimax = aicnt
                aicnt = 0
 

        pcnt = 0
        aicnt = 0
        row = 0
        #\
        for i in range(2):
            for j in range(2):
                if state[i][j] == player:
                    pcnt += 1
                if state[i + 1][j + 1] == player:
                    pcnt += 1
                if state[i + 2][j + 2] == player:
                    pcnt += 1
                if state[i+ 3][j + 3] == player:
                    pcnt += 1
                if pcnt > pmax:
                    pmax = pcnt
                pcnt = 0
        for i in range(2):
            for j in range(2):
                if state[i][j] == ai:
                    pcnt += 1
                if state[i + 1][j + 1] == ai:
                    pcnt += 1
                if state[i + 2][j + 2] == ai:
                    pcnt += 1
                if state[i+ 3][j + 3] == ai:
                    pcnt += 1
                if aicnt > aimax:
                    aimax = aicnt
                pcnt = 0

        #3x3
        pcnt = 0
        aicnt = 0

        for i in range(3):
            for j in range(3):
                if state[i][j] == player:
                    pcnt += 1
                if state[i][j + 2] == player:
                    pcnt += 1
                if state[i + 2][j] == player:
                    pcnt += 1
                if state[i+ 2][j + 2] == player:
                    pcnt += 1
                if state[i+1][j+1] == ai:
                    pcnt += 0  
                if pcnt > pmax:
                    pmax = pcnt
                pcnt = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] == ai:
                    pcnt += 1
                if state[i][j + 2] == ai:
                    pcnt += 1
                if state[i + 2][j] == ai:
                    pcnt += 1
                if state[i+ 2][j + 2] == ai:
                    pcnt += 1
                if state[i+1][j+1] == player:
                    pcnt += 0  
                if pcnt > pmax:
                    pmax = pcnt
                pcnt = 0

        if pmax == aimax:
            return 0,state
        if aimax >= pmax:
            return (-1) * aimax/6,state
        return pmax/6,state

    #SLIDE 40
    def max_value(self, state, depth):
        beta_state = state

        if self.game_value(state) !=0:
            return self.game_value(state),state
        if depth >= 3:
            return self.heuristic_game_value(state,self.my_piece)
        else:
            alpha = float('-Inf')
            for s in self.succ(state, self.my_piece):
                score = self.min_value(s, depth + 1)
                if score[0] > alpha:    #MAX OF MIN
                    alpha = score[0]
                    beta_state = s
        return alpha,beta_state
   
   
    def min_value(self, state, depth):
        beta_state = state

        if self.game_value(state) !=0:
            return self.game_value(state),state
        if depth >= 3:
           return self.heuristic_game_value(state,self.opp)
        else:
            beta = float('Inf')
            for s in self.succ(state, self.opp):
                score = self.max_value(s, depth + 1)
                if score[0] < beta:     #MIN OF MAX
                    beta = score[0]
                    beta_state = s
        return beta,beta_state
    
   
############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
