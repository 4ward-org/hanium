const btn = document.getElementById("btn");

function handleLogin(response) {
  if (response.status === 200) {
    const token = response.data.token;
    const name = response.data.name;

    // 토큰과 이름을 사용하여 추가적인 통신 또는 작업을 수행합니다.
    // 예시: 로그인 성공 시 다른 API 호출
    // 예시: 사용자 정보 저장
  
    // 페이지 이동 등 로직을 수행합니다.
    window.location.replace("http://localhost:5173/index.html"); // 대시보드 페이지로 이동
  }else{
    console.log("에러")
  }
}

function login() {
  const userId = document.getElementById("userId").value;
  const password = document.getElementById("password").value;

  const jsonData = JSON.stringify({
    user_id: userId,
    password: password,
  });

  // AJAX 요청
  $.ajax({
    url: "http://127.0.0.1:8000/users/login/",
    type: "POST",
    dataType: "json",
    contentType: "application/json; charset=utf-8",
    data: jsonData,
    success: handleLogin,
    error: function (xhr, textStatus, error) {
      console.log(xhr.responseText);
    },
  });
}

btn.addEventListener("click", login);

// let userId = document.getElementById("userId");
// let pw = document.getElementById("password");
// let signBtn = document.getElementById("btn");

// function requestPostBodyJson() {
//   var reqURL = "http://127.0.0.1:8000/users/login/";
//   var jsonData = {
//     user_id: userId.value,
//     password: pw.value,
//   };
//   $.ajax({
//     url: "http://127.0.0.1:8000/users/login/",
//     data: JSON.stringify(jsonData),
//     type: "post",
//     async: false,
//     timeout: 5000,
//     dataType: "JSON",
//     contentType: "application/json",
//     // success: function (data, textStatus, xhr) {
//     //   if (data == "loginFail") {
//     //     alert("로그인에 실패하였습니다.");
//     //   } else {
//     //     window.location.href = "index.html";
//     //   }
//     // }
//     success: function (response) {
//         if (response['result'] == 'success') {
//             $.cookie('token', response['token.key'], {path: '/'});
//             window.location.replace("/")
//         } else {
//             alert(response['msg'])
//         }
//     }
//   });
// }

// function test() {
//   console.log(userId.value);
//   console.log(pw.value);
// }

// signBtn.addEventListener("click", requestPostBodyJson);