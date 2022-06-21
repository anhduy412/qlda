const btnEditProfile = document.querySelector('#btn-edit-profile');
const inputUsername = document.querySelector('#input-username');
const inputEmail = document.querySelector('#input-email');
const inputFullName = document.querySelector('#input-fullname');
const inputPhoneNumber = document.querySelector('#input-phonenumber');
const inputGender = document.querySelector('#gender');
const inputTeam = document.querySelector('#team');
const inputPosition = document.querySelector('#position');
// const btnSaveEditProfile = document.querySelector('#btn-save-edit-profile');
const btnEditProfileDiv = document.querySelector('.btn-edit-profile-div-footer');

btnEditProfile.addEventListener('click',() =>{
    inputUsername.readOnly = true;
    inputEmail.readOnly = false;
    inputFullName.readOnly = false;
    inputPhoneNumber.readOnly = false;
    inputTeam.disabled = false;
    inputPosition.disabled = false;
    inputGender.disabled = false;
    btnEditProfileDiv.innerHTML = '<button id="btn-save-edit-profile" class="btn btn-neutral">Lưu sự thay đổi </button>';
})
btnSaveEditProfile.addEventListener('click',() => {
    inputUsername.readOnly = true;
    inputEmail.readOnly = true;
    inputFullName.readOnly = true;
    inputPhoneNumber.readOnly = true;
    inputTeam.disabled = true;
    inputPosition.disabled = true;
    inputGender.disabled = true;
    btnSaveEditProfile.remove();
})