package tictactoesimple;

public class Game {


    private static char EMPTY = ' ';
    private char PLAYER_1 = 'X';
    private char PLAYER_2 = 'O';
    private static char [][] BOARD  = new char [3][3];




    public static void Value_Empty_Board() {
        for (int i = 0; i < BOARD.length; i++) {
            for (int x = 0; x < BOARD[i].length; x++) {
                BOARD[i][x]= EMPTY;

            }

        }
    }
  public static void DrawBoard(){
      System.out.println("   1  2  3");
        for(int i =1; i< BOARD.length+1; i ++){
            System.out.print(" "+i+" ");
            for ( int x =1; x < BOARD.length+1;x++){

                if ( x == 3)  System.out.println(BOARD[i-1][x-1]+"  ");
                else System.out.print(BOARD[i-1][x-1]+"  ");


            }
        }

  }


  public void player_move(){

  }

  public void switch_player(){

  }


  public boolean isWinner(){
     for(int i= 0 ; i < BOARD.length; i ++) {
          

     }

          return false;

  }


public boolean Board_Full(){
 return false;
}

    public static void main(String[] args) {
        System.out.println(" ");
        System.out.println("Welcome, Player 1 begins mit X , Player 2 with 0");
        System.out.println(" ");
        Value_Empty_Board();
        DrawBoard();
        System.out.println();
        System.out.println("Insert Player1 Move :" );
        System.out.println( " Row:        Column:     ");


    }


}
