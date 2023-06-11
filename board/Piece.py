from tkinter import Canvas, PhotoImage, NW


class Piece:
    """
    a class representing a chess piece that contains the following attributes:
        1) a canvas where the pieces will be drawn to
        2) a matrix representing the game board
        3) both of the king pieces

    instances of the class contains the following attributes
        1) coordinates - the location of the piece on the board
        2) moves - the possible moves for the piece
        3) specials - the special moves for the price
        4) has_not_moved - determines if the piece has moved or not yet
        5) color - the color of the piece
        6) name - the name of the piece
        7) image_id - the id of the image for the piece
        8) possible_move_ids - a list of canvas objects representing the possible moves for the piece
        9) possible_moves - a list of possible moves for the current position of the piece
        10) possible_specials - a dict of possible special moves for the current position of the piece as the key as
            well as the action function as the value
        11) id - the id for the image on the canvas

    class contains the following functions:
        1) __init__ - creates the chess piece
        2) update_moves - updates the pieces moves
        3) toggle_show_moves - display or hides possible moves for the piece
        4) move - moves the piece
        5) click - handles when the mouse is clicked on the board
        6) attacked - checks if a location is blocked by another pieces moves or not
        7) update_board - checks for checks and mates
        8) check - updates the pieces moves for when there is a check
        9) __repr__ - returns the name of the piece, useful when printing Piece.board
    """

    # creates the canvas
    CANVAS = Canvas(width=900, height=800)
    CANVAS.pack()
    CANVAS.master.resizable(False, False)

    # creates board matrix turn variable and king variables
    board = [[None for _ in range(8)] for _ in range(8)]  # note board is rotated 90 degrees for easier indexing
    turn = 'black'  # should be opposite of starting color because update_board is called during initialization
    WHITE_KING = None
    BLACK_KING = None

    # places the board spaces on the canvas
    for y in range(8):
        y *= 100
        for x in range(8):
            x *= 100
            CANVAS.create_rectangle(x, y, x + 100, y + 100, fill=['#e3c16f', '#b88b4a'][((x + y) // 100) % 2])

    def __init__(self, coordinates: tuple, image: str, offset: tuple, moves: set, specials: dict):
        """
        creates the chess piece

        :param coordinates: the coordinates of the chess piece in the form (0-7, 0-7)
        :param image: the file path to the image, images will anchor to the top left (NW) corner when placed
        :param offset: the number of pixels to offset the image for it to be centered on the board in the form (x, y)
        :param moves: a set of moves for the piece in the form (x, y) where x is the relative distance in the x
            direction and y is the relative distance in the y direction, use 'i' to indicate that the piece can be moved
            infinitely in that direction (until end of board or another piece is reached). for example (0, 'i') means
            the piece can be moved infinitely in the +y direction, ('i', 0) means the piece can be moved infinitely in
            the +x direction and ('i', 'i') means the piece can move infinitely in the positive diagonal direction use
            '-i' to indicate the piece can move infinitely in the negative direction
        :param specials: a dict containing special moves for the piece where the key is the move and the id (see param
            moves for more info and the value is a list of tuples of functions, where the function at index 0 is the
            pre-test function to determine if the move can be made (returns true or false) and the function at index 1
            is the action function, the function that will be called when the move is made. both functions take 1
            parameter, the piece that will move. the list of these functions should be ordered so that the lower index
            special moves will have priority over the later index moves
        """

        # creates fields
        self.coordinates = coordinates
        self.image = PhotoImage(file=image).subsample(5, 5)
        self.moves = moves if moves else set()
        self.specials = specials if specials else {}
        self.has_not_moved = True
        image = image.split('/')
        self.color = image[-2]
        self.name = image[-1].replace('.png', '')
        self.possible_move_ids = set()
        self.possible_moves = set()
        self.possible_specials = {}

        # places piece on board
        Piece.board[self.coordinates[0]][self.coordinates[1]] = self
        x = (self.coordinates[0] * 100) + offset[0]
        y = (self.coordinates[1] * 100) + offset[1]
        self.id = Piece.CANVAS.create_image(x, y, image=self.image, anchor=NW)

        # saves piece if it is a king
        if self.name == 'king' and self.color == 'white':
            Piece.WHITE_KING = self
        elif self.name == 'king' and self.color == 'black':
            Piece.BLACK_KING = self

    def update_moves(self):
        """
        updates the pieces moves and special moves
        """

        # clears old moves
        self.possible_moves.clear()
        self.possible_specials.clear()

        # gets every possible move
        for move in self.moves:
            x = self.coordinates[0]
            y = self.coordinates[1]

            # increments/decrements x and y to draw diagonal moves
            while isinstance(move[0], str) or isinstance(move[1], str):
                x += 1 if isinstance(move[0], str) and move[0] == 'i' else 0
                x -= 1 if isinstance(move[0], str) and move[0] == '-i' else 0
                y += 1 if isinstance(move[1], str) and move[1] == 'i' else 0
                y -= 1 if isinstance(move[1], str) and move[1] == '-i' else 0

                # blocks moves if end of board or same color piece has been reached
                off_board = not (0 <= x <= 7 and 0 <= y <= 7)
                if off_board or Piece.board[x][y] is not None and Piece.board[x][y].color == self.color:
                    break

                # handles when enemy piece has been reached
                self.possible_moves.add((x, y))
                if Piece.board[x][y] is not None:
                    break

            # handles when move is a fixed displacement
            if isinstance(move[0], int) and isinstance(move[1], int):
                x += move[0]
                y += move[1]

                # blocks moves if end of board or same color piece has been reached
                if 0 <= x <= 7 and 0 <= y <= 7 and (Piece.board[x][y] is None or Piece.board[x][y].color != self.color):
                    self.possible_moves.add((x, y))

        # gets special moves
        for move in self.specials.keys():
            x = self.coordinates[0]
            y = self.coordinates[1]

            # finds which special move takes priority
            for i in range(len(self.specials[move])):
                if self.specials[move][i][0](self):
                    x += move[0]
                    y += move[1]
                    self.possible_specials[(x, y)] = self.specials[move][i][1]

    def toggle_show_moves(self):
        """
        performs one of the following actions:
            1) displays the possible moves for the piece when clicked
            2) hides possible moves when piece is clicked and moves are already displayed

        additionally if a different piece is already displaying moves, its moves will be hidden before showing current
        pieces moves
        """

        # handles when another pieces moves are being displayed
        if Piece.clicked_piece != self and Piece.clicked_piece is not None:
            Piece.clicked_piece.toggle_show_moves()
            self.toggle_show_moves()
            return

        # handles when piece is clicked and moves should be hidden
        elif Piece.clicked_piece == self:
            [Piece.CANVAS.delete(move) for move in self.possible_move_ids]
            self.possible_move_ids.clear()
            Piece.clicked_piece = None
            return

        # draws every possible move
        Piece.clicked_piece = self
        for move in self.possible_moves:
            x = move[0] * 100
            y = move[1] * 100
            shape_id = Piece.CANVAS.create_oval(x, y, x + 100, y + 100, fill='blue')
            self.possible_move_ids.add(shape_id)

        # draws every possible special move
        for move in self.possible_specials.keys():
            x = move[0] * 100
            y = move[1] * 100
            shape_id = Piece.CANVAS.create_oval(x, y, x + 100, y + 100, fill='blue')
            self.possible_move_ids.add(shape_id)

    def move(self, position: tuple, temporary: bool = False):
        """
        moves the piece to the new location and kills the piece in that new location if there is one
        additionally if moves are displayed they will be hidden after the move

        :param position: the new position to move the piece to
        :param temporary: determines if the move is temporary, used in getting moves during a check
        """

        # hides moves and kills piece in new spot if possible
        self.toggle_show_moves() if not temporary else None
        if (not temporary) and (self.board[position[0]][position[1]] is not None):
            Piece.CANVAS.delete(self.board[position[0]][position[1]].id)

        # moves piece
        self.board[self.coordinates[0]][self.coordinates[1]] = None
        self.board[position[0]][position[1]] = self
        x, y = (position[0] - self.coordinates[0]) * 100, (position[1] - self.coordinates[1]) * 100
        Piece.CANVAS.move(self.id, x, y) if not temporary else None
        self.coordinates = position
        self.has_not_moved = False if not temporary else self.has_not_moved

    @staticmethod
    def click(event):
        """
        handles when the mouse is clicked on the canvas

        :param event: the mouse click event
        """

        # converts canvas coordinates to game board coordinates
        x = event.x // 100
        y = event.y // 100

        # handles when click was outside of game
        if x >= 8:
            Piece.clicked_piece.toggle_show_moves() if Piece.clicked_piece is not None else None

        # handles when move has been clicked
        elif Piece.clicked_piece is not None and (x, y) in Piece.clicked_piece.possible_moves:
            Piece.clicked_piece.move((x, y))
            Piece.update_board()

        # handles when special move has been clicked
        elif Piece.clicked_piece is not None and (x, y) in Piece.clicked_piece.possible_specials.keys():
            Piece.clicked_piece.possible_specials[(x, y)](Piece.clicked_piece)
            Piece.update_board()

        # handles when piece is clicked
        elif Piece.board[x][y] is not None and Piece.board[x][y].color == Piece.turn:
            Piece.board[x][y].toggle_show_moves()

        # handles when empty spot is clicked
        elif Piece.clicked_piece is not None:
            Piece.clicked_piece.toggle_show_moves()

    # binds click event to click function and sets clicked piece
    CANVAS.bind('<Button-1>', click)
    clicked_piece = None

    @staticmethod
    def attacked(position: tuple, color: str) -> list:
        """
        checks if a given position on the board is "blocked" by another piece and would cause the king to be in check

        :param position: the board position to check
        :param color: the color of the king that will move, for example if king is white then function will see if black
            moves will cause a check
        :return: a list of pieces that are attacking this position
        """

        # gets every possible move from the other colors pieces
        attacking_pieces = []
        for column in Piece.board:
            for piece in column:

                # gets information about the piece used in multiple edge cases
                base_condition = piece is not None and piece.color != color
                x, y = piece.coordinates if base_condition else (None, None)

                # handles pawns moves where attack isn't currently possible
                if base_condition and piece.name == 'pawn':
                    delta_y = -1 if piece.color == 'white' else 1
                    pawn_moves = {(x - 1, y + delta_y), (x + 1, y + delta_y)}
                    attacking_pieces.append(piece) if position in pawn_moves else None

                # handles when the piece is a king
                elif base_condition and piece.name == 'king':
                    king_moves = [(x + move[0], y + move[1]) for move in piece.specials.keys()]
                    attacking_pieces.append(piece) if position in king_moves else None

                # makes sure piece is enemy color
                elif base_condition:
                    moves = piece.possible_moves.union(set(piece.possible_specials.keys()))
                    attacking_pieces.append(piece) if position in moves else None

        # returns list of attacking pieces
        return attacking_pieces

    @staticmethod
    def update_board():
        """
        updates the board by performing the following actions
            1) updates which players move it is
            2) updates possible piece moves
            3) checks for checks
        """

        # updates turn and piece moves
        Piece.turn = 'black' if Piece.turn == 'white' else 'white'
        for column in Piece.board:
            for piece in column:
                piece.update_moves() if piece is not None else None
        Piece.WHITE_KING.update_moves()
        Piece.BLACK_KING.update_moves()

        # checks if the king is in check
        king = Piece.WHITE_KING if Piece.turn == 'white' else Piece.BLACK_KING
        if Piece.attacked(king.coordinates, king.color):
            Piece.check(king)

    @staticmethod
    def check(king):
        """
        handles when there is a check on the board. only allows moves that would get king out of check

        :param king: the king that is in check
        """

        # loops over every possible move for the king
        board_copy = [row.copy() for row in Piece.board]
        king_coordinates = king.coordinates
        invalid_moves = []
        for move in tuple(king.possible_specials.keys()):

            # moves the king to the possible move and updates other pieces moves
            king.move(move, True)
            for column in Piece.board:
                for piece in column:
                    piece.update_moves() if piece is not None else None
            king.update_moves()

            # adds move to list of invalid moves if king would be in check
            if Piece.attacked(king.coordinates, king.color):
                invalid_moves.append(move)

            # resets the board
            king.move(king_coordinates, True)
            Piece.board = [row.copy() for row in board_copy]

        # resets board
        king.move(king.coordinates, True)
        for column in Piece.board:
            for piece in column:
                piece.update_moves() if piece is not None else None

        # updates king moves
        king.update_moves()
        [king.possible_specials.pop(move) for move in invalid_moves]

        # loops over every piece of the same color as the king
        attacking_pieces = set([piece.coordinates for piece in Piece.attacked(king.coordinates, king.color)])
        can_attack_attacking = False
        for column in Piece.board:
            for piece in column:
                if (piece is not None) and (piece != king) and (piece.color == king.color):

                    # updates pieces moves
                    piece.possible_moves = piece.possible_moves.intersection(attacking_pieces)
                    for move in tuple(piece.possible_specials.keys()):
                        if move not in attacking_pieces:
                            piece.possible_specials.pop(move)

                    # checks if the piece can attack
                    if len(piece.possible_moves) + len(piece.possible_specials) >= 1:
                        can_attack_attacking = True

        # checks if there is a checkmate
        if len(king.possible_specials) == 0 and (len(attacking_pieces) > 1 or (not can_attack_attacking)):
            raise NotImplementedError('checkmate')  # todo

    def __repr__(self):
        """
        returns the name of the piece the color and the coordinates as a string

        :return: the name of the piece the color and the coordinates
        """
        return f'{self.name} {self.color} {self.coordinates}'
