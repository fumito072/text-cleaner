from flask import Flask, render_template, request, jsonify, send_file
from text_cleaner import remove_chars, remove_time_patterns, split_text_by_length
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
    remove_time = data.get('removeTime', False)
    split_text = data.get('splitText', False)
    split_length = data.get('splitLength', 1000)
    
    if not text:
        return jsonify({'error': 'テキストが入力されていません'}), 400
    
    result = remove_chars(text, chars_to_remove)
    
    # 時間削除が有効な場合
    if remove_time:
        result = remove_time_patterns(result)
    
    # 文字数分割が有効な場合
    if split_text:
        result = split_text_by_length(result, split_length)
    
    return jsonify({'result': result})

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    text = data.get('text', '')
    chars_to_remove = data.get('chars', [])
    remove_time = data.get('removeTime', False)
    split_text = data.get('splitText', False)
    split_length = data.get('splitLength', 1000)
    
    if not text:
        return jsonify({'error': 'テキストが入力されていません'}), 400
    
    result = remove_chars(text, chars_to_remove)
    
    # 時間削除が有効な場合
    if remove_time:
        result = remove_time_patterns(result)
    
    # 文字数分割が有効な場合
    if split_text:
        result = split_text_by_length(result, split_length)
    
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