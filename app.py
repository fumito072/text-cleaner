from flask import Flask, render_template, request, jsonify, send_file
from text_cleaner import remove_chars
import os
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_text():
    data = request.json
    text = data.get('text', '')
    chars_to_remove = data.get('chars', [])
    
    if not text:
        return jsonify({'error': 'テキストが入力されていません'}), 400
    
    result = remove_chars(text, chars_to_remove)
    return jsonify({'result': result})

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    text = data.get('text', '')
    chars_to_remove = data.get('chars', [])
    
    if not text:
        return jsonify({'error': 'テキストが入力されていません'}), 400
    
    result = remove_chars(text, chars_to_remove)
    
    # 一時ファイルを作成
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as temp_file:
        temp_file.write(result)
        temp_path = temp_file.name
    
    return send_file(
        temp_path,
        as_attachment=True,
        download_name='cleaned_text.txt',
        mimetype='text/plain'
    )

# Vercel用のエントリーポイント
if __name__ == '__main__':
    app.run(debug=True)
else:
    # Vercel用の設定
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 