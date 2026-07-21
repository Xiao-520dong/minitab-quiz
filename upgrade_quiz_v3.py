#!/usr/bin/env python3
"""
批量升级 quiz 页面 v3：极简反馈 - 只显示 ✓ 或 ✗，无文字说明
"""
import re
import os
import glob

OUTPUT_DIR = "output"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换所有 feedback 文案为纯符号
    content = content.replace(
        "feedback.textContent = '✓ 正确';",
        "feedback.textContent = '✓';"
    )
    content = content.replace(
        "feedback.textContent = '✓ 这是正确答案';",
        "feedback.textContent = '✓';"
    )
    content = content.replace(
        "feedback.textContent = ' 你选了这个，但不是正确答案';",
        "feedback.textContent = '✗';"
    )
    content = content.replace(
        "feedback.textContent = '✗ 不是正确答案';",
        "feedback.textContent = '✗';"
    )

    # 简化 feedback 样式：去掉背景色，只显示符号
    content = content.replace(
        "background: #d4edda; \n            color: #155724;",
        "background: transparent; \n            color: #28a745; \n            font-weight: 600;"
    )
    content = content.replace(
        "background: #f8d7da; \n            color: #721c24;",
        "background: transparent; \n            color: #dc3545; \n            font-weight: 600;"
    )
    content = content.replace(
        "background: #fff3cd; \n            color: #856404;",
        "background: transparent; \n            color: #fd7e14; \n            font-weight: 600;"
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
