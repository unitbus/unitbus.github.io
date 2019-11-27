$(function() {
    $("a").on("click", function() {
        var url = this.href;
        if (url && url.match(/\.7z$/)) {
            ga('send', {
                'hitType': 'pageview',
                'location': url
            });
        }
        if (url && url.match(/\.py$/)) {
            ga('send', {
                'hitType': 'pageview',
                'location': url
            });
        }
    });
});
