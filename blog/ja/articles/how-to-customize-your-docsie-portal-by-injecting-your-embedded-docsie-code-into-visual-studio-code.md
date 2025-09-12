<iframe width="560" height="315" src="https://www.youtube.com/embed/xRdJhd9SAV0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


# Visual Studio Codeを使ってDocsieポータルをカスタマイズする方法

Docsieには多くのカスタマイズ機能があります。この記事では、Docsieポータルのカスタマイズを始めるために必要な手順をご紹介します。私はプロの開発者やデザイナーではないことをご了承ください。実際には、技術チームがこれらのツールを使って、私よりもはるかに美しいDocsieポータルを作成できます。これは単に、彼らが始めるための手順ガイドです！

## STEP 1

最初のステップは、埋め込みコードを取得することです。右上にあるアカウント名の横にある3つのドットをクリックします。これでDocsieの設定ダッシュボードに移動します。

## STEP 2

次に、左側にある「Deployment（デプロイメント）」ボタンをクリックします。

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_UNFgmrrV4LJRPPcLD/boo_OKQpsM12uk8DtYPzL/f551ad37-a3a0-78bb-f97a-1246d5d57899Snag_1113a5f7.png)

デプロイメント設定画面では、Docsieクラウドを通じてナレッジポータルを作成するか、HTMLに追加できるコードを使って自社ウェブサイトにナレッジポータルを作成するかを選択できます。「Configure a new deployment +（新しいデプロイメントを設定+）」をクリックするだけです。

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_66sDikYE16JfYewXU/boo_OKQpsM12uk8DtYPzL/4a8b6dd2-03d2-5d7a-837d-e3afdbe66900Snag_11161d31.png)

## STEP 3

次に「Custom deployment（カスタムデプロイメント）」タブをクリックし、「Deployment URL（デプロイメントURL）」にウェブサイトを入力して、「Create web portal（ウェブポータルを作成）」をクリックします。

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_6CGgetG9GizkqY87p/boo_OKQpsM12uk8DtYPzL/4b102fcb-a424-8966-1f92-59b56e14241dimage.png)

完了したら、ポータルリストの一番下までスクロールして、作成したポータルを見つけ、「Get deployment script（デプロイメントスクリプトを取得）」をクリックします。

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_el02yIrEUA3rf28CG/boo_OKQpsM12uk8DtYPzL/a64fc5d5-4e2c-9c6a-8325-6ed88a291db3Snag_1119813c.png)

## STEP 4

スクリプトをコピーして、Visual Studio Codeに移りましょう！

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_a3ExYoQ3yZSLnkf4y/boo_OKQpsM12uk8DtYPzL/1a26f697-45e9-b0c4-53d2-8ad808b8d49fSnag_111a44da.png)

Docsieから埋め込みコードを取得する方法についての詳細は、[こちら](https://www.docsie.io/blog/articles/publishing-product-documentation-with-docsie/)のドキュメント公開に関するブログをご覧ください。

Visual Studio Codeでindex.html、index.css、index.jsファイルを作成します（すでにファイルがある場合は不要です）。HTMLファイルを開き、コードをHTMLのbodyタグ内（</head>タグの下）に貼り付けます。

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_ss2981O27UrVWVfrx/boo_OKQpsM12uk8DtYPzL/64bda798-9915-3b7b-274f-dc707b9118a2Snag_111c041e.png)

## STEP 5

ステップ5では「基本スタイル」を作成します。

Docsieポータルに基本スタイルを適用する方法についての詳細は[こちら](https://help.docsie.io/?doc=/publish-documentation-portal/docsie-styling-guide/base-style/)でご確認いただけます。

例として、HTMLに会社名のリンクを追加し、CSSで少し調整してみました。

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_xg25e1fVbKEZbjJYl/boo_OKQpsM12uk8DtYPzL/a49b8d34-7911-10aa-741a-781224f57212Snag_1122dccd.png)

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_fRoPLO0Df6JhTcf2h/boo_OKQpsM12uk8DtYPzL/7c668c24-8d5e-8fdf-5b2a-ad93de3b313cSnag_11238581.png)

結果はとてもシンプルですが、技術チームがDocsieナレッジポータルをカスタマイズし、ブランドの外観や雰囲気に合ったポータルを作成できる可能性をお見せしたかったのです。あなたの場合は異なるスタイルや色を使うかもしれませんが、多くのユーザーは自社のロゴを配置し、ナビゲーションバーを追加して、Docsieナレッジポータルが自社ウェブサイトにシームレスに自然に溶け込むようにしています。

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_StvlIomWiDjQ8wV0h/boo_OKQpsM12uk8DtYPzL/e02de6be-1990-cbe1-7078-4e477ec4a6d9Snag_112473e8.png)

## STEP 6

最後のステップでは、以下のようなスタイリングの変更を追加しました：

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

これを「基本スタイル」の最後のdivタグの下に貼り付けました。

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_ORs7jTN5WvXJ7VkuB/boo_OKQpsM12uk8DtYPzL/4cc0127b-2bca-4d38-3040-864b8f5054fdSnag_112741dd.png)

非常にシンプルなスタイル変更の結果はこのようになりました：

![](https://cdn.docsie.io/workspace_WxPJSQ5gsES8Bzjxy/doc_ydgtE07E6Rp4AMmKv/file_uCSLHwdeVry8finx8/boo_OKQpsM12uk8DtYPzL/82ffd090-9575-e89b-b0ed-16f4af08a405Snag_1127954c.png)

これで必要なツールはすべて揃いました。ぜひ自分で試してみて、様々な変更を加えて、誇れる美しいナレッジポータルを作成してみてください！あなたのナレッジポータルは私のものよりもはるかに洗練されたものになると確信しています！ぜひ試してみて、何より楽しんでください！