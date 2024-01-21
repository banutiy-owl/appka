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

function resetFieldWarning(fieldName, inputId) {
  var warningRequiredElement = document.getElementById(
    fieldName + "-required-warning"
  );
  var warningExistsElement = document.getElementById(
    fieldName + "-exists-warning"
  );
  var inputElement = document.getElementById(inputId);

  if (warningRequiredElement && inputElement && warningExistsElement) {
    warningRequiredElement.innerText = "";
    warningExistsElement.innerText = "";
    inputElement.style.border = "1px solid #ccc";
  }
}

function resetPasswordWarning() {
  var passwordInputs = document.querySelectorAll('input[name^="password"]');
  passwordInputs.forEach(function (passwordInput) {
    passwordInput.style.border = "1px solid #ccc";
  });
  document.getElementById("password-required-warning").innerText = "";
}

function validateCardNumber() {
  var cardNumberInput = document.getElementById("card_number");
  cardNumberInput.value = cardNumberInput.value.replace(/[^0-9]/g, "");
}

function updatePasswordStrength() {
  var passwordInputs = document.querySelectorAll('input[name^="password"]');
  var password = "";

  passwordInputs.forEach(function (passwordInput) {
    password += passwordInput.value || "";
  });

  var strength = getPasswordStrength(password);
  displayPasswordStrength(strength);
}

function getPasswordStrength(password) {
  var uppercaseStrength = /[A-Z]/.test(password) ? 1 : 0;
  var lowercaseStrength = /[a-z]/.test(password) ? 1 : 0;
  var numberStrength = /\d/.test(password) ? 1 : 0;
  var specialCharStrength = /[!@#$%^&*(),.?":{}|<>]/.test(password) ? 1 : 0;

  var totalStrength =
    uppercaseStrength +
    lowercaseStrength +
    numberStrength +
    specialCharStrength;

  if (password.length < 8) {
    return 0;
  }

  if (totalStrength >= 3) {
    return 2; // silny
  } else if (totalStrength >= 1) {
    return 1; // sredni
  } else {
    return 0; // slaby
  }
}

function displayPasswordStrength(strength) {
  var indicator = document.getElementById("password-strength-indicator");
  var strengthText = "";

  switch (strength) {
    case 0:
      strengthText = "Weak";
      break;
    case 1:
      strengthText = "Medium";
      break;
    case 2:
      strengthText = "Strong";
      break;
    default:
      strengthText = "";
  }

  indicator.innerText = strengthText;
  indicator.style.backgroundColor = getStrengthColor(strength);
  indicator.style.width = "60px";
  indicator.style.borderRadius = "5px";
}

function getStrengthColor(strength) {
  switch (strength) {
    case 0:
      return "red";
    case 1:
      return "yellow";
    case 2:
      return "green";
    default:
      return "transparent";
  }
}

function validateUsername() {
  var usernameInput = document.getElementById("username");
  var username = usernameInput.value.trim();

  var isValid = /^[a-zA-Z0-9_]{3,20}$/.test(username);

  var warningElem = document.getElementById("username-warning");
  var requiredWarningElem = document.getElementById(
    "username-required-warning"
  );

  if (!username) {
    warningElem.innerHTML = "";
    requiredWarningElem.innerHTML = "Username is required.";
  } else if (!isValid) {
    warningElem.innerHTML =
      "Invalid characters or length. Use 3-20 alphanumeric characters and underscores.";
    requiredWarningElem.innerHTML = "";
  } else {
    warningElem.innerHTML = "";
    requiredWarningElem.innerHTML = "";
  }
}

function validateDocumentId() {
  var documentIdInput = document.getElementById("document_id");
  var documentId = documentIdInput.value.trim();

  var isValid = /^[A-Z0-9_]+$/.test(documentId);

  var warningElem = document.getElementById("document-id-warning");
  var requiredWarningElem = document.getElementById(
    "document-id-required-warning"
  );

  if (!documentId) {
    warningElem.innerHTML = "";
    requiredWarningElem.innerHTML = "Document ID is required.";
  } else if (!isValid) {
    warningElem.innerHTML = "Invalid characters.";
    requiredWarningElem.innerHTML = "";
  } else {
    warningElem.innerHTML = "";
    requiredWarningElem.innerHTML = "";
  }
}
