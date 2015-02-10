import xmpp
import os
import ssl
contin = 'y'
rmessage = ''

def message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        if msg['type'] in ('chat', 'normal'):
             rmessage = msg['body']


while contin == 'y':


	print rmessage
	username = 'finchb79@grandline.terracrypt.net'
	passwd = 'Brionater1'
	to=raw_input('To: ')+ '@grandline.terracrypt.net'
	msg=raw_input('Message: ')


	client = xmpp.Client('grandline.terracrypt.net')
	client.connect(server=('grandline.terracrypt.net',5223))
	client.auth(username, passwd, 'botty')
	client.sendInitPresence()
	message = xmpp.Message(to, msg)
	message.setAttr('type', 'chat')
	client.send(message)
	os.system('clear')
	contin = raw_input('\ncontinue? (y/n): ')
