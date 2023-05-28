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
  } else {
    // 로그인 실패 처리
    console.log("로그인에 실패하였습니다.");
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
