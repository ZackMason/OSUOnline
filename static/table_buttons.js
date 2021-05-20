




let delete_btns = document.querySelectorAll(".deleteRow");
let update_btns = document.querySelectorAll(".updateRow");

let exampleModal = document.getElementById('exampleModal');
let sbt_btn = document.getElementById('submit_id');

delete_btns.forEach(btn => {
    btn.addEventListener('click', event => {
        $.post(window.location.pathname, {
            id:btn.id, 
            query_type:"DELETE"
        })
        const Http = new XMLHttpRequest();
        const url = window.location.pathname;
        Http.open("GET", url);
        Http.send();

        Http.onreadystatechange = (e) => {
          location.reload()
        }
    })
})

sbt_btn.addEventListener('click', event => {
    fields = exampleModal.querySelectorAll('.upd_input');
        data = {}
        for (var i = 0; i < fields.length; i++)
        {
            data[fields[i].name] = (fields[i].value)
        }
        console.log(data)
       $.post(window.location.pathname, {
               id:sbt_btn.id,
               query_type:"UPDATE",
               data: JSON.stringify(data)
       })

       const Http = new XMLHttpRequest();
        const url = window.location.pathname;
        Http.open("GET", url);
        Http.send();

        Http.onreadystatechange = (e) => {
          location.reload()
        }
})


update_btns.forEach(btn => {
    btn.addEventListener('click', event => {
        let sbt_btn = document.getElementById('submit_id');
        sbt_btn.id = btn.id;
    })
})

if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
    } 
