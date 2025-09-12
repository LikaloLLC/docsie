<iframe width="560" height="315" src="https://www.youtube.com/embed/xRdJhd9SAV0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


Cómo personalizar tu portal Docsie inyectando el código embebido de Docsie en Visual Studio Code.

Docsie ofrece muchas posibilidades de personalización. En este artículo te guiaré por los pasos necesarios para empezar a personalizar tu portal Docsie. Ten en cuenta que no soy desarrollador ni diseñador profesional, y tu equipo técnico puede utilizar estas herramientas para crear portales Docsie mucho más atractivos que los míos. ¡Esta es simplemente una guía paso a paso para ayudarles a empezar!

## PASO 1

El primer paso es obtener tu línea de código. Así es como se hace. Encuentra tu cuenta en la esquina superior derecha donde hay tres puntos y haz clic. Te llevará al panel de configuración de Docsie.

## PASO 2

A continuación, haz clic en el botón 'Deployment' (Implementación) en el lado izquierdo.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_UNFgmrrV4LJRPPcLD/boo_OKQpsM12uk8DtYPzL/f551ad37-a3a0-78bb-f97a-1246d5d57899Snag_1113a5f7.png)

Una vez en la configuración de implementación, tienes la posibilidad de crear un portal de conocimiento a través de Docsie Cloud, o crear un portal de conocimiento en tu propio sitio web mediante una línea de código que puedes añadir a tu HTML para comenzar el proceso de estilización. Esto se hace simplemente haciendo clic en 'Configure a new deployment +' (Configurar una nueva implementación +)

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_66sDikYE16JfYewXU/boo_OKQpsM12uk8DtYPzL/4a8b6dd2-03d2-5d7a-837d-e3afdbe66900Snag_11161d31.png)

## PASO 3

A continuación, haz clic en la pestaña 'Custom deployment' (Implementación personalizada), escribe tu sitio web en 'Deployment URL' (URL de implementación) y luego haz clic en 'Create web portal' (Crear portal web).

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_6CGgetG9GizkqY87p/boo_OKQpsM12uk8DtYPzL/4b102fcb-a424-8966-1f92-59b56e14241dimage.png)

Una vez hecho esto, asegúrate de desplazarte hacia abajo para encontrar tu portal al final de la lista de portales y luego haz clic en 'Get deployment script' (Obtener script de implementación).



![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_el02yIrEUA3rf28CG/boo_OKQpsM12uk8DtYPzL/a64fc5d5-4e2c-9c6a-8325-6ed88a291db3Snag_1119813c.png)



## PASO 4

Ahora copia tu script y ¡pasemos a Visual Studio Code!

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_a3ExYoQ3yZSLnkf4y/boo_OKQpsM12uk8DtYPzL/1a26f697-45e9-b0c4-53d2-8ad808b8d49fSnag_111a44da.png)

Si necesitas más información sobre cómo obtener el código embebido de tu Docsie, consulta mi blog sobre cómo publicar tu documentación con el código embebido [aquí.](https://www.docsie.io/blog/articles/publishing-product-documentation-with-docsie/)

Ahora, en Visual Studio Code crea un archivo (a menos que ya tengas uno listo) para index.html, index.css e index.js. Una vez hecho esto, abre tu HTML y pega tu código dentro del cuerpo de tu HTML (debajo de la etiqueta </head>).

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_ss2981O27UrVWVfrx/boo_OKQpsM12uk8DtYPzL/64bda798-9915-3b7b-274f-dc707b9118a2Snag_111c041e.png)

## PASO 5

Ahora para el paso 5 necesitamos crear un 'Estilo básico'.

Puedes encontrar más información sobre cómo aplicar estilos básicos a tus portales Docsie a través de nuestro enlace aquí [https://help.docsie.io/?doc=/publish-documentation-portal/docsie-styling-guide/base-style/](https://help.docsie.io/?doc=/publish-documentation-portal/docsie-styling-guide/base-style/)

Para mi ejemplo, añadí esto a mi HTML. Como puedes ver, agregué un enlace con el nombre de la empresa e hice algunas modificaciones leves en CSS para alterarlos.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_xg25e1fVbKEZbjJYl/boo_OKQpsM12uk8DtYPzL/a49b8d34-7911-10aa-741a-781224f57212Snag_1122dccd.png)

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_fRoPLO0Df6JhTcf2h/boo_OKQpsM12uk8DtYPzL/7c668c24-8d5e-8fdf-5b2a-ad93de3b313cSnag_11238581.png)

Mis resultados se ven muy básicos, pero quería que vieras el potencial que tu equipo técnico puede aprovechar para mejorar los portales de conocimiento Docsie y crear portales que coincidan con la apariencia y sensación de tu marca. Ten en cuenta que puedes tener un estilo y colores diferentes; de hecho, en la mayoría de los casos, nuestros usuarios colocan su logotipo con enlaces a su sitio web, agregan barras de navegación en la parte superior para que su portal de conocimiento Docsie se integre perfectamente en sus sitios web corporativos y coincida con el entorno y el CSS de sus sitios actuales.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_StvlIomWiDjQ8wV0h/boo_OKQpsM12uk8DtYPzL/e02de6be-1990-cbe1-7078-4e477ec4a6d9Snag_112473e8.png)

## PASO 6

El último paso fue añadir algunos cambios de estilo mediante este texto:

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
Lo pegué debajo de la última etiqueta div del 'estilo básico'.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_ORs7jTN5WvXJ7VkuB/boo_OKQpsM12uk8DtYPzL/4cc0127b-2bca-4d38-3040-864b8f5054fdSnag_112741dd.png)

Y los resultados de mis cambios de estilo muy básicos fueron estos:

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_uCSLHwdeVry8finx8/boo_OKQpsM12uk8DtYPzL/82ffd090-9575-e89b-b0ed-16f4af08a405Snag_1127954c.png)

Ahora que tienes todas las herramientas a tu disposición, pruébalo tú mismo y experimenta cómo se siente cambiar las cosas y crear hermosos portales de conocimiento de los que puedas estar orgulloso. Estoy 100% seguro de que tus portales de conocimiento se verán mucho más elegantes que los míos. :) ¡Así que inténtalo y, sobre todo, diviértete con ello!