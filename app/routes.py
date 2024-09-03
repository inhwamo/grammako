from flask import render_template, request, jsonify
from nlp.language_model import analyze_sentence
from nlp.grammar_checker import check_grammar
import logging
import traceback

def init_routes(app, komoran):
    @app.route('/')
    def index():
        return render_template('index.html')

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
                'simplified_pos_tagged': analysis['simplified_pos_tagged']
            }

            logging.info("Analysis completed successfully")
            return jsonify(result)
        except ValueError as ve:
            logging.error(f"ValueError: {str(ve)}")
            return jsonify({'error': str(ve)}), 400
        except Exception as e:
            logging.error(f"Error during analysis: {str(e)}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500