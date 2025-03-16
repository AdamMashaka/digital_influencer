
function validateUsername() {
                            const usernameInput = document.getElementById('id_username');
                            const usernameError = document.getElementById('username-error');

                            const username = usernameInput.value.trim();
                            if (username.includes('@')) {
                                usernameError.textContent = 'Username cannot contain "@" symbol.';
                                usernameError.classList.add('show');
                            } else {
                                usernameError.textContent = '';
                                usernameError.classList.remove('show');
                            }
                        }


function validatePasswords() {
       const password1Input = document.getElementById('id_password1');
       const password2Input = document.getElementById('id_password2');
       const passwordError = document.getElementById('password2-error');

       const password1 = password1Input.value;
       const password2 = password2Input.value;
       if (password1 !== password2) {
           passwordError.textContent = 'Passwords do not match.';
       } else {
           passwordError.textContent = '';
       }
}
