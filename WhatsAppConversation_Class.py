import pandas as pd
from pathlib import Path
        
class WhatsAppConversation():
    """ Expects a WhatsApp Chat log in .txt format and creates conversation object
    containing title, message log as Pandas DataFrame, and participants list (tuple)."""
        
    def __init__(self, file):
        file = Path(file)

        # Open WhatsApp .txt chat
        with open(file, encoding='iso-8859-1') as f:
            data = {"date": [], "sender" : [], "message" : []}
            participants = set() # Set of conversation participants
            while line := f.readline():

                 # skip blank lines and system messages
                if len(line) <= 1:
                    continue

                # Extract date from line
                try:
                    # Get everything before first hyphen, strip white space, convert to pd datetime
                    thisline = line.split("-", 1) # split line into list (max 1 split)

                    if len(thisline) <= 1: # multiline messages may insert blank lines into log. Skips these.
                        continue
                    
                    dt = pd.to_datetime(thisline[0].strip(), dayfirst=True) # use day first dates. Set false if you're backwards.
                except ValueError:
                    continue # Usually here if there's a system message with no timestamp
                
                if ":" not in thisline[1]: # Ignore system messages. eg. "This chat is now secure" or "person changed the group description"
                    continue
                else:
                    namemessage = thisline[1].split(":", 1) # Get name and message (after first colon) and split into list
               
                sender = namemessage[0].strip() # Get name (everything before first colon)
                message = namemessage[1].strip().rstrip("\n") # Get everything after first colon, (ie. message), remove white space and trailing \n

                participants.add(sender)

                data["date"].append(dt)
                data["sender"].append(sender)
                data["message"].append(message)

        # Set up class variables        
        self.title = file.resolve().stem # The title of the chat (taken from file name)
        self.message_log = pd.DataFrame(data) # A DataFrame of all the messages in the conversation (date, sender, message)
        self.participants = tuple(participants) # A tuple containing all participants of the conversation
        self.num_participants = len(participants) # number of participants in the conversation