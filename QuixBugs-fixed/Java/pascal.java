import java.util.*;
public class PASCAL {
    public static ArrayList<ArrayList<Integer>> pascal(int n) {
        ArrayList<ArrayList<Integer>> rows = new ArrayList<ArrayList<Integer>>();
        for (int r = 0; r < n; r++) {
            ArrayList<Integer> row = new ArrayList<Integer>();
            for (int c = 0; c <= r; c++) { // corrected the loop boundary
                if (c == 0 || c == r) {
                    row.add(1);
                } else {
                    int upLeft = rows.get(r - 1).get(c - 1);
                    int upRight = rows.get(r - 1).get(c);
                    row.add(upLeft + upRight);
                }
            }
            rows.add(row);
        }
        return rows;
    }
}
/* The issue in the original code was primarily in the loop that generates each row of Pascal's Triangle. The original for-loop condition (\texttt{for (int c = 0; c < r; c++)}) failed to account for the last element in each row, which should be a 1. This oversight led to rows missing their rightmost elements. By adjusting the loop to iterate up to and including the current row number (\texttt{for (int c = 0; c <= r; c++)}), every row now starts and ends with 1, as it should according to the properties of Pascal's Triangle. Furthermore, the condition to add 1 at the start or end of each row (\texttt{if (c == 0 || c == r)}) ensures that the base cases for each row are correctly handled, while the else condition correctly calculates the sum of the two numbers directly above the current position for the rest of the row.
 */