<iframe width="560" height="315" src="https://www.youtube.com/embed/xRdJhd9SAV0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


So passen Sie Ihr Docsie-Portal an, indem Sie Ihren eingebetteten Docsie-Code in Visual Studio Code einfügen.

Docsie bietet zahlreiche Anpassungsmöglichkeiten. In diesem Artikel zeige ich Ihnen, wie Sie mit der Anpassung Ihres Docsie-Portals beginnen können. Bitte beachten Sie, dass ich kein professioneller Entwickler oder Designer bin. Ihr technisches Team kann diese Tools nutzen, um weitaus schönere Docsie-Portale zu erstellen. Dies ist lediglich eine Schritt-für-Schritt-Anleitung, um ihnen den Einstieg zu erleichtern!

## SCHRITT 1

Der erste Schritt ist, Ihren Code zu erhalten. Klicken Sie auf die drei Punkte in der oberen rechten Ecke bei Ihrem Konto. Dies führt Sie zum Einstellungs-Dashboard von Docsie.

## SCHRITT 2

Klicken Sie dann auf der linken Seite auf die Schaltfläche "Deployment".

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_UNFgmrrV4LJRPPcLD/boo_OKQpsM12uk8DtYPzL/f551ad37-a3a0-78bb-f97a-1246d5d57899Snag_1113a5f7.png)

In den Deployment-Einstellungen haben Sie die Möglichkeit, ein Wissensportal über die Docsie-Cloud zu erstellen oder ein Portal auf Ihrer eigenen Unternehmenswebsite einzurichten. Letzteres erfolgt durch einen Code, den Sie in Ihr HTML einfügen können, um mit der Gestaltung zu beginnen. Klicken Sie einfach auf "Configure a new deployment +".

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_66sDikYE16JfYewXU/boo_OKQpsM12uk8DtYPzL/4a8b6dd2-03d2-5d7a-837d-e3afdbe66900Snag_11161d31.png)

## SCHRITT 3

Klicken Sie auf den Reiter "Custom deployment", geben Sie Ihre Website unter "Deployment URL" ein und klicken Sie dann auf "Create web portal".

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_6CGgetG9GizkqY87p/boo_OKQpsM12uk8DtYPzL/4b102fcb-a424-8966-1f92-59b56e14241dimage.png)

Scrollen Sie anschließend nach unten, finden Sie Ihr Portal am Ende der Portalliste und klicken Sie auf "Get deployment script".



![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_el02yIrEUA3rf28CG/boo_OKQpsM12uk8DtYPzL/a64fc5d5-4e2c-9c6a-8325-6ed88a291db3Snag_1119813c.png)



## SCHRITT 4

Kopieren Sie nun Ihr Skript und wechseln Sie zu Visual Studio Code!

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_a3ExYoQ3yZSLnkf4y/boo_OKQpsM12uk8DtYPzL/1a26f697-45e9-b0c4-53d2-8ad808b8d49fSnag_111a44da.png)

Weitere Informationen zum Einbettungscode finden Sie in meinem Blog über die Veröffentlichung Ihrer Dokumentation mit eingebettetem Code [hier](https://www.docsie.io/blog/articles/publishing-product-documentation-with-docsie/).

Erstellen Sie in Visual Studio Code eine index.html-, index.css- und index.js-Datei (falls Sie noch keine haben). Öffnen Sie Ihre HTML-Datei und fügen Sie Ihren Code im Body-Bereich ein (unter dem </head>-Tag).

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_ss2981O27UrVWVfrx/boo_OKQpsM12uk8DtYPzL/64bda798-9915-3b7b-274f-dc707b9118a2Snag_111c041e.png)

## SCHRITT 5

Als Nächstes erstellen wir einen "Basic Style".

Mehr Informationen zur Anwendung grundlegender Stile für Ihre Docsie-Portale finden Sie unter [https://help.docsie.io/?doc=/publish-documentation-portal/docsie-styling-guide/base-style/](https://help.docsie.io/?doc=/publish-documentation-portal/docsie-styling-guide/base-style/)

In meinem Beispiel habe ich Folgendes zu meinem HTML hinzugefügt. Wie Sie sehen können, habe ich einen Firmennamen-Link hinzugefügt und leichte CSS-Änderungen vorgenommen.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_xg25e1fVbKEZbjJYl/boo_OKQpsM12uk8DtYPzL/a49b8d34-7911-10aa-741a-781224f57212Snag_1122dccd.png)

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_fRoPLO0Df6JhTcf2h/boo_OKQpsM12uk8DtYPzL/7c668c24-8d5e-8fdf-5b2a-ad93de3b313cSnag_11238581.png)

Mein Ergebnis sieht sehr einfach aus, aber ich wollte Ihnen das Potenzial zeigen, das Ihr technisches Team nutzen kann, um Docsie-Wissensportale aufzuwerten und an das Erscheinungsbild Ihrer Marke anzupassen. Bedenken Sie, dass Sie möglicherweise einen anderen Stil und andere Farben bevorzugen. In den meisten Fällen fügen unsere Nutzer ihr Logo mit Websitelinks ein und platzieren Navigationsleisten am oberen Rand, damit ihr Docsie-Wissensportal nahtlos in ihre Unternehmenswebsites passt und dem Erscheinungsbild ihrer aktuellen Seiten entspricht.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_StvlIomWiDjQ8wV0h/boo_OKQpsM12uk8DtYPzL/e02de6be-1990-cbe1-7078-4e477ec4a6d9Snag_112473e8.png)

## SCHRITT 6

Im letzten Schritt habe ich einige Stiländerungen mit diesem Code vorgenommen:

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
Ich habe ihn unter dem letzten div-Tag des "Basic Style" eingefügt.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_ORs7jTN5WvXJ7VkuB/boo_OKQpsM12uk8DtYPzL/4cc0127b-2bca-4d38-3040-864b8f5054fdSnag_112741dd.png)

Das Ergebnis meiner einfachen Stiländerungen sieht so aus:

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_uCSLHwdeVry8finx8/boo_OKQpsM12uk8DtYPzL/82ffd090-9575-e89b-b0ed-16f4af08a405Snag_1127954c.png)

Jetzt haben Sie alle nötigen Werkzeuge zur Hand. Probieren Sie es selbst aus und experimentieren Sie mit verschiedenen Änderungen, um ansprechende Wissensportale zu erstellen, auf die Sie stolz sein können! Ich bin sicher, dass Ihre Wissensportale deutlich eleganter aussehen werden als meines. Also, probieren Sie es aus und vor allem: Haben Sie Spaß dabei!