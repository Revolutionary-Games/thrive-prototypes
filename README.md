# Thrive-Prototypes

This repo holds various self-contained prototypes and tests of potential Thrive features.

Each prototype gets its own subfolder on the root directory, and can do almost anything it wants within.

Work on a prototype can be committed straight to master, however:
* No commit should affect more than one prototype without a good reason
* It would be good form to use a branch for a specific prototype if master ever starts getting very busy with lots of prototypes being worked on.
* If a prototype gets big and complicated it might be a good idea to do code review through pull requests.
* Commit messages should be descriptive. If you're doing a bugfix on a particular commit for a particular prototype, don't be afraid to use interactive rebase to merge the right commits. Yes, even on master -- prototypes shouldn't depend on each other, so rebasing the commits on one won't bother the others. Remember, rebase responsibly.

Each prototype is responsible for its own documentation -- keep in mind, though, that prototypes are meant to be tweaked and studied. Writing a monolithic spec is a bad idea, but taking extensive notes on ideas, analyses, etc is very good.

I'm not sure what we should use the issue tracker for. Discussion, most likely -- as long as we keep the discussion pertinent to the implementation of prototypes (Comments like "Upboat" and issues like "I have this idea that's really cool but I'm not a programmer so can someone do all the work for me pretty please?" are just asking to be deleted). We could use labels to organize issues by topic (eg, a "membrane" label, a "terrain" label, each with possibly multiple, overlapping prototypes and discussions).

## Why Prototype?
Prototypes are important for testing out aspects of the game before they enter production. You likely knew that already, but this gives us an important way to judge them -- We should learn something from them. Document the reasons behind major decisions, whether the reasons are important technical ones, or teh guiding philosophy behind the prototype. Once a prototype has reached the end of its useful life, it's important to gather all our results together, so we know what the prototype is telling us. If in summing up we uncover more questions, those are often perfect material for new prototypes!

## Python Version
Some of the older prototypes are writting in Python 2 and the newer ones are written in Python 3. In most cases the only difference is to the print function. If it throws an error when running , such as:

Missing parentheses in call to 'print'. Did you mean print(i)?

Then all you need to do is edit the file so that print has parenthesis, as it says above after "Did you mean" and then it should work fine in Python 3. 

## Installing pygame
A lot of the prototypes in this repo are writting in python + pygame. If you would like to run them here are some installation instructions, it might take as little as 10 minutes. 

1. Download and install python 3 from  https://www.python.org/downloads/ If it gives you the option to "add python to path" then choose that option and skip step 2.

2. If it doesn't you need to add python to your path variables. Basically what that means is each time you type in a terminal "python some_program.py" it will look in the path variables to see what to do when python is called.

To do this (if on win 10) click in the search box and type "path" and "edit the system control variables" should come up, click on the Advanced tab and then at the bottom click "Environmental Variables". In the "system variables" box click on the "Path" entry and click edit. Add a new line pointing to your python install, mine looks like "C:\Program Files (x86)\Python36-32\" but it should point to wherever python is with the right version.

3. In the search box type "cmd" and right click on command prompt and select "run as administrator" (this lets cmd install things on your pc). Type "python --version" and it should tell you which version of python is installed, if this works I think it means the path variable is set correctly. Congrats! You now have python.

4. now type "pip --version" and it should tell you pip is installed (it auto-installs as part of python now).

5. It's now really easy. Just type "pip install pygame" and it should install pygame for you and "pip install numpy" and it should install numpy for you.

6. navigate to a folder with a .py file in it (like one of the prototypes) and in your command prompt type "python <name_of_file>.py" to run it. One useful trick is that if you find the right folder in file explorer you can hold shift and then right click and one of the options in the menu (mine is open PowerShell window here) should open a command prompt at that location, which I think is easier than doing a lot of cd'ing.

If you have any trouble with this please post on our community forums and we will try to help you out :)

https://community.revolutionarygamesstudio.com/
