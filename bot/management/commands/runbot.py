import datetime
from collections import defaultdict

import slack
from bot.models import CakeRatio, Meeting, MeetingAttendee
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

bot_user_id = None


@slack.RTMClient.run_on(event='hello')
def connected(**payload):
    global bot_user_id
    web_client: slack.WebClient = payload['web_client']
    auth = web_client.auth_test()
    bot_user_id = auth['user_id']
    print('CakeBot has connected as ' + bot_user_id)


@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    global bot_user_id
    data = payload['data']
    web_client: slack.WebClient = payload['web_client']
    user = data.get('user')
    cmd = data.get('text', None)

    response = parse_command(cmd)

    if user:
        channel_id = data['channel']
        #thread_ts = data['ts']
        web_client.chat_postMessage(
            channel=channel_id,
            text=response
        )


def parse_command(cmd):
    if not cmd:
        return 'Empty command'

    try:
        if cmd.startswith('new meeting '):
            return handle_new_meeting(cmd[12:])
        elif cmd.startswith('next'):
            return handle_next(cmd)
        elif cmd.startswith('list'):
            return handle_list(cmd[4:])
        elif 'recalculate' in cmd:
            recalculate_ratios()
            return 'done'
        elif cmd.startswith('help'):
            return help()
        else:
            return help()
    except Exception as e:
        print(e)
        return 'An unexpected error has occurred!'


def help():
    return """
Usage: @CakeBot <command>

All persons should be references by initials, e.g., kse, frh, etc.

Commands:
help:    Show help.
next:    Show who should bring the next cake.
list:    List users and their cake ratio.
new meeting YYYY-MM-DD BAKER [ATTENDEES]:    Add new meeting."""

def handle_new_meeting(cmd):
    ss = cmd.split(' ')

    if len(ss) < 2:
        return 'Error: new meeting command requires at least a date and a baker'

    try:
        dt = datetime.datetime.strptime(ss[0], '%Y-%m-%d')
    except:
        return f'Error: Could not parse {ss[0]} as a date. Should be on the format YYYY-mm-dd'

    try:
        user = User.objects.get(username=ss[1])
    except:
        return f'Error: Person {ss[1]} does not exist'

    meeting = Meeting.objects.create(baker=user, date=dt)

    attendees = ss[1:]
    attendees = set(attendees)

    for attendee_name in attendees:
        try:
            attendee = User.objects.get(username=attendee_name)
        except:
            return f'Error: Person {attendee_name} does not exist'

        ma = MeetingAttendee.objects.create(meeting=meeting, attendee=attendee)
        ma.save()

    meeting.save()

    recalculate_ratios()

    return 'Meeting on ' + dt.strftime("%d %B, %Y") + ' with ' + str(len(attendees)) + ' attendees ' + user.username + ' will bring cake'


def handle_next(cmd):
    user = User.objects.order_by('cakeratio__ratio')[0]
    return user.username + ' is next with a ratio of ' + str(user.cakeratio.ratio)


def handle_list(cmd):
    list_usage = """Usage:

list users:     Show list of users and their cake ratio
list meetings:  Show list of meetings"""

    if not cmd:
        return list_usage

    if 'users' in cmd:
        users = User.objects.order_by('cakeratio__ratio')
        response = ""
        for user in users:
            response += f"{user.username}: {user.cakeratio.ratio}\n"
        return response
    elif 'meetings' in cmd:
        meetings = Meeting.objects.order_by('-date')
        response = ""
        for meeting in meetings:
            response += f"{meeting.id}: {meeting.date}\n"
        return response
    else:
        return list_usage


def recalculate_ratios():
    ratios = defaultdict(lambda: defaultdict(float))

    meetings = Meeting.objects.all()

    for meeting in meetings:
        ratios[meeting.baker.username]['given'] += 1.0

        meeting_attendees = MeetingAttendee.objects.filter(meeting_id=meeting.id)

        for ma in meeting_attendees:
            ratios[ma.attendee.username]['eaten'] += 1.0 / len(meeting_attendees)
            ratios[ma.attendee.username]['ratio'] = ratios[ma.attendee.username]['given'] / ratios[ma.attendee.username]['eaten']

    for user, ratio in ratios.items():
        user = User.objects.get(username=user)
        user.cakeratio.ratio = ratio['ratio']
        user.cakeratio.baked_cakes = ratio['given']
        user.cakeratio.eaten_cakes = ratio['eaten']
        user.cakeratio.save()

        print(user.username + ' now has a ratio of ' + str(user.cakeratio.ratio))


class Command(BaseCommand):
    help = 'Run CakeBot'

    def handle(self, *args, **options):
        slack_token = "insert token here"
        rtm_client = slack.RTMClient(token=slack_token)
        rtm_client.start()
