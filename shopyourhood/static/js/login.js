window.onload = function () {
    console.log("✅ JavaScript file loaded successfully!");

    // Wait for a short delay to ensure elements are available
    setTimeout(() => {
        let usernameField = document.querySelector("input[name='username']");
        let passwordField = document.querySelector("input[name='password']");
        let rememberMeCheckbox = document.querySelector("input[name='remember_me']");

        if (usernameField && passwordField && rememberMeCheckbox) {
            console.log("✅ Form fields found!");

            let username = localStorage.getItem("username") || "";
            let password = localStorage.getItem("password") || "";
            let rememberMe = localStorage.getItem("remember_me") === "true";

            console.log("🔹 Stored Username:", username);
            console.log("🔹 Stored Password:", password ? "******" : "No password saved");
            console.log("🔹 Remember Me:", rememberMe);

            if (rememberMe) {
                usernameField.value = username;
                passwordField.value = password;
                rememberMeCheckbox.checked = true;
                console.log("✅ Autofill applied!");
            }
        } else {
            console.error("❌ Form elements not found! Check your HTML.");
        }
    }, 500); // Small delay to wait for Django-rendered elements
};

// Save credentials to localStorage on form submission
document.addEventListener("submit", function (event) {
    let usernameField = document.querySelector("input[name='username']");
    let passwordField = document.querySelector("input[name='password']");
    let rememberMeCheckbox = document.querySelector("input[name='remember_me']");

    if (usernameField && passwordField && rememberMeCheckbox) {
        if (rememberMeCheckbox.checked) {
            localStorage.setItem("username", usernameField.value);
            localStorage.setItem("password", passwordField.value);
            localStorage.setItem("remember_me", "true");
            console.log("✅ Credentials saved in localStorage!");
        } else {
            localStorage.removeItem("username");
            localStorage.removeItem("password");
            localStorage.removeItem("remember_me");
            console.log("🗑️ Credentials removed from localStorage!");
        }
    }
});


// ✅ Handle logout and clear LocalStorage if necessary
function customLogout() {
    fetch("/logout/", { method: "GET" })  // Call Django logout view
        .then(response => response.json())
        .then(data => {
            console.log("🔹 Logout response:", data);
            if (!data.remember_me) {
                localStorage.clear();
                console.log("🗑️ LocalStorage cleared on logout!");
            }
            window.location.href = "/login/";  // Redirect to login page
        })
        .catch(error => console.error("❌ Logout Error:", error));
}