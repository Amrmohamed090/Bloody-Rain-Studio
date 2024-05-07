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