/*
file: core.js
handles key web functions for CSH 5K FunRun responsive site
Created By: Brandon Hudson
Date: 9/19/14
*/

// Page Scrolling
$(function() {
  $('a[href*=#]:not([href=#])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html,body').animate({
          scrollTop: target.offset().top
        }, 1000);
        return false;
      }
    }
  });
});

//Map
	  function initialize() {
  var image = 'startingline.png';
  var startLatlng = new google.maps.LatLng(43.085546,-77.665937);
   var mapOptions = {
          center: {lat: 43.083885,lng: -77.671666}, //43.0844° N, 77.6749° W
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
    	new google.maps.LatLng(43.083885,-77.665894), 
    	new google.maps.LatLng(43.082537,-77.665894), 
   	 	new google.maps.LatLng(43.081863,-77.665958),
		new google.maps.LatLng(43.08133,-77.66613),
    	new google.maps.LatLng(43.080892,-77.666323),
    	new google.maps.LatLng(43.080531,-77.666709), 
   	 	new google.maps.LatLng(43.080249,-77.667096),
		new google.maps.LatLng(43.079967,-77.667439), 
		new google.maps.LatLng(43.0797,-77.668018), 
   	 	new google.maps.LatLng(43.07945,-77.668576), 
		new google.maps.LatLng(43.079309,-77.669134), 
		new google.maps.LatLng(43.079183,-77.669692), 
   	 	new google.maps.LatLng(43.079152,-77.670336), 
		new google.maps.LatLng(43.079136,-77.671001), 
		new google.maps.LatLng(43.079215,-77.671666), 
   	 	new google.maps.LatLng(43.079387,-77.672417), 
		new google.maps.LatLng(43.0797,-77.673104), 
		new google.maps.LatLng(43.080061,-77.673705), 
   	 	new google.maps.LatLng(43.080531,-77.674241), 
		new google.maps.LatLng(43.081048,-77.674799), 
		new google.maps.LatLng(43.081362,-77.675421), 
   	 	new google.maps.LatLng(43.081503,-77.676151),
		new google.maps.LatLng(43.081377,-77.676795), 
		new google.maps.LatLng(43.081111,-77.677374), 
   	 	new google.maps.LatLng(43.080829,-77.677953), 
		new google.maps.LatLng(43.080343,-77.67879),
		new google.maps.LatLng(43.080139,-77.679284), 
   	 	new google.maps.LatLng(43.08097,-77.679348),
		new google.maps.LatLng(43.082036,-77.679369), 
   	 	new google.maps.LatLng(43.08304,-77.67938), 
		new google.maps.LatLng(43.083847,-77.679391), 
   	 	new google.maps.LatLng(43.084858,-77.679402), 
		new google.maps.LatLng(43.084944,-77.677621),
   	 	new google.maps.LatLng(43.084529,-77.677181), 
		new google.maps.LatLng(43.084544,-77.676687), 
   	 	new google.maps.LatLng(43.084889,-77.676097), 
   	 	new google.maps.LatLng(43.085038,-77.675561), 
		new google.maps.LatLng(43.085728,-77.675571), 
   	 	new google.maps.LatLng(43.085861,-77.674434),  
		new google.maps.LatLng(43.085829,-77.673426), 
		new google.maps.LatLng(43.08474,-77.673318), 
   	 	new google.maps.LatLng(43.084278,-77.673372),  
		new google.maps.LatLng(43.084333,-77.670357),
		new google.maps.LatLng(43.084685,-77.670679), 
   	 	new google.maps.LatLng(43.085265,-77.670883),  
		new google.maps.LatLng(43.085634,-77.670979),// 
		new google.maps.LatLng(43.085641,-77.672964),
   	 		
		new google.maps.LatLng(43.085641,-77.672964),
		new google.maps.LatLng(43.085939,-77.673029),
		new google.maps.LatLng(43.085971,-77.673415), 
		new google.maps.LatLng(43.086104,-77.674284),
		new google.maps.LatLng(43.086652,-77.674391), 
   	 	new google.maps.LatLng(43.087177,-77.674423),  
		new google.maps.LatLng(43.087663,-77.674177),// 
   	 	new google.maps.LatLng(43.087749,-77.67319),
		new google.maps.LatLng(43.087749,-77.672213), 
   	 	new google.maps.LatLng(43.087945,-77.67114),
		new google.maps.LatLng(43.088431,-77.66996), 
   	 	new google.maps.LatLng(43.088846,-77.668909), //ended here
		new google.maps.LatLng(43.088995,-77.66819), 
   	 	new google.maps.LatLng(43.088995,-77.667654),
		new google.maps.LatLng(43.088995,-77.667654), 
   	 	new google.maps.LatLng(43.088854,-77.667203),
		new google.maps.LatLng(43.088642,-77.666838), 
   	 	new google.maps.LatLng(43.088423,-77.666495),
		new google.maps.LatLng(43.088102,-77.666184), 
   	 	new google.maps.LatLng(43.087694,-77.665991),
		new google.maps.LatLng(43.087248,-77.665958), 
   	 	new google.maps.LatLng(43.086738,-77.66598),
		new google.maps.LatLng(43.086159,-77.665926), //ended here
   	 	new google.maps.LatLng(43.083885,-77.665894)
		
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
google.maps.event.addDomListener(window, 'load', initialize);