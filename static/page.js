const CaptureBtn = document.querySelector("#capture-btn");

CaptureBtn.addEventListener("click", takePhoto);


function takePhoto() {
    fetch("/take-photo").then(resp => resp.json())
    .then(data => window.open(data.photoLocation.substring(1), "_blank"));
}