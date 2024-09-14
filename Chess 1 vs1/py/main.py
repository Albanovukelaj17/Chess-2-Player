import pygame
import sys

# Initialize Pygame and create a display window for the chess game.
pygame.init()

# Set up display dimensions and window title.
WIDTH, HEIGHT = 1300, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

# Define basic configurations like font and square size.
font = pygame.font.SysFont(None, 24)
SQUARE_SIZE = 100
pieces = {}  # Dictionary to store the pieces on the board.
last_move = None
column_to_alpha = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
moves = []  # List of all moves made during the game.
selected_square = None  # Tracks the currently selected square.
selected_legal_moves = []  # Legal moves for the selected piece.

# Track if important pieces (king/rook) have moved for castling logic.
white_king_moved = False
black_king_moved = False
white_rook_kingside_moved = False
white_rook_queenside_moved = False
black_rook_kingside_moved = False
black_rook_queenside_moved = False

# Variables to manage game state like checkmate and winning player.
checkmate = False
winning_player = ""


# Convert row and column into chess notation (e.g., A1, H8).
def chess_notation(row, column):
    return f"{column_to_alpha[column]}{8 - row}"


# Draw the chessboard and highlight selected squares and legal moves.
def draw_board(selected_legal_moves):
    global checkmate, winning_player
    WIN.fill(pygame.Color("black"))
    colors = [pygame.Color("white"), pygame.Color("gray")]
    selected_color = pygame.Color("light blue")
    light_blue = pygame.Color("light blue")
    move_highlight_color = pygame.Color(min(light_blue.r + 50, 255),
                                        min(light_blue.g + 50, 255),
                                        min(light_blue.b + 50, 255))
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H"]
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8"]

    # Loop through rows and columns to draw the chess squares.
    for row in range(8):
        for columns in range(8):
            color = colors[(row + columns) % 2]
            # Highlight the selected square.
            if selected_square:
                selected_row = 8 - int(selected_square[1])
                selected_column = ord(selected_square[0]) - ord('A')
                if selected_row == row and selected_column == columns:
                    color = selected_color
            # Highlight legal moves.
            pos = chess_notation(row, columns)
            if pos in selected_legal_moves:
                color = move_highlight_color
            pygame.draw.rect(WIN, color,
                             pygame.Rect(columns * SQUARE_SIZE + 50, row * SQUARE_SIZE + 50, SQUARE_SIZE, SQUARE_SIZE))

            # Draw column and row labels (A-H and 1-8).
            if row == 7:
                text = font.render(alphabet[columns], True, pygame.Color("red"))
                WIN.blit(text, (columns * SQUARE_SIZE + 100 - text.get_width() // 2, HEIGHT - 25))
            if columns == 0:
                text_surface = font.render(numbers[7 - row], True, pygame.Color("red"))
                WIN.blit(text_surface, (25, row * SQUARE_SIZE + 100 - text_surface.get_height() // 2))

    # Display checkmate message if the game is over.
    if checkmate:
        draw_checkmate_message(winning_player)


# Load an image for a chess piece and resize it to fit the squares.
def load_piece(image_path):
    try:
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
        return image
    except pygame.error as e:
        print(f"Unable to load image: {e}")
        sys.exit()


# Place black pieces on the board (initial positions).
def place_black_pieces():
    pawn_image = load_piece(
        "/Users/albanovukelaj/Desktop/Motherfucker/Chess-2-Player/Chess 1 vs1/black pieces/Chess_pdt60.png")
    for col in range(8):
        pieces[chess_notation(1, col)] = ("black_pawn", pawn_image)
    pieces[chess_notation(0, 0)] = ("black_rook", load_piece("../black pieces/Chess_rdt60.png"))
    pieces[chess_notation(0, 7)] = ("black_rook", load_piece("../black pieces/Chess_rdt60.png"))
    pieces[chess_notation(0, 2)] = ("black_bishop", load_piece("../black pieces/Chess_bdt60.png"))
    pieces[chess_notation(0, 5)] = ("black_bishop", load_piece("../black pieces/Chess_bdt60.png"))
    pieces[chess_notation(0, 1)] = ("black_knight", load_piece("../black pieces/Chess_ndt60.png"))
    pieces[chess_notation(0, 6)] = ("black_knight", load_piece("../black pieces/Chess_ndt60.png"))
    pieces[chess_notation(0, 3)] = ("black_queen", load_piece("../black pieces/Chess_qdt60.png"))
    pieces[chess_notation(0, 4)] = ("black_king", load_piece("../black pieces/Chess_kdt60.png"))


# Place white pieces on the board (initial positions).
def place_white_pieces():
    pawn_image = load_piece("../white pieces/Chess_plt60.png")
    for col in range(8):
        pieces[chess_notation(6, col)] = ("white_pawn", pawn_image)
    pieces[chess_notation(7, 0)] = ("white_rook", load_piece("../white pieces/Chess_rlt60.png"))
    pieces[chess_notation(7, 7)] = ("white_rook", load_piece("../white pieces/Chess_rlt60.png"))
    pieces[chess_notation(7, 2)] = ("white_bishop", load_piece("../white pieces/Chess_blt60.png"))
    pieces[chess_notation(7, 5)] = ("white_bishop", load_piece("../white pieces/Chess_blt60.png"))
    pieces[chess_notation(7, 1)] = ("white_knight", load_piece("../white pieces/Chess_nlt60.png"))
    pieces[chess_notation(7, 6)] = ("white_knight", load_piece("../white pieces/Chess_nlt60.png"))
    pieces[chess_notation(7, 3)] = ("white_queen", load_piece("../white pieces/Chess_qlt60.png"))
    pieces[chess_notation(7, 4)] = ("white_king", load_piece("../white pieces/Chess_klt60.png"))


# Draw all chess pieces on the board based on their current positions.
def draw_pieces():
    for position, (piece_name, piece_image) in pieces.items():
        col = ord(position[0]) - ord('A')
        row = 8 - int(position[1])
        WIN.blit(piece_image, (col * SQUARE_SIZE + 50, row * SQUARE_SIZE + 50))


# Get the square currently under the mouse cursor.
def get_square_under_mouse():
    mouse_pos = pygame.mouse.get_pos()
    column = (mouse_pos[0] - 50) // SQUARE_SIZE
    row = (mouse_pos[1] - 50) // SQUARE_SIZE
    if 0 <= row < 8 and 0 <= column < 8:
        return chess_notation(row, column)
    return None


# Draw the list of moves made so far in the game.
def draw_move_list():
    start_y = 50
    y_offset = 30
    start_x_white = 900
    start_x_black = 1100

    # Titles for the move list.
    white_title = font.render("White side", True, pygame.Color("white"))
    black_title = font.render("Black side", True, pygame.Color("white"))

    WIN.blit(white_title, (start_x_white, start_y - 30))
    WIN.blit(black_title, (start_x_black, start_y - 30))

    # Display each move in two columns (one for white, one for black).
    for i, move in enumerate(moves):
        move_text = font.render(move, True, pygame.Color("white"))

        if i % 2 == 0:
            WIN.blit(move_text, (start_x_white, start_y + (i // 2) * y_offset))
        else:
            WIN.blit(move_text, (start_x_black, start_y + (i // 2) * y_offset))


# Move a piece from the start position to the end position.
def move_piece(start_pos, end_pos):
    global last_move, selected_square
    if start_pos not in pieces:
        return  # No piece at the start position, return.

    # Check for valid move and apply move.
    piece_name, _ = pieces[start_pos]
    if move_validator(start_pos, end_pos):
        original_position = pieces.pop(start_pos)
        captured_piece = pieces.pop(end_pos, None)
        pieces[end_pos] = original_position
        move_notation = generate_chess_notation(piece_name, start_pos, end_pos, captured_piece)
        moves.append(move_notation)
        last_move = (piece_name, end_pos)
        selected_square = None
    else:
        print("Invalid move")
        selected_square = None  # Deselect the square if the move is invalid.


# Draw a message on the screen when checkmate is detected.
def draw_checkmate_message(winning_player):
    font = pygame.font.SysFont(None, 72)  # Use a larger font for the message.
    text = font.render(f"Checkmate! {winning_player} wins!", True, pygame.Color("gold"))
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))


# Generate chess notation for a move (e.g., "e4", "Nf3").
def generate_chess_notation(piece_name, start_pos, end_pos, captured_piece):
    piece_symbol = {
        "white_pawn": "",
        "black_pawn": "",
        "white_rook": "R",
        "black_rook": "R",
        "white_knight": "N",
        "black_knight": "N",
        "white_bishop": "B",
        "black_bishop": "B",
        "white_queen": "Q",
        "black_queen": "Q",
        "white_king": "K",
        "black_king": "K",
    }
    capture = "x" if captured_piece else ""
    start_pos = start_pos.lower()
    end_pos = end_pos.lower()
    check = "+" if (white_king_in_check() or black_king_in_check()) else ""
    if piece_name in ["white_pawn", "black_pawn"]:
        if capture:
            notation = f"{start_pos[0]}{capture}{end_pos}{check}"
        else:
            notation = f"{end_pos}{check}"
    else:
        notation = f"{piece_symbol[piece_name]}{capture}{end_pos}{check}"
    return notation


# Check if a move is valid by verifying its legality based on the piece and game rules.
def move_validator(start_pos, end_pos, check_for_check=True):
    if start_pos not in pieces:
        return False
    piece_name, _ = pieces[start_pos]
    if piece_name == "white_pawn":
        return move_validator_white_pawn(start_pos, end_pos)
    elif piece_name == "black_pawn":
        return move_validator_black_pawn(start_pos, end_pos)
    elif piece_name == "white_rook" or piece_name == "black_rook":
        return move_validator_rook(start_pos, end_pos)
    elif piece_name == "white_bishop" or piece_name == "black_bishop":
        return move_validator_bishop(start_pos, end_pos)
    elif piece_name == "white_queen" or piece_name == "black_queen":
        return move_validator_queen(start_pos, end_pos)
    elif piece_name == "white_king" or piece_name == "black_king":
        return move_validator_king(start_pos, end_pos)
    elif piece_name == "white_knight" or piece_name == "black_knight":
        return move_validator_knight(start_pos, end_pos)
    return False


# Function to handle en passant validation for pawns.
def move_validator_en_passant(start_pos, end_pos):
    global last_move
    if not last_move:
        return False
    last_piece_name, last_pos = last_move
    start_column = ord(start_pos[0]) - ord('A')
    end_column = ord(end_pos[0]) - ord('A')
    if last_piece_name == "black_pawn" and start_pos[1] == '5' and end_pos[1] == '6':
        if last_pos[0] == end_pos[0] and abs(start_column - end_column) == 1:
            return True
    if last_piece_name == "white_pawn" and start_pos[1] == '4' and end_pos[1] == '3':
        if last_pos[0] == end_pos[0] and abs(start_column - end_column) == 1:
            return True
    return False


# Validate if a knight's move is legal.
def move_validator_knight(start_pos, end_pos):
    start_row = int(start_pos[1])
    end_row = int(end_pos[1])
    start_column = ord(start_pos[0]) - ord('A')
    end_column = ord(end_pos[0]) - ord('A')
    start_row_notation = -start_row + 8
    if end_pos in pieces:
        pieces_name, _ = pieces[end_pos]
        s_pieces_name, _ = pieces[start_pos]
        if "white" in pieces_name and "white" in s_pieces_name:
            return False
        if "black" in pieces_name and "black" in s_pieces_name:
            return False
    theoretical_moves = [(start_row_notation - 2, start_column - 1),
                         (start_row_notation - 2, start_column + 1),
                         (start_row_notation - 1, start_column - 2),
                         (start_row_notation - 1, start_column + 2),
                         (start_row_notation + 1, start_column - 2),
                         (start_row_notation + 1, start_column + 2),
                         (start_row_notation + 2, start_column - 1),
                         (start_row_notation + 2, start_column + 1)]
    valid_moves = []
    for row, column in theoretical_moves:
        if 0 <= row < 8 and 0 <= column < 8:
            valid_moves.append(chess_notation(row, column))
    if end_pos in valid_moves:
        return True
    return False


# Validate if a king's move is legal, including castling logic.
def move_validator_king(start_pos, end_pos):
    global white_king_moved, white_rook_kingside_moved, black_king_moved, black_rook_kingside_moved, black_rook_queenside_moved
    start_row = int(start_pos[1])
    end_row = int(end_pos[1])
    start_column = ord(start_pos[0]) - ord('A')
    end_column = ord(end_pos[0]) - ord('A')
    if end_pos in pieces:
        pieces_name, _ = pieces[end_pos]
        s_pieces_name, _ = pieces[start_pos]
        if ("white" in s_pieces_name and "white" in pieces_name) or (
                "black" in s_pieces_name and "black" in pieces_name):
            return False
    row_diff = abs(start_row - end_row)
    col_diff = abs(start_column - end_column)
    if row_diff <= 1 and col_diff <= 1:
        if "white" in pieces[start_pos]:
            white_king_moved = True
            return True
        elif "black" in pieces[start_pos]:
            black_king_moved = True
            return True

    # Castling logic for white king.
    if start_pos == "E1" and end_pos == "G1":
        if not white_king_moved and not white_rook_kingside_moved:
            if "F1" not in pieces and "G1" not in pieces:
                if not white_king_in_check() and not is_square_attacked("F1", "black") and not is_square_attacked("G1",
                                                                                                                  "black"):
                    pieces["F1"] = pieces.pop("H1")
                    white_king_moved = True
                    white_rook_kingside_moved = True
                    return True
    if start_pos == "E1" and end_pos == "C1":
        if not white_king_moved and not white_rook_queenside_moved:
            if "D1" not in pieces and "C1" not in pieces:
                if not white_king_in_check() and not is_square_attacked("D1", "black") and not is_square_attacked("C1",
                                                                                                                  "black"):
                    pieces["D1"] = pieces.pop("A1")
                    white_king_moved = True
                    white_rook_queenside_moved = True
                    return True

    # Castling logic for black king.
    if start_pos == "E8" and end_pos == "G8":
        if not black_king_moved and not black_rook_kingside_moved:
            if "F8" not in pieces and "G8" not in pieces:
                if not black_king_in_check() and not is_square_attacked("F8", "white") and not is_square_attacked("G8",
                                                                                                                  "white"):
                    pieces["F8"] = pieces.pop("H8")
                    black_king_moved = True
                    black_rook_kingside_moved = True
                    return True
    if start_pos == "E8" and end_pos == "C8":
        if not black_king_moved and not black_rook_queenside_moved:
            if "D8" not in pieces and "C8" not in pieces:
                if not black_king_in_check() and not is_square_attacked("D8", "white") and not is_square_attacked("C8",
                                                                                                                  "white"):
                    pieces["D8"] = pieces.pop("A8")
                    black_king_moved = True
                    black_rook_queenside_moved = True
                    return True
    return False


# Check if a square is attacked by an opponent's piece.
def is_square_attacked(square, opponent_color):
    for piece_pos, (piece_name, _) in pieces.items():
        if opponent_color in piece_name:
            if move_validator(piece_pos, square, check_for_check=False):
                return True
    return False


# Get all legal moves for a player (either white or black).
def get_all_legal_moves(player_color):
    legal_moves = []
    for piece_pos, (piece_name, _) in pieces.items():
        if player_color in piece_name:
            for row in range(1, 9):
                for col in 'ABCDEFGH':
                    potential_move = f"{col}{row}"
                    if move_validator(piece_pos, potential_move, check_for_check=True):
                        legal_moves.append((piece_pos, potential_move))
    return legal_moves


# Get legal moves for a particular piece.
def get_legal_moves_for_piece(start_pos):
    legal_moves = []
    piece_name, _ = pieces[start_pos]
    for row in range(1, 9):
        for col in 'ABCDEFGH':
            potential_move = f"{col}{row}"
            if move_validator(start_pos, potential_move, check_for_check=True):
                legal_moves.append(potential_move)
    return legal_moves


# Check if a player is in checkmate (i.e., no legal moves and the king is in check).
def is_checkmate(player_color):
    if player_color == "white":
        if not white_king_in_check():
            return False
    else:
        if not black_king_in_check():
            return False

    legal_moves = get_all_legal_moves(player_color)

    for start_pos, end_pos in legal_moves:
        original_position = pieces[start_pos]
        captured_piece = pieces.pop(end_pos, None)
        pieces[end_pos] = pieces.pop(start_pos)
        if player_color == "white" and not white_king_in_check():
            pieces[start_pos] = original_position
            if captured_piece:
                pieces[end_pos] = captured_piece
            else:
                del pieces[end_pos]
            return False
        elif player_color == "black" and not black_king_in_check():
            pieces[start_pos] = original_position
            if captured_piece:
                pieces[end_pos] = captured_piece
            else:
                del pieces[end_pos]
            return False
        pieces[start_pos] = original_position
        if captured_piece:
            pieces[end_pos] = captured_piece
        else:
            del pieces[end_pos]
    return True


# Validate if a queen's move is legal by combining the rules for rooks and bishops.
def move_validator_queen(start_pos, end_pos):
    if move_validator_rook(start_pos, end_pos) or move_validator_bishop(start_pos, end_pos):
        if end_pos in pieces:
            piece_name, _ = pieces[start_pos]
            end_piece_name, _ = pieces[end_pos]
            if ("white" in piece_name and "white" in end_piece_name) or (
                    "black" in piece_name and "black" in end_piece_name):
                return False
        return True
    return False


# Validate if a bishop's move is legal.
def move_validator_bishop(start_pos, end_pos):
    start_row = int(start_pos[1])
    end_row = int(end_pos[1])
    start_column = ord(start_pos[0]) - ord('A')
    end_column = ord(end_pos[0]) - ord('A')
    start_row_notation = -start_row + 8
    if abs(start_row - end_row) != abs(start_column - end_column):
        return False
    step_row = 1 if end_row > start_row else -1
    step_col = 1 if end_column > start_column else -1
    for step in range(1, abs(end_row - start_row)):
        intermediate_row = start_row + step * step_row
        intermediate_col = start_column + step * step_col
        pos_to_check = chess_notation(8 - intermediate_row, intermediate_col)
        if pos_to_check in pieces:
            return False
    if end_pos in pieces:
        s_piece_name, _ = pieces[start_pos]
        pieces_name, _ = pieces[end_pos]
        if ("white" in s_piece_name and "white" in pieces_name) or ("black" in s_piece_name and "black" in pieces_name):
            return False
    return True


# Validate if a rook's move is legal.
def move_validator_rook(start_pos, end_pos):
    start_row = int(start_pos[1])
    end_row = int(end_pos[1])
    start_column = ord(start_pos[0]) - ord('A')
    end_column = ord(end_pos[0]) - ord('A')
    start_row_notation = -start_row + 8

    if end_pos in pieces:
        s_pieces_name, _ = pieces[start_pos]
        pieces_name, _ = pieces[end_pos]
        if s_pieces_name == 'white_rook' and "white" in pieces_name:
            return False
        if s_pieces_name == 'black_rook' and "black" in pieces_name:
            return False

    if start_row != end_row and start_column != end_column:
        return False

    if start_row == end_row:  # Horizontal movement.
        step = 1 if end_column > start_column else -1
        for column in range(start_column + step, end_column, step):
            pos_to_check = chess_notation(start_row_notation, column)
            if pos_to_check in pieces and pos_to_check != end_pos:
                return False
    else:  # Vertical movement.
        step = 1 if end_row > start_row else -1
        for row in range(start_row + step, end_row, step):
            row = -row + 8
            pos_to_check = chess_notation(row, start_column)
            if pos_to_check in pieces and pos_to_check != end_pos:
                return False
    return True


# Validate if a white pawn's move is legal.
def move_validator_white_pawn(start_pos, end_pos):
    start_row = int(start_pos[1])
    start_row_piece_notation = -start_row + 8
    start_column = ord(start_pos[0]) - ord('A')
    end_row = int(end_pos[1])
    end_column = ord(end_pos[0]) - ord('A')
    one_step_forward = chess_notation(start_row_piece_notation - 1, start_column)
    two_step_forward = chess_notation(start_row_piece_notation - 2, start_column)
    if start_column + 1 < 8:
        right_step_diagonal = chess_notation(start_row_piece_notation - 1, start_column + 1)
    else:
        right_step_diagonal = None
    if start_column - 1 >= 0:
        left_step_diagonal = chess_notation(start_row_piece_notation - 1, start_column - 1)
    else:
        left_step_diagonal = None
    if end_pos in pieces:
        piece_name, _ = pieces[end_pos]
        if "white" in piece_name:
            return False

    if start_row == 2 and end_row == 4 and start_column == end_column and one_step_forward not in pieces and two_step_forward not in pieces:
        return True
    if start_row + 1 == end_row and start_column == end_column and one_step_forward not in pieces:
        if end_row == 8:
            chosen_piece, piece_image = white_promotion(end_column)
            pieces[end_pos] = (chosen_piece, piece_image)
            moves.append(f"{end_pos.lower()}={chosen_piece[6].upper()}")
            del pieces[start_pos]
        return True
    if start_row + 1 == end_row and start_column != end_column:
        if start_column + 1 == end_column and right_step_diagonal in pieces:
            if end_row == 8:
                chosen_piece, piece_image = white_promotion(end_column)
                moves.append(f"{end_pos.lower()}={chosen_piece[6].upper()}")
                pieces[end_pos] = (chosen_piece, piece_image)
                del pieces[start_pos]
            return True
    if start_row + 1 == end_row and start_column != end_column:
        if left_step_diagonal in pieces and start_column - 1 == end_column:
            if end_row == 8:
                chosen_piece, piece_image = white_promotion(end_column)
                moves.append(f"{end_pos.lower()}={chosen_piece[6].upper()}")
                pieces[end_pos] = (chosen_piece, piece_image)
                del pieces[start_pos]
            return True
    return False


# Handle promotion for white pawns.
def white_promotion(end_pos):
    valid_pieces = ["queen", "rook", "bishop", "knight"]
    chosen_piece = ""
    while chosen_piece not in valid_pieces:
        chosen_piece = input("Choose a piece for promotion (queen, rook, bishop, knight): ").strip().lower()
        if chosen_piece not in valid_pieces:
            print("Invalid choice. Please choose again.")
    if chosen_piece == "queen":
        piece_image = load_piece("../white pieces/Chess_qlt60.png")
    elif chosen_piece == "rook":
        piece_image = load_piece("../white pieces/Chess_rlt60.png")
    elif chosen_piece == "bishop":
        piece_image = load_piece("../white pieces/Chess_blt60.png")
    elif chosen_piece == "knight":
        piece_image = load_piece("../white pieces/Chess_klt60.png")
    return f"white_{chosen_piece}", piece_image


# Validate if a black pawn's move is legal.
def move_validator_black_pawn(start_pos, end_pos):
    start_row = int(start_pos[1])
    start_row_piece_notation = -start_row + 8
    start_column = ord(start_pos[0]) - ord('A')
    end_row = int(end_pos[1])
    end_column = ord(end_pos[0]) - ord('A')
    one_step_forward = chess_notation(start_row_piece_notation + 1, start_column)
    two_step_forward = chess_notation(start_row_piece_notation + 2, start_column)
    if start_column + 1 < 8:
        left_step_diagonal = chess_notation(start_row_piece_notation + 1, start_column + 1)
    else:
        left_step_diagonal = None
    if start_column - 1 >= 0:
        right_step_diagonal = chess_notation(start_row_piece_notation + 1, start_column - 1)
    else:
        right_step_diagonal = None
    if end_pos in pieces:
        piece_name, _ = pieces[end_pos]
        if "black" in piece_name:
            return False
    if start_row == 7 and end_row == 5 and start_column == end_column and one_step_forward not in pieces and two_step_forward not in pieces:
        return True
    if start_row - 1 == end_row and start_column == end_column and one_step_forward not in pieces:
        if end_row == 1:
            chosen_piece, piece_image = black_promotion(end_column)
            pieces[end_pos] = (chosen_piece, piece_image)
            moves.append(f"{end_pos.lower()}={chosen_piece[6].upper()}")
            del pieces[start_pos]
        return True
    if start_row - 1 == end_row and start_column != end_column:
        if start_column - 1 == end_column and right_step_diagonal in pieces:
            if end_row == 1:
                chosen_piece, piece_image = black_promotion(end_column)
                moves.append(f"{end_pos.lower()}={chosen_piece[6].upper()}")
                pieces[end_pos] = (chosen_piece, piece_image)
                del pieces[start_pos]
            return True
    if start_row - 1 == end_row and start_column != end_column:
        if left_step_diagonal in pieces and start_column + 1 == end_column:
            if end_row == 1:
                chosen_piece, piece_image = black_promotion(end_column)
                moves.append(f"{end_pos.lower()}={chosen_piece[6].upper()}")
                pieces[end_pos] = (chosen_piece, piece_image)
                del pieces[start_pos]
            return True
    return False


# Handle promotion for black pawns.
def black_promotion(end_pos):
    valid_pieces = ["queen", "rook", "bishop", "knight"]
    chosen_piece = ""
    while chosen_piece not in valid_pieces:
        chosen_piece = input("Choose a piece for promotion (queen, rook, bishop, knight): ").strip().lower()
        if chosen_piece not in valid_pieces:
            print("Invalid choice. Please choose again.")
    if chosen_piece == "queen":
        piece_image = load_piece("../black pieces/Chess_qdt60.png")
    elif chosen_piece == "rook":
        piece_image = load_piece("../black pieces/Chess_rdt60.png")
    elif chosen_piece == "bishop":
        piece_image = load_piece("../black pieces/Chess_bdt60.png")
    elif chosen_piece == "knight":
        piece_image = load_piece("../black pieces/Chess_ndt60.png")
    return f"black_{chosen_piece}", piece_image


# Check if the white king is in check.
def white_king_in_check():
    king_pos = None
    for piece_pos, (piece_name, _) in pieces.items():
        if piece_name == "white_king":
            king_pos = piece_pos
            break
    if king_pos is None:
        raise ValueError("White King missing, failed Game")
    for piece_pos, (piece_name, _) in pieces.items():
        if "black" in piece_name:
            if move_validator(piece_pos, king_pos, check_for_check=False):
                return True
    return False


# Check if the black king is in check.
def black_king_in_check():
    king_pos = None
    for piece_pos, (piece_name, _) in pieces.items():
        if piece_name == "black_king":
            king_pos = piece_pos
            break
    if king_pos is None:
        raise ValueError("Black King missing, failed Game")
    for piece_pos, (piece_name, _) in pieces.items():
        if "white" in piece_name:
            if move_validator(piece_pos, king_pos, check_for_check=False):
                return True
    return False


# Get the current player based on the number of moves made.
def get_current_player():
    if len(moves) % 2 == 1:
        return "black"
    return "white"


# Main game loop to handle game events and manage the game state.
def main():
    global selected_square, checkmate, winning_player
    selected_legal_moves = []
    place_black_pieces()
    place_white_pieces()
    selected_piece = None
    game_over = False

    while True:
        draw_board(selected_legal_moves)
        draw_pieces()
        draw_move_list()

        if game_over:
            draw_checkmate_message(winning_player)
            pygame.display.update()
            continue

        if not checkmate:
            if is_checkmate("black"):
                checkmate = True
                winning_player = "White"
                game_over = True
            elif is_checkmate("white"):
                checkmate = True
                winning_player = "Black"
                game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not checkmate:
                    clicked_square = get_square_under_mouse()
                    if clicked_square:
                        if selected_piece:
                            move_piece(selected_piece, clicked_square)
                            selected_piece = None
                            selected_legal_moves = []
                            if not checkmate:
                                if get_current_player() == "black" and is_checkmate("white"):
                                    checkmate = True
                                    winning_player = "White"
                                    game_over = True
                                elif get_current_player() == "white" and is_checkmate("black"):
                                    checkmate = True
                                    winning_player = "Black"
                                    game_over = True
                        elif clicked_square in pieces:
                            selected_piece = clicked_square
                            selected_square = clicked_square
                            selected_legal_moves = get_legal_moves_for_piece(selected_piece)

        pygame.display.update()


if __name__ == "__main__":
    main()
