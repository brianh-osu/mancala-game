# Author: Brian Hsiang
# GitHub username: brianh-osu
# Date: 11/22/22
# Description: Assignment Portfolio Project


class Mancala:
    """
    Mancala class will be used to play the game primarily. We also create_player()
    It's data members include whole_board which stores pit objects as well as player_roster which stores player objects.
    """
    def __init__(self):
        self._whole_board = []  # stores pit objects
        self._first_player = True
        self._player_roster = []  # stores player objects (used only to initialize new players)
        self._game_over = False

    def get_board_list(self):
        """returns a list of the pit values across the board"""
        board_list = []
        for list_obj in self._whole_board:
            board_list.append(list_obj.get_val())
        return board_list

    def create_player(self, name):
        """
        1. takes 1 parameter (player's name) as a string, and returns the player object (class can be defined by your own design)
        2. Also adds the each player_obj's _player_board (their side, elements 1-7) to Mancala's whole board
        """

        # initializes the player_index (1 or 2)
        if self._first_player == True:
            player_index = 1
            self._first_player = False
        else:
            player_index = 2

        player_obj = Player(name, player_index)  # creates player object

        # iterates through player_obj's _player_board and appends it to _whole_board
        for x in player_obj.get_player_board():
            self._whole_board.append(x)


        # This section is to fix the mistake I made of formatting the board initially
        if player_index == 2:
            temp = []
            for x in self._whole_board[7:14]:
                temp.append(x)  # list of temp pit_objects
            counter1 = 5
            counter2 = 7
            for pit_obj in self._whole_board[7:13]:
                self._whole_board[counter2] = temp[counter1]
                counter1 -= 1
                counter2 += 1

        # adds player_obj to the roster
        self._player_roster.append(player_obj)

        return player_obj

    def print_board(self):
        """prints the current board in specified format. """
        print('player1:')
        print(f"store: {self._player_roster[0].get_store_value()}")
        print(f"{self._player_roster[0].get_pit_values()}")
        print('player2:')
        print(f"store: {self._player_roster[1].get_store_value()}")
        print(f"{self._player_roster[1].get_pit_values()}")


    def play_game(self, player_index, pit_index):
        """
        takes 2 parameters: player_index (1 or 2), and the pit index(1-6).
        The method should follow the rules of the game (including the 2 special rules) and
        1. update the seeds # in each pit
        *1b. check if ending state is reached
        2. If the ending state is reached, update the seed #s in the pit and store for both players
        3. Returns a list of the current seed number in specified format.
        """
        if pit_index > 6 or pit_index <= 0:
            return 'Invalid number for pit index'

        #Game state has been duplicated here to check.
        pre_result = self.get_board_list()
        list1 = pre_result[0:7]
        list2 = pre_result[7:14]
        if list1.count(0) == 6 or list2.count(0) == 6:
            self._game_over = True

            # collect seeds and add it to store total for end game
            temp_total_1 = 0  # add to this and then reset the pit to 0
            for obj in self._whole_board[0:7]:
                temp_total_1 += obj.get_val()
                obj.set_val(0)

            temp_total_2 = 0
            for obj in self._whole_board[7:14]:
                temp_total_2 += obj.get_val()
                obj.set_val(0)

            self._whole_board[6].set_val(temp_total_1)
            self._whole_board[13].set_val(temp_total_2)

            # self.print_board()
            return 'Game is ended'

        # special_rule_2 checks if the last pit to be added contains 0. If it does, then it takes the opposing seeds (sets to 0) and your seeds to your store.
        special_rule_1, special_rule_2 = False, False

        #Player 1 is now going to play:
        if player_index == 1:
            cursor = pit_index - 1  # 'cursor' variable will traverse the map
            grabbed = self._whole_board[pit_index - 1].get_val()  # picked this up, ready to distribute
            self._whole_board[pit_index - 1].set_val(0)  # pit set to 0
            # starting_index = self._whole_board.index(self._whole_board[cursor])

            # for how many times it goes over the edge, you should create that many variables (max is 48, maybe account for 2-3)
            # if starting_index + grabbed > 13: #V1
            #     temp = grabbed
            #     grabbed = 13 - starting_index
            #     temp -= grabbed

            # while cursor >= 0:
            while grabbed > 0:
                cursor += 1
                pit_obj = self._whole_board[cursor % 14]

                if grabbed == 1 and pit_obj.get_val() == 0 and pit_obj.get_type() == 'pit':  # and self._whole_board[pit_index + grabbed - 1].get_val != 0:
                    special_rule_2 = True
                    # if pit_obj.get_val() == 0: #not correct
                    #     if pit_obj.get_type() == 'pit':
                    #         special_rule_2 = True
                # print(special_rule_2)

                if grabbed == 1 and pit_obj.get_player_index() == 1 and pit_obj.get_type() == 'store':
                    special_rule_1 = True

                # any pit type should gain a seed. Also, if it's on player 1's side it should gain a seed.
                if pit_obj.get_type() == 'pit' or pit_obj.get_player_index() == 1:
                    pit_obj.add_one()
                    grabbed -= 1
                elif pit_obj.get_player_index() == 2 and pit_obj.get_type() == 'store':  # if this is the enemy store, skip
                    pass  # do nothing

                if special_rule_2 == True:
                    # print('p1 sp rule 2 triggered')
                    # self.print_board()
                    cursor = self._whole_board.index(self._whole_board[cursor % 14])
                    # print('cursor: ', cursor) #
                    current = pit_obj.get_val()  # gets the current value after seeds updated
                    # print('current: ', current)
                    if cursor == 12:
                        gain = self._whole_board[0].get_val()
                        self._whole_board[0].set_val(0)
                    if cursor == 11:
                        gain = self._whole_board[1].get_val()
                        self._whole_board[1].set_val(0)
                    if cursor == 10:
                        gain = self._whole_board[2].get_val()
                        self._whole_board[2].set_val(0)
                    if cursor == 9:
                        gain = self._whole_board[3].get_val()
                        self._whole_board[3].set_val(0)
                    if cursor == 8:
                        gain = self._whole_board[4].get_val()
                        self._whole_board[4].set_val(0)
                    if cursor == 7:
                        gain = self._whole_board[5].get_val()
                        self._whole_board[5].set_val(0)

                    # if cursor == 6: #cannot be 6 or 13 as those are stores
                    #     gain = self._whole_board[0].get_val()
                    #     self._whole_board[0].set_val(0)
                    if cursor == 5:
                        gain = self._whole_board[7].get_val()
                        self._whole_board[7].set_val(0)
                    if cursor == 4:
                        gain = self._whole_board[8].get_val()
                        self._whole_board[8].set_val(0)
                    if cursor == 3:
                        gain = self._whole_board[9].get_val()
                        self._whole_board[9].set_val(0)
                    if cursor == 2:
                        gain = self._whole_board[10].get_val()
                        self._whole_board[10].set_val(0)
                    if cursor == 1:
                        gain = self._whole_board[11].get_val()
                        self._whole_board[11].set_val(0)
                    if cursor == 0:
                        gain = self._whole_board[12].get_val()
                        self._whole_board[12].set_val(0)

                    # v2 gain = self._whole_board[cursor%14].get_val() #gets value of seeds across board
                    # print('gain: ', gain)
                    # self._whole_board[cursor%14-7].set_val(0)
                    # v2 self._whole_board[cursor%14].set_val(0) #sets value across board to 0
                    self._whole_board[6].add_val(current + gain)  # adds current+gain to p1 store
                    pit_obj.set_val(
                        0)  # sets the pit_obj to 0 since the last pit_obj to land on value was already added to store.
                    special_rule_2 = False  # resets special_rule_2 to be retriggered
                    # self.print_board()
                    # print('p1 sp rule 2 finished')

                if special_rule_1 == True:
                    special_rule_1 = False
                    print('player 1 take another turn')


        #player 2 is now playing:
        elif player_index == 2:
            pit_index += 7
            cursor = pit_index - 1  #
            grabbed = self._whole_board[pit_index - 1].get_val()
            self._whole_board[pit_index - 1].set_val(0)

            while grabbed > 0:
                cursor += 1
                pit_obj = self._whole_board[cursor % 14]

                if grabbed == 1 and pit_obj.get_val() == 0 and pit_obj.get_type() == 'pit':
                    special_rule_2 = True

                if grabbed == 1 and pit_obj.get_player_index() == 2 and pit_obj.get_type() == 'store':
                    special_rule_1 = True

                if pit_obj.get_type() == 'pit' or pit_obj.get_player_index() == 2:
                    pit_obj.add_one()
                    grabbed -= 1

                elif pit_obj.get_player_index() == 1 and pit_obj.get_type() == 'store':
                    pass

                if special_rule_2 == True:
                    # print('p2 sp rule 2 triggered')
                    cursor = self._whole_board.index(self._whole_board[cursor % 14])
                    # print('cursor: ', cursor)
                    current = pit_obj.get_val()  # 0
                    # print('current: ', current)
                    if cursor == 12:
                        gain = self._whole_board[0].get_val()
                        self._whole_board[0].set_val(0)
                    if cursor == 11:
                        gain = self._whole_board[1].get_val()
                        self._whole_board[1].set_val(0)
                    if cursor == 10:
                        gain = self._whole_board[2].get_val()
                        self._whole_board[2].set_val(0)
                    if cursor == 9:
                        gain = self._whole_board[3].get_val()
                        self._whole_board[3].set_val(0)
                    if cursor == 8:
                        gain = self._whole_board[4].get_val()
                        self._whole_board[4].set_val(0)
                    if cursor == 7:
                        gain = self._whole_board[5].get_val()
                        self._whole_board[5].set_val(0)

                    #cursor should not do anything at 6 and 13, those are store types

                    if cursor == 5:
                        gain = self._whole_board[7].get_val()
                        self._whole_board[7].set_val(0)
                    if cursor == 4:
                        gain = self._whole_board[8].get_val()
                        self._whole_board[8].set_val(0)
                    if cursor == 3:
                        gain = self._whole_board[9].get_val()
                        self._whole_board[9].set_val(0)
                    if cursor == 2:
                        gain = self._whole_board[10].get_val()
                        self._whole_board[10].set_val(0)
                    if cursor == 1:
                        gain = self._whole_board[11].get_val()
                        self._whole_board[11].set_val(0)
                    if cursor == 0:
                        gain = self._whole_board[12].get_val()
                        self._whole_board[12].set_val(0)

                    # adds to store, sets value to 0, and resets special_rule_2  back to initial value False, awaiting to retrigger.
                    self._whole_board[13].add_val(current + gain)
                    pit_obj.set_val(0)
                    special_rule_2 = False

                #speciail_rule_1 checked
                if special_rule_1 == True:
                    special_rule_1 = False
                    print('player 2 take another turn')


        # ending state checked here
        result = self.get_board_list()
        list1 = result[0:7]
        list2 = result[7:14]
        if list1.count(0) == 6 or list2.count(0) == 6:
            self._game_over = True

            # collect seeds and add it to store total for end game
            temp_total_1 = 0  # add to this and then reset the pit to 0
            for x in self._whole_board[0:7]:
                temp_total_1 += x.get_val()
                x.set_val(0)

            temp_total_2 = 0
            for x in self._whole_board[7:14]:
                temp_total_2 += x.get_val()
                x.set_val(0)

            self._whole_board[6].set_val(temp_total_1)
            self._whole_board[13].set_val(temp_total_2)

            # self.print_board()

            return self.get_board_list()

        return result

    def return_winner(self):
        """
        takes no parameter.
        If the game is ended, return the winner in specified format.
        If the game is a tie, then return "It's a tie";
        If the game is not ended yet, return "Game ahs not ended"
        """
        if self._game_over == True:
            player_1_store_total = self._whole_board[6].get_val()
            player_2_store_total = self._whole_board[13].get_val()
            if player_1_store_total > player_2_store_total:
                winner_obj = self._player_roster[0]
            elif player_1_store_total < player_2_store_total:
                winner_obj = self._player_roster[1]
            elif player_1_store_total == player_2_store_total:
                return "It's a tie"
            return (f"Winner is player {winner_obj.get_player_index()}: {winner_obj.get_name()}")

        else:
            return "Game has not ended"


class Player:
    """Player class holds the name, player index, and a list of 7 pit objects that belong to the player"""

    def __init__(self, name, player_index):
        self._name = name
        self._player_index = player_index
        self._player_board = []  # list of 7 pit objects (initialized below)
        for x in range(1, 8):
            if x in [1, 2, 3, 4, 5, 6]:
                self._player_board.append(Pit(player_index, 4, 'pit'))
            elif x == 7:
                self._player_board.append(Pit(player_index, 0, 'store'))

    def get_name(self):
        """returns name"""
        return self._name

    def get_player_board(self):
        """gets the player_board """
        return self._player_board

    def get_pit_values(self):
        """returns a list of pit values"""
        result = []
        if self._player_index == 1:
            for x in range(0, 6):
                obj = self._player_board[x].get_val()
                result.append(obj)
        else:
            for x in range(5, -1, -1):
                obj = self._player_board[x].get_val()
                result.append(obj)
        return result

    def get_store_value(self):
        """returns the store total """
        obj = self._player_board[6]
        return obj.get_val()

    def get_player_index(self):
        """returns the player index """
        return self._player_index


class Pit:
    """Pit class has a player index, pit value, and 'type' characteristic assigned to each individual pit."""

    def __init__(self, player_index, val, type):
        self._player_index = player_index  # 1 or 2
        self._val = val  # pit type has value of 4. Store type has 0.
        self._type = type  # 'pit' or 'store'

    def get_player_index(self):
        """gets the player index this pit belongs to """
        return self._player_index

    def get_type(self):
        """"gets the pit type (store or pit)"""
        return self._type

    def get_val(self):
        """gets the pit value"""
        return self._val

    def set_val(self, num):
        """sets the value of this pit to a number argument- used for setting pit to 0"""
        self._val = num

    def add_val(self, num):
        """adds the value of this pit- used for adding to store """
        self._val += num

    def add_one(self):
        """adds 1 to the pit value- used for play_game and traversing the map"""
        self._val += 1


if __name__ == '__main__':
    # readme test 1
    # game = Mancala()
    # player1 = game.create_player("Lily")
    # player2 = game.create_player("Lucy")
    # print(game.play_game(1, 3))
    # game.play_game(1, 1)
    # game.play_game(2, 3)
    # game.play_game(2, 4)
    # game.play_game(1, 2)
    # game.play_game(2, 2)
    # game.play_game(1, 1)
    # game.print_board()
    # print(game.return_winner())

    #readme test 2
    game = Mancala()
    player1 = game.create_player("Lily")
    player2 = game.create_player("Lucy")
    game.play_game(1, 1)
    game.play_game(1, 2)
    game.play_game(1, 3)
    game.play_game(1, 4)
    game.play_game(1, 5)
    game.play_game(1, 6)

    game.print_board()
    print(game.return_winner())
    # print(game.play_game(1, 1))
    # print(game.play_game(2,1))
