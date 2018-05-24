"""An implementation of Tetris for OpenAI Gym using Pygame."""
import random, time, pygame, sys
from pygame.locals import *
# TODO: numpy randomness


# the framerate to maintain during gameplay
FPS = 144
# the width of the main game window
WINDOWWIDTH = 640
# the height of the main game window
WINDOWHEIGHT = 430
# the number of pixels to use for a box
BOXSIZE = 20
# the number of horizontal boxes on the board (classic Tetris uses 10)
BOARDWIDTH = 10
# the number of vertical boxes on the board (classic Tetris uses 20)
BOARDHEIGHT = 20
# the value denoting a blank pixel in a template
BLANK = '.'


MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1


# the number of pixels to pad the game from the right border of the screen
XMARGIN = 10
# the number of pixels to pad the game from the top border of the screen
TOPMARGIN = 20


# TODO: use a csv and numpy to remove this nastiness
#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)


BORDERCOLOR = WHITE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS = (BLUE, GREEN, RED, YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)


TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5


S_SHAPE_TEMPLATE = [
    ['.....',
     '.....',
     '..OO.',
     '.OO..',
     '.....'],
    ['.....',
     '..O..',
     '..OO.',
     '...O.',
     '.....']
]

Z_SHAPE_TEMPLATE = [
    ['.....',
     '.....',
     '.OO..',
     '..OO.',
     '.....'],
    ['.....',
     '..O..',
     '.OO..',
     '.O...',
     '.....']
]

I_SHAPE_TEMPLATE = [
    ['..O..',
     '..O..',
     '..O..',
     '..O..',
     '.....'],
    ['.....',
     '.....',
     'OOOO.',
     '.....',
     '.....']
]

O_SHAPE_TEMPLATE = [
    ['.....',
     '.....',
     '.OO..',
     '.OO..',
     '.....']
]

J_SHAPE_TEMPLATE = [
    ['.....',
     '.O...',
     '.OOO.',
     '.....',
     '.....'],
    ['.....',
     '..OO.',
     '..O..',
     '..O..',
     '.....'],
    ['.....',
     '.....',
     '.OOO.',
     '...O.',
     '.....'],
    ['.....',
     '..O..',
     '..O..',
     '.OO..',
     '.....']
]

L_SHAPE_TEMPLATE = [
    ['.....',
     '...O.',
     '.OOO.',
     '.....',
     '.....'],
    ['.....',
     '..O..',
     '..O..',
     '..OO.',
     '.....'],
    ['.....',
     '.....',
     '.OOO.',
     '.O...',
     '.....'],
    ['.....',
     '.OO..',
     '..O..',
     '..O..',
     '.....']
]

T_SHAPE_TEMPLATE = [
    ['.....',
     '..O..',
     '.OOO.',
     '.....',
     '.....'],
    ['.....',
     '..O..',
     '..OO.',
     '..O..',
     '.....'],
    ['.....',
     '.....',
     '.OOO.',
     '..O..',
     '.....'],
    ['.....',
     '..O..',
     '.OO..',
     '..O..',
     '.....']
]


PIECES = {
    'S': S_SHAPE_TEMPLATE,
    'Z': Z_SHAPE_TEMPLATE,
    'J': J_SHAPE_TEMPLATE,
    'L': L_SHAPE_TEMPLATE,
    'I': I_SHAPE_TEMPLATE,
    'O': O_SHAPE_TEMPLATE,
    'T': T_SHAPE_TEMPLATE
}


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Tetris')

    showTextScreen('Tetris')
    while True:
        runGame()
        showTextScreen('Game Over')


def runGame():
    # setup variables for the start of the game
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False # note: there is no movingUp variable
    movingLeft = False
    movingRight = False
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()

    # game loop
    while True:
        if fallingPiece is None:
            # No falling piece in play, so start a new piece at the top
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            # reset lastFallTime
            lastFallTime = time.time()

            # can't fit a new piece on the board, so game over
            if not isValidPosition(board, fallingPiece):
                return

        checkForQuit()
        # event handling loop
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_p:
                    # Pausing the game
                    DISPLAYSURF.fill(BGCOLOR)
                    # pause until a key press
                    showTextScreen('Paused')
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif event.key == K_LEFT or event.key == K_a:
                    movingLeft = False
                elif event.key == K_RIGHT or event.key == K_d:
                    movingRight = False
                elif event.key == K_DOWN or event.key == K_s:
                    movingDown = False

            elif event.type == KEYDOWN:
                # moving the piece sideways
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()

                elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()

                # rotating the piece (if there is room to rotate)
                elif event.key == K_UP or event.key == K_w:
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                elif event.key == K_q: # rotate the other direction
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])

                # making the piece fall faster with the down key
                elif event.key == K_DOWN or event.key == K_s:
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                # move the current piece all the way down
                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1

        # handle moving the piece because of user input
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        # let the piece fall if it is time to fall
        if time.time() - lastFallTime > fallFreq:
            # see if the piece has landed
            if not isValidPosition(board, fallingPiece, adjY=1):
                # falling piece has landed, set it on the board
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else:
                # piece did not land, just move the piece down
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        # drawing everything on the screen
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if fallingPiece is not None:
            drawPiece(fallingPiece)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    """Terminate the game and exit."""
    pygame.quit()
    # TODO: sys.exit not necessary in gym env
    sys.exit()


def checkForKeyPress():
    """Look for a KEYUP event in the event queue and remove KEYDOWN events."""
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key

    return None


def showTextScreen(text: str) -> None:
    """Display a string in the center of the screen until a key press."""
    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)
    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)
    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
    # lock until a key press event
    while checkForKeyPress() is None:
        pygame.display.update()
        FPSCLOCK.tick()


def checkForQuit() -> None:
    """Check if the game has quit and terminate if so."""
    # get all the QUIT events
    for event in pygame.event.get(QUIT):
        # terminate if any QUIT events are present
        terminate()
    # get all the KEYUP events
    for event in pygame.event.get(KEYUP):
        # terminate if the KEYUP event was for the Esc key
        if event.key == K_ESCAPE:
            terminate()
        # put the other KEYUP event objects back
        pygame.event.post(event)


def calculateLevelAndFallFreq(score: float) -> tuple:
    """Return the level the player is on based on score and the fall speed."""
    # get the level that the player is on
    level = int(score / 10) + 1
    # get the frequency with which to move pieces down
    fall_freq = 0.27 - (level * 0.02)

    return level, fall_freq


def getNewPiece() -> dict:
    """Return a random new piece in a random rotation."""
    shape = random.choice(list(PIECES.keys()))
    # start the new piece above the board (i.e. y < 0)
    # TODO: no random color assignment? standard colors for shapes
    return {
        'shape': shape,
        'rotation': random.randint(0, len(PIECES[shape]) - 1),
        'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
        'y': -2,
        'color': random.randint(0, len(COLORS) - 1)
    }


def addToBoard(board, piece) -> None:
    """Fill in the board based on piece's location, shape, and rotation."""
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']


def getBlankBoard() -> list:
    """Return a new blank board data structure."""
    board = []
    for _ in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board


def isOnBoard(x, y) -> bool:
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def isValidPosition(board, piece, adjX=0, adjY=0) -> bool:
    """Return True if the piece is within the board and not colliding."""
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            is_above_board = y + piece['y'] + adjY < 0
            is_blank = PIECES[piece['shape']][piece['rotation']][y][x] == BLANK
            if is_above_board or is_blank:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False

    return True


def isCompleteLine(board, y) -> bool:
    # Return True if the line filled with boxes with no gaps.
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False

    return True


def removeCompleteLines(board) -> int:
    """Remove completed lines on the board.

    Args:
        board: the board to remove completed lines from

    Returns:
        The number of completed lines removed from the board

    Note:
        - lines are moved down after complete ones are removed

    """
    num_lines_removed = 0
    # start y at the bottom of the board
    y = BOARDHEIGHT - 1
    while y >= 0:
        if isCompleteLine(board, y):
            # Remove the line and pull boxes down by one line.
            for pull_down_y in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pull_down_y] = board[x][pull_down_y - 1]
            # Set very top line to blank.
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            num_lines_removed += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also
            # complete, it will be removed.
        else:
            # move on to check next row up
            y -= 1

    return num_lines_removed


def convertToPixelCoords(box_x, box_y) -> tuple:
    """Convert x, y coordinates of tetris board to pixel coordinates."""
    return (XMARGIN + (box_x * BOXSIZE)), (TOPMARGIN + (box_y * BOXSIZE))


def drawBox(
    box_x: int,
    box_y: int,
    color: int,
    pixel_x: int = None,
    pixel_y: int = None,
) -> None:
    """
    Draw a single box of a piece at given coordinates.

    Args:
        box_x: the x coordinate in the Tetris grid
        box_y: the y coordinate in the Tetris grid
        color: the color of the box (as an index)
        pixel_x: optional x pixel coordinate to override the box coordinate
        pixel_y: optional y pixel coordinate to override the box coordinate

    Returns:
        None

    """
    # don't draw empty boxes
    if color == BLANK:
        return
    # convert the box coordinates to pixel coordinates if none are specified
    if pixel_x is None and pixel_y is None:
        pixel_x, pixel_y = convertToPixelCoords(box_x, box_y)
    # draw the main background box
    main_rect = (pixel_x + 1, pixel_y + 1, BOXSIZE - 1, BOXSIZE - 1)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], main_rect)
    # draw the smaller depth perspective effect box
    depth_rect = (pixel_x + 1, pixel_y + 1, BOXSIZE - 4, BOXSIZE - 4)
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], depth_rect)


def drawBoard(board):
    # draw the border around the board
    border_rect = (
        XMARGIN - 3,
        TOPMARGIN - 7,
        BOARDWIDTH * BOXSIZE + 8,
        BOARDHEIGHT * BOXSIZE + 8
    )
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, border_rect, 5)

    # fill the background of the board
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    # draw the individual boxes on the board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])


def drawStatus(score, level):
    # draw the score text
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    # draw the level text
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150, 50)
    DISPLAYSURF.blit(levelSurf, levelRect)


def drawPiece(piece, pixel_x=None, pixel_y=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixel_x == None and pixel_y == None:
        # if pixel_x & pixel_y hasn't been specified, use the location stored in the piece data structure
        pixel_x, pixel_y = convertToPixelCoords(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixel_x + (x * BOXSIZE), pixel_y + (y * BOXSIZE))


def drawNextPiece(piece):
    # draw the "next" text
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)
    # draw the "next" piece
    drawPiece(piece, pixel_x=WINDOWWIDTH-120, pixel_y=100)


if __name__ == '__main__':
    main()
