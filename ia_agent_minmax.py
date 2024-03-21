
# to encapsulate the game logic
class node:
    def __init__(self, TictacToe,move,player): 
        #  3X3 grid that contains the game state after the move
        
        self.board=TictacToe.grid
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
        return self.tictactoe.player == player  and self.tictactoe.check_win()
    def isTerminal(self):
        return '' in all(self.board)
    def other_player(self):
        return 'X' if self.player=='O' else 'O'
    def generate_child_nodes(self):
        self.child_nodes=[]
        for i in range(3):
            for j in range(3):
                if self.board[i][j]=='':
                    new_board=self.board
                    new_board[i][j]=self.other_player()
                    new_tictactoe=TicTacToe(new_board)
                    new_node=node(new_tictactoe,(i,j),self.other_player)
                    self.child_nodes.append(new_node)
        return self.child_nodes()     
                           
class ia_agent:
    def __init__(self):
        
        self.ai_player='O'
        self.human_player='X'

    def evaluate(self, node):
        # ia player has won
        if node.check_win(self.ai_player):
            return 1
        # human player has won:
        if  node.check_win(self.human_player):
            return -1
        if node.check_tie():
            return 0
    def minimax(self, node, depth, is_maximizing):
        #Base case
        if node.isTerminal :
            return self.evaluate(node)
        else :
        # if the node represents a state  whene the AI is to play( MAX NODE):
            # the node.player contains the player that made the move
            # so this is a max node because its the ia's turn
            is_maximizing=node.player!=self.ai_player
            is_minimazing=node.player==self.ai_player
        
            if is_maximizing:
                max_eval=float('-inf')
                for child in node.generate_child_nodes():
                    eval=self.minimax(child,depth+1,is_minimazing)
                    max_eval=max(max_eval,eval)
                return max_eval
            else :
                min_eval=float('inf')
                for child in node.generate_child_nodes():
                    eval=self.minimax(child,depth+1,is_maximizing)
                    min_eval=min(min_eval,eval)
                return min_eval
            

    def find_best_move(self, node):
        best_move = None
        best_value = float('-inf')

        for child in node.generate_child_nodes():
            value = self.minimax(child, 0, False)
            if value > best_value:
                best_value = value
                best_move = child.move

        return best_move