document.getElementById("check-grammar").addEventListener("click", function () {
  const text = document.getElementById("input-text").value;
  console.log("Analyzing text:", text.substring(0, 50) + "...");
  fetch("/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: text }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Analysis completed");
      let resultHtml = "<h2>Analysis Results:</h2>";

      // Display original text with highlighting
      resultHtml += "<h3>Analyzed Text:</h3>";
      resultHtml += "<p id='highlighted-text'></p>";

      // Display chunks
      resultHtml += "<h3>Phrasal Chunks:</h3>";
      for (const [chunkType, chunks] of Object.entries(data.chunks)) {
        resultHtml += `<h4>${chunkType.replace("_", " ")}:</h4><ul>`;
        chunks.forEach((chunk) => {
          resultHtml += `<li>${chunk}</li>`;
        });
        resultHtml += "</ul>";
      }

      // ... (rest of your existing result display code)

      document.getElementById("results").innerHTML = resultHtml;

      highlightText(
        data.original_text,
        data.simplified_pos_tagged,
        data.keywords
      );
    })
    .catch((error) => {
      console.error("Error in analysis:", error.message);
      document.getElementById(
        "results"
      ).innerHTML = `<p style="color: red;">An error occurred during analysis.</p>`;
    });
});

// ... (rest of your JavaScript code)
