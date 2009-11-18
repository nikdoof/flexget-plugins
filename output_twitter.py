""" OutputTwitter - Produces a twitter post for each entry

    MIT Licensed, derrivative work of Flexget module OutputEmail """

import logging
from flexget.plugin import *

__pychecker__ = 'unusednames=parser'

log = logging.getLogger('twitter')

class OutputTwitter:

    """
        Send a Twitter for each (downloaded) entries.

        Config:
            username	: twitter username (required)
            password	: twitter password (required)
            to          : the recipients
            apiurl      : API URL 
            active      : is this plugin active or not ?

        Config basic example:

            twitter:
                username: mythbox
                password: blargh

    """
    def validator(self):
        from flexget import validator
        twitter = validator.factory('dict')
        twitter.accept('boolean', key='active')
        twitter.accept('text', key='to')
        twitter.accept('text', key='username', required=True)
        twitter.accept('text', key='password', required=True)
        twitter.accept('text', key='apiurl')
        return twitter

    def get_config(self, feed):
        config = feed.config['twitter']
        config.setdefault('active', True)
        config.setdefault('apiurl', 'http://twitter.com/')
        return config

    def feed_exit(self, feed):
        """Send email at exit."""
        config = self.get_config(feed)

        if not config['active']:
            return

        # don't send twits when learning
        if feed.manager.options.learn:
            return

        api = twitter.Api(username=config['username'], password=config['password'])

        if not api.GetFriends():
            log.warn("Invalid twitter username or password")
            return

        entries_count = len(feed.accepted)
        if entries_count == 0:
            return # don't send empty twits

        for entry in feed.accepted:
            content = "%s found and queued" % entry['title']
            if len(content) > 120:
                return
            else:
                api.PostUpdate(content)

try:
    import twitter
except ImportError:
    log.error('Unable to import module twitter, is python-twitter installed?')
else:
    register_plugin(OutputTwitter, 'twitter')
