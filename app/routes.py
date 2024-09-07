import json
import os
from flask import render_template, request, jsonify, send_from_directory, current_app
import logging
import traceback
from nlp.language_model import analyze_sentence
from nlp.grammar_checker import check_grammar

def init_routes(app, komoran):
    @app.route('/')
    def index():
        try:
            print("Rendering index.html")
            return render_template('index.html')
        except Exception as e:
            print(f"Error rendering index.html: {str(e)}")
            return jsonify({"error": str(e)}), 500

    @app.route('/react')
    def react():
        try:
            manifest_path = os.path.join(current_app.root_path, 'app', 'static', 'react-app', 'build', 'asset-manifest.json')
            if not os.path.exists(manifest_path):
                raise FileNotFoundError(f"Manifest file not found at {manifest_path}")
            
            with open(manifest_path) as f:
                manifest = json.load(f)
            
            print("Manifest loaded:", manifest)  # Debug print
            
            if 'files' not in manifest:
                raise KeyError("'files' key not found in manifest")
            
            return render_template('react.html', manifest=manifest['files'])
        except Exception as e:
            print(f"Error loading manifest: {str(e)}")
            return f"Error loading React app: {str(e)}", 500

    @app.route('/static/react-app/build/<path:filename>')
    def serve_react_static(filename):
        directory = os.path.join(current_app.root_path, '..', 'app', 'static', 'react-app', 'build')
        return send_from_directory(directory, filename)

    @app.route('/analyze', methods=['POST'])
    def analyze():
        try:
            data = request.json
            if not data or 'text' not in data or not data['text']:
                raise ValueError("No text provided for analysis")
            
            text = data['text']
            logging.info(f"Analyzing text (first 50 chars): {text[:50]}...")

            analysis = analyze_sentence(komoran, text)
            grammar_issues = check_grammar(analysis['pos_tagged'])

            result = {
                'pos_tagged': analysis['pos_tagged'],
                'morphs': analysis['morphs'],
                'nouns': analysis['nouns'],
                'keywords': analysis['keywords'],
                'sentence_structure': analysis['sentence_structure'],
                'grammar_errors': grammar_issues,
                'original_text': analysis['original_text'],
                'simplified_pos_tagged': analysis['simplified_pos_tagged'],
                'chunks': analysis['chunks']
            }

            logging.info("Analysis completed successfully")
            return jsonify(result)
        except Exception as e:
            logging.error(f"Error during analysis: {str(e)}")
            logging.error(traceback.format_exc())
            return jsonify({'error': str(e)}), 500