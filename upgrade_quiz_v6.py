#!/usr/bin/env python3
"""
v6：重新设计 - 参考现代 UI 美学，更优雅、更克制
- 去掉强烈的背景色块
- 用微妙的阴影和圆角
- 统一的配色体系
- 更清晰的视觉层次
"""
import re, os, glob

OUTPUT_DIR = "output"

# 新的 CSS - 现代简约风格
NEW_CSS = """
        /* === 现代简约样式 v6 === */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: "Noto Sans SC", "PingFang SC", "HarmonyOS Sans SC", "Microsoft YaHei", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f5f7fa;
            min-height: 100vh;
            padding: 20px;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            color: #2c3e50;
        }
        .container { max-width: 800px; margin: 0 auto; }
        .card {
            background: white;
            border-radius: 12px;
            padding: 32px;
            margin-bottom: 24px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        }
        .header {
            text-align: center;
            margin-bottom: 32px;
            padding-bottom: 24px;
            border-bottom: 1px solid #eef0f2;
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
            background: #f0f4ff;
            color: #667eea;
            font-size: 12px;
            font-weight: 500;
            padding: 4px 12px;
            border-radius: 20px;
            margin-bottom: 12px;
        }
        .review-section {
            background: #fafbfc;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 24px;
            border: 1px solid #eef0f2;
        }
        .review-section h2 {
            color: #2c3e50;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 16px;
        }
        .review-cards { display: flex; flex-direction: column; gap: 10px; }
        .review-card {
            background: white;
            padding: 12px 16px;
            border-radius: 6px;
            border: 1px solid #eef0f2;
        }
        .review-card p { color: #555; font-size: 14px; line-height: 1.7; }
        .knowledge {
            background: #fafbfc;
            padding: 24px;
            border-radius: 8px;
            margin-bottom: 24px;
            border: 1px solid #eef0f2;
        }
        .knowledge h2 {
            color: #2c3e50;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
        }
        .knowledge p { color: #555; line-height: 1.8; margin-bottom: 12px; }
        .knowledge .highlight,
        .knowledge .highlight-green,
        .knowledge .highlight-blue {
            background: white;
            padding: 16px;
            border-radius: 6px;
            margin: 16px 0;
            border: 1px solid #eef0f2;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }
        .knowledge .highlight { border-left: 3px solid #f5a623; }
        .knowledge .highlight-green { border-left: 3px solid #7ed321; }
        .knowledge .highlight-blue { border-left: 3px solid #4a90e2; }
        .knowledge code {
            background: #f0f4ff;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 13px;
            color: #667eea;
        }
        .quiz-section { margin-top: 32px; }
        .quiz-section h2 { color: #2c3e50; font-size: 18px; margin-bottom: 20px; font-weight: 600; }
        .question {
            background: white;
            border: 1px solid #eef0f2;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 16px;
        }
        .question-num {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 12px;
            margin-bottom: 12px;
        }
        .question-type {
            display: inline-block;
            background: #eef0f2;
            color: #666;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 12px;
            margin-left: 8px;
        }
        .question-type.multi { background: #fff3e0; color: #f57c00; }
        .question-text {
            color: #1a1a1a;
            font-size: 15px;
            font-weight: 500;
            line-height: 1.6;
            margin-bottom: 16px;
        }
        .options { display: flex; flex-direction: column; gap: 8px; }
        .option {
            display: flex;
            align-items: center;
            padding: 12px 16px;
            background: #fafbfc;
            border: 1px solid #eef0f2;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .option:hover { border-color: #667eea; background: #f0f4ff; }
        .option input[type="radio"],
        .option input[type="checkbox"] {
            margin-right: 12px;
            width: 16px;
            height: 16px;
            cursor: pointer;
        }
        .option label {
            flex: 1;
            cursor: pointer;
            color: #444;
            line-height: 1.6;
            font-size: 14px;
        }
        .option .option-badge { display: none !important; }
        .option-feedback {
            display: none;
            font-size: 20px;
            font-weight: 700;
            margin-left: auto;
            padding-left: 12px;
            line-height: 1;
            flex-shrink: 0;
        }
        .option-feedback.show { display: inline-block; }
        .option-feedback.correct-fb { color: #7ed321; }
        .option-feedback.wrong-fb { color: #d0021b; }
        .option-feedback.user-wrong-fb { color: #f5a623; }
        .option.correct-answer { border-color: #7ed321; background: #f0f9eb; }
        .option.wrong-answer { border-color: #d0021b; background: #fef0f0; }
        .option.user-wrong { border-color: #f5a623; background: #fdf6ec; }
        .submit-btn {
            width: 100%;
            padding: 14px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 15px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }
        .submit-btn:hover { background: #5568d3; }
        .question-explanation {
            display: none;
            margin-top: 16px;
            padding: 12px 16px;
            background: #f0f4ff;
            border-radius: 6px;
            border-left: 3px solid #667eea;
            font-size: 14px;
            line-height: 1.7;
            color: #555;
        }
        .question-explanation.show { display: block; }
        .question-explanation strong { color: #667eea; }
        .result { text-align: center; margin-top: 24px; }
        .result .score { font-size: 28px; font-weight: 600; color: #667eea; margin-bottom: 8px; }
        .result .score-msg { font-size: 14px; color: #666; }
        input:disabled + label { cursor: default; }
        .option.no-click { pointer-events: none; }
        .screenshot { margin: 16px 0; text-align: center; }
        .screenshot img { max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .screenshot .caption { font-size: 12px; color: #666; margin-top: 8px; }
        .data-table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 14px; background: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
        .data-table th { background: #f0f4ff; color: #333; padding: 10px 12px; text-align: left; font-weight: 500; }
        .data-table td { padding: 8px 12px; border-bottom: 1px solid #eef0f2; font-family: "Courier New", monospace; font-size: 13px; }
        .data-table tr:last-child td { border-bottom: none; }
        .copy-btn { display: inline-block; margin-left: 8px; padding: 4px 12px; background: #667eea; color: white; border: none; border-radius: 4px; font-size: 12px; cursor: pointer; }
        .copy-btn:hover { background: #5568d3; }
        .copy-btn.copied { background: #7ed321; }
        .table-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
        .table-title { font-weight: 600; color: #333; font-size: 15px; }
"""

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换整个 <style> 块
    style_pattern = r'<style>[\s\S]*?</style>'
    content = re.sub(style_pattern, f'<style>\n{NEW_CSS}\n    </style>', content, count=1)

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
