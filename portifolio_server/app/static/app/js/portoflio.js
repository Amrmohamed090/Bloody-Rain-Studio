document.addEventListener("DOMContentLoaded", function() {
    // Wait for all images to be loaded
    var images = document.querySelectorAll('img');
    var imagesLoaded = 0;
    images.forEach(function(img) {
        if (img.complete) {
            imagesLoaded++;
        } else {
            img.addEventListener('load', function() {
                imagesLoaded++;
                if (imagesLoaded === images.length) {
                    initializeIsotope();
                }
            });
        }
    });
    
    // If all images are already loaded, initialize Isotope immediately
    if (imagesLoaded === images.length) {
        initializeIsotope();
    }
});

function initializeIsotope() {
    // Initialize Isotope
    var $ = jQuery; // Assuming jQuery is available
    var t, e, i = $(".portfolio-container").isotope({
        itemSelector: ".portfolio-item",
        layoutMode: "masonry"
    });
    
    // Filter based on URL parameter
    var t = location.search.match(/pageid=([^&]+)/i);
    var o = t ? ".service" + t[1] : "*";
    $('#portfolio-flters li[data-filter="' + o + '"]').addClass("active");
    i.isotope({
        filter: o
    });
    
    // Handle filter click events
    $("#portfolio-flters li").on("click", function() {
        $("#portfolio-flters li").removeClass("active");
        $(this).addClass("active");
        i.isotope({
            filter: $(this).data("filter")
        });
    });
}

