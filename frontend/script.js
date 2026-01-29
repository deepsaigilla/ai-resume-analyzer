let selectedFile = null;

const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("resume");
const fileName = document.getElementById("file-name");

dropArea.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropArea.classList.add("dragover");
});

dropArea.addEventListener("dragleave", () => {
  dropArea.classList.remove("dragover");
});

dropArea.addEventListener("drop", (e) => {
  e.preventDefault();
  dropArea.classList.remove("dragover");

  selectedFile = e.dataTransfer.files[0];
  fileInput.files = e.dataTransfer.files;
  fileName.textContent = selectedFile.name;
});

fileInput.addEventListener("change", () => {
  selectedFile = fileInput.files[0];
  fileName.textContent = selectedFile.name;
});

function analyze() {
  const jd = document.getElementById("jd").value;
  const resultDiv = document.getElementById("result");

  if (!selectedFile || !jd) {
    alert("Please upload a resume and paste job description.");
    return;
  }

  resultDiv.innerHTML = "<p class='loading'>Analyzing resume using AI...</p>";

  let formData = new FormData();
  formData.append("resume", selectedFile);
  formData.append("job_description", jd);

  fetch("http://127.0.0.1:5000/analyze", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => {
  resultDiv.innerHTML = `
    <div class="result-card">
      <h3>Match Score: ${data.match_percentage}%</h3>
      <pre>${data.ai_suggestions}</pre>
    </div>
  `;
})
  .catch(() => {
    resultDiv.innerHTML =
      "<p style='color:red;'>Something went wrong. Try again.</p>";
  });
}
