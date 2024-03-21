from game import TicTacToe,ia_agent,node
import pygame
from reusable import LabeledRect
from time import sleep

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

class Game :
    def __init__(self) :
        self.display=pygame.display      
        self.surface=pygame.display.set_mode((WIDTH_FRAME,HEIGHT_FRAME))
        pygame.display.set_caption('TIC TAC TOE ...')
        self.color=BLACK
        self.tictactoe=TicTacToe()
        self.ia_agent=ia_agent(self.tictactoe.current_player)
    def build_ui(self):
        x_coord=WIDTH_GAME + 1
        pygame.draw.line(self.surface,WHITE,(x_coord,0),(x_coord,self.surface.get_height()),3)
        # the new game button:
        self.start =LabeledRect((x_coord+30,5+100),(150,30),label="New game")
        
        pygame.draw.rect(self.surface,RED,self.start)
        self.start.write(self.surface,FONT,35,WHITE)
        # the new game against ia button:
        
        # the ia move button :
        self.ia_move =LabeledRect((x_coord+30,50+200),(150,30),label="IA move")
        
        pygame.draw.rect(self.surface,RED,self.ia_move)
        self.ia_move.write(self.surface,FONT,35,WHITE)
        self.display.flip()   
    
    def get_winning_line_coordinates(self, winning_line):
    # Get the Rect objects for the start and end points of the winning line
        start_rect = self.tictactoe.rects[winning_line[0][0]][winning_line[0][1]]
        end_rect = self.tictactoe.rects[winning_line[1][0]][winning_line[1][1]]

    # Get the center points of the Rect objects
        start_screen = start_rect.center
        end_screen = end_rect.center

        return start_screen, end_screen
    def draw_winning_line(self, start, end):
        pygame.draw.line(self.surface, RED, start, end, 3)
    def check_win(self):
        self.board=self.tictactoe.grid
    # Check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
             return True, [(i, 0), (i, 2)]
    # Check columns
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                return True, [(0, i), (2, i)]
    # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return True, [(0, 0), (2, 2)]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] !='':
            return True, [(0, 2), (2, 0)]
    # No winner
        return False, []
    def run(self):
        #set initial color
        
        self.surface.fill(self.color)
        self.build_ui()
        running=True
        while running:
            
        
            self.tictactoe.draw_game(self.surface)  # Draw the Tic Tac Toe board
            winner, winning_line = self.check_win()
            if winner:
                start, end = self.get_winning_line_coordinates(winning_line)
                self.draw_winning_line(start, end)
                
                self.display.flip()  # Update the display
            self.display.flip()  # Update the display
            
            for event in pygame.event.get():
                
                if event.type==pygame.QUIT:
                    running=False
                    print('Game Session ended...')
                    pygame.quit()
                if event.type==pygame.MOUSEBUTTONDOWN:
                    Xmouse,Ymouse=pygame.mouse.get_pos()
                    if Xmouse<WIDTH_GAME:
                        self.tictactoe.handleClick(Xmouse,Ymouse)
                        if self.tictactoe.check_win()==True:
                            self.handle_win()
                        if self.tictactoe.check_tie()==True:
                            self.handle_tie()
                        
                    else :
                        if self.start.collidepoint(Xmouse,Ymouse):
                            self.tictactoe.reset()
                            # Create a pygame.Rect object representing the area to clear
                            area_to_clear = pygame.Rect(0, 0, WIDTH_GAME, HEIGHT_GAME)
                            # Fill the area with the specified color
                            self.surface.fill((0, 0, 0), area_to_clear)
                            print('Game Restarted')
                            self.ia_agent=ia_agent(self.tictactoe.current_player)
                        elif self.ia_move.collidepoint(Xmouse,Ymouse):
                            # if self.tictactoe.current_player==self.ia_agent.ai_player:
                                
                                best_move=self.ia_agent.find_best_move(node(self.tictactoe,self.tictactoe.lastMove,player=self.tictactoe.current_player))
                                self.tictactoe.make_move((best_move[0],best_move[1]))
                                
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        self.tictactoe.reset()
                        print('Game Restarted')
            # self.color_play()
    def handle_win(self):
        self.tictactoe.alternate_player()
        print(f'Game Ended : Player {self.tictactoe.current_player} has won!')
        # self.tictactoe.reset()
    def handle_tie(self):
        
        print(f'Game is Tied!')        
    def color_play(self):
        #play with colors
            self.surface.fill(self.color)
            sleep(1)
            self.display.flip()
            if self.color==WHITE:
                self.color=RED
            elif self.color==RED:
                self.color=BLUE
            elif self.color==BLUE:
                self.color=GREEN
            else :
                self.color=WHITE       

game=Game()
game.run()                 