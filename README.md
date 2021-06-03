# Docsie.io

## Purpose of this repo is to

* Host the static portion of docsie.io
* Serve as Tech Support and feature request hub for docsie.io
* Serve as a live example of a Docsie.io project

For any questions please contact support@likalo.com, open a ticket here or ask us on gitter https://gitter.im/docsie/Lobby/

We used to have a support board/forum, but we did not see it being used much and we do not want to maintain unused infrastructure, so we are moving all our free support over to github.



# How to Build this


setup virtual environment if needed
pip install -r requirements.txt
sh start.sh

### To compile the site
python main.py


We also had a lot of problems hosting out static content on AWS infrastructure. From cryptic soft 404's on google bot to slow route and lag while connecting to Amazon network. Github pages solves that problems for us, as their network is uber fast.

This made us decide to move https://docsie.io over to github pages.

We started by moving our blog (https://blog.docsie.io) to github pages and saw the issues we were having with AWS resolved. Which made us think that either google deprioritizes crawling pages hosted on AWS, google bot craps out due to AWS
network issues or some other configuration issues with django. Either or, our static site is now going to be open on github pages.

We see it as an alternative to AWS static site hosting and cloudflare. The site is mostly built with docsie and only uses a few
react components for the dynamic functionality.

pybabel init -d locale -l it -i locale/messages.pot
pybabel compile -d locale -l it

