<iframe width="560" height="315" src="https://www.youtube.com/embed/xRdJhd9SAV0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


How to customize your Docsie portal by injecting your embedded Docsie code into Visual Studio Code.

Docsie has a lot of customization capabilities. In this article i will guide you on the steps you need to take to get started on customizing your Docsie portal. Please keep in mind that i am not a professional developer, or designer and know that your tech team can use these tools to create beautifully fashioned Docsie portal far better then I can. This is merely a step by step guide on how to get them started!

## STEP 1

The first step is to get your line of code. He is how it is done. Find your account on the top right corner where there are three dots and click it. It will take you to Docsie's settings dashboard.

## STEP 2

Next, click on 'Deployment' button on the left hand side.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_UNFgmrrV4LJRPPcLD/boo_OKQpsM12uk8DtYPzL/f551ad37-a3a0-78bb-f97a-1246d5d57899Snag_1113a5f7.png)

Once you are in the deployment settings now you the ability to create a knowledge portal via Docsie cloud, or to create a knowledge portal via your own companies website by summoning a line of code in which you can add to your HTML and begin the styling process. This is done simply by clicking 'Configure a new deployment +'

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_66sDikYE16JfYewXU/boo_OKQpsM12uk8DtYPzL/4a8b6dd2-03d2-5d7a-837d-e3afdbe66900Snag_11161d31.png)

## STEP 3

Next click on the tab that says 'Custom deployment' type your website within 'Deployment URL' and then click 'Create web portal'.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_6CGgetG9GizkqY87p/boo_OKQpsM12uk8DtYPzL/4b102fcb-a424-8966-1f92-59b56e14241dimage.png)

Once that is done, make sure to scroll down and find your portal at the bottom of the list of portals and then click 'Get deployment script.



![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_el02yIrEUA3rf28CG/boo_OKQpsM12uk8DtYPzL/a64fc5d5-4e2c-9c6a-8325-6ed88a291db3Snag_1119813c.png)



## STEP 4

Now copy your script and lets jump onto Visual Studio Code!

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_a3ExYoQ3yZSLnkf4y/boo_OKQpsM12uk8DtYPzL/1a26f697-45e9-b0c4-53d2-8ad808b8d49fSnag_111a44da.png)

If you need more information about how to get the Embedded code from your Docsie check out my blog about publishing your documentation with your embedded code[ here.](https://www.docsie.io/blog/articles/publishing-product-documentation-with-docsie/)

Now, within Visual Studio Code create a file (unless you have a file ready) for index.html, index.css. and index.js. Once that is done open your HTML and paste your code within the body of your html (under the </head> tag).

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_ss2981O27UrVWVfrx/boo_OKQpsM12uk8DtYPzL/64bda798-9915-3b7b-274f-dc707b9118a2Snag_111c041e.png)

## STEP 5

Now for step 5 we need to create a 'Basic style'.

You can find more information about how to apply basic styling to your Docsie portals via our link here [https://help.docsie.io/?doc=/publish-documentation-portal/docsie-styling-guide/base-style/](https://help.docsie.io/?doc=/publish-documentation-portal/docsie-styling-guide/base-style/)

For my example I added this to my HTML. and as you can see I added a company name link and I did some mild CSS to alter them.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_xg25e1fVbKEZbjJYl/boo_OKQpsM12uk8DtYPzL/a49b8d34-7911-10aa-741a-781224f57212Snag_1122dccd.png)

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_fRoPLO0Df6JhTcf2h/boo_OKQpsM12uk8DtYPzL/7c668c24-8d5e-8fdf-5b2a-ad93de3b313cSnag_11238581.png)

My results look very basic, but I wanted you to see the potential that your tech team can do to spice up Docsie knowledge portals and create portals that match your brands look and feel. Keep in mind that you may have a different style, and colors; in fact in most cases our users put their logo which is embedded with their website links, they add navigations bars on top so that their Docsie knowledge portal fit seamlessly and naturally onto their company websites and match the environment and CSS of their current sites.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_StvlIomWiDjQ8wV0h/boo_OKQpsM12uk8DtYPzL/e02de6be-1990-cbe1-7078-4e477ec4a6d9Snag_112473e8.png)

## STEP 6

Then the last step I did was add some styling changes via this text here:

```
  <style>
    :root {
        --docsie-font-family: garamond;
        --docsie-font-family-head: inherit;
        --docsie-font-family-mono: monospace;
        --docsie-hue-primary: 200;
        --docsie-hue-gray: var(--docsie-hue-primary);
        --docsie-sat-primary: 100%;
     
        --docsie-page-width: 1800px;   
        --docsie-notice-background: var(--docsie-color-primary-darker);
    }
    </style>

```
I pasted it below the last div tag of the ‘basic style’.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_ORs7jTN5WvXJ7VkuB/boo_OKQpsM12uk8DtYPzL/4cc0127b-2bca-4d38-3040-864b8f5054fdSnag_112741dd.png)

And the results for my very basic style changes were this:

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_uCSLHwdeVry8finx8/boo_OKQpsM12uk8DtYPzL/82ffd090-9575-e89b-b0ed-16f4af08a405Snag_1127954c.png)

Now that you have all the tools at your disposal, give it a try yourself, and see how it feels to change things around and create beautiful knowledge portals that you can be proud of! I am 100% certain that your knowledge portals will look way fancier then mine! :) So give it a try and most importantly have fun with it!



