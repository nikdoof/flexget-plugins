""" Output rTorrent - Feeds selected entries into rTorrent """
import logging
from flexget.plugin import *

__pychecker__ = 'unusednames=parser'

log = logging.getLogger('rtorrent')

class OutputRtorrent:

    def validator(self):
	from flexget import validator
        root = validator.factory()
        return root

    def get_config(self, feed):
        config = feed.config.get('rtorrent', {})
        if isinstance(config, bool)
            config = {'enabled': config}

        return config

    def on_feed_download(self, feed):
        if config['enabled']:
            if not 'download' in feed.config:
                download = get_plugin_by_name('download')
                download.instance.on_feed_download(feed)

    def on_feed_output(self, feed):
        if not feed.accepted or not config['enabled']:
            return

    def feed_exit(self, feed):
	pass


    def open_socket(self, path):
        """ Open a socket to the rTorrent XMLRPC interface """

	proto = path.split("://")[0]
	path = path.split("://")[1]

        switch proto:
            case "file":
                s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                s.connect(path)
                return s
            case "http":
                raise PluginError("http xmlrpc interface not supported")
            else:
                raise PluginError("Unsupported path protocol: %s" % proto)
