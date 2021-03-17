# The Monty project
## TEE3201
### Final Project

***

<p>The Monty Project is an educational software project designed to take you through the steps of building a small software incrementally, while applying as many Python and SE techniques as possible along the way.</p>
<br>
The project aims to build a product named Monty, a Personal Assistant Chatbot that helps a person to keep track of various things. The name Monty was chosen as a placeholder name, in honor of the Monty Python comedy group whose work inspired the name of the the Python language. You may give it any other name and personality you wish.<br>
<br>
Here is a sample interaction with Monty:</p>
```markdown
*******************************************************************************************
*  __          __  _                            _          __  __             _           *
*  \ \        / / | |                          | |        |  \/  |           | |          *
*   \ \  /\  / /__| | ___ ___  _ __ ___   ___  | |_ ___   | \  / | ___  _ __ | |_ _   _   *
*    \ \/  \/ / _ \ |/ __/ _ \| '_ ' _ \ / _ \ | __/ _ \  | |\/| |/ _ \| '_ \| __| | | |  *
*     \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) | | |  | | (_) | | | | |_| |_| |  *
*      \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/  |_|  |_|\___/|_| |_|\__|\__, |  *
*                                                                                  __/ |  *
*                                                                                 |___/   *
*******************************************************************************************

>>> What can I do for you?

help
>>> I'm glad you asked. Here it is:
==================================================
Monty can understand the following commands:

add DESCRIPTION
Adds a task with the DESCRIPTION to the list
Example: add read book
done INDEX
Marks the task at INDEX as 'done'
Example: done 1
exit
Exits the application
help
Shows the help information
list
Lists the tasks in the list
--------------------------------------------------

>>> What can I do for you?

add read book
>>> Task added to the list
>>> What can I do for you?

add return book
>>> Task added to the list
>>> What can I do for you?

done 1
>>> Congrats on completing a task! :-)
>>> What can I do for you?

list
>>> Here is the list of tasks:
==================================================
STATUS | INDEX | DESCRIPTION                
--------------------------------------------------
X    |   1   | read book
-    |   2   | return book
--------------------------------------------------
>>> What can I do for you?
```
