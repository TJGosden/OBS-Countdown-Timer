import os

""" Using a stream software like "MixItUp", append the following variables (E.g. q, or s)
    to the "time.txt" file under a certain condition, i.e. channel point reward. 
    When redeemed the script will add time to the timer based on the input variable "addTime"."""

twitchAdd = "q"
# This variable will add "subAddTime" if written into the file
twitchAddSub = "s"
subAddTime = 3600           # 3600 seconds = 1 hour

#Function to read "time.txt" file and check for "twitchAdd" or "twitchAddSub" (q or s). 
def twitch_add(currentTime, addTime):
    fileIncrease = open(get_increase_file_path(), "r")
    #Copy the first line of the file
    increase = fileIncrease.read(1)
    if (increase == twitchAdd or increase == twitchAddSub):
        #Add based on file input (q or s).
        if (increase == twitchAdd):
            currentTime = currentTime + addTime
        elif (increase == twitchAddSub):            
            currentTime = currentTime + subAddTime
        #Remove only one instance of add time "q" incase too many are redeemed at once
        with fileIncrease as filedata:
            inputFilelines = filedata.readlines()
            lineindex = 1
            with open(get_increase_file_path(), 'w') as filedata:
                for textline in inputFilelines:
                    if (lineindex != 1):
                        filedata.write(textline)
                    lineindex += 1
            filedata.close()
    fileIncrease.close()
    return currentTime

#Get the file path in which the file "time.txt is stored.
def get_increase_file_path():
    path = os.path.join(os.getenv('APPDATA'), "obs-countdown")
    #Create the folder "obs-countdown" if it doesn't already exist.
    if not os.path.exists(path):
        os.makedirs(path)
    return os.path.join(path, "time.txt")