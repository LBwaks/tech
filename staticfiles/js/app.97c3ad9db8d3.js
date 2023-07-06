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