#!/usr/bin/env python3
"""
批量升级 quiz 页面：提交后答案解析直接显示在每个选项旁边。
"""
import re
import os
import glob

OUTPUT_DIR = "output"

# ── 1. 新增 CSS（插入到 </style> 之前） ──
NEW_CSS = """
        /* === 选项级反馈样式 === */
        .option { position: relative; transition: all 0.3s; }
        .option.correct-answer { border-color: #28a745 !important; background: #d4edda !important; }
        .option.wrong-answer { border-color: #dc3545 !important; background: #f8d7da !important; }
        .option.user-wrong { border-color: #e67e22 !important; background: #fff3cd !important; }
        .option .option-badge {
            display: none;
            font-size: 13px;
            font-weight: 600;
            margin-left: 8px;
            white-space: nowrap;
        }
        .option.correct-answer .option-badge { display: inline; color: #28a745; }
        .option.wrong-answer .option-badge { display: inline; color: #dc3545; }
        .option.user-wrong .option-badge { display: inline; color: #e67e22; }
        .option-feedback {
            display: none;
            margin-top: 6px;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 13px;
            line-height: 1.7;
        }
        .option-feedback.show { display: block; }
        .option-feedback.correct-fb { background: #d4edda; color: #155724; border-left: 3px solid #28a745; }
        .option-feedback.wrong-fb { background: #f8d7da; color: #721c24; border-left: 3px solid #dc3545; }
        .option-feedback.user-wrong-fb { background: #fff3cd; color: #856404; border-left: 3px solid #e67e22; }
        .question-explanation {
            display: none;
            margin-top: 12px;
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

# ── 2. 新的 JS（替换整个 <script> 块中的 checkAnswers 和 explanations 部分） ──
def build_new_js(explanations_dict):
    """生成新的 JS 代码，包含选项级反馈逻辑。"""
    # explanations_dict: {"q1": "原始解析文本", ...}
    exp_items = []
    for k, v in explanations_dict.items():
        # 转义引号
        v_escaped = v.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')
        exp_items.append(f"            '{k}': '{v_escaped}'")
    exp_str = ",\n".join(exp_items)

    return f"""
    <script>
        const explanations = {{
{exp_str}
        }};

        function checkAnswers() {{
            let score = 0;
            const questions = document.querySelectorAll('.question');
            const resultDiv = document.getElementById('result');
            const scoreDiv = document.getElementById('score');

            questions.forEach((q, index) => {{
                const qKey = 'q' + (index + 1);
                const correct = q.dataset.correct.split(',').map(s => s.trim());
                const inputs = q.querySelectorAll('input[type="radio"], input[type="checkbox"]');
                const options = q.querySelectorAll('.option');
                const selected = [];

                // 收集用户选择
                inputs.forEach(input => {{
                    if (input.checked) selected.push(input.value);
                }});

                const isCorrect = JSON.stringify([...correct].sort()) === JSON.stringify([...selected].sort());
                if (isCorrect) score++;

                // 题目整体标记
                if (isCorrect) {{
                    q.classList.add('correct');
                    q.classList.remove('wrong');
                }} else {{
                    q.classList.add('wrong');
                    q.classList.remove('correct');
                }}

                // 遍历每个选项，给出反馈
                options.forEach((opt, optIdx) => {{
                    const input = opt.querySelector('input');
                    const val = input.value;
                    const feedback = opt.querySelector('.option-feedback');
                    const badge = opt.querySelector('.option-badge');

                    // 禁用交互
                    input.disabled = true;
                    opt.classList.add('no-click');

                    const isCorrectOption = correct.includes(val);
                    const isUserSelected = input.checked;

                    // 清除旧状态
                    opt.classList.remove('correct-answer', 'wrong-answer', 'user-wrong');
                    feedback.classList.remove('show', 'correct-fb', 'wrong-fb', 'user-wrong-fb');

                    if (isCorrectOption && isUserSelected) {{
                        // 选对了
                        opt.classList.add('correct-answer');
                        badge.textContent = '✅ 正确';
                        feedback.textContent = '✅ 回答正确';
                        feedback.classList.add('show', 'correct-fb');
                    }} else if (isCorrectOption && !isUserSelected) {{
                        // 是正确答案但用户没选
                        opt.classList.add('correct-answer');
                        badge.textContent = '✅ 正确答案';
                        feedback.textContent = '✅ 这是正确答案';
                        feedback.classList.add('show', 'correct-fb');
                    }} else if (!isCorrectOption && isUserSelected) {{
                        // 用户选错了
                        opt.classList.add('user-wrong');
                        badge.textContent = '❌ 你的选择';
                        feedback.textContent = '❌ 你选了这个，但不是正确答案';
                        feedback.classList.add('show', 'user-wrong-fb');
                    }} else {{
                        // 不是正确答案，用户也没选
                        opt.classList.add('wrong-answer');
                        badge.textContent = '❌';
                        feedback.textContent = '❌ 不是正确答案';
                        feedback.classList.add('show', 'wrong-fb');
                    }}
                }});

                // 题目级解析（移到题目区域内）
                let qExp = q.querySelector('.question-explanation');
                if (!qExp) {{
                    qExp = document.createElement('div');
                    qExp.className = 'question-explanation';
                    q.appendChild(qExp);
                }}
                qExp.innerHTML = '<strong>📖 解析：</strong>' + (explanations[qKey] || '');
                qExp.classList.add('show');
            }});

            // 显示总分
            scoreDiv.textContent = '得分：' + score + ' / ' + questions.length;
            resultDiv.classList.add('show');

            // 禁用提交按钮
            document.querySelector('.submit-btn').disabled = true;
            document.querySelector('.submit-btn').style.opacity = '0.5';
            document.querySelector('.submit-btn').textContent = '已提交';
        }}

        // 重新答题功能
        function resetQuiz() {{
            const questions = document.querySelectorAll('.question');
            questions.forEach(q => {{
                q.classList.remove('correct', 'wrong');
                const inputs = q.querySelectorAll('input[type="radio"], input[type="checkbox"]');
                inputs.forEach(input => {{
                    input.disabled = false;
                    input.checked = false;
                }});
                const options = q.querySelectorAll('.option');
                options.forEach(opt => {{
                    opt.classList.remove('correct-answer', 'wrong-answer', 'user-wrong', 'no-click');
                    const fb = opt.querySelector('.option-feedback');
                    if (fb) {{ fb.classList.remove('show', 'correct-fb', 'wrong-fb', 'user-wrong-fb'); }}
                    const badge = opt.querySelector('.option-badge');
                    if (badge) {{ badge.textContent = ''; }}
                }});
                const qExp = q.querySelector('.question-explanation');
                if (qExp) {{ qExp.classList.remove('show'); }}
            }});
            document.getElementById('result').classList.remove('show');
            const btn = document.querySelector('.submit-btn');
            btn.disabled = false;
            btn.style.opacity = '1';
            btn.textContent = '提交答案';
        }}
    </script>"""


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # ── 提取 explanations 字典 ──
    exp_match = re.search(r'const explanations\s*=\s*\{([^}]+)\};', content, re.DOTALL)
    if not exp_match:
        print(f"  ⚠️  未找到 explanations: {filepath}")
        return False

    exp_body = exp_match.group(1)
    # 解析 key: value 对
    explanations = {}
    for m in re.finditer(r"['\"]?(q\d+)['\"]?\s*:\s*['\"](.+?)['\"]\s*(?:,|$)", exp_body):
        explanations[m.group(1)] = m.group(2)

    # ── 1. 插入新 CSS ──
    if 'option-feedback' not in content:
        content = content.replace('</style>', NEW_CSS + '\n    </style>', 1)

    # ── 2. 为每个 .option 添加 feedback div 和 badge ──
    # 匹配每个 option div 的结束标签前
    def add_feedback_to_option(match):
        opt_html = match.group(0)
        if 'option-feedback' in opt_html:
            return opt_html  # 已经加过了
        # 在 </label> 后面插入 badge span 和 feedback div
        # 在 </div> (option的结束) 前插入 feedback
        opt_html = opt_html.replace(
            '</label>',
            '</label><span class="option-badge"></span>'
        )
        # 在 option div 的 </div> 前插入 feedback
        # 找到最后一个 </div>
        last_div_idx = opt_html.rfind('</div>')
        if last_div_idx >= 0:
            opt_html = opt_html[:last_div_idx] + '<div class="option-feedback"></div>\n                    </div>'
        return opt_html

    content = re.sub(
        r'<div class="option">[\s\S]*?</label>\s*</div>',
        add_feedback_to_option,
        content
    )

    # ── 3. 替换底部 result div（简化为只显示分数 + 重做按钮） ──
    old_result_pattern = r'<div class="result" id="result">[\s\S]*?<div id="explanations"></div>\s*</div>'
    new_result = '''<div class="result" id="result">
                    <div class="score" id="score"></div>
                    <div class="score-msg">答案解析已显示在每道题的选项旁边 ↑</div>
                    <button class="submit-btn" style="margin-top:16px;background:#667eea;" onclick="resetQuiz()">🔄 重新答题</button>
                </div>'''
    content = re.sub(old_result_pattern, new_result, content)

    # ── 4. 替换整个 <script> 块（explanations + checkAnswers） ──
    # 找到从 const explanations 到 checkAnswers 函数结束的整个 script 块
    script_pattern = r'<script>\s*const explanations\s*=\s*\{[\s\S]*?function checkAnswers\(\)\s*\{[\s\S]*?\}\s*</script>'
    new_js = build_new_js(explanations)
    content = re.sub(script_pattern, new_js.strip(), content)

    # ── 5. 移除旧的底部 explanations div（如果还存在） ──
    # 有些文件可能有残留的 <div id="explanations">
    content = re.sub(r'<div id="explanations"></div>', '', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True


def main():
    files = sorted(glob.glob(os.path.join(OUTPUT_DIR, "Day*.html")))
    print(f"找到 {len(files)} 个文件\n")

    success = 0
    for f in files:
        name = os.path.basename(f)
        print(f"处理: {name}")
        if process_file(f):
            success += 1
            print(f"  ✅ 完成")
        else:
            print(f"  ❌ 跳过")

    print(f"\n完成: {success}/{len(files)} 个文件已更新")


if __name__ == "__main__":
    main()
