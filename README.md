# **'Who Wants to be a Millionaire?' Flask Quiz App CS50x**
#### **Video Demo**:  https://youtu.be/3naBNU8C3MA
### **Description**:

Hello, this is bek000han from Kazakhstan and here is my CS50x final project I have made. This is a web-based quiz game inspired by the iconic 'Who Wants to be a Millionaire' trivia game show and strives to be a faithful recreation. The application was developed using Flask and SQLite, written mainly in Python and some Javascript, and uses a number of libraries to provide additional utility.

The app lets users create their own account, play the classic quiz game and track their progress, and of course compete with other users on a global leaderboard. The game consists of multiple stages (12 questions) with increasing difficulty levels for the questions as the user progresses. At each stage, the user is presented with a question and multiple-choice answers. The user needs to select the correct answer continue to the next stage. If the user fails or reaches the million dollar question, they are rewarded their prize pool, which is saved onto the leaderboard for all to see.

### **Installation**:

- Clone the repository:
> $ git clone <repository_url>
- Change to the project directory:
> $ cd quiz-game

> Feel free to clear all sessions
- Install the required dependencies using pip:
> $ pip install Flask cs50
- Run the Flask application:
> $ flask run

> Ctrl + left click the flask provided hyperlink

### **Play Instructions**:

* Register/Login
    * Register an account by clicking on the "Register" link.
    - Providing a unique username and a good password.
    - Click the return to "Login" link.
    - Log in using your registered username and password.


- Main Menu
    - "New Game" starts a new round of the quiz game.
    - "High Scores" displays the top 10 users with the highest amount of money earned.
    - "Log Out" logs out the current user and redirects to the login page.

&nbsp;
- Quiz Game:
    - When you start a new game, you will be presented with a series of questions.
    - Select the correct answer to progress to the next stage and earn money.
    - If you choose the correct answer, you keep playing the game and the winnings will increase.
        - A modal window will also pop up to track your ingame progress.
    - If you choose the wrong answer or exit the game, the game ends.
    - After completing the game by losing or winning, you will see the amount of money earned.
    - The prize pool is added to your total winnings on the leaderboard.
    - You can choose to play again, go back to the main menu, or log out.

### **Present Issues**:

- The application currently does not have robust error handling or validation for user inputs.
Invalid inputs may cause unexpected behavior.
- The design and layout of the application could be improved for a more visually appealing user interface.
- Audio clipping and the looping can be improved significantly if done properly.
- Performance optimizations can be made, especially for database queries and loading questions during gameplay.
- The application lacks comprehensive unit tests and could benefit from a testing framework for automated testing.
- Some unsafe SQL queries may be present in the code, and must be validated at a later date.

### **Future Plans**:

- Implement additional features such as lifelines to provide hints or assistance during gameplay.
    - Ask the audience
    - 50 / 50
    - Ask the Expert
- Add support for different quiz categories and allow users to choose specific categories for their quiz sessions.
- Create an admin panel or dashboard for managing quiz questions, user accounts, and leaderboard entries.
- Add more questions with hopefully at least 1000 different questions, of which include
    - x400 level 0 questions
    - x400 level 1 questions
    - x200 level 3 questions

### **Contributing**:

Contributions to the Quiz Game project are welcome and encouraged! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.

### **License**:

The Quiz Game project is licensed under the MIT License.
