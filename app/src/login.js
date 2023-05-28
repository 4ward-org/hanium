const btn = document.getElementById("btn");
const userId = document.getElementById("userId");
const password = document.getElementById("password");

function handleLogin(response) {
  if (response.result === "success") {
    // 토큰과 이름을 사용하여 추가적인 통신 또는 작업을 수행합니다.
    // 예시: 로그인 성공 시 다른 API 호출
    // 예시: 사용자 정보 저장
    const token = response.data.token;
    const name = response.data.name;
    // 페이지 이동 등 로직을 수행합니다.
    window.location.replace("http://localhost:5173/index.html");
    // 대시보드 페이지로 이동
    console.log(response);
  } else {
    alert("로그인 정보가 일치하지 않습니다.");
  }
}
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

btn.addEventListener("click", login);
