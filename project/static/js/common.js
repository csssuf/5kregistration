window.flash = function(message, type) {
  var element = $('#flash-message');

  if (message === '') {
    element.hide();
    return;
  }

  element.removeClass(function(index, css) {
      return (css.match (/(^|\s)alert-\S+/g) || []).join(' ');
  });
  element.addClass("alert-" + type);

  element.html(message);
  element.fadeIn(125);
};
