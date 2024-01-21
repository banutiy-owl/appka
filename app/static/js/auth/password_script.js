function validateAndSubmit() {
  var password = getPassword();
  if (password.trim() === "") {
    document.getElementById("warning-message").innerText =
      "Password cannot be empty";
    return false;
  }

  if (!formSubmitted) {
    formSubmitted = true;
    document.getElementById("submit-button").setAttribute("disabled", "true");
    document.getElementById("loading-spinner").style.display = "block";
    setTimeout(function () {
      hideLoading();
    }, 5000);
    return true;
  } else {
    return false;
  }
}

function hideLoading() {
  document.getElementById("loading-spinner").style.display = "none";
}

function getPassword() {
  var password = "";
  for (var i = 0; i < 16; i++) {
    var input = document.getElementsByName("password" + i)[0];
    password += input.value || "";
  }
  return password;
}

function clearPasswordInputs() {
  var passwordInputs = document.querySelectorAll('input[type="password"]');

  passwordInputs.forEach(function (input) {
    input.value = "";
  });
}
