let search_bar = document.getElementsByClassName("form-control form-control-dark w-100")[0];

var rows = [...document.querySelectorAll('tr')]
rows.shift()

search_bar.addEventListener('input', e => {
    let search_term = e.target.value
    rows.forEach(row => {
        if(row.innerHTML.indexOf(search_term) != -1)
        {
            row.style.display = 'table-row';
        }
        else
        {
            row.style.display = 'none';
        }
    })
})