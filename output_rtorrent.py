""" Output rTorrent - Feeds selected entries into rTorrent """
import logging
from flexget.plugin import *
from urlparse import uses_netloc


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

            case "http":
                raise PluginError("http xmlrpc interface not supported")
            else:
                raise PluginError("Unsupported path protocol: %s" % proto)


class ScgiTransport(xmlrpclib.Transport):

    """ SGI Transport

        Used to communicate xmlrpc over raw SCGI services, like rTorrent """

    def __init__(self, use_datetime=0):
        self.headers=[]

    def _make_headers(self, headers):
        """ Generate the request headers """
        return '\x00'.join(['%s\x00%s'%t for t in headers])+'\x00'

    def _add_header(self, header, data):
        if not self.headers:
            self.headers = [('SCGI', '1'),] 
        self.headers.append((header, data))

    def _gen_netstring(self, data):
        return '%d:%s,' % (len(data), data)

    def _gen_request(self, data):
        """ Generates the full SCGI request """
        headers = [("CONTENT_LENGTH", len(data))]
        headers += [('SCGI', '1')]
        rheaders = self._make_headers( headers.extend(self.headers) )

        return self._gen_netstring(rheaders) + data

    def make_connection(self, url):
        uses_netloc.append('unix')
        scheme, netloc, path, query, frag = urlparse.urlsplit(url)
        host, port = urllib.splitport(netloc)

        if netloc:
            addrinfo = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM)
                       
            sock = socket.socket(*addrinfo[0][:3])
            sock.connect(addrinfo[0][4])
        else:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(path)

        return sock

    def send_request(self, connection, handler, request_body):

        pass

    def send_host(self, connection, host):
        pass

