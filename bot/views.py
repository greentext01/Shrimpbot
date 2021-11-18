import json
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
import requests
import threading

from bot.models import Game

# Create your views here.
zoom_verification_token = 'BOEocvS7TbC-CQdnhLjFHw'
zoom_bot_jid = 'v1flibvr30rwamemhltiewsa@xmpp.zoom.us'
zoom_client_id = 'jrYOVqXdSAGpD_rPQDI6g'
zoom_client_secret = '81qupvgxJrZX8V4NQx787N0nTK0zA31a'


def exec_command(cmd: str, payload):
    match cmd.split(' ')[0]:
        case 'say':
            send_msg(cmd.removeprefix('say '), payload)

        case 'list':
            msg = '*Games List (With Shrimp 🦐)*\n\n*Consider contributing! Send me or @✨Winning Lisa✨ a message and you will get credited with the game.*'

            for item in Game.objects.all():
                msg += f'\n\n{item.name}: {item.url}'

            send_msg(msg, payload)

        case 'add':
            split = cmd.removeprefix('add ').split(';')
            try:
                game = Game(name=split[0], url=split[1])
                game.save()
                notify('Game added!', payload)
            except:
                notify('Syntax error!', payload)
        
        case 'del':
            name = cmd.removeprefix('del ')
            try:
                Game.objects.get(name=name).delete()
                notify('Game removed!', payload)
            except Game.DoesNotExist:
                notify('This game does not exist!', payload)

def get_token():
    return requests.post('https://zoom.us/oauth/token?grant_type=client_credentials',
                          auth=(zoom_client_id, zoom_client_secret)).json()['access_token']


def notify(message, payload):
    message_id = send_msg(message, payload)["message_id"]

    timer = threading.Timer(5, delete_msg, [message_id, payload])
    timer.start()


def delete_msg(message_id, payload):
    token = get_token()

    requests.delete(f'https://api.zoom.us/v2/im/chat/messages/{message_id}', headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }, json={
        'robot_jid': zoom_bot_jid,
        'account_id': payload['accountId']
    })


def send_msg(message, payload):
    token = get_token()

    message = requests.post('https://api.zoom.us/v2/im/chat/messages', headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }, json={
        'robot_jid': zoom_bot_jid,
        'to_jid': payload['toJid'],
        'account_id': payload['accountId'],
        'content': {
            'head': {
                'text': message
            }
        },
        'is_markdown_support': True
    }).json()

    return message


@require_GET
def index(request):
    return HttpResponse('You found an easter egg!')


@require_GET
def authorize(request):
    return redirect(f'https://zoom.us/launch/chat?jid=robot_{zoom_bot_jid}')


@require_POST
@csrf_exempt
def shb(request):
    body = json.loads(request.body)
    payload = body['payload']
    exec_command(payload['cmd'], payload)
    return HttpResponse()
