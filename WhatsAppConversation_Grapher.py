import datetime

import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
from plotly import subplots
from itertools import cycle

def collate_data(conversation, bin_size="W", start_date=pd.Timestamp("2010-01-01 00:00:00"), end_date=pd.Timestamp("2050-01-01 00:00:00")):
    """ Expects a WhatsApp Chat log as a list item,
    and returns x data (time) and y data (messages sent, as a dict)
    Can return cumulative data for stack plots, or non cumulative for bar/line graphs.
    For non cumulative data, you can group messages in bins (eg. bin_size=7 is messages grouped by week)
    If someone tends to send lots of short messages at once, you can set group_messages=True to treat them as one """

    # Create x axes of Time data
    if start_date > end_date:
        print("Error. start_date is after end_date")
        exit()

    # Filter dataframe by date
    filt = (conversation.message_log["date"] >= start_date) & (conversation.message_log["date"] <= end_date)
    df = conversation.message_log[filt]

    # Group messages by sender and get message counts
    df.set_index("date", inplace=True)

    count_df = (df.groupby(["sender"])[["sender"]] # We group by sender, and only display sender column (we could actually display any column because we're going to count these later and use that data)
                        .resample(bin_size) # Resample to bin_size (eg. msgs sent per day). See pandas docs, can use D, 2W, M etc.
                        .count() # count messages sent per day (or per bin size)
                        .unstack(0, fill_value=0) # unstack grouped data to put senders as columns
                        .droplevel(0, axis=1) # We have multi indexed column. 1st index is "sender" so drop it.
                )

    cum_df = (df.groupby(["sender"])[["sender"]] # We group by sender, and only display sender column (we could actually display any column because we're going to count these later and use that data)
                        .resample("D") # Resample by day. By minute creates too much data.
                        .count() # count messages sent per day (or per bin size)
                        .unstack(0, fill_value=0) # unstack grouped data to put senders as columns
                        .droplevel(0, axis=1) # We have multi indexed column. 1st index is "sender" so drop it.
                        .cumsum()
                )

    return count_df, cum_df

def colour_selection(rainbow_colours, num_participants):
    """ Expects a list of colours and an int for the number of participants in the chat.
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

def plot_messages_time(conversation, chart_types={"stack plot":True, "bar chart":True},
                       bin_size="W", barmode="stack",
                       start_date=pd.Timestamp("2010-01-01 00:00:00"), end_date=pd.Timestamp("2050-01-01 00:00:00")):
    """ Expects a WhatsApp Conversation Log Class object and displays a graph of messages sent/received over time.
    Optiona Parameters include graph types to display, bin_size for sampling data by day, week etc, and a time frame to plot """

    # Get chart data
    print("Collating data")
    cnt_df, cum_df = collate_data(conversation, bin_size=bin_size,
                        start_date=start_date, end_date=end_date)
    participants = list(cnt_df.columns) # as we may have narrowed down the time frame, we don't want to use conversation.participants
    num_participants = len(participants)
    print("Data successfully collated")
            
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
    colours = cycle(colours) # turn into a generator that cycles through each colour

    # Create a colour map dictionary
    colour_map = {}
    for participant in participants:
        colour_map[participant] = next(colours)

    print("Plotting Data")

    # Bar Chart
    if chart_types["bar chart"]:
        traces1 = []
        for participant in participants:
            traces1.append(go.Bar(
                x=cnt_df.index, y=cnt_df[participant],
                name=participant,
                marker={"color":colour_map[participant], "line_color":colour_map[participant]},
                legendgroup=participant, # Ensures one legend for multiple plots
            ))

    # Stack Plot
    if chart_types["stack plot"]:
        traces2 = []
        for participant in participants:
            traces2.append(go.Scatter(
                x=cum_df.index, y=cum_df[participant],
                name=participant,
                marker={"color":colour_map[participant], "line_color":colour_map[participant]},
                fillcolor=colour_map[participant],
                hoveron = 'points+fills', # I think this is a known bug, doesn't work without fill=toself which messes up chart
                stackgroup="one",
                legendgroup=participant,
                showlegend=False if chart_types["stack plot"] == True else True, # Only show legend if first legend is not shown
            ))

    print("Formatting charts")
    subplot_count = 2 if chart_types["bar chart"] and chart_types["stack plot"] else 1

    # Plot Multiple subplots
    fig = subplots.make_subplots(
        rows=subplot_count, cols=1,
        shared_yaxes=True,
        vertical_spacing = 0.10, # 10%
        )

    if chart_types["bar chart"]:
        for trace in traces1:
            fig.append_trace(trace,1,1)

    if chart_types["stack plot"]:
        for trace in traces2:
            fig.append_trace(trace,subplot_count,1) # if you add more plots, this needs editing

    # TODO: Add minor Tick Marks

    fig.update_layout(
            title=f"{conversation.title}",
            xaxis={"title":"Date", "gridcolor":"#aaaaaa",
                "ticks":"outside"},
            xaxis2={"title":"Date", "gridcolor":"#aaaaaa",
                "ticks":"outside"},
            yaxis={"title":"Messages sent", "gridcolor":"#aaaaaa"},
            yaxis2={"title":"Messages sent", "gridcolor":"#aaaaaa"},
            plot_bgcolor="#242424",
            barmode=barmode,
            hovermode='x', # compare all traces on hover
            margin=dict(
                    b=30,
                    t=40
                    ),
        )

    # Range Slider
    # TODO: Tick marks not changing
    # fig.update_xaxes(
    #     rangeslider_visible=True,
    #         tickformatstops = [
    #             dict(dtickrange=["D1", "W2"], value="%d %b"),
    #             dict(dtickrange=["W2", "M3"], value="%b '%y"),
    #             dict(dtickrange=["M6", None], value="%Y Y")
    #         ]
    # )

    pyo.plot(fig, filename=f"{conversation.title}.html")
