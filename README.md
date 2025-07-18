Description:
<br>
Pong Game:
<br>
This Python game is a classic Brick Breaker implemented using OpenGL (PyOpenGL). The player controls a green paddle at the bottom of the screen using keyboard keys 'a' and 'd' to move left and right. A white ball bounces around the screen, and the player must prevent it from falling off the bottom edge by deflecting it with the paddle.
<br>
The objective is to break all the colored bricks arranged in rows at the top. When the ball hits a brick, the brick disappears and the player earns points. The ball also speeds up slightly after each successful paddle hit, increasing the challenge over time. If the ball misses the paddle and falls below the screen, the game ends, showing a "Game Over" message along with the final score.
<br>
A “Restart” button appears on the screen upon game over. Clicking it with the mouse restarts the game. The game features randomly colored bricks, dynamic ball and paddle color changes, a scoring system, and a simple grid background for aesthetics. The game uses OpenGL drawing primitives and GLUT functions to manage rendering, input handling, and real-time updates.