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
            text = request.json['text']
            logging.debug(f"Received text for analysis: {text[:50]}...")  # Log first 50 chars
            
            analysis = analyze_sentence(komoran, text)
            logging.debug("Sentence analysis completed")
            
            grammar_issues = check_grammar(analysis['pos_tagged'])
            logging.debug("Grammar check completed")
            
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
            
            logging.debug("Analysis completed successfully")
            return jsonify(result)
        except Exception as e:
            logging.error(f"Error during analysis: {str(e)}")
            logging.error(traceback.format_exc())
            return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500