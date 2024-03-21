import pygame
import time
from reusable import LabeledRect
import numpy as np
import copy
  
pygame.init()
#define constants

RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
WHITE=(255,255,255)
BLACK=(0,0,0)
GAME_ICON=None

# game settings
HEIGHT_FRAME,WIDTH_FRAME=400,600
HEIGHT_GAME,WIDTH_GAME=400,400
ROWS,COLS=3, 3
SQUARE_WIDTH=(WIDTH_GAME-50)//3 
SQUARE_HEIGHT=(HEIGHT_GAME-50)//3 
GAP=7
FONT_size=60
FONT = pygame.font.Font(None,FONT_size )

DEFAULT_GRID=[['' for _ in range(COLS)] for _ in range(ROWS)]

#game logic : 

class TicTacToe:
    def __init__(self,grid=DEFAULT_GRID):
    
        self.grid=grid
        self.rects=[[None for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player='X'
        self.game_over=False
        self.lastMove=None
        
    def alternate_player(self):
        
        self.current_player = 'O' if self.current_player=='X' else 'X'

    def handleClick(self,x_clicked,y_clicked):
        for i in range(ROWS):
            for j in range(COLS):
                if  self.rects[i][j].collidepoint(x_clicked,y_clicked):
                    x,y=self.rects[i][j].label
                    self.lastMove=(x,y)
                    self.grid[i][j]=self.current_player
                    print(f'current_player {self.current_player} square:{(i,j)}')
                    self.alternate_player()
                    
    def check_win(self):
        
        for i in range(3):
            # check_row
            if self.grid[i][0]==self.grid[i][1]==self.grid[i][2] !='':
                    self.game_over=True
                    return True
                
            for j in range(3):
                # check column
                if self.grid[0][j]==self.grid[1][j]==self.grid[2][j]!='':
                    self.game_over=True
                    return True
                
         #check first diag
        if  self.grid[0][0]==self.grid[1][1]==self.grid[2][2]!='':
            self.game_over=True
            return True
        #check second diag
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] !='':
            self.game_over=True
            return True
        return False      
    def check_winner(self, board):
        # Check rows for a winner
        for row in board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]

        # Check columns for a winner
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != ' ':
                return board[0][col]

        # Check diagonals for a winner
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            return board[0][2]

        # No winner found
        return None
    def check_tie(self):
        if '' not in np.array(self.grid).reshape(-1,1).flatten() and not self.check_win():
            return True
        return False
    def draw_game(self,surface):
        top=15
        
        
        for i in range(ROWS):
            # in a new row reinitialize left coordinates to the start
            left=15
            for j in range(COLS):
                rect =  LabeledRect((left, top), (SQUARE_WIDTH, SQUARE_HEIGHT), label=(i,j))
                #store the rect reference
                self.rects[i][j]=rect
                #draw the rect into the surface 
                pygame.draw.rect(surface,WHITE,rect)
                current_player=self.grid[i][j]
                
                symbol_surface= FONT.render(current_player, True, BLACK)
                # draw into the rect the symbol
                  #coordinates of the center (where the symbol will be drawn)
                center_x=left + (SQUARE_WIDTH - symbol_surface.get_width()) // 2
                center_y=top + (SQUARE_HEIGHT - symbol_surface.get_height()) // 2
                surface.blit(symbol_surface, (center_x,center_y))
                # increment coordinates
                left+=SQUARE_WIDTH+GAP
                
            top +=SQUARE_HEIGHT+GAP
           
    def reset(self):
        self.grid=[['' for _ in range(COLS)] for _ in range(ROWS)]
        self.rects=[[None for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player='X'
        self.game_over=False      
    def make_move(self, move):
        # Assume move is a tuple (row, col)
        row, col = move
        # Update the grid with the current player's symbol
        self.grid[row][col] = self.current_player
        # Switch the current player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
#ia logic :

# to encapsulate the game logic
class node:
    def __init__(self, tictacto,move,player): 
        #  3X3 grid that contains the game state after the move
        self.tictactoe=tictacto
        self.board=copy.deepcopy(tictacto.grid)
        # accepts a tuple(x,y) to define the move that lead to this state
        self.value=None
        self.move=move
        # the player that made the move resulting in this gameState
        # self.player=self.tictactoe.player
        self.player=player
    def check_tie(self):
        return self.tictactoe.check_tie()
    def check_win(self,player):
        #retyrn the player  that won
        return self.tictactoe.current_player == player  and self.tictactoe.check_win()
    def isTerminal(self):
         # Check rows
        for row in self.board:
            if row.count(row[0]) == len(row) and row[0] != '':
                return True

    # Check columns
        for col in range(len(self.board[0])):
            check = []
            for row in self.board:
                check.append(row[col])
            if check.count(check[0]) == len(check) and check[0] != '':
                return True

    # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != '':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != '':
            return True

    # Check if board is full
        for row in self.board:
            for val in row:
                if val == '':
                    return False

    # If no winner and the board is full, it's a terminal state
        return True
    def other_player(self):
        return 'X' if self.player=='O' else 'O'
    def generate_child_nodes(self):
        self.child_nodes=[]
        for i in range(3):
            for j in range(3):
                if self.board[i][j]=='':
                    new_board=copy.deepcopy(self.board)
                    new_board[i][j]=self.other_player()
                    new_tictactoe=TicTacToe(new_board)
                    new_node=node(new_tictactoe,(i,j),self.other_player)
                    self.child_nodes.append(new_node)
        return self.child_nodes     
                           
class ia_agent:
    def __init__(self,ia_player):
        
        self.ai_player='X' if ia_player=='O' else 'O'
        self.human_player=ia_player

    def evaluate(self, node):
    # Check rows for winning line
        board=node.board
        for row in board:
            if row.count(row[0]) == len(row) and row[0] != 0:
                return 10 if row[0] == 'X' else -10
    # Check columns for winning line
        for col in zip(*board):
            if col.count(col[0]) == len(col) and col[0] != 0:
                return 10 if col[0] == 'X' else -10
    # Check diagonals for winning line
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
            return 10 if board[0][0] == 'X' else -10
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != 0:
            return 10 if board[0][2] == 'X' else -10
    # No one has won, return 0
        return 0
    def evaluate2(self, node):
        if node.tictactoe.check_win():
            return 1
        elif node.tictactoe.check_win():
            return -1
        else:
            return 0 
    def evaluate3(self, node):
        board = node.board
        winner = node.tictactoe.check_winner(node.board)
    
        if winner == self.ai_player:
            return 1000
        elif winner == self.human_player:
            return -1000
        elif node.isTerminal():
            return 0
        else:
        # Evaluate based on potential winning moves, blocking opponent, and positional advantages
            score = 0
        
        # Evaluate rows and columns for potential winning moves and blocking opponent
            for i in range(3):
                score += self.evaluate_line(board[i])
                score += self.evaluate_line([board[j][i] for j in range(3)])
        
        # Evaluate diagonals for potential winning moves and blocking opponent
            score += self.evaluate_line([board[i][i] for i in range(3)])
            score += self.evaluate_line([board[i][2-i] for i in range(3)])
        
            return score

    def evaluate_line(self, line):
        '''
        Evaluate a single row, column, or diagonal for potential winning moves and blocking opponent.
        '''
        score = 0
    
    # Count 'X's and 'O's in the line
        x_count = line.count('X')
        o_count = line.count('O')
    
    # Potential winning move for 'X'
        if x_count == 2 and line.count(' ') == 1:
            score += 5
    
    # Potential winning move for 'O'
        if o_count == 2 and line.count(' ') == 1:
            score -= 5
    
        # Blocking opponent's winning move for 'X'
        if x_count == 0 and line.count('O') == 2:
            score -= 4
    
        # Blocking opponent's winning move for 'O'
        if o_count == 0 and line.count('X') == 2:
            score += 4
    
        return score     
    def minimax(self, node, depth, is_maximizing):
        #Base case
        if node.isTerminal() or depth==0 :
            return self.evaluate(node)
        else :
        # if the node represents a state  whene the AI is to play( MAX NODE):
            # the node.player contains the player that made the move
            # so this is a max node because its the ia's turn
            
            if is_maximizing:
                max_eval=float('-inf')
                for child in node.generate_child_nodes():
                    eval=self.minimax(child,depth-1,False)
                    max_eval=max(max_eval,eval)
                return max_eval
            else :
                min_eval=float('inf')
                for child in node.generate_child_nodes():
                    eval=self.minimax(child,depth-1,True)
                    min_eval=min(min_eval,eval)
                return min_eval
            

    def find_best_move(self, node):
        best_move = None
        best_value = float('-inf')
        depth=9
        for child in node.generate_child_nodes():
            value = self.minimax(child, depth, False)
            if value > best_value:
                best_value = value
                best_move = child.move

        return best_move      
    
