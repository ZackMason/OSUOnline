




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
        fields = document.querySelectorAll('.form_input');
        data = {}
        for (var i = 0; i < fields.length; i++)
        {
            data[fields[i].name] = (fields[i].value)
        }
        console.log(data)
            
       $.post(window.location.pathname, {
               id:btn.id, 
               query_type:"UPDATE",
               data: JSON.stringify(data)
       })      
    })
})
