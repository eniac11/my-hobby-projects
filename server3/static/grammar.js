$(document).ready(() => {
var done = false;
var last_response_len = false;

//let stats = await fetch("/stats").then((response) => response.json())

//    console.log(stats)
//
//    let paragraphs = stats.paragraphs;
//    let chapters = stats.chapters;

//$(".ui.dimmer").dimmer("show");
//console.log($(".ui.dimmer .ui.progress"))
//setTimeout(() => {
//$prog1 = $("#prog1")
//$prog2 = $("#prog2")
//$prog1.progress({text: {active: "Chapters loaded {value} of {total}"}, total: chapters})
//$prog2.progress({text: {active: "Paragraphs loaded {value} of {total}"}, total: paragraphs[0]})
////$prog1.progress("increment")
////$prog1.progress()
////$prog1.progress({value:0})
////$prog2.progress("increment")
////$prog2.progress({value:0})
//}, 300)


    $.ajax('/lazy', {
            xhrFields: {
                onprogress: function(e)
                {
                    var this_response, response = e.currentTarget.response;

                    if(last_response_len === false)
                    {
                        this_response = response;
                        last_response_len = response.length;
                    }
                    else
                    {
                        this_response = response.substring(last_response_len);
                        last_response_len = response.length;
                    }
//                    console.log(this_response.includes(":done:"), this_response)
                    if (done === false)
                        done = this_response.includes(":done:")
                    if (this_response.includes(":done:")) {
                        $('#lazy').append(this_response.replace(":done:", ''))
                        return
                    }
                    if (done === false){
                        $('#lazy').append(this_response);
                        } else {
                        $('#data').append(this_response)
                        }
                }
            }
        })
        .done(() => {
            popup()
        })
        .fail(function(data)
        {
            console.log('Error: ', data);
        });
        console.log('Request Sent');

//    await fetch_("/lazy")


        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    toggleDarkMode()
}

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
    event.matches ? toggleDarkMode() : toggleLightMode();
});


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





})




function popup() {
var last_response_len = false;
$.ajax('/popup', {
            xhrFields: {
                onprogress: function(e)
                {
                    var this_response, response = e.currentTarget.response;

                    if(last_response_len === false)
                    {
                        this_response = response;
                        last_response_len = response.length;
                    }
                    else
                    {
                        this_response = response.substring(last_response_len);
                        last_response_len = response.length;
                    }

                        $('#data').append(this_response)
                }
            }
        })
        .done(() => {
        installCallbacks()
        })
        .fail(function(data)
        {
            console.log('Error: ', data);
        });
        console.log('Request Sent');
}

 function toggleDarkMode () {
    // add fomantic's inverted class to all ui elements
    $('body').find('.ui:not(.dimmer)').addClass('inverted');
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

  function installCallbacks() {
  $('u')
  .popup({
    popup: $('div#hover'),
    hoverable: true,
//     boundary: 'body'

  })
$('.error').mouseenter(function(e) {
//clearTimeout(timeout);
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
}
// mimic native fetch() instantiation and return Promise
// async function fetch_(input, init = {}) {
//    const request = (input instanceof Request)? input : new Request(input)
//
//    let stats = await fetch("/stats").then((response) => response.json())
//
//    console.log(stats)
//
//    let paragraphs = stats.paragraphs;
//    let chapters = stats.chapters;
//
//    var current_popup_index = 0;
//
//
//    console.log(chapters)
//
//    var current_chapter = 0;
//
//    var reader;
//
//    return
//    return fetch(request, init).then(response => {
//      if (!response.body) {
//        throw Error('ReadableStream is not yet supported in this browser.  <a href="https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream">More Info</a>')
//      }
//
//      let loaded = 0;
//
//      reader=response.body.getReader()
//
//      return new Response(
//        new ReadableStream({
//          start(controller) {
//
//            read();
//            function read() {
//              reader.read().then(({done, value}) => {
//                if (done) {
//                  // process chapter increment and paragraph
//
//                  controller.close();
//                  return;
//                }
//                controller.enqueue(value);
//                read();
//              }).catch(error => {
//                console.error(error);
//                controller.error(error)
//              });
//            }
//          }
//        })
//      )
//    });
//  }