
const current_window_url = window.location.href
const searchForm = document.getElementById('search-form')
const searchInput = document.getElementById('search-text')
const resultBox = document.getElementById('result-box')
const csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value
const tableOuptput = document.querySelector(".table-search-output")
const tableBody = document.querySelector(".table-body")
const tableAppList = document.querySelector(".table-app-list")
tableOuptput.style.display = "none"

const sendSearchData = (lastname) =>{
    tableBody.innerHTML = ""
    $.ajax({
        type: 'POST',
        url: "/search_results/",
        data: {
            'csrfmiddlewaretoken': csrf_token,
            'lastname': lastname,
        },
        success:(res)=>{
            console.log("success")
            const data = res.data
            tableOuptput.style.display = 'block'
            tableAppList.style.display = 'none'

            if(Array.isArray(data)){
                console.log("Is an array")
                data.forEach((data) => {
                    console.log(data)
                    tableBody.innerHTML +=`
                        <tr>
                            <td>${data.fname}</td>
                            <td>${ data.lname }</td>
                            <td>${data.email}</td>
                            <td>${data.phone }</td>
                            <td>${data.roomno }</td>
                            <td>${data.subject }</td>
                        </tr>
                    `
                })
            }
            else{
                console.log("Not array")
                tableOuptput.innerHTML = "No Results Found"
            }
        },
        error: (err)=>{
            console.log("error")
            console.log(err)
        }

    })
}

searchInput.addEventListener('keyup',e=>{
    console.log(e.target.value)
    if(resultBox.classList.contains('not-visible')){
        resultBox.classList.remove('not-visible')
    }
    sendSearchData(e.target.value)
})