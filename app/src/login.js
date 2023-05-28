const btn = document.getElementById("btn");
const userId = document.getElementById("userId");
const password = document.getElementById("password");

function handleLogin(response) {
  if (response.result === "success") {
    const token = response.data.token // 로그인 회원 토큰 정보 저장
    const name = response.data.name // 로그인 회원 유저네임 저장
    window.location.replace("http://localhost:5173/index.html"); // 메인 페이지로 이동
    console.log(response);
  } else {
    alert("회원정보가 없습니다.");
  }
}
//로그인 기능
function login() {
  const jsonData = JSON.stringify({
    user_id: userId.value,
    password: password.value,
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

// 로그인 버튼 클릭
btn.addEventListener("click", login);
