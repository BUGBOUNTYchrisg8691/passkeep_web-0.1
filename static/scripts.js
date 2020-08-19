function showPassword() {
    const pwDiv = document.getElementById("password");
    if (pwDiv.style.display === "none") {
        pwDiv.style.display = "block";
    } else {
        pwDiv.style.display = "none";
    }

    const button = document.getElementsByTagName("BUTTON")[0];
    if (pwDiv.style.display === 'none') {
        button.innerHTML = 'Show Password';
    } else {
        button.innerHTML = 'Hide Password';
    }
}

function submit() {
    const form = document.getElementById('serviceForm')
    form.submit()
}