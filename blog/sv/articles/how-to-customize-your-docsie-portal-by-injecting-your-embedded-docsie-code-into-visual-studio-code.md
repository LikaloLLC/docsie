<iframe width="560" height="315" src="https://www.youtube.com/embed/xRdJhd9SAV0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


Hur du anpassar din Docsie-portal genom att infoga din inbäddade Docsie-kod i Visual Studio Code.

Docsie har många anpassningsmöjligheter. I den här artikeln guidar jag dig genom stegen du behöver ta för att börja anpassa din Docsie-portal. Tänk på att jag inte är en professionell utvecklare eller designer. Ditt tekniska team kan använda dessa verktyg för att skapa betydligt snyggare Docsie-portaler än jag kan. Detta är bara en steg-för-steg-guide för att hjälpa dem komma igång!

## STEG 1

Första steget är att hämta din kod. Så här gör du. Hitta ditt konto i det övre högra hörnet där det finns tre prickar och klicka på dem. Det tar dig till Docsies inställningspanel.

## STEG 2

Klicka sedan på knappen "Deployment" på vänster sida.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_UNFgmrrV4LJRPPcLD/boo_OKQpsM12uk8DtYPzL/f551ad37-a3a0-78bb-f97a-1246d5d57899Snag_1113a5f7.png)

När du är i deployment-inställningarna kan du skapa en kunskapsportal via Docsie Cloud eller på din egen företagswebbplats genom att använda en kodrad som du kan lägga till i din HTML för att börja anpassa. Detta gör du enkelt genom att klicka på "Configure a new deployment +".

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_66sDikYE16JfYewXU/boo_OKQpsM12uk8DtYPzL/4a8b6dd2-03d2-5d7a-837d-e3afdbe66900Snag_11161d31.png)

## STEG 3

Klicka sedan på fliken "Custom deployment", skriv in din webbplats i "Deployment URL" och klicka på "Create web portal".

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_6CGgetG9GizkqY87p/boo_OKQpsM12uk8DtYPzL/4b102fcb-a424-8966-1f92-59b56e14241dimage.png)

När det är klart, scrolla ner och hitta din portal längst ner i portallistan och klicka på "Get deployment script".



![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_el02yIrEUA3rf28CG/boo_OKQpsM12uk8DtYPzL/a64fc5d5-4e2c-9c6a-8325-6ed88a291db3Snag_1119813c.png)



## STEG 4

Kopiera nu ditt skript och låt oss hoppa till Visual Studio Code!

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_a3ExYoQ3yZSLnkf4y/boo_OKQpsM12uk8DtYPzL/1a26f697-45e9-b0c4-53d2-8ad808b8d49fSnag_111a44da.png)

Om du behöver mer information om hur du får den inbäddade koden från din Docsie, kolla in min blogg om hur du publicerar din dokumentation med inbäddad kod [här](https://www.docsie.io/blog/articles/publishing-product-documentation-with-docsie/).

Skapa nu en fil i Visual Studio Code (om du inte redan har en) för index.html, index.css och index.js. När det är klart, öppna din HTML och klistra in din kod i body-delen av din html (under </head>-taggen).

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_ss2981O27UrVWVfrx/boo_OKQpsM12uk8DtYPzL/64bda798-9915-3b7b-274f-dc707b9118a2Snag_111c041e.png)

## STEG 5

I steg 5 behöver vi skapa en "Basic style".

Du hittar mer information om hur du tillämpar grundläggande styling på dina Docsie-portaler via vår länk här [https://help.docsie.io/?doc=/publish-documentation-portal/docsie-styling-guide/base-style/](https://help.docsie.io/?doc=/publish-documentation-portal/docsie-styling-guide/base-style/)

I mitt exempel har jag lagt till detta i min HTML. Som du ser har jag lagt till en företagsnamn-länk och gjort några mindre CSS-ändringar.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_xg25e1fVbKEZbjJYl/boo_OKQpsM12uk8DtYPzL/a49b8d34-7911-10aa-741a-781224f57212Snag_1122dccd.png)

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_fRoPLO0Df6JhTcf2h/boo_OKQpsM12uk8DtYPzL/7c668c24-8d5e-8fdf-5b2a-ad93de3b313cSnag_11238581.png)

Mitt resultat ser ganska enkelt ut, men jag ville visa potentialen som ditt tekniska team har för att förbättra Docsie-kunskapsportaler och skapa portaler som matchar ert varumärkes utseende och känsla. Kom ihåg att du kan ha en annan stil och färger. I de flesta fall lägger våra användare till sin logotyp tillsammans med sina webbplatslänkar och navigeringsfält högst upp så att deras Docsie-kunskapsportal passar sömlöst in på företagets webbplatser och matchar miljön och CSS:en på deras befintliga sajter.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_StvlIomWiDjQ8wV0h/boo_OKQpsM12uk8DtYPzL/e02de6be-1990-cbe1-7078-4e477ec4a6d9Snag_112473e8.png)

## STEG 6

I det sista steget lade jag till några stiländringar med följande kod:

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
Jag klistrade in det under den sista div-taggen i "basic style".

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_ORs7jTN5WvXJ7VkuB/boo_OKQpsM12uk8DtYPzL/4cc0127b-2bca-4d38-3040-864b8f5054fdSnag_112741dd.png)

Och resultaten för mina mycket enkla stiländringar blev detta:

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_uCSLHwdeVry8finx8/boo_OKQpsM12uk8DtYPzL/82ffd090-9575-e89b-b0ed-16f4af08a405Snag_1127954c.png)

Nu när du har alla verktyg till ditt förfogande, prova själv och se hur det känns att ändra saker och skapa vackra kunskapsportaler som du kan vara stolt över! Jag är 100% säker på att dina kunskapsportaler kommer att se mycket snyggare ut än mina! :) Så prova och ha framför allt kul med det!