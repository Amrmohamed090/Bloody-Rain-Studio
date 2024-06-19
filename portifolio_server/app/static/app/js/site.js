"use strict";

$(document).ready(function () {
	/* Video Lightbox */
	if (!!$.prototype.simpleLightboxVideo) {
		$('.video').simpleLightboxVideo();
	}

	/*ScrollUp*/
	if (!!$.prototype.scrollUp) {
		$.scrollUp();
	}

	/*Responsive Navigation*/
	$("#nav-mobile").html($("#nav-main").html());
	$("#nav-trigger span").on("click",function() {
		if ($("nav#nav-mobile ul").hasClass("expanded")) {
			$("nav#nav-mobile ul.expanded").removeClass("expanded").slideUp(250);
			$(this).removeClass("open");
		} else {
			$("nav#nav-mobile ul").addClass("expanded").slideDown(250);
			$(this).addClass("open");
		}
	});

	$("#nav-mobile").html($("#nav-main").html());
	$("#nav-mobile ul a").on("click",function() {
		if ($("nav#nav-mobile ul").hasClass("expanded")) {
			$("nav#nav-mobile ul.expanded").removeClass("expanded").slideUp(250);
			$("#nav-trigger span").removeClass("open");
		}
	});

	/* Sticky Navigation */
	if (!!$.prototype.stickyNavbar) {
		$('#header').stickyNavbar();
	}

	$('#about').waypoint(function (direction) {
		if (direction === 'down') {
			$('#header').addClass('nav-solid fadeInDown');
		}
		else {
			$('#header').removeClass('nav-solid fadeInDown');
		}
	});

});


$(window).on('load', function() {
    $('#preloader').delay(350).fadeOut('slow', function() {
        $(this).addClass('hidden'); // Add hidden class after fade out
    });
    $('body').delay(350).css({'overflow-y': 'visible'});
});



document.addEventListener('DOMContentLoaded', function() {
	const contactUsButton = document.getElementById('contactUsButton');
	const firstSectionHeight = document.querySelector('section').offsetHeight;
  
	window.addEventListener('scroll', function() {
	  if (window.scrollY > 300) {
		contactUsButton.classList.add('visible');
	  } else {
		contactUsButton.classList.remove('visible');
	  }
	});
  });

