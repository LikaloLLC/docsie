<iframe width="560" height="315" src="https://www.youtube.com/embed/xRdJhd9SAV0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


Comment personnaliser votre portail Docsie en injectant votre code Docsie intégré dans Visual Studio Code.

Docsie offre de nombreuses possibilités de personnalisation. Dans cet article, je vais vous guider à travers les étapes nécessaires pour commencer à personnaliser votre portail Docsie. Gardez à l'esprit que je ne suis ni développeur ni designer professionnel, et que votre équipe technique pourra utiliser ces outils pour créer des portails Docsie bien plus élégants que ce que je peux faire. Il s'agit simplement d'un guide étape par étape pour les aider à démarrer !

## ÉTAPE 1

La première étape consiste à récupérer votre ligne de code. Voici comment procéder. Trouvez votre compte en haut à droite où se trouvent trois points et cliquez dessus. Cela vous amènera au tableau de bord des paramètres de Docsie.

## ÉTAPE 2

Ensuite, cliquez sur le bouton 'Deployment' (Déploiement) sur le côté gauche.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_UNFgmrrV4LJRPPcLD/boo_OKQpsM12uk8DtYPzL/f551ad37-a3a0-78bb-f97a-1246d5d57899Snag_1113a5f7.png)

Une fois dans les paramètres de déploiement, vous avez la possibilité de créer un portail de connaissances via le cloud Docsie, ou de créer un portail de connaissances via le site web de votre entreprise en utilisant une ligne de code que vous pouvez ajouter à votre HTML pour commencer le processus de stylisation. Il suffit de cliquer sur 'Configure a new deployment +' (Configurer un nouveau déploiement +).

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_66sDikYE16JfYewXU/boo_OKQpsM12uk8DtYPzL/4a8b6dd2-03d2-5d7a-837d-e3afdbe66900Snag_11161d31.png)

## ÉTAPE 3

Ensuite, cliquez sur l'onglet 'Custom deployment' (Déploiement personnalisé), saisissez votre site web dans 'Deployment URL' (URL de déploiement), puis cliquez sur 'Create web portal' (Créer un portail web).

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_6CGgetG9GizkqY87p/boo_OKQpsM12uk8DtYPzL/4b102fcb-a424-8966-1f92-59b56e14241dimage.png)

Une fois cela fait, assurez-vous de faire défiler vers le bas pour trouver votre portail en bas de la liste des portails, puis cliquez sur 'Get deployment script' (Obtenir le script de déploiement).

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_el02yIrEUA3rf28CG/boo_OKQpsM12uk8DtYPzL/a64fc5d5-4e2c-9c6a-8325-6ed88a291db3Snag_1119813c.png)

## ÉTAPE 4

Copiez maintenant votre script et passons à Visual Studio Code !

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_a3ExYoQ3yZSLnkf4y/boo_OKQpsM12uk8DtYPzL/1a26f697-45e9-b0c4-53d2-8ad808b8d49fSnag_111a44da.png)

Si vous avez besoin de plus d'informations sur comment obtenir le code intégré de votre Docsie, consultez mon article sur la publication de votre documentation avec votre code intégré [ici](https://www.docsie.io/blog/articles/publishing-product-documentation-with-docsie/).

Dans Visual Studio Code, créez un fichier (sauf si vous en avez déjà un) pour index.html, index.css et index.js. Une fois cela fait, ouvrez votre HTML et collez votre code dans le corps de votre HTML (sous la balise </head>).

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_ss2981O27UrVWVfrx/boo_OKQpsM12uk8DtYPzL/64bda798-9915-3b7b-274f-dc707b9118a2Snag_111c041e.png)

## ÉTAPE 5

Pour l'étape 5, nous devons créer un 'Style de base'.

Vous pouvez trouver plus d'informations sur comment appliquer un style de base à vos portails Docsie via notre lien ici [https://help.docsie.io/?doc=/publish-documentation-portal/docsie-styling-guide/base-style/](https://help.docsie.io/?doc=/publish-documentation-portal/docsie-styling-guide/base-style/)

Pour mon exemple, j'ai ajouté ceci à mon HTML. Comme vous pouvez le voir, j'ai ajouté un lien avec le nom de l'entreprise et j'ai fait quelques légères modifications CSS.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_xg25e1fVbKEZbjJYl/boo_OKQpsM12uk8DtYPzL/a49b8d34-7911-10aa-741a-781224f57212Snag_1122dccd.png)

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_fRoPLO0Df6JhTcf2h/boo_OKQpsM12uk8DtYPzL/7c668c24-8d5e-8fdf-5b2a-ad93de3b313cSnag_11238581.png)

Mes résultats sont très basiques, mais je voulais vous montrer le potentiel que votre équipe technique peut exploiter pour embellir les portails de connaissances Docsie et créer des portails qui correspondent à l'apparence et à l'ambiance de votre marque. Gardez à l'esprit que vous pouvez avoir un style et des couleurs différents ; en fait, dans la plupart des cas, nos utilisateurs intègrent leur logo avec les liens de leur site web, ajoutent des barres de navigation en haut pour que leur portail de connaissances Docsie s'intègre parfaitement à leurs sites web et corresponde à l'environnement et au CSS de leurs sites actuels.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_StvlIomWiDjQ8wV0h/boo_OKQpsM12uk8DtYPzL/e02de6be-1990-cbe1-7078-4e477ec4a6d9Snag_112473e8.png)

## ÉTAPE 6

Pour la dernière étape, j'ai ajouté quelques modifications de style via ce texte :

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
Je l'ai collé sous la dernière balise div du 'style de base'.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_ORs7jTN5WvXJ7VkuB/boo_OKQpsM12uk8DtYPzL/4cc0127b-2bca-4d38-3040-864b8f5054fdSnag_112741dd.png)

Et voici le résultat de mes changements de style très basiques :

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_uCSLHwdeVry8finx8/boo_OKQpsM12uk8DtYPzL/82ffd090-9575-e89b-b0ed-16f4af08a405Snag_1127954c.png)

Maintenant que vous disposez de tous les outils nécessaires, essayez-le vous-même et voyez comment ça fait de changer les choses et de créer de beaux portails de connaissances dont vous pouvez être fier ! Je suis certain à 100% que vos portails de connaissances auront l'air bien plus élégants que le mien ! :) Alors essayez et surtout, amusez-vous bien !