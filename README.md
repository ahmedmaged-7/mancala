# Mancala AI Game

## About the game

the object of the game is to capture the most stones. set up lay out the board horizontally between two players and place four stones into each of the 12 small pockets. the board is divided into two rows of six pockets each. each player controls the six pockets on the side, closest to them the two larger pockets are called Mon Calas. each player owns the Mancala to the right of their row. pick a player to go first on your turn. pick all the stones in any one of your pockets on your side of the board moving counterclockwise from the pocket picked. deposit one of the stones in each pocket. you pass until the stones run out. if you run into your own Mancala deposit one stone in it. if you run into your opponent's Mancala skip it. if the last piece you drop is in your own Mancala take another turn. immediately if the last piece you drop is in an empty pocket on your side of, the board you capture that piece and any piece in the hole directly opposite it always place all captured pieces in your Mancala (stealing). the game ends when all six spaces on one side of the board are empty. the player who still has pieces on his side of the board when the game ends captures all those pieces and puts them into their Mancala. count all the pieces in each Mancala. the player with the most pieces wins.

## Our project

A simple implementation for Mancala game along with an AI player using the Minimax algorithm with alpha-beta pruning. The game alow user to play against AI algorithm in two modes (stealing & without stealing).The algorithm uses a depth-first strategy when exploring the game tree to ensure efficient memory usage. We Also support saving and loading games.

