from flask import render_template, request, jsonify
from nlp import check_grammar, analyze_sentence

def init_routes(app, komoran):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/analyze', methods=['POST'])
    def analyze():
        text = request.json['text']
        analysis = analyze_sentence(komoran, text)
        grammar_issues = check_grammar(analysis['pos_tagged'])
        return jsonify({
            'pos_tagged': analysis['pos_tagged'],
            'morphs': analysis['morphs'],
            'nouns': analysis['nouns'],
            'grammar_errors': grammar_issues
        })