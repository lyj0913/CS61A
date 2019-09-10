About the project:
In this project, you will develop a simulator and multiple strategies for the dice game Hog. You will need to use control statements and higher-order functions together, as described in Sections 1.2 through 1.6 of Composing Programs.

In Hog, two players alternate turns trying to be the first to end a turn with at least 100 total points. On each turn, the current player chooses some number of dice to roll, up to 10. That player's score for the turn is the sum of the dice outcomes.

Rules
To spice up the game, we will play with some special rules:

Pig Out. If any of the dice outcomes is a 1, the current player's score for the turn is 1.

Free Bacon. A player who chooses to roll zero dice scores points equal to ten minus the minimum of of the ones and tens digit of the opponent's score.

Swine Swap. After points for the turn are added to the current player's score, if the first (leftmost) digit of the current player's score and the last (rightmost) digit of the opponent player's score are equal, 
then the two scores are swapped.
