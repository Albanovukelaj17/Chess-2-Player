import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 900, 900
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
def main():
    draw_board()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()

