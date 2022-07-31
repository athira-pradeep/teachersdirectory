console.log("JSSSSS")
const form = document.getElementById('form')

const first_name = document.getElementById('id_firstname')
const last_name = document.getElementById('id_lastname')
const email = document.getElementById('id_email')
const phone = document.getElementById('id_phone')
const roomno = document.getElementById('id_roomno')
const subject = document.getElementById('id_subjects')
const image = document.getElementById('id_profile_pic')
const csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value
console.log("**************")
console.log(form)

const url = "{% url 'create_teachers' %}"

form.addEventListener('submit',e=>{
    e.preventDefault()
    console.log("SUBMIT")
    console.log(csrftoken,first_name.value)
    var fd = new FormData()
    fd.append('csrftoken',csrftoken)
//    fd.append('firstname',first_name.value)
//    fd.append('lastname',last_name.value)
//    fd.append('email',email.value)
//    fd.append('phone',phone.value)
//    fd.append('subject',subject.value)
//    fd.append('image',image.files[0])
    console.log(fd)
    $.ajax({
        type: 'POST',
        url: "{% url 'create_teachers' %}",
        data: $("#form")
        success: function(response){
            console.log(response)
        },
        error: function(error){
            console.log(error)
        },
        cache: false,
        contentType: false,
        processData: false,
    })
})


