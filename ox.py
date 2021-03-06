import numpy as np

class Game:
    def __init__(self):
        # Board Map Do Not Alter
        self.map = np.array([['1','2','3'],
                             ['4','5','6'],
                             ['7','8','9'],])
        # Moves Left, Do Not Later
        self.list = ['1','2','3','4','5','6','7','8','9']
        # Board map copy, reinitable
        self.board = self.map.copy()
        # Moves left copy, reinitable 
        self.remain = self.list.copy()
        # Game data
        self.data  = {
                        'player1':{
                            'name' : '',
                            'piece' : '',
                            'score' : 0,
                        },
                        'player2':{
                            'name' : '',
                            'piece' : '',
                            'score' : 0,
                        },
                    }
        # Winner's name
        self.winner = ''

    def gameSetup(self):
        self.data['player1']['name'] = input('Enter player 1 name\n')
        selection = input('Player 1 choose X or O\n')
        while selection not in ['x','X','o','O']:
            selection = input('Please enter alphabet x or o only, not case sensitive.\n')
        if selection == 'x' or selection == 'X':    
            self.data['player1']['piece'] = 'x'
            self.data['player2']['piece'] = 'o'
        elif selection == 'o' or selection == 'O':
            self.data['player1']['piece'] = 'o'
            self.data['player2']['piece'] = 'x'             
        self.data['player2']['name'] = input('Enter player 2 name\n')
        
    def insertBoard(self, pos, value):
        self.board[self.board == pos] = value
        self.remain.remove(pos)
        
    def reinit(self):
        self.board = self.map.copy()
        self.remain = self.list.copy()
    
    def run(self):
        while True:
            # Display board for player 1
            print(self.board,'\n')
            # Player 1 is x and choose position to put x in
            x_move = input(f"{self.data['player1']['name']} {self.data['player1']['piece']} Move\n")
            # Check if the position is empty and valid
            while True:
                # If position is remain and valid
                if x_move in self.remain:
                    # Insert x into the position of the board and break loop
                    self.insertBoard(x_move, self.data['player1']['piece'])
                    break
                else:
                    # If position not available or not valid, enter again
                    print("The position could be taken or you have enter position other than 1-9, please try again.\n")
                    x_move = input(f"{self.data['player1']['name']} {self.data['player1']['piece']} Move\n")
            # Check win condition, if is true, stop the game, print the winner and display the board
            if self.win() == True:
                print(self.board,'\n')
                print(f'Winner is {self.winner}')
                break

            # Display board for player 2
            print(self.board,'\n')    
            # Player 2 is o and choose position to put o in
            o_move = input(f"{self.data['player2']['name']} {self.data['player2']['piece']} Move\n")
            # Check if the position is empty and valid            
            while True:
                # If position is remain and valid
                if o_move in self.remain:
                    # Insert o into the position of the board and break loop
                    self.insertBoard(o_move, self.data['player2']['piece'])
                    break
                else:
                    # If position not available or ot valid, enter again
                    print("The position could be taken or you have enter position other than 1-9, please try again.\n")
                    o_move = input(f"{self.data['player2']['name']} {self.data['player2']['piece']} Move\n")
            # Check win condition, if is true, stop the game, print the winner and display the board
            if self.win() == True:
                print(self.board,'\n')
                print(f'Winner is {self.winner}')
                break
                     
    def win(self):
        # If row is same
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2]:
                self.winner = self.board[row][0]
                if self.winner == self.data['player1']['piece']:
                    self.data['player1']['score'] += 1
                elif self.winner == self.data['player2']['piece']:
                    self.data['player2']['score'] += 1
                return True
        # If column is same
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col]:
                self.winner = self.board[0][col]
                if self.winner == self.data['player1']['piece']:
                    self.data['player1']['score'] += 1
                elif self.winner == self.data['player2']['piece']:
                    self.data['player2']['score'] += 1
                return True
        # If left to right diagonal is same
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            self.winner = self.board[0][0]
            if self.winner == self.data['player1']['piece']:
                self.data['player1']['score'] += 1
            elif self.winner == self.data['player2']['piece']:
                self.data['player2']['score'] += 1
            return True
        # If right to left diagonal is same
        if self.board[0][2] == self.board[1][1] == self.board[2][0]:
            self.winner = self.board[0][2]
            if self.winner == self.data['player1']['piece']:
                self.data['player1']['score'] += 1
            elif self.winner == self.data['player2']['piece']:
                self.data['player2']['score'] += 1
            return True
        elif not self.remain:
            self.winner = 'No Winner'
            return True
        else:
            return False

    def start(self):
        self.gameSetup()
        self.run()
        while True:
            print(f"{self.data['player1']['name']} score : {self.data['player1']['score']} \t {self.data['player2']['name']} score : {self.data['player2']['score']}\n")
            command = input("r to play again, or q to quit the game\n")
            while command not in ['r', 'R', 'q', 'Q']:
                command = input("r to play again, or q to quit the game, not case sensitive\n")
            if command == 'r' or command == 'R':
                self.reinit()
                self.run()
            elif command == 'q' or command == 'Q':
                print(f"{self.data['player1']['name']} score : {self.data['player1']['score']} \t {self.data['player2']['name']} score : {self.data['player2']['score']}\n")
                if self.data['player1']['score'] > self.data['player2']['score']:
                    print(f'Winner is {self.data['player1']['name']}')
                elif self.data['player2']['score'] > self.data['player1']['score']:
                    print(f'Winner is {self.data['player2']['name']}')
                break
            
def main():
    game = Game()
    game.start()

if __name__ == '__main__':
           main()              