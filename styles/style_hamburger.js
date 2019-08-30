/* Hamburger Navigation Sample */
$(function() {

  /* 開閉ボタンをクリックしたら以下の関数を実行 */
  $('#hamburger-nav-toggle').click(function() {

    /* 開閉ボタンのクラスが'close'（閉じている状態）の場合 */
    if($('#hamburger-nav-toggle').attr("class") == 'hamburger-nav-toggle-btn close') {

      /* ハンバーガーメニューを展開 */
      $('.hamburger-nav-list').slideDown();

      /* さらに、開閉ボタンのクラスから'close'を削除し、'open'を付与する */
      $(this).removeClass("close").addClass("open");
    }

    /* 開閉ボタンのクラスが'close'ではない場合 */
    else {

      /* ハンバーガーメニューを収束 */
      $('.hamburger-nav-list').slideUp(function() {

        /* メニューが収束したのち、開閉ボタンのクラスから'open'を削除し、'close'を付与する */
        $('#hamburger-nav-toggle').removeClass("open").addClass("close");
      });
    }
  }); /* 開閉ボタンをクリックした時の動作はここまで */

  /* ハンバーガーメニューのアンカーをクリックしたら以下の関数を実行 */
  $('.hamburger-nav-list a').click(function() {

    /* 開いている必要はないので、ハンバーガーメニューを収束 */
    $('.hamburger-nav-list').slideUp(function() {

      /* メニューが収束したのち、開閉ボタンのクラスから'open'を削除し、'close'を付与する */
      $('#hamburger-nav-toggle').removeClass("open").addClass("close");
    });
  });

  /* SmoothScroll（おまけ） */
  $('.hamburger-nav-list a').smoothScroll();

});