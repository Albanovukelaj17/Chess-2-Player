import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1400, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

font = pygame.font.SysFont(None, 24)

def draw_board():
    WIN.fill(pygame.Color("black"))
    colors = [pygame.Color("white"), pygame.Color("gray")]
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H"]
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8"]
    for row in range(8):
        for columns in range(8):
            color =colors[( row+columns)%2]
            pygame.draw.rect(WIN,color,pygame.Rect(row*100+50,columns*100+50,100,100))


            if row == 7:
                text = font.render(alphabet[columns],True,pygame.Color("red"))
                WIN.blit(text,(columns*100+100-text.get_width()//2,HEIGHT-25))
            if columns == 0:  # First column (where numbers should appear)
                text_surface = font.render(numbers[7 - row], True, pygame.Color("red"))
                WIN.blit(text_surface, (25, row * 100 + 100 - text_surface.get_height() // 2))

    pygame.display.update()

def draw_text(text,position,color):
    text_surface = font.render(text,True,color)
    WIN.blit(text_surface,position)


def load_piece(image_path, position):
    try:
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (100, 100))
        WIN.blit(image, position)
        pygame.display.update()
    except pygame.error as e:
        print(f"Unable to load image: {e}")
        sys.exit()


def place_black_pieces():
    pawns_positions = [(x * 100 + 50, 150) for x in range(8)]
    pawn_image_path = "/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/black pieces/Chess_pdt60.png"
    for pos in pawns_positions:
        load_piece(pawn_image_path, pos)

    #rooks
    load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/black pieces/Chess_rdt60.png",(50,50))
    load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/black pieces/Chess_rdt60.png",(750,50))

    #bishops
    load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/black pieces/Chess_bdt60.png",(250,50))
    load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/black pieces/Chess_bdt60.png",(550,50))

    #knights
    load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/black pieces/Chess_ndt60.png",(150,50))
    load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/black pieces/Chess_ndt60.png",(650,50))

    #queen,king
    load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/black pieces/Chess_qdt60.png",(350,50))
    load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/black pieces/Chess_kdt60.png",(450,50))


def place_white_pieces():
    pawns_positions = [(x * 100 + 50, 650) for x in range(8)]
    pawn_image_path = "/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/white pieces/Chess_plt60.png"
    for pos in pawns_positions:
        load_piece(pawn_image_path, pos)

    #rooks
    load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/white pieces/Chess_rlt60.png",(50,750))
    load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/white pieces/Chess_rlt60.png",(750,750))

    #bishops
    load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/white pieces/Chess_blt60.png",(250,750))
    load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/white pieces/Chess_blt60.png",(550,750))

    #knights
    load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/white pieces/Chess_nlt60.png",(150,750))
    load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/white pieces/Chess_nlt60.png",(650,750))

    #queen,king
    load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/white pieces/Chess_qlt60.png",(350,750))
    load_piece("/Users/albanovukelaj/Desktop/Motherfucker/Just-Learning/Chess 1 vs1/white pieces/Chess_klt60.png",(450,750))
def move_detector():
    draw_text("Move List", (1100,100),pygame.Color("white"))  # Draw text in the center
    pygame.display.update()
    pygame.time.delay(1000)

def main():
    draw_board()
    place_black_pieces()
    place_white_pieces()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        move_detector()
if __name__ == "__main__":
    main()

