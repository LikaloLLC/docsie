# Docsie.io
Purpose of this repo is to host the static portion of docsie.io

We had a lot of problems hosting out static content on AWS infrastructure. From cryptic soft 404's on google bot to slow route and lag while connecting to Amazon network. Github pages solves that problems for us, as their network is uber fast.

This made us decide to move https://docsie.io over to github pages.

We started by moving our blog (https://blog.docsie.io) to github pages and saw the issues we were having with AWS resolved and our
site indexed. Which made us think that either google deprioritizes crawling pages hosted on AWS, google bot craps out due to AWS
network issues or some other configuration issues with django. Either or, our static site is now going to be open on github pages.

We see it as an alternative to AWS static site hosting and cloudflare. The site is mostly built with docsie and only uses a few
react components for the dynamic functionality.
