from urllib import urlencode
import urllib2

def notify(message, config):
    data = {
        'room_id':config['HIPCHAT_ROOM_ID'],
        'from':config['HIPCHAT_FROM_NAME'],
        'message':message,
        "message_format":"text",
        "color":"green",
    }
    import pdb;pdb.set_trace()
    urllib2.urlopen('http://api.hipchat.com/v1/rooms/message?auth_token={0}'.format(config['HIPCHAT_AUTH_TOKEN']), urlencode(data))
