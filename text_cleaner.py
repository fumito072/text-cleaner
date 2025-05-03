def remove_char(text: str, char_to_remove: str) -> str:
    """
    文字列から特定の文字を削除する関数
    
    Args:
        text: 元の文字列
        char_to_remove: 削除したい文字
    
    Returns:
        削除後の文字列
    """
    return text.replace(char_to_remove, '')

def remove_chars(text: str, chars_to_remove: list) -> str:
    """
    文字列から複数の文字を削除する関数
    
    Args:
        text: 元の文字列
        chars_to_remove: 削除したい文字のリスト
    
    Returns:
        削除後の文字列
    """
    for char in chars_to_remove:
        text = text.replace(char, '')
    return text

def remove_newlines(text: str) -> str:
    """
    文字列から改行文字、その表記（\n）、時間表記を削除する関数
    
    Args:
        text: 元の文字列（長文を想定）
    
    Returns:
        改行文字、\n、時間表記を削除した文字列
    """
    # まず実際の改行文字を削除
    text = text.replace('\n', '')
    # 文字列としての\nを削除
    text = text.replace('\\n', '')
    # 読点を削除
    text = text.replace('、', '')
    # 時間表記（xx:xx）を削除
    import re
    text = re.sub(r'\d+:\d+', '', text)
    return text

def read_file(file_path: str) -> str:
    """
    ファイルから文章を読み込む関数
    
    Args:
        file_path: 入力ファイルのパス
    
    Returns:
        ファイルの内容
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='文章から改行を削除するプログラム')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--text', help='直接文字列を入力')
    group.add_argument('-f', '--file', help='入力ファイルのパス')
    parser.add_argument('-o', '--output', help='出力ファイルのパス（指定しない場合は標準出力）')
    
    args = parser.parse_args()
    
    if args.text:
        input_text = args.text
    else:
        input_text = read_file(args.file)
    
    # 改行の削除
    result = remove_newlines(input_text)
    
    # 結果の出力
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"結果を {args.output} に保存しました。")
        print(f"出力ファイルの文字数: {len(result)}")
    else:
        print(result)
        print(f"出力の文字数: {len(result)}") 