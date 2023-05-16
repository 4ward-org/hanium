let userId = document.getElementById("user-id")
let userName = document.getElementById("user-name")
let pw = document.getElementById("pw")
let pwCheck = document.getElementById("pw-check")
let email = document.getElementById("email")
let address = document.getElementById("address")
let phone = document.getElementById("phone")
let gender = document.getElementById("gender")
let birth = document.getElementById("birth")

let signBtn = document.getElementById("sign-in")

function check(){
if(pw.value != pwCheck.value){
    alert("동일한 비밀번호를 입력해주세요.")
}
}


function requestPostBodyJson(){
    console.log("")
    console.log('122')
    console.log("[requestPostBodyJson] : [start]")

    var reqURL ="http://127.0.0.1:8000/users/register/"
    var jsonData = {
        "user_id" : userId.value,
        "name" : userName.value,
        "password" : pw.value,
        "password2" : pwCheck.value,
        "gender" : gender.value,
        "phone_number" : phone.value,
        "address" : address.value,
        "birth" : birth.value,
        "email" : email.value,
    }
    $.ajax({
        url: "http://127.0.0.1:8000/users/register/",
        data : JSON.stringify(jsonData),
        type : "post",
        async : false,
        timeout : 5000,
        dataType: "JSON",
        contentType : "application/json; charset=utf-8"
    })
}
signBtn.addEventListener("click",requestPostBodyJson)


