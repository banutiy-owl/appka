var existingValues = {
  username: [],
  card_number: [],
  document_id: [],
};

function checkIfExists(field, value) {
  return existingValues[field].includes(value);
}

function fetchExistingValues() {
  fetch("/get_existing_values")
    .then((response) => response.json())
    .then((data) => {
      existingValues = data;
    })
    .catch((error) => {
      console.error("Error fetching existing values:", error);
    });
}

fetchExistingValues();

function validateForm() {
  var warningElements = document.querySelectorAll(".warning-message");
  warningElements.forEach(function (element) {
    element.innerText = "";
  });

  var inputElements = document.querySelectorAll("input[required]");
  inputElements.forEach(function (input) {
    input.style.border = "1px solid #ccc";
  });

  var isValid = true;

  var username = document.getElementById("username").value.trim();
  if (username === "") {
    document.getElementById("username-required-warning").innerText =
      "Username is required.";
    document.getElementById("username").style.border = "1px solid red";
    isValid = false;
  }

  var password = "";
  var passwordInputs = document.querySelectorAll('input[name^="password"]');
  passwordInputs.forEach(function (passwordInput) {
    password += passwordInput.value || "";
  });

  if (password === "") {
    document.getElementById("password-required-warning").innerText =
      "Password is required.";
    passwordInputs.forEach(function (passwordInput) {
      passwordInput.style.border = "1px solid red";
    });
    isValid = false;
  } else if (password.length < 8 || password.length > 16) {
    document.getElementById("password-warning").innerText =
      "Password must be between 8 and 16 characters.";
    isValid = false;
  }

  var documentId = document.getElementById("document_id").value.trim();
  if (documentId === "") {
    document.getElementById("document-id-required-warning").innerText =
      "Document ID is required.";
    document.getElementById("document_id").style.border = "1px solid red";
    isValid = false;
  }

  var cardNumber = document.getElementById("card_number").value.trim();
  if (cardNumber === "") {
    document.getElementById("card-number-required-warning").innerText =
      "Card Number is required.";
    document.getElementById("card_number").style.border = "1px solid red";
    isValid = false;
  }

  var isExistValid = true;

  var usernameExists = checkIfExists(
    "username",
    document.getElementById("username").value
  );
  var cardNumberExists = checkIfExists(
    "card_number",
    document.getElementById("card_number").value
  );
  var documentIdExists = checkIfExists(
    "document_id",
    document.getElementById("document_id").value
  );

  if (usernameExists) {
    document.getElementById("username-exists-warning").innerText =
      "Username is already taken.";
  } else {
    document.getElementById("username-exists-warning").innerText = "";
    document.getElementById("registration-error").innerText = "";
  }

  if (cardNumberExists) {
    document.getElementById("card-number-exists-warning").innerText =
      "Card with this number already exists.";
  } else {
    document.getElementById("card-number-exists-warning").innerText = "";
    document.getElementById("registration-error").innerText = "";
  }

  if (documentIdExists) {
    document.getElementById("document-id-exists-warning").innerText =
      "User with this document ID already exists.";
  } else {
    document.getElementById("document-id-exists-warning").innerText = "";
    document.getElementById("registration-error").innerText = "";
  }

  if (usernameExists || cardNumberExists || documentIdExists) {
    document.getElementById("registration-error").innerText =
      "Please choose different values for the highlighted fields.";
    isExistValid = false;
    return;
  }

  if (isValid && isExistValid) {
    document.querySelector("form").submit();
  }
}

document
  .getElementById("register_button")
  .addEventListener("click", validateForm);
