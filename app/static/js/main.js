document.getElementById("check-grammar").addEventListener("click", function () {
  const text = document.getElementById("input-text").value;
  fetch("/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: text }),
  })
    .then((response) => response.json())
    .then((data) => {
      let resultHtml = "<h2>Analysis Results:</h2>";
      resultHtml += "<h3>POS Tagged:</h3><ul>";
      data.pos_tagged.forEach((item) => {
        resultHtml += `<li>${item[0]} - ${item[1]}</li>`;
      });
      resultHtml += "</ul>";

      if (data.grammar_errors.length > 0) {
        resultHtml += "<h3>Grammar Errors:</h3><ul>";
        data.grammar_errors.forEach((error) => {
          resultHtml += `<li>${error}</li>`;
        });
        resultHtml += "</ul>";
      } else {
        resultHtml += "<p>No grammar errors detected.</p>";
      }

      document.getElementById("results").innerHTML = resultHtml;
    });
});
