from tkinter import Canvas, PhotoImage


class Piece:
    """
    a class representing a chess piece that contains the following attributes:
        1) a canvas where the pieces will be drawn to
        2) a matrix representing the game board

    instances of the class contains the following attributes
        1) coordinates - the location of the piece on the board
        2) image - the image for the piece
        3) moves - the possible moves for the piece
        4) specials - the special moves for the price

    class contains the following functions:
        1) __init__ - creates the chess piece
        2) toggle_show_moves - display or hides possible moves for the piece
        3) move - moves the piece
        4) kill - removes the piece from the board
    """

    # creates the canvas and the board matrix
    CANVAS = Canvas(width=800, height=800)
    CANVAS.pack()
    CANVAS.master.resizable(False, False)
    board = [[None] * 8] * 8

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
            the piece can be moved infinitely in the y direction, ('i', 0) means the piece can be moved infinitely in
            the x direction and ('i', 'i') means the piece can move infinitely in the diagonal direction
        :param specials: a dict containing special moves for the piece where the key is the move (see param moves for
            more info) and the value is a tuple of functions, where the function at index 0 is the pre-test function to
            determine if the move can be made (returns true or false) and the function at index 1 is the action
            function, the function that will be called when the move is made
        """

        # creates fields
        self.coordinates = coordinates
        self.image = PhotoImage(file=image).subsample(4, 4)
        self.moves = moves
        self.specials = specials
        self.has_moved = False

        # places piece on board
        x = (self.coordinates[0] * 140) + offset[0]
        y = (self.coordinates[1] * 140) + offset[1]
        self.CANVAS.create_image(x, y, image=self.image)

    def toggle_show_moves(self):
        """
        performs one of the following actions:
            1) displays the possible moves for the piece when clicked
            2) hides possible moves when piece is clicked and moves are already displayed

        additionally if a different piece is already displaying moves, its moves will be hidden before showing current
        pieces moves
        """

    def move(self, position: tuple):
        """
        moves the piece to the new location and kills the piece in that new location if there is one
        additionally if moves are displayed they will be hidden after the move

        :param position: the new position to move the piece to
        """

    def kill(self):
        """
        removes the piece from the board when it is taken out
        """
