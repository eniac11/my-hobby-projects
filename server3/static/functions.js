// Global variables
var mouseX = 0;
var mouseY = 0;

// Sets callback pointers for mousehover and mousemove, for function references on function tag.
function SetFunctionTagCallbacks()
{    
    // Callback that ensures that the div will show when the user hoves over the reference
    $('.reference').hoverIntent(function(e) {
        $('div#hover').fadeIn(250)
          .css('top', mouseY + CalculateOffset(e, false))
          .css('left', mouseX + CalculateOffset(e, true))
          .appendTo('body');
      }, function() 
      {
        $('div#hover').hide();
      });

    // Callback to make sure the div stays close to the mouse
    $('.reference').mousemove(function(e) {
    console.log("mousemove");
        mouseX = e.pageX;
        mouseY = e.pageY;
        var posX = e.pageX + CalculateOffset(e, true);
        var posY = e.pageY + CalculateOffset(e, false);
        $("div#hover").css('top', posY).css('left', posX);          
    });
      
    // Callback that loads the content via ajax in the div
    $('.reference').mouseenter(function(e) {
    console.log("mouseenter");
        $('div#hover').hide();
        $('div#hover').html('');
        var id = ($(this).attr('data'));
        console.log(id);
        var data = document.getElementById(id).innerHTML;
        console.log(data);
        $('div#hover').html(data);

    });      
    // Ensures that if the user accidentilly enters the hover div, it's still able to hide it by removing the mouse from this div
    $('div#hover').mouseleave(function(e) {
        $(this).hide();
    });
}
