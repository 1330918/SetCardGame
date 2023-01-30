# SetCardGame
An algorithm for playing the Set card game

The images of the cards should be downloaded as a “Cards” folder. 
If they are in a different folder or in a different place than where the code is stored, pygame will not be able to import the images properly. 

Pygame also needs to be installed. This can be done with pip. After that, the code can be used in Spyder or Jupyter Notebook, for example.

The notation of a SET is very important. The card numbers must be entered from lowest to highest, separated by a comma. 
Valid formats are for example: 1,5,6 and 8,10,12. Not valid is 123 or 12,8,10.

To fill in a SET, the player must click anywhere on the screen with the mouse and then you can type.
After finding a SET, it remains on the screen. By clicking again you can enter a new SET. This works the same way if an incorrect SET is entered.

The difficulty level can be adjusted by the user by changing the value of “timermax”. This can be another value in the “difficulties” dictionary or just a random time. 
The text colors can also be adjusted with other RGB values if desired. 
The other variables should not be changed.
