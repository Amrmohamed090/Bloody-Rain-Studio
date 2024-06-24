document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll("#portfolio-flters li").forEach(function(t) {
        t.addEventListener("click", function() {
            var t, e = this.getAttribute("data-service-id"),
                i = window.location.href;
            t = null !== e && "" !== e ? i.includes("?pageid=") ? i.replace(/(pageid=)[^&]+/, "$1" + e) : i + "?pageid=" + e : i.split("?")[0], window.history.replaceState({}, "", t)
        })
    })
}), $(document).ready(function() {
    var t, e, i = $(".portfolio-container").isotope({
            itemSelector: ".portfolio-item",
        }),
        o = (e = (t = location.search.match(/pageid=([^&]+)/i)) && t[1]) ? ".service" + e : "*";
    $('#portfolio-flters li[data-filter="' + o + '"]').addClass("active"), i.isotope({
        filter: o
    }), $("#portfolio-flters li").on("click", function() {
        $("#portfolio-flters li").removeClass("active"), $(this).addClass("active"), i.isotope({
            filter: $(this).data("filter")
        })
    })
});