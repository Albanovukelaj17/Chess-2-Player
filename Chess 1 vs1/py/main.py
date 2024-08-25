import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1600, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

font = pygame.font.SysFont(None, 24)

pieces = {}
SQUARE_SIZE = 100

column_to_alpha = { 0 : 'A', 1: 'B', 2: 'C', 3: 'D',4 : 'E', 5: 'F',6: 'G',7: 'H'}

moves = []
def chess_notation(row,column):
    return f"{column_to_alpha[column]}{8-row}"

def draw_board():
    WIN.fill(pygame.Color("black"))
    colors = [pygame.Color("white"), pygame.Color("gray")]
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H"]
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8"]
    for row in range(8):
        for columns in range(8):
            color = colors[(row + columns) % 2]
            pygame.draw.rect(WIN, color, pygame.Rect(columns * SQUARE_SIZE + 50, row * SQUARE_SIZE + 50, SQUARE_SIZE, SQUARE_SIZE))

            if row == 7:
                text = font.render(alphabet[columns], True, pygame.Color("red"))
                WIN.blit(text, (columns * SQUARE_SIZE + 100 - text.get_width() // 2, HEIGHT - 25))
            if columns == 0:  # First column (where numbers should appear)
                text_surface = font.render(numbers[7 - row], True, pygame.Color("red"))
                WIN.blit(text_surface, (25, row * SQUARE_SIZE + 100 - text_surface.get_height() // 2))

def load_piece(image_path):
    try:
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
        return image
    except pygame.error as e:
        print(f"Unable to load image: {e}")
        sys.exit()

def place_black_pieces():
    pawn_image = load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/black pieces/Chess_pdt60.png")
    for col in range(8):
        pieces[chess_notation(1, col)] = ("black_pawn", pawn_image)

    pieces[chess_notation(0, 0)] = ("black_rook", load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/black pieces/Chess_rdt60.png"))
    pieces[chess_notation(0, 7)] = ("black_rook", load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/black pieces/Chess_rdt60.png"))

    pieces[chess_notation(0, 2)] = ("black_bishop", load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/black pieces/Chess_bdt60.png"))
    pieces[chess_notation(0, 5)] = ("black_bishop", load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/black pieces/Chess_bdt60.png"))

    pieces[chess_notation(0, 1)] = ("black_knight", load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/black pieces/Chess_ndt60.png"))
    pieces[chess_notation(0, 6)] = ("black_knight", load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/black pieces/Chess_ndt60.png"))

    pieces[chess_notation(0, 3)] = ("black_queen", load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/black pieces/Chess_qdt60.png"))
    pieces[chess_notation(0, 4)] = ("black_king", load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/black pieces/Chess_kdt60.png"))

def place_white_pieces():
    pawn_image = load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/white pieces/Chess_plt60.png")
    for col in range(8):
        pieces[chess_notation(6, col)] = ("white_pawn", pawn_image)

    pieces[chess_notation(7, 0)] = ("white_rook", load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/white pieces/Chess_rlt60.png"))
    pieces[chess_notation(7, 7)] = ("white_rook", load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/white pieces/Chess_rlt60.png"))

    pieces[chess_notation(7, 2)] = ("white_bishop", load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/white pieces/Chess_blt60.png"))
    pieces[chess_notation(7, 5)] = ("white_bishop", load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/white pieces/Chess_blt60.png"))

    pieces[chess_notation(7, 1)] = ("white_knight", load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/white pieces/Chess_nlt60.png"))
    pieces[chess_notation(7, 6)] = ("white_knight", load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/white pieces/Chess_nlt60.png"))

    pieces[chess_notation(7, 3)] = ("white_queen", load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/white pieces/Chess_qlt60.png"))
    pieces[chess_notation(7, 4)] = ("white_king", load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/white pieces/Chess_klt60.png"))

def draw_pieces():
    for position, (piece_name, piece_image) in pieces.items():
        col = ord(position[0]) - ord('A')
        row = 8 -int(position[1])
        WIN.blit(piece_image, (col * SQUARE_SIZE + 50, row * SQUARE_SIZE + 50))

def get_square_under_mouse():
    mouse_pos = pygame.mouse.get_pos()
    column = (mouse_pos[0] - 50) // SQUARE_SIZE
    row = (mouse_pos[1] - 50) // SQUARE_SIZE
    if 0 <= row < 8 and 0 <= column< 8:
        return chess_notation(row, column)
    return None

def move_piece(start_pos, end_pos):

    if move_validator(start_pos, end_pos):
             if end_pos in pieces:
                 del pieces[end_pos]
             piece_name, _ = pieces[start_pos]
             moves.append(f"{piece_name}: {start_pos} to {end_pos}")
             pieces[end_pos] = pieces.pop(start_pos)


def draw_move_list():
    start_y = 50
    y_offset = 30
    start_x_white = 900
    start_x_black = 1100

    for i, move in enumerate(moves):
        move_text = font.render(move, True, pygame.Color("white"))


        if i % 2 == 0:
            WIN.blit(move_text, (start_x_white, start_y + (i // 2) * y_offset))
        else:
            WIN.blit(move_text, (start_x_black, start_y + (i // 2) * y_offset))


def move_validator(start_pos, end_pos):
    pieces_name, _ = pieces[start_pos]
    if pieces_name== "white_pawn":
        return move_validator_white_pawn(start_pos,end_pos)
    elif pieces_name== "black_pawn":
        return move_validator_black_pawn(start_pos,end_pos)
    return True

def move_validator_white_pawn(start_pos, end_pos):
    start_row= int(start_pos[1])  #A1 -> 1
    start_row_piece_notation= -start_row+ 8
    start_column= ord(start_pos[0])-ord('A')
    end_row = int(end_pos[1])
    end_column= ord(end_pos[0])-ord('A')

    one_step_forward =chess_notation(start_row_piece_notation-1, start_column)
    two_step_forward = chess_notation(start_row_piece_notation-2, start_column)

    if start_column +1 <8 :
        right_step_diagonal = chess_notation(start_row_piece_notation-1, start_column+1)
    else:
        right_step_diagonal = None #index out of bounds exception

    if start_column - 1 >= 0:
        left_step_diagonal = chess_notation(start_row_piece_notation-1, start_column-1)
    else:
        left_step_diagonal = None #index out of bounds exception

    if end_pos in pieces:
        piece_name, _= pieces[end_pos]
        if "white" in piece_name:
          return False #not same color

    if start_row == 2 and end_row == 4 and start_column == end_column and one_step_forward not in pieces and two_step_forward not in pieces :
        return True #first 2 steps

    if start_row +1 == end_row and start_column== end_column and one_step_forward not in pieces:
        return True #normal 1 step

    if start_row +1 == end_row and start_column!= end_column:
           if start_column +1 == end_column and right_step_diagonal in pieces:
               return True #take diagonally right

    if start_row + 1 == end_row and start_column != end_column:
            if left_step_diagonal in pieces and  start_column -1 == end_column:
                 return True #take diagonally left
    return False


def move_validator_black_pawn(start_pos, end_pos):
    start_row = int(start_pos[1])  # A1 -> 1
    start_row_piece_notation = -start_row + 8
    start_column = ord(start_pos[0]) - ord('A')
    end_row = int(end_pos[1])
    end_column = ord(end_pos[0]) - ord('A')

    one_step_forward = chess_notation(start_row_piece_notation + 1, start_column)
    two_step_forward = chess_notation(start_row_piece_notation + 2, start_column)

    if start_column + 1 < 8:
        left_step_diagonal = chess_notation(start_row_piece_notation +1, start_column + 1)
    else:
        left_step_diagonal = None #index out of bounds exception

    if start_column - 1 >= 0:
        right_step_diagonal = chess_notation(start_row_piece_notation +1, start_column - 1)
    else:
        right_step_diagonal = None #index out of bounds exception


    if end_pos in pieces:
        piece_name, _ = pieces[end_pos]
        if "black" in piece_name:
            return False  # not same color

    if start_row == 7 and end_row == 5 and start_column == end_column and one_step_forward not in pieces and two_step_forward not in pieces:
        return True  # first 2 steps

    if start_row -1 == end_row and start_column == end_column and one_step_forward not in pieces:
        return True  # normal 1 step

    if start_row -1 == end_row and start_column != end_column:
        if start_column -1 == end_column and right_step_diagonal in pieces:
            return True  # take diagonally right

    if start_row -1 == end_row and start_column != end_column:
        if start_column + 1 == end_column and left_step_diagonal in pieces:
            return True  # take diagonally left
    return False


def main():

    draw_board()
    place_black_pieces()
    place_white_pieces()


    selected_piece = None

    while True:
        draw_board()
        draw_pieces()
        draw_move_list()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_square = get_square_under_mouse()
                if clicked_square:
                    if selected_piece:
                        move_piece(selected_piece, clicked_square)
                        selected_piece = None
                    elif clicked_square in pieces:
                        selected_piece = clicked_square

        pygame.display.update()

if __name__ == "__main__":
    main()
