document.getElementById("check-grammar").addEventListener("click", function () {
  const text = document.getElementById("input-text").value;
  fetch("/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: text }),
  })
    .then((response) => {
      if (!response.ok) {
        return response.json().then((err) => {
          throw err;
        });
      }
      return response.json();
    })
    .then((data) => {
      let resultHtml = "<h2>Analysis Results:</h2>";

      // POS Tagged
      if (data.pos_tagged && data.pos_tagged.length > 0) {
        resultHtml += "<h3>POS Tagged:</h3><ul>";
        data.pos_tagged.forEach((item) => {
          resultHtml += `<li>${item[0]} - ${item[1]}</li>`;
        });
        resultHtml += "</ul>";
      }

      // Morphemes
      if (data.morphs && data.morphs.length > 0) {
        resultHtml += "<h3>Morphemes:</h3><ul>";
        data.morphs.forEach((morph) => {
          resultHtml += `<li>${morph}</li>`;
        });
        resultHtml += "</ul>";
      }

      // Nouns
      if (data.nouns && data.nouns.length > 0) {
        resultHtml += "<h3>Nouns:</h3><ul>";
        data.nouns.forEach((noun) => {
          resultHtml += `<li>${noun}</li>`;
        });
        resultHtml += "</ul>";
      }

      // Keywords
      if (data.keywords && data.keywords.length > 0) {
        resultHtml += "<h3>Top Keywords:</h3><ul>";
        data.keywords.forEach(([keyword, count]) => {
          resultHtml += `<li>${keyword} (${count})</li>`;
        });
        resultHtml += "</ul>";
      }

      // Sentence Structure
      if (data.sentence_structure && data.sentence_structure.length > 0) {
        resultHtml += "<h3>Sentence Structure:</h3><p>";
        resultHtml += data.sentence_structure.join(" - ");
        resultHtml += "</p>";
      }

      // Grammar Errors
      if (data.grammar_errors && data.grammar_errors.length > 0) {
        resultHtml += "<h3>Grammar Errors:</h3><ul>";
        data.grammar_errors.forEach((error) => {
          resultHtml += `<li>${error}</li>`;
        });
        resultHtml += "</ul>";
      } else {
        resultHtml += "<p>No grammar errors detected.</p>";
      }

      document.getElementById("results").innerHTML = resultHtml;
    })
    .catch((error) => {
      console.error("Error:", error);
      let errorMessage = "An error occurred while analyzing the text.";
      if (error.error) {
        errorMessage += ` Details: ${error.error}`;
      }
      if (error.traceback) {
        console.error("Traceback:", error.traceback);
      }
      document.getElementById(
        "results"
      ).innerHTML = `<p style="color: red;">${errorMessage}</p>`;
    });
});
