from staticjinja import Site
from jinja2 import Environment
import gettext
import sys
from os import listdir
from os.path import isfile, join
import os
cwd = os.getcwd()
import feedparser
from os import listdir
from os.path import isfile, join
import dateutil.parser
import arrow

if __name__ == "__main__":
    # d = 'locale'
    # dirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
    # for loc in dirs:
    #     locale = loc.replace('locale/', '')
    #     if locale == 'ja_JP':
    #         loc_name = '/jp'
    #     else:
    #         loc_name = '/' + locale
    #     site = Site.make_site(searchpath='./src', env_globals={"locale": loc_name},locale=locale, extensions=['jinja2.ext.i18n','jinja_markdown.MarkdownExtension'])
    #
    #     # enable automatic reloading
    #     site.render(use_reloader=False)

    ###Grabbing blogposts and converting them to

    feed = feedparser.parse('https://www.docsie.io/blog/rss.xml?skip=1&limit=3').entries
    feed.reverse()



    for f in feed:
        f['link'] = f['link'].replace('/blog/blog/', '/blog/')
        f['published'] = arrow.get(dateutil.parser.parse(f['published'])).humanize()


    site = Site.make_site(searchpath='src/', env_globals={"feed":feed[::-1]},
                          extensions=['jinja2.ext.i18n', 'jinja2.ext.autoescape', 'jinja2.ext.with_','jinja_markdown.MarkdownExtension'])

    # enable automatic reloading
    site.render(use_reloader=True)
