from staticjinja import Site
from jinja2 import Environment
import gettext
from django.utils.translation import gettext, ngettext

if __name__ == "__main__":

    site = Site.make_site(searchpath='./src', extensions=['jinja2.ext.i18n'])

    # enable automatic reloading
    site.render(use_reloader=True)
