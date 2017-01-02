# This class will handle converting Fantasy data into a format that can be relayed to Slack
# Author: Jonathan Zwiebel
# Version: 1 January 2017

import Slack
from FormattedTeam import formatted_team

def initial_update(eventid):
     message = "Tracking started for " + eventid
     Slack.send_message(message, attach="")

def quals_update(eventid, data):
    # TODO: Include rosters in data
    rosters = []
    rosters.append(["MemeTeam", "8"])
    rosters.append(["DreamTeam", "254", "330"])
    rosters.append(["CleanTeam", "118", "971"])

    attachment_text = ""

    quals_data = open(data + "/qual_data.csv", "r")    
    with quals_data:
        content = quals_data.read().splitlines()
    quals_data.close()

    info_data = open(data +"/information.txt", "r")
    with info_data:
        event_name = info_data.read().splitlines()[0]
    info_data.close()

    for i in range(len(content)):
        comma1 = content[i].index(",")
        comma2 = content[i].index(",", comma1 + 1)
        comma3 = content[i].index(",", comma2 + 1)

        number = content[i][:comma1]
        fantasy_points = content[i][comma1+1:comma2]
        rp = content[i][comma2+1:comma3]
        record = content[i][comma3+1:]

        attachment_text += str(i + 1) + ". "
        attachment_text += "Team " + formatted_team(str(number), rosters)
        attachment_text += " scores " + str(fantasy_points) + " fantasy points"
        attachment_text += " with " + str(rp) + " RP"
        attachment_text += " going " + str(record)
        attachment_text += "\n"

    attachments = [
        {
            "fallback": "Error in sending message",
            "color": "#0000ff",
            "title_link": "https://www.thebluealliance.com/event/" + eventid,
            "mrkdwn_in": ["text"],
            "text": attachment_text,
            "footer": "Fantasy FIRST Bot"
        }
    ]

    message = "Qualification results are out at the *" + event_name+ "*!"
    message += "\nCheck thebluealliance.com/event/" + eventid + " for updates."

    Slack.send_message(message, attachments)



def alliance_selection_update(eventid, data):
    rosters = []
    rosters.append(["MemeTeam", "8"])
    rosters.append(["DreamTeam", "254", "330"])
    rosters.append(["CleanTeam", "118", "971"])

    attachment_text = ""

    print(data + "/alliance_selection_data.csv")
    alliance_selection_data = open(data + "/alliance_selection_data.csv", "r")    
    with alliance_selection_data:
        content = alliance_selection_data.read().splitlines()
    alliance_selection_data.close()

    info_data = open(data +"/information.txt", "r")
    with info_data:
        event_name = info_data.read().splitlines()[0]
    info_data.close()

    # TODO: Find some library that can process csv files
    for alliance in content:
        commas = [alliance.index(",")]
        last_index = commas[0]
        while alliance.find(",", last_index + 1) != -1:
            last_index = alliance.index(",", last_index + 1)
            commas.append(last_index)
        commas.append(len(alliance))

        attachment_text += "*Alliance " + alliance[:commas[0]] + "*"
        for i in range(1, len(commas)):
            attachment_text += "  |  " + formatted_team(str(alliance[commas[i-1]+1:commas[i]][3:]), rosters)
        attachment_text += "\n"

    attachments = [
        {
            "fallback": "Error in sending message.",
            "color": "#0000ff",
            "title_link": "https://www.thebluealliance.com/event/" + eventid,
            "mrkdwn_in": ["text"],
            "text": attachment_text,
            "footer": "Fantasy FIRST Bot"
        }
    ]

    message = "Alliance selection is complete at the *" + event_name+ "*!"
    message += " Alliances are listed in pick order with Alliance Captain first."
    message += "\nCheck thebluealliance.com/event/" + eventid + " for updates."
    Slack.send_message(message, attachments)