// Thank you for まろりか.
// https://www.marorika.com/entry/create-toc

document.addEventListener('DOMContentLoaded', function () {
    // 目次を追加する先(table of contents)
    var contentsList = document.getElementById('toc');
    
    // .entry-content配下のh1、h2要素を全て取得する
    var matches = document.querySelectorAll('h1, h2');
    
    // 新しい<ul>追加
    var ul = document.createElement('ul');
    var ol = document.createElement('ol');
    var ol_build = true;
    
    // 取得した見出しタグ要素の数だけ以下の操作を繰り返す
    matches.forEach(function (value, i) {
        if(!ol_build){
            ol = document.createElement('ol');
            ul.appendChild(ol);
            ol_build = true;
        }
        
        // 見出しタグ要素のidを取得し空の場合は内容をidにする
        var id = value.id;
        if(id == '') {
            id = value.textContent;
            value.id = id;
        }
        
        if(value.tagName == 'H1' || value.tagName == 'H2') {
            var li = document.createElement('li');
            var a = document.createElement('a');
            
            // 追加する<li><a>タイトル</a></li>を準備する
            a.innerHTML = value.textContent;
            a.href = '#' + value.id;
            li.appendChild(a);
            
            // 要素がh1タグの場合
            if(value.tagName == 'H2') {
                ol.appendChild(li);
            }
            
            // 要素がh1タグの場合
            if(value.tagName == 'H1') {
                ul.appendChild(li);
                ol_build = false;
            }
        }
    });
    
    // <ul>を閉じる
    // 最後に画面にレンダリング
    contentsList.appendChild(ul);
});
