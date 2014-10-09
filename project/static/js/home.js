(function () {

  // Page Scrolling
  $(function () {
    $('a[href*=#]:not([href=#])').click(function () {
      if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
        if (target.length) {
          $('html,body').animate({
            scrollTop: target.offset().top - 50
          }, 1000);
          $('.navbar-collapse.in').collapse('hide');
          return false;
        }
      }
    });
  });

  // Map
  function initialize_map() {
    var image = 'startingline.png';
    var startLatlng = new google.maps.LatLng(43.080713,-77.674472);
    var mapOptions = {
      center: {
        lat: 43.083885,
        lng: -77.671666
      },
      //43.0844° N, 77.6749° W
      zoom: 14,
      zoomControl: false
    };
    var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

    var marker = new google.maps.Marker({
      position: startLatlng,
      map: map,
      title: 'Starting Line',

    });

    var courseCoords = [
   		new google.maps.LatLng(43.0821,-77.675051),
		new google.maps.LatLng(43.081935,-77.67503),
		new google.maps.LatLng(43.081739,-77.675019),
		new google.maps.LatLng(43.081457,-77.675073),
		new google.maps.LatLng(43.081253,-77.675169),
		new google.maps.LatLng(43.080713,-77.674472),
		new google.maps.LatLng(43.080062,-77.67371),
		new google.maps.LatLng(43.079616,-77.672841),
		new google.maps.LatLng(43.079271,-77.671725),
		new google.maps.LatLng(43.079177,-77.670427),
		new google.maps.LatLng(43.079255,-77.669536),
		new google.maps.LatLng(43.079482,-77.668603),
		new google.maps.LatLng(43.079866,-77.66768),
		new google.maps.LatLng(43.080352,-77.666994),
		new google.maps.LatLng(43.080971,-77.66635),
		new google.maps.LatLng(43.081575,-77.666028),
		new google.maps.LatLng(43.082711,-77.665889),
		new google.maps.LatLng(43.083957,-77.665899),
		new google.maps.LatLng(43.085304,-77.665964),
		new google.maps.LatLng(43.086456,-77.665964),
		new google.maps.LatLng(43.087671,-77.666007),
		new google.maps.LatLng(43.088211,-77.666296),
		new google.maps.LatLng(43.088635,-77.666758),
		new google.maps.LatLng(43.088893,-77.667337),
		new google.maps.LatLng(43.089011,-77.668077),
		new google.maps.LatLng(43.088854,-77.668989),
		new google.maps.LatLng(43.088595,-77.669579),
		new google.maps.LatLng(43.088313,-77.670234),
		new google.maps.LatLng(43.088047,-77.670942),
		new google.maps.LatLng(43.087796,-77.671714),
		new google.maps.LatLng(43.087694,-77.672605),
		new google.maps.LatLng(43.087686,-77.673066),
		new google.maps.LatLng(43.087412,-77.673045),
		new google.maps.LatLng(43.087326,-77.672262),
		new google.maps.LatLng(43.087334,-77.671725),
		new google.maps.LatLng(43.087013,-77.671543),
		new google.maps.LatLng(43.086574,-77.671521),
		new google.maps.LatLng(43.086159,-77.671543),
		new google.maps.LatLng(43.086057,-77.671886),
		new google.maps.LatLng(43.086198,-77.672305),
		new google.maps.LatLng(43.086613,-77.672326),
		new google.maps.LatLng(43.087052,-77.672369),
		new google.maps.LatLng(43.087326,-77.672262),
    ];
    var course = new google.maps.Polyline({
      path: courseCoords,
      geodesic: true,
      strokeColor: '#FF9900',
      strokeOpacity: .5,
      strokeWeight: 8
    });
    course.setMap(map)


  }
  google.maps.event.addDomListener(window, 'load', initialize_map);

})();
