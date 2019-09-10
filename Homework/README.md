In this project, I developed a simulator and multiple strategies for the dice game Hog. 
In Hog, two players alternate turns trying to be the first to end a turn with at least 100 total points. 
On each turn, the current player chooses some number of dice to roll, up to 10. 
That player's score for the turn is the sum of the dice outcomes.
Rules
To spice up the game, we will play with some special rules:

Pig Out. If any of the dice outcomes is a 1, the current player's score for the turn is 1.

Example 1: The current player rolls 7 dice, 5 of which are 1's. They score 1 point for the turn.

Example 2: The current player rolls 4 dice, all of which are 3's. Since Pig Out did not occur, they score 12 points for the turn.

Free Bacon. A player who chooses to roll zero dice scores points equal to ten minus the minimum of of the ones and tens digit of the opponent's score.

Example 1: The opponent has 13 points, and the current player chooses to roll zero dice. The minimum of 1 and 3 is 1, so the current player gains 10 - 1 = 9 points.

Example 2: The opponent has 85 points, and the current player chooses to roll zero dice. The minimum of 8 and 5 is 5, so the current player gains 10 - 5 = 5 points.

Example 3: The opponent has 7 points, and the current player chooses to roll zero dice. The minimum of 0 and 7 is 0, so the current player gains 10 - 0 = 10 points.

Swine Swap. After points for the turn are added to the current player's score, if the first (leftmost) digit of the current player's score and the last (rightmost) digit of the opponent player's score are equal, then the two scores are swapped.

Example 1: The current player has a total score of 31 and the opponent has 83. The current player rolls one dice with value 5. The player's new score is 36, and the opponent's score is 83. The leftmost digit of the current player's score and the rightmost digit of the opponent's score are both 3, so the scores are swapped.

Example 2: The current player has a total score of 1 and the opponent has 2. The current player rolls one dice with value 6. The player's new score is 7, and the opponent's score is 2. The leftmost digit of the current player's score is 7, and the rightmost digit of the opponent's score is 2. The scores are not swapped.

Example 3: The current player has a total score of 99 and the opponent has 21. The current player rolls three dice that total 8. The player's new score is 107, and the opponent's score is 21. The leftmost digit of the player's score is and the rightmost digit of the opponent's score are both 1, so the scores are swapped.

Example 4: The current player has a total score of 35 and the opponent has 25. The current player rolls two dice that total 10. The player's new score is 45, and the opponent's score is 25. The leftmost digit of the player's score is not equal to the rightmost digit of the opponent's score, so the scores are not swapped
