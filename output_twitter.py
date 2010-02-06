""" OutputTwitter - Produces a twitter post for each entry

    MIT Licensed, derrivative work of Flexget module OutputEmail """

import logging
from flexget.plugin import *

log = logging.getLogger('twitter')


class OutputTwitter:

    """
        Send a Twitter for each (downloaded) entries.

        Config:
            username	: twitter username (required)
            password	: twitter password (required)
            to          : the recipients
            active      : is this plugin active or not ?

        Config basic example:

            twitter:
                username: mythbox
                password: blargh

    """

    _validated = False

    def validator(self):
        from flexget import validator
        twitter = validator.factory('dict')
        twitter.accept('boolean', key='active')
        twitter.accept('text', key='to')
        twitter.accept('text', key='username', required=True)
        twitter.accept('text', key='password', required=True)
        return twitter

    def get_config(self, feed):
        config = feed.config['twitter']
        config.setdefault('active', False)
        return config

    def on_feed_exit(self, feed):
        """Send email at exit."""
        config = self.get_config(feed)

        if not config['active']:
            log.debug("twitter plugin not active")
            return

        # don't send twits when learning
        if feed.manager.options.learn:
            log.debug("learn mode, skipping")
            return

        log.debug("Loading twitter api")
        api = twitter.Api(username=config['username'],
                          password=config['password'])

        if not self._validated:
            try:
                api.GetFriends()
            except TwitterError:
                log.warn("Error testing twitter connectivity, check your username/password")
                return

        if len(feed.accepted) == 0:
            return # don't send empty twits

        for entry in feed.accepted:
            if len(entry['title']) > 103:
                content = "%s... found and queued" % entry['title'][:104]
            else:
                content = "%s found and queued" % entry['title']
            log.debug("Sending Twitter: %s", content)
            api.PostUpdate(content)

try:
    import twitter
except ImportError:
    raise PluginError('Unable to import module twitter, python-twitter is required to use output_twitter')
else:
    log.debug("Registering plugin: twitter")
    register_plugin(OutputTwitter, 'twitter')
