let userId = document.getElementById("userId");
let pw = document.getElementById("password");
let signBtn = document.getElementById("btn");

function requestPostBodyJson() {
  var reqURL = "http://127.0.0.1:8000/users/login/";
  var jsonData = {
    user_id: userId.value,
    password: pw.value,
  };
  $.ajax({
    url: "http://127.0.0.1:8000/users/login/",
    data: JSON.stringify(jsonData),
    type: "post",
    async: false,
    timeout: 5000,
    dataType: "JSON",
    contentType: "application/json; charset=utf-8",
    // success: function (data, textStatus, xhr) {
    //   if (data == "loginFail") {
    //     alert("로그인에 실패하였습니다.");
    //   } else {
    //     window.location.href = "index.html";
    //   }
    // }
  });
}

function test() {
  console.log(userId.value);
  console.log(pw.value);
}

signBtn.addEventListener("click", requestPostBodyJson);
