import React, { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [results, setResults] = useState(null);

  const handleAnalyze = async () => {
    console.log("Analyzing text:", text.substring(0, 50) + "...");
    try {
      const response = await fetch("/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });
      const data = await response.json();
      console.log("Analysis completed");
      console.log("Keywords:", data.keywords);
      console.log("Grammar errors:", data.grammar_errors);
      setResults(data);
    } catch (error) {
      console.error("Error in analysis:", error.message);
      setResults({ error: "An error occurred during analysis." });
    }
  };

  const handleClear = () => {
    setText("");
    setResults(null);
  };

  const highlightText = (text, posTagged, keywords) => {
    console.log("Highlighting text...");
    let highlightedText = text;
    const colors = {
      Noun: "#FFCCCB",
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
      const regex = new RegExp(
        `(${escapedTopKeyword})(?![^<]*>|[^<>]*</)`,
        "g"
      );
      highlightedText = highlightedText.replace(
        regex,
        `<span style="border-bottom: 2px solid red;" title="Top Keyword">$1</span>`
      );
    }

    return highlightedText;
  };

  const renderResults = () => {
    if (!results) return null;

    if (results.error) {
      return <p style={{ color: "red" }}>{results.error}</p>;
    }

    return (
      <div>
        <h2>Analysis Results:</h2>
        {/* Render keywords */}
        {results.keywords && results.keywords.length > 0 && (
          <div>
            <h3>Top Keywords:</h3>
            <ul>
              {results.keywords.map(([keyword, count], index) => (
                <li key={index}>
                  {keyword} ({count})
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Render highlighted text */}
        <h3>Analyzed Text:</h3>
        <p
          id="highlighted-text"
          dangerouslySetInnerHTML={{
            __html: highlightText(
              results.original_text,
              results.simplified_pos_tagged,
              results.keywords
            ),
          }}
        ></p>

        {/* Render POS Tagged, Simplified POS, Nouns, and Morphemes */}
        <table>
          <tbody>
            <tr>
              {/* Render POS Tagged */}
              {results.pos_tagged && results.pos_tagged.length > 0 && (
                <td>
                  <h3>POS Tagged (first 10):</h3>
                  <ul>
                    {results.pos_tagged.slice(0, 10).map((item, index) => (
                      <li key={index}>
                        {item[0]} - {item[1]}
                      </li>
                    ))}
                  </ul>
                </td>
              )}

              {/* Render Simplified POS Tagged */}
              {results.simplified_pos_tagged &&
                results.simplified_pos_tagged.length > 0 && (
                  <td>
                    <h3>Parts of Speech (first 10):</h3>
                    <ul>
                      {results.simplified_pos_tagged
                        .slice(0, 10)
                        .map((item, index) => (
                          <li key={index}>
                            {item[0]} - {item[1]}
                          </li>
                        ))}
                    </ul>
                  </td>
                )}

              {/* Render Nouns */}
              {results.nouns && results.nouns.length > 0 && (
                <td>
                  <h3>Nouns (first 10):</h3>
                  <ul>
                    {results.nouns.slice(0, 10).map((noun, index) => (
                      <li key={index}>{noun}</li>
                    ))}
                  </ul>
                </td>
              )}

              {/* Render Morphemes */}
              {results.morphs && results.morphs.length > 0 && (
                <td>
                  <h3>Morphemes (first 10):</h3>
                  <ul>
                    {results.morphs.slice(0, 10).map((morph, index) => (
                      <li key={index}>{morph}</li>
                    ))}
                  </ul>
                </td>
              )}
            </tr>
          </tbody>
        </table>

        {/* Render Grammar Errors */}
        {results.grammar_errors && results.grammar_errors.length > 0 ? (
          <div>
            <h3>Grammar Errors:</h3>
            <ul>
              {results.grammar_errors.map((error, index) => (
                <li key={index}>{error}</li>
              ))}
            </ul>
          </div>
        ) : (
          <p>No grammar errors detected.</p>
        )}
      </div>
    );
  };

  return (
    <div className="App">
      <h1>Korean Grammar Checker - Test</h1>
      <div className="input-container">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter Korean text to analyze here"
          maxLength={256}
        />
        {text && (
          <button className="clear-button" onClick={handleClear}>
            ×
          </button>
        )}
        <div className="char-count">{text.length} / 256</div>
        <button className="analyze-button" onClick={handleAnalyze}>
          Analyze
        </button>
      </div>
      {renderResults()}
    </div>
  );
}

export default App;
