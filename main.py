from WhatsAppConversation_Class import *
from WhatsAppConversation_Grapher import *

if __name__ == "__main__":            

    # Create Conversation Log object
    # Go to a WhatsApp Conversation, click the 3 dots in the top right,
    # hit "more" and press "export chat" to get a .txt file.
    filepath = "WhatsApp Chat with Gary Miranda.txt" # Can be a full path eg. "C:\\Chats\\WhatsApp Chat with Joe Bloggs.txt"  
    myConvo = WhatsAppConversation(filepath)
    
    # Choose which charts to plot
    chart_types = {
        "stack plot" : True,
        "stacked bar" : True,
        "grouped bar" : False,
        "line plot" : False
        }

    start_date = datetime.datetime(2019, 1, 1) #yyyy, mm, dd
    end_date = datetime.datetime(2019, 12, 31)

    group_messages = False # Group messages will treat bursts of messages (within 30 seconds) as 1 message
    bin_size = 7 # bin_size will collect data in bins (ie. bin_size=7 will tally messages by week)

    # Plot Charts
    plot_messages_time(myConvo, chart_types=chart_types,
                       bin_size=bin_size, group_messages=group_messages)
                       # start_date=start_date, end_date=end_date) # To use the entire conversation, comment out this line
