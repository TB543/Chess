"""
a few functions for special moves that the following pieces can have (note: not all of these functions will be in this
file as some can be written as one line lambda functions when creating the piece):

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
