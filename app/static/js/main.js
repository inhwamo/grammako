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
      console.log("Keywords:", data.keywords);
      console.log("Grammar errors:", data.grammar_errors);

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

      // POS Tagged (limited to first 10 items)
      if (data.pos_tagged && data.pos_tagged.length > 0) {
        resultHtml += "<td><h3>POS Tagged (first 10):</h3><ul>";
        data.pos_tagged.slice(0, 10).forEach((item) => {
          resultHtml += `<li>${item[0]} - ${item[1]}</li>`;
        });
        resultHtml += "</ul></td>";
      }

      // Simplified POS Tagged (limited to first 10 items)
      if (data.simplified_pos_tagged && data.simplified_pos_tagged.length > 0) {
        resultHtml += "<td><h3>Parts of Speech (first 10):</h3><ul>";
        data.simplified_pos_tagged.slice(0, 10).forEach((item) => {
          resultHtml += `<li>${item[0]} - ${item[1]}</li>`;
        });
        resultHtml += "</ul></td>";
      }

      // Nouns (limited to first 10 items)
      if (data.nouns && data.nouns.length > 0) {
        resultHtml += "<td><h3>Nouns (first 10):</h3><ul>";
        data.nouns.slice(0, 10).forEach((noun) => {
          resultHtml += `<li>${noun}</li>`;
        });
        resultHtml += "</ul></td>";
      }

      // Morphemes (limited to first 10 items)
      if (data.morphs && data.morphs.length > 0) {
        resultHtml += "<td><h3>Morphemes (first 10):</h3><ul>";
        data.morphs.slice(0, 10).forEach((morph) => {
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

function highlightText(text, posTagged, keywords) {
  console.log("Highlighting text...");
  let highlightedText = text;
  const colors = {
    Noun: "#FFB3BA",
    Verb: "#BAFFC9",
    Adjective: "#BAE1FF",
    Adverb: "#FFFFBA",
    Particle: "#FFD700",
    Ending: "#DDA0DD",
    Unknown: "#FFFFFF",
  };

  // Function to escape special characters in a string for use in a regular expression
  function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  // Sort posTagged by word length (descending) to ensure longer words are processed first
  posTagged.sort((a, b) => b[0].length - a[0].length);

  // Highlight POS tags
  posTagged.forEach(([word, tag]) => {
    const color = colors[tag] || colors.Unknown;
    const escapedWord = escapeRegExp(word);
    const regex = new RegExp(`(${escapedWord})(?![^<]*>|[^<>]*</)`, "g");
    highlightedText = highlightedText.replace(
      regex,
      `<span style="background-color: ${color};" title="${tag}">$1</span>`
    );
  });

  // Highlight top keyword
  if (keywords.length > 0) {
    const topKeyword = keywords[0][0];
    const escapedTopKeyword = escapeRegExp(topKeyword);
    const regex = new RegExp(`(${escapedTopKeyword})(?![^<]*>|[^<>]*</)`, "g");
    highlightedText = highlightedText.replace(
      regex,
      `<span style="border-bottom: 2px solid red;" title="Top Keyword">$1</span>`
    );
  }

  document.getElementById("highlighted-text").innerHTML = highlightedText;
}
