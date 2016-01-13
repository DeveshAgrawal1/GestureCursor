# GestureCursor
The program is made to give a simple demonstration of controlling the cursor on the screen using hand gestures recognition.
If the user raises a single finger, the cursor will be taken to the position of the finger.

The main functionality used to find out the hand from the total video feed is colocr differentiation, Orange color is separated from the 
rest of the scene (this is very unstable as it is largely dependent on the surroundings' color and lightings, but it is just a small demonstration nonetheless). However, the right color can be found out by tweaking the values in eroding and dilating functions.

The program then determines the topmost point in the hull found, and uses it to determine the finger.
