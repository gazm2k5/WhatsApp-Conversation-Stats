from WhatsAppConversation_Class import WhatsAppConversation
from WhatsAppConversation_Grapher import *

if __name__ == "__main__":            

    # Create Conversation Log object
    # Go to a WhatsApp Conversation, click the 3 dots in the top right,
    # hit "more" and press "export chat" to get a .txt file.
    filepath = "WhatsApp Chat with Joe Bloggs.txt" # Can be a full path eg. "C:\\Chats\\WhatsApp Chat with Joe Bloggs.txt"  
    myConvo = WhatsAppConversation(filepath)

    # Choose which charts to plot
    chart_types = {
        "stack plot" : True,
        "bar chart" : True,
        }

    start_date = pd.Timestamp("2019-01-01") # yyyy-mm-dd
    end_date = pd.Timestamp("2019-12-31")

    bin_size = "W" # bin_size will collect data for bar charts into bins. day, week, month, quarter and year are valid: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
    barmode = "stack" # stack or group. Warning: Grouped bars take more horizontal space, so may need larger bin size

    # Plot Charts
    plot_messages_time(
        myConvo,
        chart_types=chart_types,
        bin_size=bin_size,
        barmode = barmode,
        #start_date=start_date, end_date=end_date, # To use the entire conversation, comment out this line
    ) 