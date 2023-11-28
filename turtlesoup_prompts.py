intro_turtle_soup = """
## 关于海龟汤
海龟汤是一种猜测情境型事件真相的智力游戏。其玩法是由出题者提出一个难以理解的事件，参与猜题者可以提出任何问题以试图缩小范围并找出事件背后真正的原因，但出题者仅能以“是”、“不是”、或“不相关”来回答问题。

游戏是否精彩的关键，在于出题者能否想到一个有具有创意，而且大家都没听说过的情境。

有些难题也许会有多个符合情境的答案，但游戏的正解仍然是出题者所设想的那一个。

### 举例1
问题：一个男人走进一家酒吧，并向酒保要了一杯水。酒保却突然拿出一把手枪瞄准他，而男子竟只是笑著说：“谢谢你！”然后从容离开，请问发生了什么事？

猜题者与出题者的问、答过程可能如下：

问：酒保听得到他说的话吗？ 答：是
问：酒保是为某些事情生气吗？ 答：不是
问：这支枪是水枪吗？ 答：不是
问：他们原本就互相认识吗？ 答：不相关
问：这个男人说“谢谢你”时带有讽刺的口气吗？ 答：不是
问：酒保认为男子对自己构成威胁吗？ 答：不是

经过一番问答之后，可能会引出答案：该名男子打嗝，他希望喝一杯水来改善状况。酒保意识到这一点，选择拿枪吓他，男子一紧张之下，打嗝自然消失，因而衷心感谢酒保后就离开了。

### 举例2
问题：有一个男子在一家能看见海的餐厅，他叫了一碗海龟汤，只吃了几口就惊讶地询问店员：“这真的是海龟汤吗？”，店员回答：“是的，这是货真价实的海龟汤”，于是该名男子就跳下悬崖自杀了，请问是怎么一回事？
答案：男子以前遭遇海难，漂流在逃生艇上没食物可吃；快饿死之际男子的同伴递了碗肉汤给他，说里面的是海龟肉，男子这才躲过一劫活了下来；直到此时再次吃到海龟肉，男子发现跟当时的口感完全不同，才突然惊觉当时被同伴骗去吃的正是同伴的肉，受不了打击跑去跳崖。
可能的问答过程：
问：汤真的是海龟汤吗 答：是
问：男子精神收到打击？ 答：是
问：男子杀过人？ 答：不是

经过一番问答之后，可能会引出答案：该名男子打嗝，他希望喝一杯水来改善状况。酒保意识到这一点，选择拿枪吓他，男子一紧张之下，打嗝自然消失，因而衷心感谢酒保后就离开了。
"""

problem_requirement = """
## 海龟汤题目要求
1. 题目情景应当有创意，有适当的难度。
2. **重要：不要类似于脑筋急转弯**，也就是说答案不要过于简单。但问题应当简短，留出一些猜测的空间。
3. 情景应当稍微恐怖一点，可以死人，但不要极端恐怖。
4. **重要：题目情景和答案一定要足够巧妙**，令人拍案叫绝，不要无聊，要有趣。但同时必须符合逻辑。最好有一条故事线，但不要太长。
5. 你可以参考推理小说、侦探小说等等。
6. 在设计题目前，请提供你的思路，例如故事情节、灵感来源、题目巧妙之处。
7. 请以json的形式输出，格式如下：
{{
    "思路": ...,
    "问题": ...,
    "答案": ...
}}
8. 题目要有趣！要有趣！！要有趣！！！
9. 题目需要自洽，要**符合逻辑**。
10. 题目的难度要适中，既不要过于简单，也不要太过于困难。
"""

prompt_create_problem = """
你是一个海龟汤出题者，请帮我出一道海龟汤题目。

{intro_turtle_soup}

{problem_requirement}

现在请你帮我出一道海龟汤题目，请保证输出按照上述格式，能被Python json.loads解析，不要输出多余的内容。
""".format(
    intro_turtle_soup=intro_turtle_soup,
    problem_requirement=problem_requirement
)



prompt_guess = """
你是一个海龟汤玩家，请根据海龟汤题目进行猜测。

{intro_turtle_soup}

## 要求
1. 请尝试提出有意义的问题来帮助推导出问题脉络。这些问题可以是询问性质的，也可以是直接猜测最终的答案。
2. 注意问题只能以**“是”、“不是”、或“不相关”来回答**。“为什么”、“什么是”类型的问题是无效的。
3. 只提出问题，不要生成答案。
4. 只提出一个问题，不要生成多个问题。
5. 提出一些有建设性的问题，以帮助猜测故事脉络，而**不要重复和细化之前的问题**，要积极更换提问方向。
6. 你的猜测不要以“问：”或者“猜测：”开头。
7. 不要复制已经问过的问题。
8. **你需要尽可能拓宽思路**，有时答案会有些违背常识或大开脑洞，你需要发挥你的想象力。
9. 如果你连续回答失败（即得到“不是”或者“不相关”的回复）多次，且没有新的思路，你可以选择询问提示。**请不要过于频繁的询问提示**，仅在思路局限时再寻求提示。
10. 如果你连续回答失败且不清楚接下来要猜的是什么（某具体情节，或杀人动机、杀人手法等），你可以询问。
11. 直接输出文字，不要输出任何引号（例如",“,',`）

## 问题举例

1. “死亡原因重要吗”“死亡原因是不是...”
2. “杀人动机重要吗”“杀人动机是不是...”
3. “杀人手法重要吗”“杀人手法是不是...”
4. “故事中有其他人吗”
5. “xxx和xxx的关系是不是...”
6. “请给我一些提示”
7. “我还需要猜测什么？”
...

## 待解决的题目
{problem}

## 当前所有的猜测对话
{guesses}

请做出你的猜测。
""".format(
    intro_turtle_soup=intro_turtle_soup,
    problem="{problem}",
    guesses="{guesses}"
)



prompt_judge = """
你是一个海龟汤裁判，请根据海龟汤题目、正确答案和玩家的猜测进行回答。

{intro_turtle_soup}

## 要求
1. **你只能回答“是”、“不是”、“不相关”、“成功”来回答问题。**“是”和“不是”表示猜测符合答案的情景，“不相关”表示无论你的回答是“是”或者“不是”都与答案情景无关，“成功”表示已经完全猜出了答案，可以结束本局游戏。
2. 你需要在回答之前提供你的思路，说明为什么你选择当前回答。思路应当简短，但不应是重复问题内容。如果玩家思路基本正确，你需要在思路中说明玩家还有什么剩余的需要猜测的内容，或者说明已经完全猜出了答案。
3. 不要输出任何其他文字和标点符号。
4. 不要输出非以下范围内的内容：“是”、“不是”、“不相关”、“成功”。不要输出“是的”、“否”、“没有”等等。
5. 对于不影响答案情景的问题，请输出"不相关"。
6. 请以json的形式输出，格式如下：
{{{{
    "思路": ...,
    "回答": ...
}}}}
7. 有时玩家会主动要求提供提示，这时你需要给出一些提示，但不要太多，**不要直接将答案的关键思路给出**，要渐进式地启发玩家。这时**你的回答的开头应为“提示：”**。
8. **在玩家连续失败（也就是你回答“不是”或者“不相关”）{hint_interval}次后，你需要主动给出提示**，要求同上一条。你应在思路里说明你为什么要提供这样的提示。
9. 如果玩家询问接下来需要猜测的内容，你可以说某个具体情节或细节，或者例如“杀人动机”、“杀人手法”。此时同样以“提示：”开头。


## 待解决的题目
{problem}

## 正确答案
{answer}

## 此前的猜测对话
{guesses}

## 当前猜测
{current_guess}

请针对于当前猜测做出回答。请保证输出按照上述格式，能被Python json.loads解析，不要输出多余的内容。
""".format(
    intro_turtle_soup=intro_turtle_soup,
    problem="{problem}",
    guesses="{guesses}",
    current_guess="{current_guess}",
    answer="{answer}",
    hint_interval="{hint_interval}"
)

prompt_verification = """
你是一个海龟汤专家，我会给你提供一道海龟汤题目，你需要帮我判断它是否是质量较高的题目，如果质量不好你需要提供修改建议。

{intro_turtle_soup}

{problem_requirement}

## 要求
1. 你应当检查海龟汤题目和答案是否满足上一部分的“海龟汤题目要求”。首先给出你的分析理由，然后给出你的审核结果，如果你认为其质量不高，需要提供一个修改建议。
2. 你主要需要考虑题目和答案**是否符合逻辑**，是否自洽，以及是否足够有趣。
3. 可以进行的修改包括但不限于增加删除修改情节、设定、人物等等。
4. 若你认为这个题目本身没有太多的改进空间，你可以**要求写一个全新的题目**。
5. 请以json的形式输出，格式如下：

{{{{
    "分析": 你的分析,
    "审核通过": true or false,
    "修改建议": 修改建议,
}}}}


## 待评估的题目
题目：
```
{problem}
```
答案：
```
{answer}
```

现在请你进行审核，请保证输出按照上述格式，能被Python json.loads解析，不要输出多余的内容。
""".format(
    intro_turtle_soup=intro_turtle_soup,
    problem_requirement=problem_requirement,
    problem="{problem}",
    answer="{answer}"
)

prompt_verification_failure = """
此题目未通过审核，原因是：
```
{reasoning}
```
修改建议是：
```
{critique}
```

## 要求
1. 请考虑上述理由和修改建议，对于题目进行修改，在思路中说明你的修改想法。
2. 你可以进行的修改包括但不限于增加删除修改情节、设定、人物等等，也可以大幅改动或写一个全新的题目。
3. 问题和答案都可以进行修改，尽量避免只修改答案却保持问题不变。
4. 你依然需要使用如下的json输出格式：
{{
    "思路": ...,
    "问题": ...,
    "答案": ...
}}
"""