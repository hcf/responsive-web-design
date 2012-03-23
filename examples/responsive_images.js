$(function(){
  $("noscript").each(function() {
    var ns = $(this),
        best_fit = 0,
        content_width = ns.parent().width(),
        img_widths = $.map(ns.data("widths").split(","),
                           function(width) { return parseInt(width) });

    $.each(img_widths, function(i, img_width) {
      best_fit = i;
      return img_width < content_width;
    });

    var src = ns.data("base-src").replace(/(.+)(\.\w{3})/,
                      "$1-" + img_widths[best_fit] + "$2")
    ns.after($("<img>").attr("src", src));
  });
});
