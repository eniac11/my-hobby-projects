// Calculates the horizontal or vertical offset to accomdate for different window sizes.
// Also ensures that if a location is above a certain treshold it will switch values (so html won't overflow out of the window)
function CalculateOffset(e, isHorizontal)
{
    var tresholdHor = 0.55;
    var tresholdVer = 0.45;
    var moveLeft = 20;
    var moveDown = 10;
    // Do horizontal offset calculations
    if(isHorizontal)
    {
        var windowWidth = window.innerWidth;
        var horPos = e.pageX / windowWidth;
        if(horPos > tresholdHor)
        {
            var hoverWidth = $('div#hover').width() ;
            moveLeft = -hoverWidth;
            return moveLeft;
        }
        else
            return moveLeft;
    }
    // Do vertical offset calculations
    if(!isHorizontal)
    {
        var windowHeight = window.innerHeight;
        // Offset the actual scrolling position from the pageY variable (gets actual window location instead of page location)
        var mouseY = e.pageY - $(window).scrollTop();
        var vertPos = mouseY / windowHeight;
        // $('div#hover').html(windowHeight + ' ' + mouseY); // Debug
        if(vertPos > tresholdVer)
        {
            var hoverHeight = $('div#hover').height();
            moveDown = -hoverHeight;
            return moveDown;
        }
        else
            return moveDown;
    }
}
function setupPopupCallbacks() {

var timeout = null;
$(document).on('mouseleave click', 'div#hover', function() {
//   $("div#hover").fadeOut(300);
})
$(document).on('mouseenter', 'div#hover', function() {
//  clearTimeout(timeout);

})

if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    toggleDarkMode()
}

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
    event.matches ? toggleDarkMode() : toggleLightMode();
});

$('.reference')
  .popup({
    popup: $('div#hover'),
    hoverable: true,
     boundary: 'body'

  })
$('u').popup();

$('.ui.sticky')
  .sticky()
;

$('.main.menu').visibility({
        type: 'fixed'
      });
      $('.mmenu').visibility({
        type: 'fixed',
        offset: 80
      });


if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {

  $(document).on('click', '.reference', function() {
  $('div#hover').hide();
        $('div#hover').html('');
        var id = ($(this).attr('data'));
//        console.log(id);
        var data = $('#'+id).innerHTML;
//        console.log(data);
        $('div#hover').html(data);
     var popupContent = $(this).parent('.popup-container').find('.popup-body');
     if (!popupContent.hasClass('show-popup')) {
       popupContent.addClass('show-popup');
     } else {
       popupContent.removeClass('show-popup');
     }
  })

  $(document).on('touchstart', '.page-content', function(e) {
    if ( !e.target.classList.contains(".popup-body") ) {
      $(".popup-body").removeClass('show-popup');
    }
  });

} else {

  $('.reference').mouseenter(function(e) {
clearTimeout(timeout);
//        $('div#hover').fadeIn(300)
//          .css('top', e.pageY + CalculateOffset(e, false))
//          .css('left', e.pageX + CalculateOffset(e, true)).show();
        $('div#hover').html('');
        var id = ($(this).attr('data'));
//        console.log(id);
        var data = document.getElementById(id).innerHTML;
//        console.log(data);
        $('div#hover').html(data);

  });
  $('.reference').mouseleave(function(e) {
  timeout = setTimeout(() => {
        $("div#hover").fadeOut(300);
      }, 2000);
  });
  }

  $('body div.text.container.ui').css()
}

 function toggleDarkMode () {
    // add fomantic's inverted class to all ui elements
    $('body').find('.ui').addClass('inverted');
    // add custom inverted class to body
    $('body').addClass('inverted');

    // simple toggle icon change
    $("#darkmode > i").removeClass('moon');
    $("#darkmode > i").addClass('sun');

    return;
  }

  function toggleLightMode() {
    // remove fomantic's inverted from all ui elements
    $('body').find('.ui').removeClass('inverted');
    // remove custom inverted class to body
    $('body').removeClass('inverted');

    // change button icon
    $("#darkmode > i").removeClass('sun')
    $("#darkmode > i").addClass('moon');

    return;
  }

