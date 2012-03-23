var throttle = function(fn, delay) {
  var timer = null;
  return function () {
    var context = this, args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function () {
      fn.apply(context, args);
    }, delay);
  };
}

$(function() {
  responsiveTables();
});

$(window).on('resize', function() {
  throttle(responsiveTables(), 50);
});

var prependHeadersToTableCells = function(table) {
  var headers = $.map(table.find("th"), function(th) {
    return $(th).text();
  });

  table.find("tr").each(function() {
    var $tr = $(this);

    $tr.find("td").each(function(i) {
      var $td = $(this);
      if($td.find(".header").length === 0) {
        var header = headers[i];
        $td.html("<strong class='header'>" + header.trim()
                 + ":</strong> " + $td.html());
      }
    });
  });
}

var removeHeadersFromTableCells = function(table) {
  table.find("tr td .header").remove();
}

var responsiveTables = function() {
  $("article table").each(function() {
    var $table = $(this);

    if($table.css("display") === "block") {
      prependHeadersToTableCells($table);
    } else if($table.css("display") === "table") {
      removeHeadersFromTableCells($table);
    }
  });
}
