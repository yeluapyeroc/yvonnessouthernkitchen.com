// Create the root navigation ajax and bindings arrays for jquery.django.ajax
$my.ajax = {
    home : [],
    menu : [],
};

/*
 * $my.ajax.home[0].
 *
 */
$my.ajax.home[0] = function() {
};

/*
 * $my.ajax.home[0].
 *
 */
$my.ajax.menu[0] = function() {
  console.log('got here');
  $('div.menu-item').click(function(e){
    $(this).animate({'margin':'2px 0 8px 10px'}, 0, function(){
      $(this).animate({'margin':'0 0 10px 10px'}, 50);
      });
    });
};

/*
 * jQuery.ready. Called when the document is ready to be traversed.
 *
 */
$(function() {
    // Store common jQuery selections in the global $my object
});
