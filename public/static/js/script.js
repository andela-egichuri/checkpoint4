$(document).ready(function(){
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });

    getHeight()

    document.getElementsByTagName("BODY")[0].onresize = function() {getHeight()};

    $('#effectsholder').carousel({
      interval: false
  })

    $('.carousel .item').each(function(){
        var next = $(this);
        var last;
        for (var i=0;i<5;i++) {
            next=next.next();
            if (!next.length) {
                next = $(this).siblings(':first');
            }

            last=next.children(':first-child').clone().appendTo($(this));
        }
        last.addClass('rightest');

    });

    $("#effectsholder a").click(function () {
        console.log($(this))
        $.ajax({
          method: "POST",
          url: "../image/edit/",
          data: { effect: "rotate", id:'31'}
      })
        .done(function( msg ) {
            console.log(msg)
        });
    });

});

function getHeight() {
    var vHeight = $(window).height();
    h = 0.9 * (vHeight)
    $('#content').css({"max-height":h });

}

function loadpic(name, id) {
    var vHeight = $(window).height();
    h = 0.7 * (vHeight - 100)
    var img = $("<img />").attr('src', '{{ STATIC_URL }}' + name)
    $(img).load(function(){
        $("#picholder").empty().append(img);
        $("#picholder img").addClass("thumbnail img-responsive");
        $("#wrapper").toggleClass("toggled");
    }).error(function () {
        $("#picholder").empty().append('Error Loading Image');
    }).attr({
        id: 'myimage',
    }).css({"max-height": h + 'px'})
    console.log(id )
}

// function editpic(pic) {
//     $.ajax({
//       method: "POST",
//       url: "image/edit/",
//       data: { effect: "rotate", id:'31'}
//   })
//     .done(function( msg ) {
//         alert( "Data Saved: " + msg );
//     });

// }

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