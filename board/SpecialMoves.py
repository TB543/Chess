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
        --> pre-test to see if king must be moved (when in check)
        --> pre-test to see if king is in checkmate and game has been lost
        --> pre-test to see if king can be castled

        --> action function to move king to available spots without being put in check/checkmate
        --> action function for when king must be moved (in check)
        --> action function when game has been lost (checkmate)
        --> action function to castle the king
"""


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

    border = 1 if pawn.color == 'white' else 7
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
