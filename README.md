# SQL-Recipe-Database
Database Design Project: Python application where a user is able to view and upload different cooking recipes

By Allen Lim, Malachy Ayala, and Vivek Divakarla

Instructions to run the application
- Install some version of Python 3. We used Python 3.7.9 and the Python IDLE to run our code
- Use pip in your terminal to install PyQt5, PyQt Tools, as well as pymysql
- “pip install PyQt5” should be enough to install PyQt5
- Documentation: https://pypi.org/project/PyQt5/
- “pip install pyqt5-tools” installs the Qt Tools necessary to run - Documentation: https://pypi.org/project/pyqt5-tools/
- “python3 -m pip install PyMySQL” for pymysql
- Documentation: https://pypi.org/project/PyMySQL/
- Simply open the file `finalPtest.py` in the Python IDLE and run the module, the program will then request the password needed to access your local SQL Workbench.

## Lessons Learned
- This project provided a range of opportunities for gaining new technical expertise. We
learned how to connect to a SQL database using python. Additionally, we learned how to extract the data and display it to users. In order to do this, we also figured out how to use Object-Oriented Programming in python to display an operating GUI with data from SQL loaded into it. A big learning point in this project was learning how to use SQL side defined functions and procedures to make the python code more efficient as well. While it wasn’t necessarily difficult. linking the GUI pages was definitely an interesting and important learning process. It was made even more important when we had to use the GUI and the inputted information to implement the CRUD commands for the tables in SQL.
- Beyond the programming side of things, the project as a whole really enforced good time management. If we hadn’t started early, I’m not sure how much we would have been able to finish.
- I don’t think this is really an alternative approach but we could have designed the menu table a bit better as well as it’s keys.
All of our code works but we were unable to implement the menus and display the data as we originally planned to. However, a user’s menus can be displayed.

## Future Work
- We plan to provide this database to a company that is trying to convert physical recipe books into an online format whether it is web-based or app-based. Our front end application allows our client to navigate through the capabilities of our database.
There are several functionalities that can be added to our application that would create a better user experience, including but not limited to:

a. Allow users to remove recipes

b. Allow users to create new ingredients and add ingredients to a recipe

c. Allow users to add recipes to the menu, and create/edit/remove a menu

d. Allow users to get verified as gourmet chefs

e. Allow users to get their recipes verified

f. Allow users to leave reviews on recipes

g. Allow users to view gourmet chef’s recipes and leave ratings on them

h. Allow users to search for a certain recipe by its name, location, or author
