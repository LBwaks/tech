function windowScroll() {
    var t = document.getElementById("navbar");
    50 <= document.body.scrollTop || 50 <= document.documentElement.scrollTop ? t.classList.add("nav-sticky") : t.classList.remove("nav-sticky")
}
window.addEventListener("scroll", function(t) {
    t.preventDefault(), windowScroll()
});
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]')),
    tooltipList = tooltipTriggerList.map(function(t) {
        return new bootstrap.Tooltip(t)
    });


$ = jQuery;
$( document ).ready(function() {
  
  $h_slider_options =  {
      gallery: true,
      item: 1,
      loop:true,
      slideMargin: 0,
      thumbItem: 6,
      galleryMargin: 10,
      thumbMargin: 10,
      }; 

 

  h_slider = $('#lightSlider').lightSlider($h_slider_options);

  $selector = '#lightSlider li:not(".clone") a';
  
  $().fancybox({
    selector : $selector,
    backFocus : false, 
    buttons : [ 
      'slideShow',
      'share',
      'zoom',
      'fullScreen',
      'thumbs',
      'download',
      'close'
    ]
  });
});

$( window ).resize(function() {
		slider.destroy();
		h_slider = $('#ocassions-slider').lightSlider(h_slider_options);
});

// counter
function _toConsumableArray(t) {
    if (Array.isArray(t)) {
        for (var n = 0, e = Array(t.length); n < t.length; n++) e[n] = t[n];
        return e
    }
    return Array.from(t)
}
var isCounters = document.querySelectorAll(".counter");
isCounters.forEach(function(e) {
    var r, t = [].concat(_toConsumableArray(/(\D+)?(\d+)(\D+)?(\d+)?(\D+)?/.exec(e.textContent))),
        a = !0;
    for (t.shift(), t = t.filter(function(t) {
            return null != t
        }); e.firstChild;) e.removeChild(e.firstChild);
    t.forEach(function(t) {
        if (isNaN(t)) e.insertAdjacentHTML("beforeend", "<span>" + t + "</span>");
        else
            for (var n = 0; n < t.length; n++) e.insertAdjacentHTML("beforeend", '<span data-value="' + t[n] + '">\n\t\t\t\t\t\t<span>&ndash;</span>\n\t\t\t\t\t\t' + Array(parseInt(t[n]) + 1)
                .join(0)
                .split(0)
                .map(function(t, n) {
                    return "\n\t\t\t\t\t\t\t<span>" + n + "</span>\n\t\t\t\t\t\t"
                })
                .join("") + "\n\t\t\t\t\t</span>")
    }), r = [].concat(_toConsumableArray(e.querySelectorAll("span[data-value]")));
    var o = function() {
        var t = e.getBoundingClientRect()
            .top,
            n = .8 * window.innerHeight;
        setTimeout(function() {
            a = !1
        }, 1e3), t < n && (setTimeout(function() {
            r.forEach(function(t) {
                var n = parseInt(t.getAttribute("data-value")) + 1;
                t.style.transform = "translateY(-" + 100 * n + "%)"
            }, a ? 1e3 : 0)
        }), window.removeEventListener("scroll", o))
    };
    window.addEventListener("scroll", o), o()
});
