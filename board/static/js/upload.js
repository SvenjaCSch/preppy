const form = document.getElementById('upload-form');
const fileInput = document.getElementById('file-input');
const progressBar = document.getElementById('progress');

form.addEventListener('submit', e => {
  e.preventDefault();

  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append('file', file);

  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/upload', true);
  xhr.upload.onprogress = e => {
    if (e.lengthComputable) {
      const percentComplete = (e.loaded / e.total) * 100;
      progressBar.style.width = `${percentComplete}%`;
    }
  };
  xhr.send(formData);
});