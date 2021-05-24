let progressBar = document.getElementById("progress"),
  loadBtn = document.getElementById("button"),
  display = document.getElementById("display");

function upload(data) {
  let xhr = new XMLHttpRequest();
  xhr.open("POST", "http://127.0.0.1:5000/upload_image/", true);
  xhr.setRequestHeader("Access-Control-Allow-Methods", "POST");
  xhr.setRequestHeader("Transef-Encoding", "chunked");


  if (xhr.upload) {
    xhr.upload.onprogress = function(e) {
      if (e.lengthComputable) {
        progressBar.max = e.total;
        progressBar.value = e.loaded;
        display.innerText = Math.floor((e.loaded / e.total) * 100) + '%';
      }
    }
    xhr.upload.onloadstart = function(e) {
      progressBar.value = 0;
      display.innerText = '0%';
    }
    xhr.upload.onloadend = function(e) {
      progressBar.value = e.loaded;
      loadBtn.disabled = false;
      loadBtn.innerHTML = 'Start uploading';
    }
    xhr.onreadystatechange = function() {
    if (xhr.readyState == XMLHttpRequest.DONE) {
        console.log(xhr.responseText);
      }
    }
  }
  xhr.send(data);
}

loadBtn.addEventListener("click", function(e) {
  this.disabled = true;
  this.innerHTML = "Uploading...";
  let input_data = document.querySelector("#video");

  let fd = new FormData();

  fd.append("video", input_data.files[0]);
  upload(fd);
  });