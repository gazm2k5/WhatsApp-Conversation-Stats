from collections import Counter
import datetime
import numpy as np
from matplotlib import pyplot as plt, dates as mdates

def collate_data(conversation, cumulative=False, bin_size=7, group_messages=False, start_date=mdates.num2date(730120), end_date=mdates.num2date(1000000)):
    """ Expects a WhatsApp Chat log as a list item,
    and returns x data (time) and y data (messages sent, as a dict)
    Can return cumulative data for stack plots, or non cumulative for bar/line graphs.
    For non cumulative data, you can group messages in bins (eg. bin_size=7 is messages grouped by week)
    If someone tends to send lots of short messages at once, you can set group_messages=True to treat them as one """
    
    # Create x axes of Time data
    if start_date > end_date:
        print("Error. start_date is after end date")
        exit()
    if start_date == mdates.num2date(730120): # if user hasn't specified a start date
        t1 = int(mdates.date2num(conversation.message_log[0]["date"].replace(hour=0, minute=0))) # First day where messeages were sent
    else:
        t1 = int(mdates.date2num(start_date)) # User specified start date
    if end_date == mdates.num2date(1000000): # if user hasn't specified an end date
        t2 = int(mdates.date2num(conversation.message_log[-1]["date"].replace(hour=0, minute=0))) + 1 # Day after final day
    else:
        t2 = int(mdates.date2num(end_date)) # User specified end date
        
    if cumulative == True: # To avoid spikey graph, "bin size" will group messages by week. Default is by week (7)
        bin_size = 1 # Always use 1 for cumulative data (as no risk of spikey data)

    time = [*range(t1,t2,bin_size)] # Create a list of time values
    
    # For larger bin sizes, the last few messages may have been sent half way through a week for example. Force the last date to be included here:
    if mdates.num2date(max(time)) != t2:
        final_date = max(time) + bin_size
        time.append(final_date)

    # Create y axes for sent and received messages
    participants_message_tally = dict([ (p,[]) for p in conversation.participants ]) # Dictionary of empty lists. One list for each person, containing all y values
    cnt = Counter() # Counter to track messages sent by each person

    # Track which message we're on (index j)
    j = 0 # start on first message
    if start_date != mdates.num2date(730120): # if user has specified a start date
        while conversation.message_log[j]["date"] < start_date:
            j += 1
    eoc = len(conversation.message_log) # end of conversation

    # Tally up messages
    for i in range(0, len(time)):
        # Reset counter. Don't reset for cumulative data (eg. stack plot)
        if cumulative == False:
            for person in cnt:
                cnt[person] = 0

        # Loop through messages sent on this date
        if j < eoc: # Make sure we haven't reached the last message (if j > eoc we get an error)
            while (msgdate := mdates.date2num(conversation.message_log[j]["date"])) <= time[i] and time[i] <= mdates.date2num(end_date):
                if msgdate <= time[i]:
                    if group_messages:
                        # Group messages (treat bursts of individual messages as one)
                        c0 = j > 0 # Ignore first message
                        c1 = conversation.message_log[j]["sender"] == conversation.message_log[j-1]["sender"] # Previous message was sent by the same person
                        c2 = (conversation.message_log[j]["date"] - conversation.message_log[j-1]["date"]) < datetime.timedelta(seconds=30) # Previous message was sent <2 minutes from this message
                        c_final = c0 * c1 * c2 # This is True if the participant has spammed lots of messages at once
                    else:
                        c_final = False # If group_messages is off, we are counting all messages
                        
                    if not c_final:
                        cnt[conversation.message_log[j]["sender"]] += 1 # Tally a message for this chat participant
                    
                    # Go to next message, or break if we've reached the end
                    j += 1
                    if j == eoc:
                        break

        # Add new y value for each person
        for person in conversation.participants:
            participants_message_tally[person].append(cnt[person])

    return time, participants_message_tally

def colour_selection(rainbow_colours, num_participants):
    """ Expects a list of colours and an int for the numer of participants in the chat.
    Returns a list of colours in an order that provides better contrast for charts.

    If you have a list of gradually shifting colours (eg. a rainbow) but only 2 participants,
    it's better to use colours from the top and middle of the list (eg. red and blue)
    rather than 2 adjacent colours (eg. red and orange) """

    num_colours = len(rainbow_colours)
    if num_participants > num_colours / 2: # This algorithm won't do anything in this case
        return rainbow_colours # so just return the original colours
    
    new_colours = [] # Create list of colours for result
    if num_participants >= num_colours:
            step = 1 # force step size = 1 if we have more people than colours
    else:
        step = num_colours // num_participants # step through the rainbow colours in larger steps if there are less people than colours
    
    for i in range(0, min(num_colours,num_participants)): # list should only use each colours once     
        x = (i * step) % num_colours
        new_colours.append(rainbow_colours[x])

    return new_colours

def plot_messages_time(conversation, chart_types={"stack plot":False, "stacked bar":False, "grouped bar":False, "line plot":False},
                       bin_size=7, group_messages=False, start_date=mdates.num2date(730120), end_date=mdates.num2date(1000000)):
    """ Expects a WhatsApp Chat log as a list item,
    and displays a graph of messages sent/received over time """

    print("Formatting charts")
    # Set graph style
    plt.style.use("bmh") # Change graph style https://matplotlib.org/gallery/style_sheets/style_sheets_reference.html

    # Determine what data we need
    if chart_types["stack plot"]:
        cumulative_data = True
    else:
        cumulative_data = False
        
    if chart_types["stacked bar"] or chart_types["grouped bar"] or chart_types["line plot"]:
        non_cumulative_data = True
    else:
        non_cumulative_data = False

    # Get x chart data
    # Get cumulative time data
    if cumulative_data == True:
        print("Collating cumulative data")
        x_data_cum, tally_cum = collate_data(conversation, cumulative=True,
                                             group_messages=group_messages,
                                             start_date=start_date, end_date=end_date) # Time data
        # Create alias (later we need to reference any available data)
        x_data_alias = x_data_cum
        tally_alias = tally_cum
        print("Cumulative data successfully collated")
        
    # Get non-cumulative time data
    if non_cumulative_data == True:
        print("Collating non-cumulative data")
        x_data_noncum, tally_noncum = collate_data(conversation, cumulative=False,
                                                   bin_size=bin_size, group_messages=group_messages,
                                                   start_date=start_date, end_date=end_date) # Time data (may be slightly different to cumulative data due to bin sizes)
        # Create alias
        x_data_alias = x_data_noncum
        tally_alias = tally_noncum
        print("Non-cumulative data successfully collated")
        
    # Get participants that have sent messages (if using a set time period, some people may not have sent messages)
    participants = []
    for person in tally_alias:
        if not all(x == 0 for x in tally_alias[person]): # If this person has any messages in this time period:
            participants.append(person)
    num_participants = len(participants)

    # Process tally data to y chart data
    if cumulative_data == True:
        y_data_cum = [ tally_cum[person] for person in participants ] # convert tally data from dict to lists (order matters, so we use a set list to loop, ie. participants)
    if non_cumulative_data == True:
        y_data_noncum = [ tally_noncum[person] for person in participants ]

    # Count how many subplots we need
    subplot_cnt = 0
    for key in chart_types:
        if chart_types[key]:
            subplot_cnt += 1
        
    # Create figure and a subplot for each graph
    if subplot_cnt > 1: # if we want more than 1 subplot
        fig, axs = plt.subplots(nrows=subplot_cnt, ncols=1, figsize=(20, 6*subplot_cnt)) # 6 inch height per subplot
    else:
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 6))
        axs = [ax] # The following code loops through axs a lot, so we need to create an iterable: axs
            
    # Set x axis labels
    chart_time_span = x_data_alias[-1] - x_data_alias[0] # Get chart time span in days
    if chart_time_span > 1825:   # > 5 years
        major_tick = mdates.YearLocator()   # Set major ticks to year
        x_axis_format = mdates.DateFormatter("%Y") # Label ticks eg. "2020"
        minor_tick = mdates.MonthLocator()  # minor ticks to month
    elif chart_time_span > 365: # > 1 year
        major_tick = mdates.MonthLocator() # major ticks to months
        x_axis_format = mdates.DateFormatter("%b '%y") # Label ticks eg. "Sep '19"
        minor_tick = mdates.WeekdayLocator() # minor ticks to week
    else:                       # < 1 year
        major_tick = mdates.WeekdayLocator() # major ticks to week
        x_axis_format = mdates.DateFormatter("%d %b") # label tick eg "18 Jun"
        minor_tick = mdates.DayLocator() # minor ticks to day
        

    # Format ticks on graphs
    for ax in axs:
        ax.xaxis.set_major_locator(major_tick) # Either major: years, minor months, or major months, minor weekdays
        ax.xaxis.set_major_formatter(x_axis_format)
        ax.xaxis.set_minor_locator(minor_tick)

    # Set colours of graphs
    for ax in axs:
        ax.set_facecolor("#242424") # Background colour
        ax.grid(color="#eeeeee") # Grid colour
        ax.tick_params(axis='x', which='minor', colors='#eeeeee') # set minor tick colour
        ax.tick_params(bottom=True, left= False, color="#ffffff", length=5, width=1.3) # Set little white markers for x-axis ticks

    # Rainbow colours for graph lines
    colours = [
        "#e96841",
        "#ed9a4a",
        "#f0c054",
        "#f4ef5f",
        "#c5d966",
        "#92cb6a",
        "#44bb6b",
        "#2fc0b9",
        "#1cc5ec",
        "#4398d1",
        "#5577c1",
        "#6153a8",
        "#9158a7",
        "#b75fab",
        "#e566ab",
        "#e16378",
        ]
    
    # Run colour list through an algorithm to provide better contrast
    colours = colour_selection(colours, num_participants) # comment this line out if you change the colours above

    bin_size_translation = {1: "day",
                            7: "week",
                            14: "2 weeks",
                            21: "3 weeks",
                            28: "4 weeks",
                            30: "month",
                            180: "6 months"}
    if bin_size in bin_size_translation:
        bin_label = bin_size_translation[bin_size]
    else:
        bin_label = f"{bin_size} days"

    # Plot the data on the subplots
    i = 0 # count how many graphs we're plotted
    if chart_types["stack plot"]:
        print("Plotting stack plot...", end="")
        axs[i].stackplot(x_data_cum, y_data_cum, labels=participants, colors=colours)
        handles, labels = axs[0].get_legend_handles_labels()
        axs[i].legend(reversed(handles), reversed(labels), loc='upper left')
        axs[i].set_ylabel('Cumulative Messages Sent')
        i += 1
        print(" done!")

    if chart_types["stacked bar"]:
        print("Plotting stacked bar chart...", end="")

        # Calcualte best bar width
        num_bars = ((x_data_noncum[-1] - x_data_noncum[0]) / bin_size) # Determine how many bars we're plotting
        x_units = x_data_noncum[-1] - x_data_noncum[0] # number of units on the x axis
        width = x_units / num_bars * 0.8 # (set bars at 80% width to add spacing)

        # Offset bars
        x_indexes = np.asarray(x_data_noncum) # To be able to offset bars (by width) with matplotlib, data must be an nparray
        x_offset = -width/2 # offset so the right edge of the bar lines up with the day value (better for large bin sizes)
     
        bottom_list = [ [0] * len(x_data_noncum) ] # Create a list of values for the base of each bar (starting with an array of zeroes)       
        for j in range(1, num_participants):
            temp = np.add(y_data_noncum[j-1], bottom_list[-1]).tolist() # Find starting height for bars by adding previous persons data to previous starting point
            bottom_list.append(temp)
        # Plot data
        for j in range(0, num_participants): # Each chart participant is plotted
            axs[i].bar(x_indexes+x_offset, y_data_noncum[j], bottom=bottom_list[j], width=width,
                        label=participants[j], color=colours[j % len(colours)])
        if i == 0:
            axs[i].legend()
        axs[i].set_ylabel(f'Messages Sent [per {bin_label}]')
        i += 1
        print(" done!")
        
    if chart_types["line plot"]:
        print("Plotting line plot...", end="")
        for j in range(0, num_participants): # We have to plot each chat participant separately
            axs[i].plot(x_data_noncum, y_data_noncum[j], linewidth=1,
                        label=participants[j], color=colours[j % len(colours)])
        if i == 0:
            axs[i].legend()
        axs[i].set_ylabel(f'Messages Sent [per {bin_label}]')
        i += 1
        print(" done!")
        
    if chart_types["grouped bar"]:
        print("Plotting grouped bar chart...", end="")
        num_bars = ((x_data_noncum[-1] - x_data_noncum[0]) / bin_size) * num_participants # number of bars to display
        x_units = x_data_noncum[-1] - x_data_noncum[0] # number of units on the x axis
        width = x_units / num_bars * 0.70 # (set bars at 80% width to add spacing)
        
        x_indexes = np.asarray(x_data_noncum) # To be able to offset bars (by width) with matplotlib, data must be an nparray
        for j in range(0, num_participants): # Each chart participant is plotted
            x_offset = +(0.5 * width) - (width * num_participants) + width*(j) # Right side of right most bar lines up with date value (better for large bin sizes)
            #x_offset = -(width * num_participants)/2 + width*(j) # Bars are centred around date value (with large bin size, may add excess space to the right of chart)
            axs[i].bar(x_indexes+x_offset, y_data_noncum[j], width=width,
                       label=participants[j], color=colours[j % len(colours)])
        if i == 0: # We only need 1 legend
            axs[i].legend()
        axs[i].set_ylabel(f'Messages Sent [per {bin_label}]')
        i += 1
        print(" done!")

    print("All charts plotted successfully!")    
        
    # Find max x value of graph
    if non_cumulative_data == True: # Because bin_size might be >1, the time axis for non-cumulative data may have a higher max
        min_time = x_data_noncum[0]
        # We can't simply take the last x_data value for max_time as a large bin_size may have added excess
        if end_date == mdates.num2date(1000000): # default end date
            max_time = mdates.date2num(conversation.message_log[-1]["date"]) # Last message date
        else:
            max_time = mdates.date2num(end_date)
        #if chart_types["grouped bar"]: # Depending on bar offset, we might want to add some space to the right of the chart
            #max_time = max_time + bin_size/2 
    elif cumulative_data == True:
        min_time = x_data_cum[0]
        max_time = x_data_cum[-1]
        
    # Trim graphs
    for ax in axs:     
        ax.set_xlim(min_time, max_time)
        ax.set_ylim(0)
    
    fig.suptitle(f"{conversation.title}", fontsize=15)
    plt.xlabel("Date")

    # Set tick label rotation of each axes
    for ax in fig.axes:
        plt.sca(ax) # set current axes to ax
        plt.xticks(rotation=90) # Set rotation
         
    plt.subplots_adjust(left=0.06, bottom=0.11, right=0.97, top=0.94, wspace=0.13, hspace=0.17) # Optimise white space around plots
    print("Displaying charts")
    plt.show()
