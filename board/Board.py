from Piece import Piece
from SpecialMoves import *


"""
a few functions for board management:
    1) functions to create each piece
    2) function to initialize the board
"""


def create_pawn(coordinates: tuple, color: str):
    """
    creates a pawn

    :param coordinates: the coordinates of the chess piece in the form (0-7, 0-7)
    :param color: the color of the piece, can be either 'black' or 'white'
    """

    multiplier = -1 if color == 'white' else 1
    specials = {(0, 2 * multiplier, 0): [(pawn_can_move_two, pawn_move_two)],
                (-1, 1 * multiplier, 1): [(pawn_can_attack_left_upgrade, pawn_attack_left_upgrade),
                                          (pawn_can_attack_left, pawn_attack_left)],
                (1, 1 * multiplier, 2): [(pawn_can_attack_right_upgrade, pawn_attack_right_upgrade),
                                         (pawn_can_attack_right, pawn_attack_right)],
                (0, 1 * multiplier, 3): [(pawn_can_upgrade, pawn_upgrade),
                                         (pawn_can_move_one, pawn_move_one)]}
    Piece(coordinates, f'board/assets/{color}/pawn.png', (25, 20), None, specials)


def create_bishop(coordinates: tuple, color: str):
    """
    creates a bishop

    :param coordinates: the coordinates of the chess piece in the form (0-7, 0-7)
    :param color: the color of the piece, can be either 'black' or 'white'
    """

    moves = {('i', 'i'), ('i', '-i'), ('-i', 'i'), ('-i', '-i')}
    Piece(coordinates, f'board/assets/{color}/bishop.png', (15, 10), moves, None)


def create_rook(coordinates: tuple, color: str):
    """
    creates a rook

    :param coordinates: the coordinates of the chess piece in the form (0-7, 0-7)
    :param color: the color of the piece, can be either 'black' or 'white'
    """

    moves = {(0, 'i'), (0, '-i'), ('i', 0), ('-i', 0)}
    Piece(coordinates, f'board/assets/{color}/rook.png', (20, 15), moves, None)


def create_knight(coordinates: tuple, color: str):
    """
    creates a knight

    :param coordinates: the coordinates of the chess piece in the form (0-7, 0-7)
    :param color: the color of the piece, can be either 'black' or 'white'
    """

    moves = {(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)}
    Piece(coordinates, f'board/assets/{color}/knight.png', (20, 15), moves, None)


def create_queen(coordinates: tuple, color: str):
    """
    creates a queen

    :param coordinates: the coordinates of the chess piece in the form (0-7, 0-7)
    :param color: the color of the piece, can be either 'black' or 'white'
    """

    moves = {(0, 'i'), (0, '-i'), ('i', 0), ('-i', 0), ('i', 'i'), ('i', '-i'), ('-i', 'i'), ('-i', '-i')}
    Piece(coordinates, f'board/assets/{color}/queen.png', (10, 15), moves, None)


def create_king(coordinates: tuple, color: str):
    """
    creates a king

    :param coordinates: the coordinates of the chess piece in the form (0-7, 0-7)
    :param color: the color of the piece, can be either 'black' or 'white' todo finish king move set and add turns
    """

    Piece(coordinates, f'board/assets/{color}/king.png', (10, 10), None, None)


def initialize_board():
    """
    places all the pieces on the board in the correct starting configuration
    """

    # creates the black pieces
    create_rook((0, 0), 'black')
    create_knight((1, 0), 'black')
    create_bishop((2, 0), 'black')
    create_queen((3, 0), 'black')
    create_king((4, 0), 'black')
    create_bishop((5, 0), 'black')
    create_knight((6, 0), 'black')
    create_rook((7, 0), 'black')
    [create_pawn((i, 1), 'black') for i in range(8)]

    # creates the white pieces
    [create_pawn((i, 6), 'white') for i in range(8)]
    create_rook((0, 7), 'white')
    create_knight((1, 7), 'white')
    create_bishop((2, 7), 'white')
    create_queen((3, 7), 'white')
    create_king((4, 7), 'white')
    create_bishop((5, 7), 'white')
    create_knight((6, 7), 'white')
    create_rook((7, 7), 'white')
