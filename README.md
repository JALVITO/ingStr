## GLOSSARY:
* **Playing field:** all available strings in play.
* **Player inventory:** collection of words the player has formed.

## HOW TO PLAY:
**Set-up:**
* Players input server IP address and name
* Server generates a random 30-character string
* Server starts by granting a turn to a player

**Progression:**
* Players use string commands (substring, concat, reverse) to manipulate the strings on the playing field.
* Their objective is to isolate a valid word (length > 2 and in English dictionary) in order to add it to their inventory.
* Players can use up to two string commands per turn.
* Players are allowed to identify a word after having used both their moves.

**Resolution:**
* Game ends after both players acknowledge no other words can be formed.
* Alternatively, if 7 or less characters remain in play and no words have been formed in 5 collective turns (a turn for player 1 and a turn for player 2 counts as a _collective turn_)
* The player with the most amount of characters in their inventory wins (that is, the player with the greater sum of lengths of all their formed words)
* If this results in a tie, the player with the longest word wins.
* If both have the same length for their longest word, the next-longest word is compared, until either player runs out of words.
* If both run out of words at the same time, the game results in a tie.

## COMMAND USAGE:
**Notes:**
* Words on the playing field are identified by their word_id (sequential and 0-indexed)
* Characters on words are also 0-indexed

> substring [word_id] [low_bound] [up_bound]

**Definition:** extracts a substring from a given word, adds it as a new string in the playing field and joins the remaining fragments of the string (if there are any). Low_bound and up_bound are inclusive.

**Example:** \
0 ABCDEF \
1 GHIJKL

_Query:_ substring 1 2 4

_Result:_ \
0 ABCDEF \
1 GHL \
2 IJK

> concat [word1_id] [word2_id]

**Definition:** combines two strings in the playing field to form a new one. Order of parameters _does_ affect the generated string (concat 0 1 is different than concat 1 0). Word2_id is added to the end of word1_id. New string is added to the very end of the playing field.

**Example:** \
0 AB \
1 CD \
2 EF

_Query:_ concat 0 1

_Result:_ \
0 CD \
1 ABEF

> reverse [word_id]

**Definition:** inverts the order of the characters in a string.

**Example:** \
0 ABC \
1 DEF \

_Query:_ reverse 0

_Result:_ \
0 CBA \
1 DEF

> identify [word_id]

**Definition:** removes the word from the playing field and adds the word to a player's inventory (words array in players).

**Example:** \
0 ABC \
1 DEF \

_Query:_ identify 0

_Result:_ \
0 DEF

> endTurn

**Definition:** ends a player's turn and passes control over to other player.

> end

**Definition:** ends the game. Server should calculate players' points and display the result, along with the words each player identified.