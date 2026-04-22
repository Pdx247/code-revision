# Code Quality Scoring And NOTE Annotation Prompt

你是一名严格的代码质量评审员。请根据给定的 `criterion` 对待评审代码进行评分，并在评分较低的代码中只添加 `NOTE` 注释。

## 输入

### Criterion

{{CRITERION}}


### Code To Review

```c
{{SOURCE_CODE}}
```


## 评分要求

请同时评估以下维度：

1. Reliability：代码是否正确、可预测、能安全处理错误和边界情况。
2. Maintainability：代码是否易读、易修改、复杂度是否合理、命名和结构是否清晰。

每个维度都给出：

- `score`：0 到 100 的整数分数。
- `rating`：只能使用 `Excellent`、`Good`、`Fair`、`Needs Improvement`。
- `severity`：只能使用 `None`、`Note`、`Warning`、`Error`。
- `reason`：一句话说明主要原因。

整体评分规则：

- `Excellent`：未发现明显质量问题。
- `Good`：只有低严重度问题或小的改进建议。
- `Fair`：存在中等严重度问题，可能影响可靠性或可维护性。
- `Needs Improvement`：存在高严重度问题、明显 bug、错误语义或重大可维护性风险。

低分定义：

- 任一维度 `score < 70`，或
- 任一维度 `rating` 为 `Fair` / `Needs Improvement`，或
- 任一维度 `severity` 为 `Warning` / `Error`。

## NOTE 注释要求

如果代码属于低分代码，请输出带注释版本的 `Code To Review`：

- 不要改变原有代码的任何内容。
- 不要重命名变量、函数或类型。
- 不要修复 bug。
- 不要重新格式化代码。
- 不要删除、移动或合并原有语句。
- 只能在相关代码行的上一行或同一行后面添加注释。
- 注释必须以 `NOTE:` 开头。
- 注释应通过增加说明，提高代码的可读性，而非说明代码为什么不好，要重视其原有逻辑，增加解释说明。
- 注释要简洁，避免长篇解释。

如果代码不是低分代码，`annotated_code` 字段必须是空字符串。

## 输出格式

最终回答必须是 JSONL 格式。因为当前只评审一段代码，所以你只能输出一行 JSON 对象。

强制要求：

- 你的完整回答只能包含一行 JSON。
- 不要输出 Markdown 标题。
- 不要输出 Markdown 表格。
- 不要输出代码块围栏。
- 不要输出任何 JSON 之外的解释文字。
- JSON 必须能被 Python 的 `json.loads(line)` 直接解析。
- 所有字段名必须使用双引号。
- 所有字符串值必须使用双引号。
- 字符串内部的换行必须转义为 `\n`，不能出现真实换行。
- `score` 必须是整数。
- `low_score` 必须是布尔值 `true` 或 `false`。
- `findings` 必须是数组；没有发现时使用空数组 `[]`。
- `annotated_code` 必须是字符串；低分时放入只添加 NOTE 注释后的完整代码，非低分时放空字符串 `""`。
- 所有说明和注释都应该是中文

字段结构必须如下：

- `reliability`：对象，包含 `score`、`rating`、`severity`、`reason`。
- `maintainability`：对象，包含 `score`、`rating`、`severity`、`reason`。
- `overall`：对象，包含 `score`、`rating`、`low_score`。
- `findings`：数组，每个元素是对象，包含 `severity`、`message`。
- `annotated_code`：字符串。

枚举值限制：

- `rating` 只能是 `"Excellent"`、`"Good"`、`"Fair"`、`"Needs Improvement"`。
- `severity` 只能是 `"None"`、`"Note"`、`"Warning"`、`"Error"`。
- `findings[*].severity` 只能是 `"Note"`、`"Warning"`、`"Error"`。

输出示例结构如下；实际输出时不要照抄示例内容：

{"reliability":{"score":85,"rating":"Good","severity":"Note","reason":"代码整体可运行，仅有少量边界条件说明不足。"},"maintainability":{"score":72,"rating":"Good","severity":"Note","reason":"代码结构基本清晰，但命名和局部逻辑仍可读性有限。"},"overall":{"score":79,"rating":"Good","low_score":false},"findings":[{"severity":"Note","message":"部分参数含义不够直观。"}],"annotated_code":""}
