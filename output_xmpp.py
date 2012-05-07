import logging
from uuid import uuid4
from flexget.plugin import *

__version__ = (0, 1)

log = logging.getLogger('xmpp')

class OutputXMPP:

    rooms = []

    def validator(self):
        from flexget import validator
        config = validator.factory('dict')
        config.accept('text', key='jid', required=True)
        config.accept('text', key='password', required=True)
        config.accept('text', key='nickname')
        config.accept('text', key='connection_host')
        config.accept('integer', key='connection_port')
        config.accept('text', key='message_format')
        config.accept('text', key='message_type')
        return config

    def prepare_config(self, config):
        if isinstance(config, bool):
            config = {'enabled': config}
        config.setdefault('message_format', '{{title}} has started downloading')
        config.setdefault('message_type', 'headline')
        config.setdefault('nickname', 'FlexGet')
        return config

    def on_process_start(self, feed, config):
        try:
            from xmpp import Client, Message, JID, Presence
        except ImportError:
            raise PluginError("output_xmpp requires xmppy, either `pip install xmpppy` or `apt-get install python-xmpp`")

        debug = []
        self.jid = JID(config.get('jid'))
        self.client = Client(self.jid, debug=debug)

        if self.client.connect() is None or self.client.auth(self.jid.getNode(), config['password'], uuid4()):
            self.error('Unable to connect to XMPP, disabling plugin')
            config['enabled'] = None
            return
        self.client.SendInitPresence()
        log.debug('Connected to XMPP server on JID %s' % self.jid.getNode())

    def on_process_end(self, feed):
        if hasattr(self, 'client') and self.client.isConnected():
            self.client.disconnect()
        self.client = None

    def on_feed_output(self, feed, config):
        from xmpp import Client, Message, JID, Presence

        if config['enabled'] is None or feed.manager.options.learn:
            log.debug('XMPP plugin disabled or in learning mode, skipping.')
            return

        for entry in feed.accepted:
            body = entry.render(config.get('message_format'))
            if feed.manager.options.test:
                log.info("XMPP message: %s", body)
                continue
            msg = Message(body=body)
            for dest in [x.strip() for x in config['to'].split(',')]:
                if dest[0] == '@':
                    dest = dest[1:]
                    if not dest in self.rooms:
                        self.client.send(Presence("%s/%s" % (dest, config['nickname'])))                   
                    msg.setAttr('to', dest)
                    msg.setType('groupchat')
                else:
                    msg.setAttr('to', dest)
                    msg.setType(config['message_type'])
                self.client.send(msg)


register_plugin(OutputXMPP, 'xmpp')

    

