(function () {

  $('form button[disabled]').prop('disabled', false);

  var price = $('form input[name="amount"]').val();

  // TODO: move into common.js

  var flash = function(message, type) {
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

  var processPayment = function(type, token) {
    var name = $('form input[name=name]').val();
    var price = $('form input[name=amount]').val();
    $.post( "/pay/", { type: type, name: name, price: price, token: token.id })
      .done(function() {
        flash("", "");
        $('#register').slideUp(500);
        $('#complete').delay(10).slideDown(500);
        if (type === "cash")
          $("#cash-reminder").show();
      })
      .fail(function(response) {
        setProcessing(false);
        console.log(response.responseText);
        message = response.responseText ? response.responseText : "Sorry, an error ocurred. Please try again.";
        flash(message, "danger");
      });
  };

  var setProcessing = function(status) {
    $('.checkout-buttons button').attr('disabled', status);
    if (status) {
      $('.checkout-buttons').stop().fadeTo(100, 0.5);
      flash("<i class='fa fa-circle-o-notch fa-spin'></i>&nbsp;&nbsp;Processing, please wait...", "info");
    } else {
      $('.checkout-buttons').stop().fadeTo(100, 1);
      flash("", "");
    }
  };

  var stripe = StripeCheckout.configure({
    key: 'pk_test_iTRx0tT5GH6J3m7bYjny6tBM',
    image: '/static/images/csh-stripe-checkout-logo.png',
    token: function(token) {
      processPayment("credit", token);
    },
    closed: function() {
      $('.checkout-buttons button').attr('disabled', false);
      $('.checkout-buttons').stop().fadeTo(100, 1);
      flash("", "");
    }
  });

  $('button[name=type][value=credit]').on('click', function(e) {
    setProcessing(true);
    stripe.open({
      name: 'CSH Costume 5K',
      description: 'Registration ($' + price / 100 + '.00)',
      amount: price
    });
    e.preventDefault();
  });

  $('button[name=type][value=cash]').on('click', function(e) {
    setProcessing(true);
    processPayment("cash", {});
    e.preventDefault();
  });

})();
