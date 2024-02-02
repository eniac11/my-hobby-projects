function updates() {
    let updates = fetch('/updates', {'method': 'POST'});
    updates.then((data) => {
        data.json().then((json) => {
            for (var i = 0; i < json.length; i++) {
                let macro = json[i];
                let identifier = macro.macro_identifier.control_id;
                console.log(identifier);
                let elem = document.getElementById(identifier);
                elem.value = macro.data;
            }
        });


    })
}