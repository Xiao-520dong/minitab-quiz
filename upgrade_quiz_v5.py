#!/usr/bin/env python3
"""
v5：✓/✗ 放回选项右边，选项用浅绿/浅红背景
"""
import re, os, glob

OUTPUT_DIR = "output"

NEW_CSS = """
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

    # 1. 替换 CSS
    old_css_pattern = r'/\* === 选项级反馈样式 v\d+ === \*/[\s\S]*?\.option\.no-click \{ pointer-events: none; \}'
    if not re.search(old_css_pattern, content):
        print(f"  ⚠️  未找到 CSS")
        return False
    content = re.sub(old_css_pattern, NEW_CSS.strip(), content)

    # 2. 把 feedback div 移回 label 后面（右边）
    # 先删除所有 feedback div
    content = content.replace('<div class="option-feedback"></div>\n', '')
    content = content.replace('<div class="option-feedback"></div>', '')
    # 在 </label><span class="option-badge"> 后面插入 feedback
    content = content.replace(
        '</label><span class="option-badge"></span>',
        '</label><span class="option-badge"></span><div class="option-feedback"></div>'
    )

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
