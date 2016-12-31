import Slack
import TBAconnection

points_for_rank = [45, 35, 25, 20, 15, 10, 7, 3]

def quals_update(eventid):
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
        attachment_text += "*Team " + str(team[1]) + "*"
        attachment_text += " with " + str(team[2]) + " ranking points"
        attachment_text += " and a record of " + str(team[7])
        attachment_text += " | _" + str(points) + " fantasy points_"
        attachment_text += "\n"



    attachments = [
        {
            "fallback": "Error in sending message.",
            "color": "#0000ff",
            "title_link": "https://www.thebluealliance.com/event/2016casj",
            "mrkdwn_in": ["text"],
            "text": attachment_text,
            "footer": "Fantasy FIRST Bot"
        }
    ]

    message = "Qualification results are out at the *" + event.get_name()+ "*!"

    Slack.send_message(message, attachments)



quals_update("2016cur")