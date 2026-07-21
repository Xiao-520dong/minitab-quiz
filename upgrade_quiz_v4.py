#!/usr/bin/env python3
"""
批量升级 quiz 页面 v4：把 ✓/✗ 放到选项前面，放大显示
"""
import re
import os
import glob

OUTPUT_DIR = "output"

NEW_CSS = """
        /* === 选项级反馈样式 v4 === */
        .option { 
            position: relative; 
            transition: all 0.3s;
            border-left: 4px solid transparent;
            display: flex;
            align-items: center;
            padding: 12px 16px;
        }
        .option.correct-answer { 
            border-left-color: #28a745 !important;
        }
        .option.wrong-answer { 
            border-left-color: #dc3545 !important;
        }
        .option.user-wrong { 
            border-left-color: #fd7e14 !important;
        }
        .option .option-badge {
            display: none !important;
        }
        .option-feedback {
            display: none;
            font-size: 28px;
            font-weight: 600;
            margin-right: 12px;
            line-height: 1;
            flex-shrink: 0;
        }
        .option-feedback.show { display: inline-block; }
        .option-feedback.correct-fb { 
            color: #28a745;
        }
        .option-feedback.wrong-fb { 
            color: #dc3545;
        }
        .option-feedback.user-wrong-fb { 
            color: #fd7e14;
        }
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

    # ── 1. 替换 CSS ──
    old_css_pattern = r'/\* === 选项级反馈样式 v\d+ === \*/[\s\S]*?\.option\.no-click \{ pointer-events: none; \}'
    if not re.search(old_css_pattern, content):
        print(f"  ⚠️  未找到 CSS 样式块")
        return False
    
    content = re.sub(old_css_pattern, NEW_CSS.strip(), content)

    # ── 2. 移动 feedback div ──
    # 当前结构：...<label>文字</label><span class="option-badge"></span>\n<div class="option-feedback"></div>\n</div>
    # 目标结构：<div class="option-feedback"></div>\n<input ...>\n<label>文字</label>...
    
    # 简单方法：删除所有 feedback div，然后在每个 input 前插入
    content = content.replace('<div class="option-feedback"></div>\n', '')
    content = content.replace('<div class="option-feedback"></div>', '')
    
    # 在每个 <input 前面插入 feedback div（带适当缩进）
    content = content.replace('<input type="radio"', '<div class="option-feedback"></div>\n                            <input type="radio"')
    content = content.replace('<input type="checkbox"', '<div class="option-feedback"></div>\n                            <input type="checkbox"')

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
