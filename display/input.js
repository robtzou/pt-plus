const fileInput = document.getElementById("fileInput");
const commandInput = document.getElementById("command");
const submitBtn = document.getElementById("submitBtn");
const outputArea = document.getElementById("output");

let extractedText = "";

fileInput.addEventListener("change", async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  if (file.name.endsWith(".pdf")) {
    extractedText = await extractPdfText(file);
  } else if (file.name.endsWith(".docx")) {
    extractedText = await extractDocxText(file);
  } else {
    alert("Unsupported file type.");
    return;
  }

  outputArea.value = extractedText;
});

submitBtn.addEventListener("click", async () => {
  const command = commandInput.value || "Summarize the document.";
  const response = await fetch("http://127.0.0.1:5000/summarize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: extractedText, command }),
  });

  const result = await response.json();
  outputArea.value = result.summary || result.error;
});

async function extractPdfText(file) {
  const arrayBuffer = await file.arrayBuffer();
  const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
  let text = '';
  for (let i = 1; i <= pdf.numPages; i++) {
    const page = await pdf.getPage(i);
    const content = await page.getTextContent();
    text += content.items.map(item => item.str).join(' ') + '\n';
  }
  return text;
}

async function extractDocxText(file) {
  const arrayBuffer = await file.arrayBuffer();
  const { value } = await window.mammoth.extractRawText({ arrayBuffer });
  return value;
}
