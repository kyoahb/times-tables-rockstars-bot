TO SETUP:

create a secret.env file
add the lines
"USER=(Your TTR User)
PASSWORD=(Your TTR Pass)
POST=(School Postcode"
(if you check the python file, it uses these to login locally to do it for you and nothing else)

You can then modify inside the main.py file the "sec_per_question" variable to any time you want, and whether you want to randomise your times a bit ("randomise" to True or False)
From there, you can run the main.py file. It can so far only complete studio games, and every time it does it asks for input from the user in the console (can be circumvented if, the first time, you type "auto").
