<iframe width="560" height="315" src="https://www.youtube.com/embed/xRdJhd9SAV0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


Как настроить портал Docsie с помощью внедрения кода Docsie в Visual Studio Code.

Docsie предлагает множество возможностей для настройки. В этой статье я расскажу о шагах, которые нужно предпринять, чтобы начать персонализацию вашего портала Docsie. Сразу отмечу, что я не профессиональный разработчик или дизайнер, и ваша техническая команда сможет использовать эти инструменты гораздо эффективнее. Это просто пошаговое руководство, которое поможет им начать!

## ШАГ 1

Первый шаг — получить строку кода. Найдите свою учетную запись в правом верхнем углу, где расположены три точки, и нажмите на них. Это приведет вас к панели настроек Docsie.

## ШАГ 2

Далее нажмите на кнопку «Deployment» (Развертывание) в левой части экрана.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_UNFgmrrV4LJRPPcLD/boo_OKQpsM12uk8DtYPzL/f551ad37-a3a0-78bb-f97a-1246d5d57899Snag_1113a5f7.png)

Оказавшись в настройках развертывания, вы получите возможность создать портал знаний через облако Docsie или через сайт вашей компании, используя строку кода, которую можно добавить в HTML и начать процесс стилизации. Для этого просто нажмите «Configure a new deployment +» (Настроить новое развертывание +).

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_66sDikYE16JfYewXU/boo_OKQpsM12uk8DtYPzL/4a8b6dd2-03d2-5d7a-837d-e3afdbe66900Snag_11161d31.png)

## ШАГ 3

Теперь перейдите на вкладку «Custom deployment» (Пользовательское развертывание), введите адрес вашего сайта в поле «Deployment URL» и нажмите «Create web portal» (Создать веб-портал).

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_6CGgetG9GizkqY87p/boo_OKQpsM12uk8DtYPzL/4b102fcb-a424-8966-1f92-59b56e14241dimage.png)

После этого прокрутите вниз, найдите свой портал в конце списка порталов и нажмите «Get deployment script» (Получить скрипт развертывания).


![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_el02yIrEUA3rf28CG/boo_OKQpsM12uk8DtYPzL/a64fc5d5-4e2c-9c6a-8325-6ed88a291db3Snag_1119813c.png)


## ШАГ 4

Теперь скопируйте скрипт и перейдем в Visual Studio Code!

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_a3ExYoQ3yZSLnkf4y/boo_OKQpsM12uk8DtYPzL/1a26f697-45e9-b0c4-53d2-8ad808b8d49fSnag_111a44da.png)

Если вам нужна дополнительная информация о получении кода для встраивания из Docsie, ознакомьтесь с моей статьей о публикации документации с помощью встраиваемого кода [здесь](https://www.docsie.io/blog/articles/publishing-product-documentation-with-docsie/).

Создайте в Visual Studio Code файлы index.html, index.css и index.js (если у вас их еще нет). Откройте ваш HTML и вставьте код в тело HTML (под тегом </head>).

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_ss2981O27UrVWVfrx/boo_OKQpsM12uk8DtYPzL/64bda798-9915-3b7b-274f-dc707b9118a2Snag_111c041e.png)

## ШАГ 5

Теперь создадим «Базовый стиль».

Дополнительную информацию о применении базовых стилей к порталам Docsie можно найти по ссылке [https://help.docsie.io/?doc=/publish-documentation-portal/docsie-styling-guide/base-style/](https://help.docsie.io/?doc=/publish-documentation-portal/docsie-styling-guide/base-style/)

В моем примере я добавил следующее в HTML. Как видите, я добавил ссылку с названием компании и немного изменил стили с помощью CSS.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_xg25e1fVbKEZbjJYl/boo_OKQpsM12uk8DtYPzL/a49b8d34-7911-10aa-741a-781224f57212Snag_1122dccd.png)

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_fRoPLO0Df6JhTcf2h/boo_OKQpsM12uk8DtYPzL/7c668c24-8d5e-8fdf-5b2a-ad93de3b313cSnag_11238581.png)

Мои результаты выглядят довольно просто, но я хотел показать вам потенциал, который ваша техническая команда может использовать для улучшения порталов знаний Docsie и создания порталов, соответствующих стилю вашего бренда. Имейте в виду, что у вас может быть другой стиль и цвета. На практике большинство пользователей добавляют свой логотип со ссылками на свой сайт, панели навигации сверху, чтобы их портал знаний Docsie органично вписывался в дизайн их корпоративных сайтов и соответствовал стилю CSS их текущих ресурсов.

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_StvlIomWiDjQ8wV0h/boo_OKQpsM12uk8DtYPzL/e02de6be-1990-cbe1-7078-4e477ec4a6d9Snag_112473e8.png)

## ШАГ 6

Последним шагом я добавил несколько изменений стиля с помощью следующего кода:

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
Я вставил его после последнего div-тега «базового стиля».

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_ORs7jTN5WvXJ7VkuB/boo_OKQpsM12uk8DtYPzL/4cc0127b-2bca-4d38-3040-864b8f5054fdSnag_112741dd.png)

Результаты моих простых изменений стиля выглядят так:

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_uCSLHwdeVry8finx8/boo_OKQpsM12uk8DtYPzL/82ffd090-9575-e89b-b0ed-16f4af08a405Snag_1127954c.png)

Теперь, когда у вас есть все необходимые инструменты, попробуйте сами изменить настройки и создать красивый портал знаний, которым вы будете гордиться! Я уверен на 100%, что ваши порталы знаний будут выглядеть намного лучше, чем мой! :) Так что пробуйте и, главное, получайте удовольствие от процесса!