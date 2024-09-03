document.getElementById("check-grammar").addEventListener("click", function () {
  const text = document.getElementById("input-text").value;
  console.log("Sending text for analysis:", text);
  fetch("/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: text }),
  })
    .then((response) => {
      console.log("Response status:", response.status);
      console.log("Response headers:", response.headers);
      return response.json();
    })
    .then((data) => {
      console.log("Parsed response data:", data);
      if (data.error) {
        throw new Error(data.error);
      }

      let resultHtml = "<h2>Analysis Results:</h2>";

      // Display top keywords
      if (data.keywords && data.keywords.length > 0) {
        resultHtml += "<h3>Top Keywords:</h3><ul>";
        data.keywords.forEach(([keyword, count]) => {
          resultHtml += `<li>${keyword} (${count})</li>`;
        });
        resultHtml += "</ul>";
      }

      // Display original text with highlighting
      resultHtml += "<h3>Analyzed Text:</h3>";
      resultHtml += "<p id='highlighted-text'></p>";

      // Create a table for POS Tagged, Simplified POS, Nouns, and Morphemes
      resultHtml += "<table><tr>";

      // POS Tagged
      if (data.pos_tagged && data.pos_tagged.length > 0) {
        resultHtml += "<td><h3>POS Tagged:</h3><ul>";
        data.pos_tagged.forEach((item) => {
          resultHtml += `<li>${item[0]} - ${item[1]}</li>`;
        });
        resultHtml += "</ul></td>";
      }

      // Simplified POS Tagged
      if (data.simplified_pos_tagged && data.simplified_pos_tagged.length > 0) {
        resultHtml += "<td><h3>Parts of Speech:</h3><ul>";
        data.simplified_pos_tagged.forEach((item) => {
          resultHtml += `<li>${item[0]} - ${item[1]}</li>`;
        });
        resultHtml += "</ul></td>";
      }

      // Nouns
      if (data.nouns && data.nouns.length > 0) {
        resultHtml += "<td><h3>Nouns:</h3><ul>";
        data.nouns.forEach((noun) => {
          resultHtml += `<li>${noun}</li>`;
        });
        resultHtml += "</ul></td>";
      }

      // Morphemes
      if (data.morphs && data.morphs.length > 0) {
        resultHtml += "<td><h3>Morphemes:</h3><ul>";
        data.morphs.forEach((morph) => {
          resultHtml += `<li>${morph}</li>`;
        });
        resultHtml += "</ul></td>";
      }

      resultHtml += "</tr></table>";

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

      // Add logging statement before calling highlightText
      console.log(
        "Calling highlightText with:",
        data.original_text,
        data.simplified_pos_tagged,
        data.keywords
      );
      highlightText(
        data.original_text,
        data.simplified_pos_tagged,
        data.keywords
      );
    })
    .catch((error) => {
      console.error("Error in fetch or processing:", error);
      let errorMessage = "An error occurred while analyzing the text.";
      if (error.message) {
        errorMessage += ` Details: ${error.message}`;
      }
      document.getElementById(
        "results"
      ).innerHTML = `<p style="color: red;">${errorMessage}</p>`;
    });
});
function highlightText(text, posTagged, keywords) {
  console.log("highlightText function called");
  console.log("Text length:", text.length);
  console.log("POS Tagged items:", posTagged.length);
  console.log("Keywords:", keywords.map((k) => k[0]).join(", "));

  let highlightedText = text;
  const colors = {
    Noun: "#FFB3BA",
    Verb: "#BAFFC9",
    Adjective: "#BAE1FF",
    Adverb: "#FFFFBA",
    Particle: "#FFD700",
    Ending: "#DDA0DD",
  };

  // Function to escape special characters in a string for use in a regular expression
  function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  let replacementsMade = 0;

  // Highlight POS tags
  posTagged.forEach(([word, tag], index) => {
    if (index < 5) console.log(`Processing: "${word}" (${tag})`);
    const color = colors[tag] || "#FFFFFF";
    const escapedWord = escapeRegExp(word);
    const regex = new RegExp(`${escapedWord}`, "g");
    const oldHighlightedText = highlightedText;
    highlightedText = highlightedText.replace(
      regex,
      `<span style="background-color: ${color};" title="${tag}">${word}</span>`
    );
    if (oldHighlightedText !== highlightedText) {
      replacementsMade++;
    }
  });

  console.log(`Total replacements made: ${replacementsMade}`);

  // Highlight top keyword
  if (keywords.length > 0) {
    const topKeyword = keywords[0][0];
    console.log(`Highlighting top keyword: "${topKeyword}"`);
    const escapedTopKeyword = escapeRegExp(topKeyword);
    const regex = new RegExp(`${escapedTopKeyword}`, "g");
    highlightedText = highlightedText.replace(
      regex,
      `<span style="border-bottom: 2px solid red;" title="Top Keyword">${topKeyword}</span>`
    );
  }

  console.log("Highlighted text length:", highlightedText.length);
  document.getElementById("highlighted-text").innerHTML = highlightedText;
}
