#!/usr/bin/env python3
"""
恢复到 v5 样式 - 紫色渐变背景 + 白色卡片 + 选项反馈在右边
"""
import re, os, glob

OUTPUT_DIR = "output"

# v5 的 CSS
V5_CSS = """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: "Noto Sans SC", "PingFang SC", "HarmonyOS Sans SC", "Microsoft YaHei", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        .container { max-width: 800px; margin: 0 auto; }
        .card {
            background: white;
            border-radius: 16px;
            padding: 32px;
            margin-bottom: 24px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        .header {
            text-align: center;
            margin-bottom: 24px;
            padding-bottom: 24px;
            border-bottom: 2px solid #f0f0f0;
        }
        .header h1 {
            color: #1a1a1a;
            font-size: 26px;
            font-weight: 600;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }
        .header .subtitle { color: #666; font-size: 14px; }
        .header .breadcrumb {
            display: inline-block;
            background: #e8f0fe;
            color: #1a73e8;
            font-size: 12px;
            font-weight: 500;
            padding: 4px 12px;
            border-radius: 20px;
            margin-bottom: 12px;
        }
        .review-section {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 24px;
            border-radius: 12px;
            margin-bottom: 24px;
        }
        .review-section h2 {
            color: #e65100;
            font-size: 18px;
            font-weight: 500;
            margin-bottom: 16px;
        }
        .review-cards { display: flex; flex-direction: column; gap: 12px; }
        .review-card {
            background: rgba(255,255,255,0.85);
            padding: 14px 16px;
            border-radius: 8px;
            border-left: 4px solid #ff9800;
        }
        .review-card p { color: #444; font-size: 14px; line-height: 1.9; }
        .knowledge {
            background: #f8f9fa;
            padding: 24px;
            border-radius: 12px;
            margin-bottom: 24px;
        }
        .knowledge h2 {
            color: #667eea;
            font-size: 19px;
            font-weight: 500;
            margin-bottom: 16px;
        }
        .knowledge p { color: #555; line-height: 2.0; margin-bottom: 12px; }
        .knowledge .highlight {
            background: #fff3cd;
            padding: 12px;
            border-left: 4px solid #ffc107;
            border-radius: 4px;
            margin: 16px 0;
        }
        .knowledge .highlight-green {
            background: #d4edda;
            padding: 12px;
            border-left: 4px solid #28a745;
            border-radius: 4px;
            margin: 16px 0;
        }
        .knowledge .highlight-blue {
            background: #e8f0fe;
            padding: 12px;
            border-left: 4px solid #1a73e8;
            border-radius: 4px;
            margin: 16px 0;
        }
        .knowledge code {
            background: #e9ecef;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 13px;
            color: #d63384;
        }
        .quiz-section { margin-top: 32px; }
        .quiz-section h2 { color: #333; font-size: 20px; margin-bottom: 20px; }
        .question {
            background: #fafbfc;
            border: 1px solid #e1e4e8;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .question-num {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            margin-bottom: 12px;
        }
        .question-type {
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            margin-left: 8px;
        }
        .question-type.multi { background: #fd7e14; }
        .question-text {
            color: #1a1a1a;
            font-size: 16px;
            font-weight: 500;
            line-height: 1.8;
            margin-bottom: 16px;
        }
        .options { display: flex; flex-direction: column; gap: 10px; }
        .option {
            display: flex;
            align-items: center;
            padding: 12px 16px;
            background: white;
            border: 2px solid #e1e4e8;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .option:hover { border-color: #667eea; background: #f8f9ff; }
        .option input[type="radio"],
        .option input[type="checkbox"] {
            margin-right: 12px;
            width: 18px;
            height: 18px;
            cursor: pointer;
        }
        .option label {
            flex: 1;
            cursor: pointer;
            color: #444;
            line-height: 1.7;
            font-size: 15px;
        }
        .submit-btn {
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .submit-btn:hover { transform: translateY(-2px); }
        .result {
            display: none;
            background: #f8f9fa;
            padding: 24px;
            border-radius: 12px;
            margin-top: 24px;
        }
        .result.show { display: block; }
        .score {
            text-align: center;
            font-size: 32px;
            font-weight: 600;
            color: #667eea;
            margin-bottom: 16px;
        }
        .explanation {
            background: white;
            padding: 16px;
            border-radius: 8px;
            margin-top: 12px;
            border-left: 4px solid #667eea;
        }
        .explanation h4 { color: #667eea; font-size: 14px; margin-bottom: 8px; }
        .explanation p { color: #555; font-size: 14px; line-height: 1.8; }
        .correct { border-color: #28a745 !important; background: #d4edda !important; }
        .wrong { border-color: #dc3545 !important; background: #f8d7da !important; }
        .screenshot { margin: 16px 0; text-align: center; }
        .screenshot img { max-width: 100%; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.15); border: 1px solid #e1e4e8; }
        .screenshot .caption { font-size: 12px; color: #666; margin-top: 8px; text-align: center; }
        .data-table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 14px; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .data-table th { background: #667eea; color: white; padding: 10px 12px; text-align: left; font-weight: 500; }
        .data-table td { padding: 8px 12px; border-bottom: 1px solid #e1e4e8; font-family: "Courier New", monospace; font-size: 13px; }
        .data-table tr:last-child td { border-bottom: none; }
        .data-table tr:hover { background: #f8f9ff; }
        .copy-btn { display: inline-block; margin-left: 8px; padding: 4px 12px; background: #667eea; color: white; border: none; border-radius: 4px; font-size: 12px; cursor: pointer; transition: all 0.2s; }
        .copy-btn:hover { background: #5568d3; transform: translateY(-1px); }
        .copy-btn.copied { background: #28a745; }
        .table-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
        .table-title { font-weight: 600; color: #333; font-size: 15px; }
        /* === 选项级反馈样式 v5 === */
        .option { 
            position: relative; 
            transition: all 0.3s;
            display: flex;
            align-items: center;
            padding: 12px 16px;
            border: 2px solid #e1e4e8;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        .option.correct-answer { 
            border-color: #28a745 !important;
            background: #e8f5e9 !important;
        }
        .option.wrong-answer { 
            border-color: #dc3545 !important;
            background: #ffebee !important;
        }
        .option.user-wrong { 
            border-color: #fd7e14 !important;
            background: #fff8e1 !important;
        }
        .option .option-badge {
            display: none !important;
        }
        .option-feedback {
            display: none;
            font-size: 22px;
            font-weight: 700;
            margin-left: auto;
            padding-left: 12px;
            line-height: 1;
            flex-shrink: 0;
        }
        .option-feedback.show { display: inline-block; }
        .option-feedback.correct-fb { color: #28a745; }
        .option-feedback.wrong-fb { color: #dc3545; }
        .option-feedback.user-wrong-fb { color: #fd7e14; }
        .option label {
            flex: 1;
        }
        .question-explanation {
            display: none;
            margin-top: 16px;
            padding: 12px 16px;
            background: #e8f0fe;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            font-size: 14px;
            line-height: 1.8;
            color: #333;
        }
        .question-explanation.show { display: block; }
        .question-explanation strong { color: #667eea; }
        .result { text-align: center; }
        .result .score { margin-bottom: 8px; }
        .result .score-msg { font-size: 14px; color: #666; }
        input:disabled + label { cursor: default; }
        .option.no-click { pointer-events: none; }
"""

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换整个 <style> 块
    style_pattern = r'<style>[\s\S]*?</style>'
    content = re.sub(style_pattern, f'<style>\n{V5_CSS}\n    </style>', content, count=1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

def main():
    files = sorted(glob.glob(os.path.join(OUTPUT_DIR, "Day*.html")))
    print(f"找到 {len(files)} 个文件\n")
    success = 0
    for f in files:
        name = os.path.basename(f)
        print(f"处理：{name}")
        if process_file(f):
            success += 1
            print(f"  ✅ 完成")
        else:
            print(f"  ❌ 跳过")
    print(f"\n完成：{success}/{len(files)} 个文件已更新")

if __name__ == "__main__":
    main()
