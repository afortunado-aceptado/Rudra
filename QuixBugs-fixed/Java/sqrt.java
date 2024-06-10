import java.util.*;
public class SQRT {
  public static double sqrt(double x, double epsilon) {
    double approx = x / 2d;
    while (Math.abs(approx * approx - x) > epsilon) { // Corrected line
      approx = 0.5d * (approx + x / approx);
    }
    return approx;
  }
}
/* The issue was with the while loop's condition. Initially, it wrongly checked if the absolute difference between \(x\) and the approximation (\(approx\)) was greater than \(\epsilon\), which is incorrect for verifying the accuracy of the square root approximation. By changing the condition to check if the absolute difference between \(approx^2\) (the square of the current approximation) and \(x\) is greater than \(\epsilon\), the algorithm correctly iterates until the square of the approximation is sufficiently close to \(x\), in line with the Newton-Raphson method for finding square roots. Tracking the value of \(approx\) during iterations against expected square root values revealed that it wasn't converging to the square root of \(x\), but instead stayed roughly constant when using the incorrect condition. Adjusting the condition to compare \(approx^2\) and \(x\) ensures that \(approx\) converges to the actual square root of \(x\), within the specified \(\epsilon\) tolerance.
 */