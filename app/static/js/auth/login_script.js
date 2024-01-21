var formSubmitted = false;

function showLoading() {
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
