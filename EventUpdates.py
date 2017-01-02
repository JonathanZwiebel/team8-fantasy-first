import Slack
import TBAconnection
from FormattedTeam import formatted_team

points_for_rank = [45, 35, 25, 20, 15, 10, 7, 3]

def quals_update(eventid):
    rosters = []
    rosters.append(["MemeTeam", "8"])
    rosters.append(["DreamTeam", "254", "330"])
    rosters.append(["CleanTeam", "118", "971"])

    qual_ranking = TBAconnection.get_event_ranking(eventid)
    event = TBAconnection.get_event(eventid)

    attachment_text = ""

    for i in range(len(qual_ranking.get_ranking()) - 1):
        team = qual_ranking.get_team_in_rank(i + 1)

        points = float(team[2])

        if i < 8:
            points += points_for_rank[i]

        dash_index = team[7].index('-')
        wins = int(team[7][:dash_index])
        plays = int(team[8])

        if plays - wins == 0:
            points += 14
        elif plays - wins <= 2:
            points += 5

        attachment_text += str(i + 1) + ". "
        attachment_text += "Team " + formatted_team(str(team[1]), rosters)
        attachment_text += " with " + str(team[2]) + " ranking points"
        attachment_text += " and a record of " + str(team[7])
        attachment_text += " | " + str(points) + " fantasy points"
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

    message = "Qualification results are out at the *" + event.get_name()+ "*!"

    Slack.send_message(message, attachments)


def alliance_selection_update(eventid):
    rosters = []
    rosters.append(["MemeTeam", "8"])
    rosters.append(["DreamTeam", "254", "330"])
    rosters.append(["CleanTeam", "118", "971"])

    event = TBAconnection.get_event(eventid)
    alliances_lists = event.get_alliances_lists()

    attachment_text = ""

    for rank in range(len(alliances_lists)):
        attachment_text += "*Alliance " + str(rank + 1) + "*"
        for team in alliances_lists[rank]:
            attachment_text += "  |  " + formatted_team(str(team[3:]), rosters)
        attachment_text += "\n"
    print attachment_text

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

    message = "Alliance selection is complete at the *" + event.get_name()+ "*!"
    message += " Alliances are listed in pick order with Alliance Captain first."
    Slack.send_message(message, attachments)

quals_update("2016casj")
