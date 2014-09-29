(function () {

  $('form').css('opacity', 1);
  window.paymentProcessing = false;

  $("form input[name=phone]").mask("(999) 999-9999");

  $('form input[name=name]').on('keyup, input', function() {
    var toggle = $(this).val().length > 0;
    if (toggle ^ $('form button[disabled]').first().is(':disabled'))
      return;
    $('form button').prop('disabled', !toggle);
    $('.pay-method').stop().fadeTo(250, toggle * 0.75 + 0.25);
  });

  var processPayment = function(type, token) {
    window.paymentProcessing = true;

    var name       = $('form input[name=name]').val();
    var price      = parseFloat($('form input[name=amount]').val()) * 100;
    var phone      = $('form input[name=phone]').val();
    var racetype   = $('form input[name=racetype]:checked').val();
    var uid, paths = window.location.pathname.split('/');

    if (paths.length == 4)
      uid = paths[2];

    $.post( $('form').attr('action') + uid + "/", { type: type, name: name, phone: phone, price: price, racetype: racetype, token: token.id })
      .done(function() {
        flash("", "");
        $('[data-billing-price]').text(price / 100);
        $('#billing').slideUp(500);
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
    $('.checkout-buttons button').prop('disabled', status);
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
    var price = parseFloat($('form input[name=amount]').val()) * 100;
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

  $("form.billing input[name=amount]").on('keyup', function(e) {
    var thankyou = $(this).parents('.form-group').find('.donation-thank-you');
    if (parseFloat($(this).val()) > parseFloat($(this).data('value-min')))
      thankyou.fadeIn(300);
    else
      thankyou.fadeOut(200);
  });

  $("form.billing").bootstrapValidator({
    excluded: [':disabled', ':hidden', ':not(:visible)'],
    message: false,
    trigger: "blur",
    submitButtons: 'button[type="button"]',
    feedbackIcons: {
      valid: "fa fa-check",
      invalid: "fa fa-remove",
      validating: "fa fa-refresh fa-spin"
    },
    fields: {
      name: {
        validators: {
          notEmpty: {
            message: "Please provide your full name"
          },
          regexp: {
            message: "Please provide your full name",
            regexp: /.{2,}\s+.+/
          }
        }
      },
      phone: {
        validators: {
          phone: {
            message: "Please provide your phone number",
            country: "US"
          },
          notEmpty: {
            message: "Please provide your phone number"
          }
        }
      },
      amount: {
        trigger: "blur keyup",
        validators: {
          notEmpty: {
            message: "A minimum donation of $" + $('form input[name=amount]').data('value-min') + " is required"
          },
          greaterThan: {
            inclusive: true,
            value: parseFloat($('form input[name=amount]').data('value-min')),
            message: "A minimum donation of $" + $('form input[name=amount]').data('value-min') + " is required"
          }
        }
      }
    }
  });

})();
