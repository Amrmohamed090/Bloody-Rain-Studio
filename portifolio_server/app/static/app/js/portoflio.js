document.addEventListener("DOMContentLoaded", function () {
    var serviceTabs = document.querySelectorAll("#portfolio-flters li");
    serviceTabs.forEach(function (tab) {
        tab.addEventListener("click", function () {
            
            var serviceId = this.getAttribute("data-service-id")
            console.log(serviceId);
            var currentUrl = window.location.href;
            var newUrl;
            if (serviceId !== null && serviceId !== "") {
                console.log("you tapped on not null")
                if (currentUrl.includes("?pageid=")) {
                    newUrl = currentUrl.replace(/(pageid=)[^&]+/, '$1' + serviceId);
                } else {
                    newUrl = currentUrl + "?pageid=" + serviceId;
                }
            } else {
                newUrl = currentUrl.split('?')[0];
                
            }
            console.log(serviceId)
            console.log(newUrl)
            window.history.replaceState({}, "", newUrl);
        });
    });
});



// Initiate the wowjs
$(document).ready(function() {
    // Portfolio isotope and filter
    var portfolioIsotope = $('.portfolio-container').isotope({
        itemSelector: '.portfolio-item',
        layoutMode: 'masonry'
    });

    // Function to extract pageid from URL
    function getHashFilter() {
        var hash = location.search;
        var matches = hash.match(/pageid=([^&]+)/i);
        
        var hashFilter = matches && matches[1];
        return hashFilter ? '.service' + hashFilter : '*'; // Return filter string based on pageid or return all
    }

    // Apply filter based on pageid in URL when page loads
    var initialFilter = getHashFilter();
    $('#portfolio-flters li[data-filter="' + initialFilter + '"]').addClass('active');
    portfolioIsotope.isotope({filter: initialFilter});

    // Click event for filter buttons
    $('#portfolio-flters li').on('click', function () {
        $("#portfolio-flters li").removeClass('active');
        $(this).addClass('active');

        portfolioIsotope.isotope({filter: $(this).data('filter')});
    });
});