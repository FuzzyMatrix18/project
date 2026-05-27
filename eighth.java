
import java.util.Scanner;
import java.util.Random;

public class eighth 
{
    public static void main(String[] args) 
    {
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();
        System.out.print("scissor (0), rock (1), paper (2): ");
        int uchoice = scanner.nextInt();
        int cchoice = random.nextInt(3);

        System.out.println("The computer is " + getChoice(cchoice) + ". You are " + getChoice(uchoice));

        if (uchoice == cchoice)
         {
            System.out.println("It's a draw!");
        } 
        else if ((uchoice == 0 && cchoice == 2) ||
                   (uchoice == 1 && cchoice == 0) ||
                   (uchoice == 2 && cchoice == 1)) {
            System.out.println("You won!");
        }
        else 
        {
            System.out.println("You lost!");
        }

        scanner.close();
    }

    private static String getChoice(int choice) 
    {
        switch (choice) 
        {
            case 0:
                return "scissor";
            case 1:
                return "rock";
            case 2:
                return "paper";
            default:
                return "unknown";
        }
    }
}
