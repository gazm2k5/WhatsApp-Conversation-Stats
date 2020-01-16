from pathlib import Path
import datetime
        
class WhatsAppConversation():
    """ Expects a WhatsApp Chat log in .txt format and creates conversation object
    containing title, message log (tuple of dicts), and participants list (tuple)."""
        
    def __init__(self, file):
        
        file = Path(file)
        filename = file.resolve().stem
        
        # Open WhatsApp .txt chat
        with open(file, encoding='iso-8859-1') as f:
            messages = []
            participants = set()
            while line := f.readline():
                # Get Sender name from message
                namemessage = line[20:]

                # Skip any system or irregular messages. NOTE: This will trim messages with line breaks to one line
                if len(namemessage) == 0: # Skip blank lines
                    continue 
                if ":" not in namemessage: # Ignore system messages. eg. "This chat is now secure" or "person changed the group description"
                    continue
                
                colonpos = namemessage.find(":") # find position of first colon in the message (separates sender name and message)
                sender = namemessage[0:colonpos]
                message = namemessage[colonpos+2:].rstrip("\n") # Get message and remove trailing \n

                # Get time from message
                try: # If there's no date stamp, it's likely a system message or message has \n new lines
                    day = int(line[0:2])
                    month = int(line[3:5])
                    year = int(line[6:10])
                    hour = int(line[12:14])
                    minute = int(line[15:17])
                    dt = datetime.datetime(year, month, day, hour, minute)
                except:
                    continue

                participants.add(sender)

                msg = {"date":dt, "sender":sender, "message":message}
                messages.append(msg)

        # Set up class variables        
        self.title = file.resolve().stem # The title of the chat (taken from file name)
        self.message_log = tuple(messages) # A log of all the messages in the conversation (date, sender, message)
        self.participants = tuple(participants) # A tuple containing all participants of the conversation
        self.num_participants = len(participants) # number of participants in the conversation
