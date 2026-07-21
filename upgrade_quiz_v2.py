#!/usr/bin/env python3
"""
批量升级 quiz 页面 v2：更清爽的选项反馈设计
- 去掉选项整体背景色，只保留左边框颜色
- 去掉 badge，只保留简洁的 feedback 文字
- 反馈文案更精简
"""
import re
import os
import glob

OUTPUT_DIR = "output"

# ── 新的 CSS（替换旧的 option-feedback 相关样式） ──
NEW_CSS = """
        /* === 选项级反馈样式 v2 === */
        .option { 
            position: relative; 
            transition: all 0.3s;
            border-left: 4px solid transparent;
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
            margin-top: 8px;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 13px;
            line-height: 1.6;
        }
        .option-feedback.show { display: block; }
        .option-feedback.correct-fb { 
            background: #d4edda; 
            color: #155724;
        }
        .option-feedback.wrong-fb { 
            background: #f8d7da; 
            color: #721c24;
        }
        .option-feedback.user-wrong-fb { 
            background: #fff3cd; 
            color: #856404;
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

    # ── 1. 替换 CSS（找到旧的 option-feedback 样式块并替换） ──
    old_css_pattern = r'/\* === 选项级反馈样式 === \*/[\s\S]*?\.option\.no-click \{ pointer-events: none; \}'
    content = re.sub(old_css_pattern, NEW_CSS.strip(), content)

    # ── 2. 简化 feedback 文案（去掉重复信息） ──
    # 在 JS 中修改 feedback 文案
    content = content.replace(
        "feedback.textContent = '✅ 回答正确';",
        "feedback.textContent = '✓ 正确';"
    )
    content = content.replace(
        "feedback.textContent = '✅ 这是正确答案';",
        "feedback.textContent = '✓ 这是正确答案';"
    )
    content = content.replace(
        "feedback.textContent = '❌ 你选了这个，但不是正确答案';",
        "feedback.textContent = ' 你选了这个，但不是正确答案';"
    )
    content = content.replace(
        "feedback.textContent = '❌ 不是正确答案';",
        "feedback.textContent = '✗ 不是正确答案';"
    )

    # ── 3. 去掉 badge 显示（CSS 已经隐藏了，但 JS 里也清空） ──
    # badge 已经在 CSS 中 display: none，不需要改 JS

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
