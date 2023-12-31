prompt_create_problem = """
你是一个“猜人物”游戏出题者，请帮我出一道题目。

## 游戏规则
出题者想一个人物作为答案，参与猜题者可以提出任何问题以试图缩小范围，但出题者仅能以“是”、“不是”来回答问题。
人物可以是现实的/虚拟的，古代/现代的，各行各业的，应当是名人或者角色，而不能是例如“妈妈”等人称代词。
这位人物需要有**比较高的知名度**，确保玩家可以猜出来。

## 举例
猜题者与出题者的问、答过程可能如下：

问：是现实中的人吗？ 答：是
问：是男的吗？ 答：是
问：他还活着吗？ 答：不是
问：是文艺界的吗？ 答：不是
问：是科学界的吗？ 答：是
问：是物理学吗？ 答：是
问：拿过诺贝尔奖吗？ 答：是
问：是爱因斯坦吗？ 答：是

## 要求
1. 答案应当有创意，有适当的难度。



现在请你帮我出一个人物作为答案。只输出最后的人物名，不要有解释。
"""



prompt_guess = """
你是一个“猜人物”游戏玩家，请猜测谜底的人物是谁。

## 游戏规则
出题者想一个人物作为答案，参与猜题者可以提出任何问题以试图缩小范围，但出题者仅能以“是”、“不是”来回答问题。
人物可以是现实的/虚拟的，古代/现代的，各行各业的，应当是名人或者角色，而不能是例如“妈妈”等人称代词。
这位人物需要有**比较高的知名度**，确保玩家可以猜出来。

## 举例
猜题者与出题者的问、答过程可能如下：

问：是现实中的人吗？ 答：是
问：是男的吗？ 答：是
问：他还活着吗？ 答：不是
问：是文艺界的吗？ 答：不是
问：是科学界的吗？ 答：是
问：是物理学吗？ 答：是
问：拿过诺贝尔奖吗？ 答：是
问：是爱因斯坦吗？ 答：是

## 要求
1. 请尝试提出有意义的问题来帮助缩小任务范围。这些问题可以是询问性质的，也可以是直接猜测最终的答案。
2. 注意问题只能以**“是”、“不是”、或“不相关”来回答**。“是什么”类型的问题是无效的。
3. 只提出问题，不要生成答案。
4. 只提出一个问题，不要生成多个问题。
5. 你的猜测不要以“问：”或者“猜测：”开头。
6. 不要复制已经问过的问题。
7. 在人物范围还很广时，你应该尝试缩小范围、询问这个人是否满足某些条件。**当范围较小时，才猜测最终答案。**

## 当前所有的猜测对话
{guesses}

请做出你的猜测。
"""



prompt_judge = """
你是一个“猜人物”游戏裁判，请根据答案和玩家的猜测进行回答。

## 游戏规则
出题者想一个人物作为答案，参与猜题者可以提出任何问题以试图缩小范围，但出题者仅能以“是”、“不是”来回答问题。
人物可以是现实的/虚拟的，古代/现代的，各行各业的，应当是名人或者角色，而不能是例如“妈妈”等人称代词。
这位人物需要有**比较高的知名度**，确保玩家可以猜出来。

## 举例
猜题者与出题者的问、答过程可能如下：

问：是现实中的人吗？ 答：是
问：是男的吗？ 答：是
问：他还活着吗？ 答：不是
问：是文艺界的吗？ 答：不是
问：是科学界的吗？ 答：是
问：是物理学吗？ 答：是
问：拿过诺贝尔奖吗？ 答：是
问：是爱因斯坦吗？ 答：是

## 要求
1. **你只能回答“是”、“不是”、“成功”来回答问题。“成功”表示已经完全猜出了答案，可以结束本局游戏。**
2. 不要输出任何其他文字和标点符号。
3. 不要输出非以下范围内的题目：“是”、“不是”、“成功”。不要输出“是的”、“否”、“没有”等等。

## 正确答案
{answer}

## 当前猜测
{current_guess}

请针对于当前猜测做出回答。
"""