const btnEditProfile = document.querySelector('#btn-edit-profile');
const inputUsername = document.querySelector('#input-username');
const inputEmail = document.querySelector('#input-email');
const inputFirstName = document.querySelector('#input-first-name');
const inputLastName = document.querySelector('#input-last-name');
const inputTeam = document.querySelector('#input-team');
const inputPosition = document.querySelector('#input-position');
const btnSaveEditProfile = document.querySelector('#btn-save-edit-profile');
const btnEditProfileDiv = document.querySelector('#btn-edit-profile');
btnEditProfile.addEventListener('click',() =>{
    inputUsername.readOnly = false;
    inputEmail.readOnly = false;
    inputFirstName.readOnly = false;
    inputLastName.readOnly = false;
    inputTeam.readOnly = true;
    inputPosition.readOnly = true;
    btnEditProfileDiv.style.display = 'block';
})
btnSaveEditProfile.addEventListener('click',() => {
    inputUsername.readOnly = true;
    inputEmail.readOnly = true;
    inputFirstName.readOnly = true;
    inputLastName.readOnly = true;
    inputTeam.readOnly = true;
    inputPosition.readOnly = true;
    btnEditProfileDiv.style.display = 'none';
})