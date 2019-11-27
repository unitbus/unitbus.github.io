// Thank you for まろりか.
// https://www.marorika.com/entry/create-toc

document.addEventListener('DOMContentLoaded', function () {
    // 目次を追加する先(table of contents)
    var contentsList = document.getElementById('toc');
    
    // 作成する目次のコンテナ要素
    var div = document.createElement('div');
    
    // .entry-content配下のh1、h2要素を全て取得する
    var matches = document.querySelectorAll('h1, h2');
    
    // 取得した見出しタグ要素の数だけ以下の操作を繰り返す
    matches.forEach(function (value, i) {
        
        // 見出しタグ要素のidを取得し空の場合は内容をidにする
        var id = value.id;
        if(id == '') {
            id = value.textContent;
            value.id = id;
        }
        
        if(value.tagName == 'H1' || value.tagName == 'H2') {
            var ul = document.createElement('ul');
            var li = document.createElement('li');
            var a = document.createElement('a');
            
            // 追加する<ul><li><a>タイトル</a></li></ul>を準備する
            a.innerHTML = value.textContent;
            a.href = '#' + value.id;
            
            li.appendChild(a)
            ul.appendChild(li);
            
            // 要素がh1タグの場合
            // コンテナ要素である<div>の中に要素を追加する
            if(value.tagName == 'H1') {
                div.appendChild(ul);
            }
            
            // 要素がh2タグの場合
            if (value.tagName == 'H2') {
                // コンテナ要素である<div>の中から最後の<li>を取得する。
                // 最後の<li>の中に要素を追加する
                var lastUl = div.lastElementChild;
                var lastLi = lastUl.lastElementChild;
                lastLi.appendChild(ul);
            }
        }
    });
    
    // 最後に画面にレンダリング
    contentsList.appendChild(div);
});
