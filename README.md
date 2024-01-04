# What is DisDrive?
Welcome to DisDrive, an ingenious program that transforms Discord into a file storage platform, similar to Google Drive. The best part? It offers theoretically unlimited storage at no cost!

# How It Works:
- _**File Splitting for Upload:**_ Discord has a file upload limit of 25MB. DisDrive splits the file into 25MB text files. Each segment is then uploaded to a server via a Discord bot.
- _**Tracking and Managing Files:**_ Each uploaded file chunk is associated with a unique Message ID, which is stored in our database. Need to download or delete a file? DisDrive uses these IDs to swiftly manage your requests.
- _**Downloading files:**_ Each Message ID is fetched and file is reconstructed.
- _**Sequential Request Processing:**_ To keep things straightforward and efficient, DisDrive processes one request at a time. This approach not only makes the program user-friendly but also demonstrates the potential of our concept.
- _**No Cancel Option (Yet):**_ Currently, there's no option to cancel a request once initiated. So, please be patient and let the request complete before closing the program.
# Important Note:
While DisDrive showcases a creative use of Discord for file storage, it's crucial to remember that this method is not the most secure. Think of DisDrive as a proof of concept—a demonstration that file storage is feasible on any platform allowing file uploads, even those with restrictions.
**ONLY RUN IT IN YOUR OWN SERVER WITH NO ONE OTHER THAN YOU AND THE BOT.**
# Setup:
- _**Install Dependencies:**_ I've included a setup shell script with the program. This script automatically downloads all necessary libraries and modules for DisDrive. If permission is denied ```chmod 777 setup.sh``` should do the trick.
- _**Configure Your Bot:**_
  - [Visit Discord Developer Portal.](https://discord.com/developers/applications)
  - Create a new bot and grant it all of the permissions.
  - At the end of the setup script, you'll be prompted to enter the Channel ID and your Discord Bot Token. This is crucial for linking DisDrive with your Discord.

# Compile and Run:
- _**Compilation:**_
  - Use the command ```gcc -o run run.c``` to compile the executable. This program uses child processes to run all of the 3 programs.
  - Once compiled, you can start the program by executing ```./run```.
- _**Ports and Functionality:**_
  - The program uses port ```4000``` for storing JSON data.
  - The main program runs on port ```3000```.

# Closing the Program:
- _**Procedure:**_
  - Ensure that any ongoing request is completed before attempting to close the program.
  - On a Mac, press ```^ + C``` (Control + C) a few times to safely terminate the program.
- _**Compatibility:**_
  - DisDrive is compatible with Mac and Linux systems.
  - **Note:** If on windows you can't use the C program, instead open up 3 terminals. Execute ```python3 DisDrive.py``` and ```pyhton3 server.py``` in flask-backend directory, and finally ```npm start``` in client directory. 

