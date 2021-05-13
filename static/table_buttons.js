




let delete_btns = document.querySelectorAll(".deleteRow");
let update_btns = document.querySelectorAll(".updateRow");

delete_btns.forEach(btn => {
    btn.addEventListener('click', event => {
        $.post(window.location.pathname, {
            id:btn.id, 
            query_type:"DELETE"
        })    
    })
})

update_btns.forEach(btn => {
    btn.addEventListener('click', event => {
       $.post(window.location.pathname, {
               id:btn.id, 
               query_type:"UPDATE",
               url:window.location.pathname
       })      
    })
})
