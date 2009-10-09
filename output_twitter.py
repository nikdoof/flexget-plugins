import logging
from flexget.plugin import *

__pychecker__ = 'unusednames=parser'

log = logging.getLogger('twitter')

class OutputTwitter:

    """
        Send a Twitter for each (downloaded) entries.

        Config:
	  username	: twitter username
	  password	: twitter password
          to            : the recipients (required)
	  apiurl	: API URL (optional)
          active        : is this plugin active or not ?

        Config basic example:

	twitter:
	  username: mythbox
	  password: blargh
          to: nikdoof, salkunh

    """
    def validator(self):
        from flexget import validator
        twitter = validator.factory('dict')
        twitter.accept('boolean', key='active')
        twitter.accept('text', key='to', required=True)
        twitter.accept('text', key='username', required=True)
        twitter.accept('text', key='password', required=True)
	twitter.accept('text', key='apiurl')
        return twitter

    def get_config(self, feed):
        config = feed.config['twitter']
        config.setdefault('active', True)
	config.setdefault('apirul', 'http://twitter.com/')
        return config

    def feed_exit(self, feed):
        """Send email at exit."""
        config = self.get_config(feed)

        if not config['active']:
            return

        # don't send twits when learning
        if feed.manager.options.learn:
            return

        entries_count = len(feed.accepted)
        if entries_count == 0:
            return # don't send empty twits

        for entry in feed.accepted:
            content = "%s queued" % entry['title']
	    if len(content) > 120:
		# arse!
	    else:
	        # Send Twitter

register_plugin(OutputTwitter, 'twitter')
