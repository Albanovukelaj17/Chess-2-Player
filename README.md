## Chess 1 vs1

Welcome to the Chess Game Project! This is a fun and interactive chess game built with Python and Pygame, designed to bring the classic game of chess to your screen with realistic rules and a clean interface.

## **Features**

 **Basic Gameplay**
 
-Move Pieces: Play chess by moving pieces according to standard rules. All the classic pieces are here: pawns, knights, bishops, rooks, queens, and kings.

-Highlight Legal Moves: Click on a piece to see all the valid moves highlighted, making it easy to plan your strategy.

-Square Highlighting: The square you select is highlighted, so you always know which piece you're moving.

  **Advanced Mechanics**
  
-En Passant: The game handles this special pawn capture, which occurs when a pawn moves two squares forward and lands beside an enemy pawn.

-Castling: Both kingside and queenside castling are supported, letting you protect your king by moving it along with a rook.

-Pawn Promotion: Get a pawn to the other side of the board, and you can promote it to a queen, rook, bishop, or knight.

-Check and Checkmate: The game automatically detects when a king is in check or checkmate, giving you clear feedback and ending the game when checkmate occurs.

  **User Interface**

-Move List: See a history of all moves in standard chess notation on the right side of the screen, split into columns for White and Black.

-Checkmate Notification: A clear message announces the winner when the game ends in checkmate.

-Board Design: The chessboard features alternating colors and clear labels for rows and columns, making it easy to follow the game.

## **Game Flow**

-Turn-Based Play: The game alternates turns between White and Black, ensuring fair play.

-Move Validation: Every move is checked against chess rules to prevent illegal actions.

-Game Over Detection: The game knows when it’s over, stopping play when checkmate or stalemate is reached.


## **Coming Soon**
Undo/Redo: Go back or forward a move for easier gameplay.
Restart Game: Start a new game with the press of a button.
Draw Conditions: Implementing stalemates, threefold repetition, and the fifty-move rule.
Scrollable Move List: Scroll through the move history when it gets long.
Getting Started

## **Prerequisites**
 Make sure you have Python installed. You can get it from python.org.
-Copy Repository 
```bash Copy code
git clone https://github.com/yourusername/chess-game.git
cd chess-2-Player
pip install pygame
python main.py
```


