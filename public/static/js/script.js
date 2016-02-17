var current_image = ""
var effect = ""

$(document).ready(function(){
    $('.fb-share').click(function(e) {
        e.preventDefault();
        window.open($(this).attr('href'), 'fbShareWindow', 'height=450, width=550, top=' + ($(window).height() / 2 - 275) + ', left=' + ($(window).width() / 2 - 225) + ', toolbar=0, location=0, menubar=0, directories=0, scrollbars=0');
        return false;
    });

    $('.twitter-share-button').click(function(e) {
        e.preventDefault();
        window.open($(this).attr('href'), 'fbShareWindow', 'height=450, width=550, top=' + ($(window).height() / 2 - 275) + ', left=' + ($(window).width() / 2 - 225) + ', toolbar=0, location=0, menubar=0, directories=0, scrollbars=0');
        return false;
    });

    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });

    getHeight()

    $(".carousel-inner div:first").addClass("active");

    document.getElementsByTagName("BODY")[0].onresize = function() {getHeight()};

    $('#effectsholder').carousel({
      interval: false,
  })

    $('.carousel .item').each(function(){
      var next = $(this).next();
      if (!next.length) {
        next = $(this).siblings(':first');
    }
    next.children(':first-child').clone().appendTo($(this));

    for (var i=0;i<4;i++) {
        next=next.next();
        if (!next.length) {
            next = $(this).siblings(':first');
        }

        next.children(':first-child').clone().appendTo($(this));
    }
});

    $("#effectsholder .carousel-inner img").click(function () {
        effect = $(this).attr('id')
        $.ajax({
          method: "POST",
          url: "/image/edit/",
          data: { effect: effect, id:current_image}
      })
        .done(function( msg ) {
            name = msg.url
            var img = $("<img />").attr('src', '{{ STATIC_URL }}' + name)
            $(img).load(function(){
                $("#picholder").empty().append(img);
                $("#picholder img").addClass("thumbnail img-responsive");
                $("#wrapper").toggleClass("toggled");
                $("#effectsholder").removeClass("hidden");
                $("#social").removeClass("hidden");
                $(".fb-share").attr("href", "https://www.facebook.com/sharer/sharer.php?u=" + window.location.host + {{ STATIC_URL }} + name);
                $(".twitter-share-button").attr("href", "https://twitter.com/home?status=" + window.location.host + {{ STATIC_URL }} + name);

            }).error(function () {
                $("#picholder").empty().append('Error Loading Image');
            }).attr({
                id: 'myimage',
            }).css({"max-height": h + 'px'})
            effect = ''
        });
    });

});

function getHeight() {
    var vHeight = $(window).height();
    h = 0.9 * (vHeight)
    $('#content').css({"max-height":h });

}

function getPic(id) {
    $.ajax({
      method: "POST",
      url: "/image/",
      data: { id: id}
  })
    .done(function( msg ) {
        console.log(msg)
    });

}

function loadpic(name, id) {
    console.log(name)
    var vHeight = $(window).height();
    current_image = id
    h = 0.7 * (vHeight - 100)
    var img = $("<img />").attr('src', '{{ STATIC_URL }}' + name)
    $(img).load(function(){
        $("#picholder").empty().append(img);
        $("#picholder img").addClass("thumbnail img-responsive");
        $("#wrapper").toggleClass("toggled");
        $("#effectsholder").removeClass("hidden")
        $("#social").removeClass("hidden")
        $(".fb-share").attr("href", "https://www.facebook.com/sharer/sharer.php?u=" + window.location.host + {{ STATIC_URL }} + name);
        $(".twitter-share-button").attr("href", "https://twitter.com/home?status=" + window.location.host + {{ STATIC_URL }} + name);
    }).error(function () {
        $("#picholder").empty().append('Error Loading Image');
    }).attr({
        id: 'myimage',
    }).css({"max-height": h + 'px'})

    var preview = $("<img />").attr('src', '{{ STATIC_URL }}' + name)
    $(preview).load(function(){
        $("#preview").empty().append(preview);
        $("#preview img").addClass("thumbnail img-responsive");
    }).error(function () {
        $("#preview").empty().append('Error Loading Image');
    })

}



$.ajaxSetup({
 beforeSend: function(xhr, settings) {
     function getCookie(name) {
         var cookieValue = null;
         if (document.cookie && document.cookie != '') {
             var cookies = document.cookie.split(';');
             for (var i = 0; i < cookies.length; i++) {
                 var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
 });