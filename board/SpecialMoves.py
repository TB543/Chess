from Piece import Piece


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

    return pawn.has_not_moved


def pawn_can_attack_left(pawn: Piece) -> bool:
    """
    determines if there is an enemy piece in the forward left diagonal direction of the pawn

    :param pawn: the pawn to check
    :return: true if the pawn can attack, false if it cannot
    """

    y = -1 if pawn.color == 'white' else 1
    return pawn.board[pawn.coordinates[0] - 1][pawn.coordinates[1] + y] is not None


def pawn_can_attack_right(pawn: Piece) -> bool:
    """
    determines if there is an enemy piece in the forward right diagonal direction of the pawn

    :param pawn: the pawn to check
    :return: true if the pawn can attack, false if it cannot
    """

    y = -1 if pawn.color == 'white' else 1
    return pawn.board[pawn.coordinates[0] + 1][pawn.coordinates[1] + y] is not None


def pawn_can_move_one(pawn: Piece) -> bool:
    """
    determines if the pawn can move forward a space

    :param pawn: the pawn to check
    :return: false if there is a piece occupying the forward space true if there is not
    """

    y = -1 if pawn.color == 'white' else 1
    return pawn.board[pawn.coordinates[0]][pawn.coordinates[1] + y] is None


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

    border = 1 if pawn.color == 'white' else 7
    return pawn_can_attack_left(pawn) and pawn.coordinates[1] == border


def pawn_can_attack_right_upgrade(pawn: Piece) -> bool:
    """
    determines if the pawn can attack a piece in the diagonal right direction and upgrade after

    :param pawn: the pawn to check
    :return: true if the pawn can attack and upgrade false if it cannot
    """

    border = 1 if pawn.color == 'white' else 7
    return pawn_can_attack_right(pawn) and pawn.coordinates[1] == border
