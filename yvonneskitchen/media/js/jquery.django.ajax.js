/*
 * Global Obect - Use to cache global variables and often used
 * jQuery results.
 */
window.$my = {
    domain : "http://" + document.domain + ":8000/",
    current_hash : '',
    previous_page: [],
    current_page : [],
    path_name : window.location.pathname,
    ajax : {},
    ajax_cache : {},
    current_request : null
};

/* 
 * Utilitiy Functions
 */

/*
 * jQuery.fn.loadHTML. Load HTML into a jQuery object utilizing AJAX.
 *
 * @param url_path a string that designates what URL path to call on the server
 * @param args a dictionary of arguments to pass with the AJAX call
 * @param functions an array of functions to call when the AJAX is done.
 *    Functions are called synchronously in the order they are placed in the
 *    array.
 *
 * @return the selected jQuery object that propogated the AJAX.
 *
 */
jQuery.fn.loadHTML = function(url_path, args, allow_multi) {
    if($my.current_request && !allow_multi) {
        $my.current_request.abort();
        $my.previous_page = ['none'];
        $.changeView();
        return this;
    }
    var cache_key = url_path;
    $.each(args, function(key, val){
        cache_key = cache_key + String(val) + '/';
        });
    return this.each(function(){
            var self = $(this);
            self.fadeOut(250, function(){
                if(cache_key in $my.ajax_cache) {
                    self.html($my.ajax_cache[cache_key]);
                    self.show();
                    $my.current_request = null;
                }else{
                    self.html('<img class="loader" src="/media/img/loader.gif"/>');
                    self.show();
                    $my.current_request = $.ajax({
                        type: 'POST',
                        url: $my.domain + url_path,
                        data: args,
                        dataType: 'html',
                        error: function(req, stat){
                            self.hide();
                            self.html(req.responseText);
                            },
                        success: function(data, stat){
                            $my.ajax_cache[cache_key] = data;
                            self.hide();
                            self.html(data);
                            },
                        complete: function(){
                            self.show();
                            $my.current_request = null;
                            }
                        });
                }
                });
            });
};

/*
 * jQuery.hashArray. Return the value of the window's hash as an array,
 * delimited by '-'.
 *
 * @return and array of strings
 *
 */
jQuery.hashArray = function() {
    return window.location.hash.slice(1).split('-');
};

/*
 * jQuery.hashString. Return the value of the window's hash as a string.
 *
 * @return a string
 *
 */
jQuery.hashString = function() {
    return window.location.hash.slice(1);
};

/*
 * jQuery.preLoadImages. Preload a list of images.
 *
 * @param arguments should be strings of image paths
 *
 */
jQuery.preLoadImages = function() {
    var cache = [];
    var args_len = arguments.length;
    for(var i=args_len; i--;) {
        var cacheImage = document.createElement('img');
        cacheImage.src = arguments[i];
        cache.push(cacheImage);
    }
};

//Test browser type. Internet Explorer implements makeHistory differently
if(navigator.appName == 'Microsoft Internet Explorer') {
/*
 * jQuery.makeHistory. (Internet Explorer) Loads, writes, and closes the
 * iFrame document to create a history marker in Internet Explorer.
 *
 * @param newHash a string to replace the current hash with
 *
 */
    jQuery.makeHistory = function(newHash){
        var doc = $('#historyFrame')[0].contentWindow.document;
        doc.open("javascript:'<html></html>'");
        doc.write("<html><head><scri" + "pt type=\"text/javascript\">parent.$.onFrameLoaded('" + newHash + "');</scri" + "pt></head><body></body></html>");
        doc.close();
    };
/*
 * jQuery.onFrameLoaded. (Internet Explorer) Called from the iFrame when
 * it is done loading. Changes the URI hash.
 *
 * @param newHash a string to replace the current URI hash with
 *
 */
    jQuery.onFrameLoaded = function(newHash){
        if($my.path_name == '/') {
            window.location.hash = newHash;
        }else{
            window.location.replace(domain + '#' + newHash);
        }
    };
}else{
/*
 * jQuery.makeHistory. Changes the URI hash for browsers other than
 * Internet Explorer.
 *
 * @param newHash a string to replace the current URI hash with
 *
 */
    jQuery.makeHistory = function(newHash){
        window.location.hash = newHash;
    };
}

/*
 * changeView. Determines which section of the hash has changed and calls the
 * appropriate $my.ajax function.
 *
 */
jQuery.changeView = function() {
    try {
        for(var i=0; i<$my.current_page.length; i++) {
            if($my.current_page[i] != $my.previous_page[i]) {
                $my.ajax[$my.current_page[0]][i]();
                return;
            }
        }
        $my.ajax[$my.current_page[0]][0]();
        return;
    }catch(err){
        console.log(err);
        return;
    }
};

/*
 * jQuery.handleURI. Checks to see if the URI hash has changed and calls changeView
 * if it has.
 *
 */
jQuery.handleURI = function() {
    // If the URI has changed since the last poll call the ChangeView function
    if($my.current_hash != $.hashString()) {
        $my.current_hash = $.hashString(); // update $my.current_hash
        $my.previous_page = $my.current_page; // update $my.previous_page
        if(!$my.current_hash){
            if($my.path_name == '/'){
                $my.current_page = ['home'];
            }else{
                $my.current_page = window.location.pathname.slice(1, -1).split('/');
            }
        }else{
            $my.current_page = $.hashArray(); // update $my.current_page
        }
        $.changeView();
    }
};

/*
 * jQuery.ready: Initializes the global object variables, sets an interval
 * for checking the URI hash, and binds the click event for all 'A' tags
 * to the body, using event delegation.
 *
 */
$(function(){
    if($my.path_name == '/') {
        if(!$.hashString()) {
            $my.current_page = ['home'];
        }else{
            $my.current_page = $.hashArray();
        }
    }else{
        $my.current_page = window.location.pathname.slice(1, -1).split('/');
    }
    window.setInterval("$.handleURI();", 500);
    $('body').bind('click', function(e){
        var target = e.target, $target = $(target);
        if(target.nodeName == 'A'){
            if($target.hasClass('outbound')){
                return true;
            }else{
                $.makeHistory($target.attr('rel'));
                return false;
            }
        }
        });
    return;
});
