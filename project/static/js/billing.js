(function () {

  $('form').css('opacity', 1);
  $('form button[disabled], form input').prop('disabled', false);

  var price = $('form input[name="amount"]').val();
  window.paymentProcessing = false;

  var processPayment = function(type, token) {
    window.paymentProcessing = true;

    var name = $('form input[name=name]').val();
    var price = $('form input[name=amount]').val();
    var uid, paths = window.location.pathname.split('/');
    if (paths.length == 4)
      uid = paths[2];
    $.post( $('form').attr('action') + uid + "/", { type: type, name: name, price: price, token: token.id })
      .done(function() {
        flash("", "");
        $('#register').slideUp(500);
        $('#complete').delay(10).slideDown(500);
        if (type === "cash")
          $("#cash-reminder").show();
      })
      .fail(function(response) {
        setProcessing(false);
        message = response && response.responseText.length < 250 ? response.responseText : "Our appologies, an error ocurred. Please contact <a href='mailto:5k@csh.rit.edu'>5k@csh.rit.edu</a>.";
        flash(message, "danger");
      })
      .always(function() {
        window.paymentProcessing = false;
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
      if (window.paymentProcessing)
        return;
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
      amount: price,
      email: $('form input[name=email]').val(),
      allowRememberMe: false
    });
    e.preventDefault();
  });

  $('button[name=type][value=cash]').on('click', function(e) {
    processPayment("cash", {});
    e.preventDefault();
  });

})();
