# simp-city
PRG1 Simp City Project

Turn-based building simulation game.

Each turn the player is presented with 2 random buildings from the pool of 5

The buildings can then be placed on a 4x4 grid

This repeats until all 16 squares (4x4) are occupied with a building

A building cannot be placed on an occupied cell, and a buildinng cannot be removed once placed

Re-rolls f the buildings are not allowed.

Each building will carry points based on the conditions as listed below.


# Beach (BCH)
A Beach (BCH) scores 3 points if it is built in column A or column D, or 1 point otherwise.


# Factory (FAC)
A Factory (FAC) scores 1 point per factory (FAC) in the city, up to a maximum of 4 points for the first 4 factories; all subsequent factories only score 1 point each. <br>
For example, <br>
  •	If there are 3 factories in the city, each factory will score 3 points, for a total of 3+3+3 = 9 points. <br>
  •	If there are 5 factories in the city, the first 4 factories will score 4 points each while the 5th factory will score 1 point, for a total of 4+4+4+4+1 = 17 points.


# House (HSE)
If a House (HSE) is next to a factory (FAC), then it scores 1 point only. Otherwise, it scores 1 point for each adjacent house (HSE) or shop (SHP), and 2 points for each adjacent beach (BCH).


# Shop (SHP)
A Shop (SHP) scores 1 point per different type of building adjacent to it.


# Highway (HWY)
A Highway (HWY) scores 1 point per connected highway (HWY) in the same row (horizontal).
