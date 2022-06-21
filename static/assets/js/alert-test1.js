// add event alert 
const toast = document.querySelector(".toast");
const closeIcon = document.querySelector(".close");
const progress = document.querySelector(".progress");
closeIcon.addEventListener("click", () =>{ 
    toast.classList.remove("active");
})

// if add event alert toast.classList.add("active"); progress.classList.add("active"); 