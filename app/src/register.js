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

signBtn.addEventListener("click",test)
function test(){
    console.log("Test")
    check()
}