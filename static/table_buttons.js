




let delete_btns = document.querySelectorAll(".deleteRow");
let update_btns = document.querySelectorAll(".updateRow");

delete_btns.forEach(btn => {
    btn.addEventListener('click', event => {
        alert("Deleting entity #" + btn.id + "......")
    })
})

update_btns.forEach(btn => {
    btn.addEventListener('click', event => {
        alert("Updating entity #" + btn.id + "......")
    })
})
