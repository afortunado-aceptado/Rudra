import java.util.*;

public class HANOI {
    public static List<Pair<Integer, Integer>> hanoi(int height, int start, int end) {
        List<Pair<Integer, Integer>> steps = new ArrayList<Pair<Integer, Integer>>();
        if (height > 0) {
            Set<Integer> pegs = new HashSet<>(Arrays.asList(1, 2, 3));
            pegs.remove(start);
            pegs.remove(end);
            int helper = pegs.iterator().next();
            steps.addAll(hanoi(height - 1, start, helper));
            steps.add(new Pair<>(start, end));
            steps.addAll(hanoi(height - 1, helper, end));
        }
        return steps;
    }

    public static class Pair<F, S> {
        private F first;
        private S second;

        public Pair(F first, S second) {
            this.first = first;
            this.second = second;
        }

        public void setFirst(F first) {
            this.first = first;
        }

        public void setSecond(S second) {
            this.second = second;
        }

        public F getFirst() {
            return first;
        }

        public S getSecond() {
            return second;
        }

        @Override
        public String toString() {
            return "(" + String.valueOf(first) + ", " + String.valueOf(second) + ")";
        }
    }
}
/* The critical change in the code involves the faulty line where a disk was moved from the start peg to the helper peg instead of the end peg directly. By reviewing the steps of moving disks in the Towers of Hanoi puzzle, it's clear that, after moving the smaller stack to the helper peg, the largest disk should move directly from the start peg to the end peg, and not to the helper peg as previously coded. This correction aligns with the puzzle's rule that each move should progress towards the goal of moving the entire stack to the end peg. Additionally, I replaced the PriorityQueue with a HashSet for clarity and to avoid unnecessary ordering, as the order of the helper pegs does not matter, only their value. This change ensures the code now correctly reflects the algorithm for solving the Towers of Hanoi puzzle, accurately transferring disks from the start peg to the end peg through the required steps.
 */