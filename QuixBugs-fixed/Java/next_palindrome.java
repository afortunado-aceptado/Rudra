import java.util.*;
import java.lang.Math.*;

public class NEXT_PALINDROME {
    public static String next_palindrome(int[] digit_list) {
        int high_mid = digit_list.length / 2;
        int low_mid = (digit_list.length - 1) / 2;
        while (low_mid >= 0) {
            if (digit_list[low_mid] < 9) {
                digit_list[low_mid]++;
                if (low_mid != high_mid) {
                    digit_list[high_mid]++;
                }
                break;
            } else {
                digit_list[low_mid] = 0;
                if (low_mid != high_mid) {
                    digit_list[high_mid] = 0;
                }
                high_mid++;
                low_mid--;
            }
        }
        if (digit_list[0] == 0) {
            digit_list = new int[digit_list.length + 1];
            digit_list[0] = 1;
            digit_list[digit_list.length - 1] = 1;
        }
        return Arrays.toString(digit_list);
    }
}
/* \text{The problem with the original code was that it was trying to increment the middle digits first, which was not correct.
The code now correctly increments the middle digit and moves outwards incrementing the high and low digits. 
If the middle digit is 9, it is reset to 0 and the high and low digits are incremented.
If the incremented digit is now 0, the code checks if it is the first digit and if it is, it creates a new array with length plus one, 
sets the first and last digits to 1, and returns it.}
 */