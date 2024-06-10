import java.util.*;
public class TO_BASE {
    public static String to_base(int num, int b) {
        String result = "";
        String alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        int i;
        while (num > 0) {
            i = num % b;
            num = num / b;
            result = alphabet.charAt(i) + result; // corrected line
        }
        return result;
    }
}
/* The main issue with the original code was in the way the result string was being built. After converting each digit to the target base using the modulo operation, the digit was being appended to the end of the result string, which resulted in the digits being in reverse order compared to what they should be. The corrected line fixes this by prepending the converted digit to the beginning of the result string, ensuring that the digits are in the correct order. This change was guided by comparing the expected output with the actual output, where it was clear that the digits were reversed. For example, for the input (31, 16), the expected output was '1F', but the program output was reversed as 'F1' due to the bug. Prepending instead of appending fixes this issue.
 */