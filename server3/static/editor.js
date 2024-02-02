var timer = 0;
var delay = 200;
var prevent = false;
var editing;
var target_context_element;

async function close_editing() {

    await send_edit(editing.id)
    var elem = $(editing)
    elem.attr('contenteditable', false)
//    target.css('color', 'black')
    elem.blur()
    elem = null;
}

class EditorQuery {
    constructor(id, method, sentence, data) {
        this.id = id;
        this.sentence = sentence;
        this.method = method;
        this.data = data;
        this._resp = null;
    }

    async edit_request() {
        var resquet = await fetch('/editor', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({'id': this.id, 'method': 'edit', 'sentence':this.sentence, 'data': {}})})
        return resquet.text()
    }

    async history_request(resp) {
        if (resp === undefined){
            var resquet = await fetch('/editor', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({'id': this.id, 'method': 'history', 'sentence': '', 'data': this.data})})
            return resquet.text()
        }
    }


    async send() {
        if (this.method === "edit") {
            return this.edit_request()

        } else if (this.method == 'history') {
            return this.history_request()
        }
    }
}

async function send_edit(id) {
console.log(id)
    var elem = $('#'+id);
    var query = new EditorQuery(id, 'edit', elem.text(), {})
    query.send().then((text) => {
        elem.html(text)
    })

}

async function show_history() {
console.log(target_context_element[0])
    var id = target_context_element[0].id;
    var query = new EditorQuery(id, 'history', '', {})
    query.send().then((text) => {
        console.log(text)
        $('#history-modal .description').html(text)
        $('#history-modal')
          .modal('show');
    })

}



$(document).ready(async () => {
    $('.edit').click(async(evt) => {
        timer = setTimeout(async function() {

          if (!prevent) {
            var target = $(evt.target);
            editing = target[0];
            if (editing !== target[0] && editing != null) {
                await close_editing();
            }
            console.log(target)
            target.attr('contenteditable', true)
//            target.css('color', 'red');
            target.focus()


          }
          prevent = false;
        }, delay);

    }).dblclick((evt) => {
        clearTimeout(timer);
        prevent = true;

        evt.preventDefault()
        console.log(evt)
    })
    .bind('keydown', 'ctrl+return', async (evt) => {
        await close_editing()
    })

    // cache some selectors
    var $td;
    var $contextmenu = $('#context-menu');
    var $nameInput = $contextmenu.find("input").first();

    // initiate the context menu
    $contextmenu.menu({
        // allow context menu to open on td elements
        // otherwise, the default browser context menu will open
        targets: '.edit',

        // When it's shown, we capture the td which was chosen
        // and we put the current text into our input
        onShow: function (target) {
            target_context_element = $(target);
            return true
        },

        // by default any element with the "option" class will triger this
        // function when clicked
        // return false from here to prevent the contextmenu from hiding
        // this is a good place to handle updating things, which we only do here
        // if it was the positive button that was pressed
//        onSelect: function (selectedElement) {
//            target_context_element = $(selectedElement);
//        },

        // we're going to set the delay for how long you need to hold down/touch the tds before
        // the context menu opens.  1 seconds sounds good
        // you can also set touch: false to prevent opening by holding and only allow real contextmenu events
        delay: 1000
    });

    // We can also manually show it on an element
//    $('.new.button').click(function (event) {
//        var $thisButton = $(this);
//        var $td = $thisButton.parent();
//
//        // show the menu by telling it the element and location
//        // if you just tell it the element, it'll go to one side of the element
//        $contextmenu.menu("show", $td, event.pageX, event.pageY)
//    });
})

$(function () {

});