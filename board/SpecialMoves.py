from Piece import Piece
from tkinter import PhotoImage, NW


"""
a few functions for special moves that the following pieces can have:

    1) Pawn

        --> pre-test to see if pawn has moved yet and can move 2 spaces if not blocked
        --> pre-test to see if pawn can attack an enemy piece in the forward diagonal direction
        --> pre-test to make sure pawn can move forward 1 space if not blocked by another piece
        --> pre-test to see if pawn can advance to the end of the board and upgrade to another piece
        --> pre-test to see if pawn can advance to the end of the board and upgrade to another piece after a
            diagonal attack

        --> action function to move forward 2 spaces
        --> action function to attack a diagonal enemy and move to its place
        --> action function to move forward 1 space
        --> action function to move pawn to end of board and update to another piece
        --> action function to move pawn to end of board and update to another piece after diagonal attack

    2) King

        --> pre-test to see if king can move to available spots without being put in check/checkmate
        --> pre-test to see if king can be castled

        --> action function to move king to available spots without being put in check/checkmate
        --> action function to castle the king
"""


#  =============================================== PAWN HELPER-FUNCTIONS ===============================================


def choose_upgrade(pawn: Piece):
    """
    lets the user choose an upgrade for their pawn

    :param pawn: the pawn to upgrade
    """

    # loads images
    pawn.queen = PhotoImage(file=f'board/assets/{pawn.color}/queen.png').subsample(5, 5)
    pawn.knight = PhotoImage(file=f'board/assets/{pawn.color}/knight.png').subsample(5, 5)
    pawn.rook = PhotoImage(file=f'board/assets/{pawn.color}/rook.png').subsample(5, 5)
    pawn.bishop = PhotoImage(file=f'board/assets/{pawn.color}/bishop.png').subsample(5, 5)

    # places images
    squares = [Piece.CANVAS.create_rectangle(800, (y * 100) + 200, 900, (y * 100) + 300, fill='gray') for y in range(4)]
    queen_id = Piece.CANVAS.create_image(810, 215, image=pawn.queen, anchor=NW)
    knight_id = Piece.CANVAS.create_image(820, 315, image=pawn.knight, anchor=NW)
    rook_id = Piece.CANVAS.create_image(820, 415, image=pawn.rook, anchor=NW)
    bishop_id = Piece.CANVAS.create_image(815, 510, image=pawn.bishop, anchor=NW)

    # changes click function
    def click(event):
        """
        waits for user to click on choice

        :param event: the click event
        """

        # scales coordinates for easy indexing
        x = event.x // 100
        y = event.y // 100

        # makes sure a choice was selected
        if x == 8 and 2 <= y <= 5:
            Piece.CANVAS.delete(pawn.id)
            piece = None

            # handles when queen is selected
            if y == 2:
                moves = {(0, 'i'), (0, '-i'), ('i', 0), ('-i', 0), ('i', 'i'), ('i', '-i'), ('-i', 'i'), ('-i', '-i')}
                piece = Piece(pawn.coordinates, f'board/assets/{pawn.color}/queen.png', (10, 15), moves, None)

            # handles when knight is selected
            elif y == 3:
                moves = {(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)}
                piece = Piece(pawn.coordinates, f'board/assets/{pawn.color}/knight.png', (20, 15), moves, None)

            # handles when rook is selected
            elif y == 4:
                moves = {(0, 'i'), (0, '-i'), ('i', 0), ('-i', 0)}
                piece = Piece(pawn.coordinates, f'board/assets/{pawn.color}/rook.png', (20, 15), moves, None)

            # handles when bishop is selected
            elif y == 5:
                moves = {('i', 'i'), ('i', '-i'), ('-i', 'i'), ('-i', '-i')}
                piece = Piece(pawn.coordinates, f'board/assets/{pawn.color}/bishop.png', (15, 10), moves, None)

            # places new piece, deletes choice images and continues game
            Piece.board[pawn.coordinates[0]][pawn.coordinates[1]] = piece
            [Piece.CANVAS.delete(square) for square in squares]
            Piece.CANVAS.delete(queen_id)
            Piece.CANVAS.delete(knight_id)
            Piece.CANVAS.delete(rook_id)
            Piece.CANVAS.delete(bishop_id)
            Piece.CANVAS.bind('<Button-1>', Piece.click)

    Piece.CANVAS.bind('<Button-1>', click)


#  ================================================== PAWN PRE-TESTS ===================================================


def pawn_can_move_two(pawn: Piece) -> bool:
    """
    determines if the pawn can move forward 2 spaces

    :param pawn: the pawn to check
    :return: true if the pawn has not moved yet, false if it has
    """

    y = -2 if pawn.color == 'white' else 2
    test_one = pawn.has_not_moved and pawn_can_move_one(pawn)
    return test_one and Piece.board[pawn.coordinates[0]][pawn.coordinates[1] + y] is None


def pawn_can_attack_left(pawn: Piece) -> bool:
    """
    determines if there is an enemy piece in the forward left diagonal direction of the pawn

    :param pawn: the pawn to check
    :return: true if the pawn can attack, false if it cannot
    """

    # handles when pawn is at end of board
    if pawn.coordinates[0] == 0:
        return False

    # checks if pawn can attack if pawn is not at end of board
    y = -1 if pawn.color == 'white' else 1
    piece = Piece.board[pawn.coordinates[0] - 1][pawn.coordinates[1] + y] is not None
    return piece and Piece.board[pawn.coordinates[0] - 1][pawn.coordinates[1] + y].color != pawn.color


def pawn_can_attack_right(pawn: Piece) -> bool:
    """
    determines if there is an enemy piece in the forward right diagonal direction of the pawn

    :param pawn: the pawn to check
    :return: true if the pawn can attack, false if it cannot
    """

    # handles when pawn is at end of board
    if pawn.coordinates[0] == 7:
        return False

    # checks if pawn can attack if pawn is not at end of board
    y = -1 if pawn.color == 'white' else 1
    piece = Piece.board[pawn.coordinates[0] + 1][pawn.coordinates[1] + y] is not None
    return piece and Piece.board[pawn.coordinates[0] + 1][pawn.coordinates[1] + y].color != pawn.color


def pawn_can_move_one(pawn: Piece) -> bool:
    """
    determines if the pawn can move forward a space

    :param pawn: the pawn to check
    :return: false if there is a piece occupying the forward space true if there is not
    """

    y = -1 if pawn.color == 'white' else 1
    return Piece.board[pawn.coordinates[0]][pawn.coordinates[1] + y] is None


def pawn_can_upgrade(pawn: Piece) -> bool:
    """
    determines if the next move will cause the pawn to reach the end of the board

    :param pawn: the pawn to check
    :return: true if the next move will cause the pawn to reach the end of the board false if it will not
    """

    border = 1 if pawn.color == 'white' else 6
    return pawn_can_move_one(pawn) and pawn.coordinates[1] == border


def pawn_can_attack_left_upgrade(pawn: Piece) -> bool:
    """
    determines if the pawn can attack a piece in the diagonal left direction and upgrade after

    :param pawn: the pawn to check
    :return: true if the pawn can attack and upgrade false if it cannot
    """

    border = 1 if pawn.color == 'white' else 6
    return pawn_can_attack_left(pawn) and pawn.coordinates[1] == border


def pawn_can_attack_right_upgrade(pawn: Piece) -> bool:
    """
    determines if the pawn can attack a piece in the diagonal right direction and upgrade after

    :param pawn: the pawn to check
    :return: true if the pawn can attack and upgrade false if it cannot
    """

    border = 1 if pawn.color == 'white' else 6
    return pawn_can_attack_right(pawn) and pawn.coordinates[1] == border


#  =============================================== PAWN ACTION FUNCTIONS ===============================================


def pawn_move_two(pawn: Piece):
    """
    moves the pawn forward 2 spaces

    :param pawn: the pawn to move
    """

    y = -2 if pawn.color == 'white' else 2
    pawn.move((pawn.coordinates[0], pawn.coordinates[1] + y))


def pawn_attack_left(pawn: Piece):
    """
    makes the pawn attack to piece to the left

    :param pawn: the pawn to attack
    """

    y = -1 if pawn.color == 'white' else 1
    pawn.move((pawn.coordinates[0] - 1, pawn.coordinates[1] + y))


def pawn_attack_right(pawn: Piece):
    """
    makes the pawn attack the piece to the right

    :param pawn: the pawn to attack
    """

    y = -1 if pawn.color == 'white' else 1
    pawn.move((pawn.coordinates[0] + 1, pawn.coordinates[1] + y))


def pawn_move_one(pawn: Piece):
    """
    makes the pawn move forward 1 space

    :param pawn: the pawn to move
    """

    y = -1 if pawn.color == 'white' else 1
    pawn.move((pawn.coordinates[0], pawn.coordinates[1] + y))


def pawn_upgrade(pawn: Piece):
    """
    moves the pawn forward one space and upgrades the pawn

    :param pawn: the pawn to upgrade
    """

    pawn_move_one(pawn)
    choose_upgrade(pawn)


def pawn_attack_left_upgrade(pawn: Piece):
    """
    makes the pawn attack in the left diagonal direction and upgrades the pawn

    :param pawn: the pawn to move and upgrade
    """

    pawn_attack_left(pawn)
    choose_upgrade(pawn)


def pawn_attack_right_upgrade(pawn: Piece):
    """
    makes the pawn attack in the right diagonal direction and upgrades the pawn

    :param pawn: the pawn to move and upgrade
    """

    pawn_attack_right(pawn)
    choose_upgrade(pawn)


#  ================================================== KING PRE-TESTS ===================================================


def generate_king_can_move(move: tuple):
    """
    a wrapper function that generates a check move function for the king and a given move

    :param move: the move that the king can make in the form (displacement x, displacement y)
    :return: a wrapped function to check if the king can make the move
    """

    def wrapped_function(king: Piece) -> bool:
        """
        checks if the king can move in a given direction without putting it in check

        :param king: the king to check
        :return: true if the king can move, false if it cannot
        """

        x = king.coordinates[0] + move[0]
        y = king.coordinates[1] + move[1]
        not_blocked = 0 <= y <= 7 and not (Piece.board[x][y] is not None and Piece.board[x][y].color == king.color)
        return not_blocked and Piece.not_blocked((x, y), king.color)

    return wrapped_function


def king_can_castle_left(king: Piece) -> bool:
    """
    checks if the king can castle with the rook on the left

    :param king: the king to check if it can castle
    :return: true if the king can castle false if it cannot
    """

    y = 7 if king.color == 'white' else 0
    not_moved = king.has_not_moved and Piece.board[0][y] is not None and Piece.board[0][y].has_not_moved
    no_pieces_between = Piece.board[1][y] is None and Piece.board[2][y] is None and Piece.board[3][y] is None
    not_in_check = Piece.not_blocked(king.coordinates, king.color)
    no_checks = Piece.not_blocked((2, y), king.color) and Piece.not_blocked((3, y), king.color)
    return not_moved and no_pieces_between and not_in_check and no_checks


def king_can_castle_right(king: Piece) -> bool:
    """
    checks if the king can castle with the rook on the right

    :param king: the king to check if it can castle
    :return: true if the king can castle false if it cannot
    """

    y = 7 if king.color == 'white' else 0
    not_moved = king.has_not_moved and Piece.board[7][y] is not None and Piece.board[7][y].has_not_moved
    no_pieces_between = Piece.board[5][y] is None and Piece.board[6][y] is None
    not_in_check = Piece.not_blocked(king.coordinates, king.color)
    no_checks = Piece.not_blocked((5, y), king.color) and Piece.not_blocked((6, y), king.color)
    return not_moved and no_pieces_between and not_in_check and no_checks


#  =============================================== KING ACTION FUNCTIONS ===============================================


def generate_king_move(move: tuple):
    """
    a wrapper function that generates a move function for the king and a given move

    :param move: the move that the king can make in the form (displacement x, displacement y)
    :return: a wrapped function to check if the king can make the move
    """

    def wrapped_function(king: Piece):
        """
        moves the king

        :param king: the king to move
        """

        king.move((king.coordinates[0] + move[0], king.coordinates[1] + move[1]))

    return wrapped_function


def king_castle_left(king: Piece):
    """
    castles the king with the rook to the left

    :param king: the king to castle
    """

    y = 7 if king.color == 'white' else 0
    king.move((2, y))
    Piece.board[0][y].move((3, y))


def king_castle_right(king: Piece):
    """
    castles the king with the rook to the right

    :param king: the king to castle
    """

    y = 7 if king.color == 'white' else 0
    king.move((6, y))
    Piece.board[7][y].move((5, y))
