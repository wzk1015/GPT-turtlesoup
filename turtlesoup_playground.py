import openai
import time
import traceback
import logging
import os
import json

from turtlesoup_prompts import prompt_create_problem, prompt_guess, prompt_judge


class TurtleSoup:
    def __init__(self, stream=True, response_max_tokens=2048, player_temperature=0.7, judge_temperature=0.7, create_problem_temperature=0.7, gpt_model="gpt-3.5-turbo-16k", max_iters=100):
        self.stream = stream
        self.response_max_tokens = response_max_tokens
        self.player_temperature = player_temperature
        self.judge_temperature = judge_temperature
        self.create_problem_temperature = create_problem_temperature
        self.gpt_model = gpt_model
        self.max_iters = max_iters
    
    def query_gpt_nostream(self, messages, temperature):
        server_error_cnt = 0
        if isinstance(messages, str):
            messages = {"role": "user", "content" : messages}
        while server_error_cnt < 3:
            try:
                response = openai.ChatCompletion.create(
                    model=self.gpt_model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=self.response_max_tokens,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    )
                response = response['choices'][0]['message']['content']
                return response
            except Exception as e:
                server_error_cnt += 1
                print(traceback.format_exc())
                time.sleep(pow(2, server_error_cnt))
        raise ValueError("Error with querying GPT")

    def query_gpt_stream(self, messages, temperature):
        server_error_cnt = 0
        if isinstance(messages, str):
            messages = {"role": "user", "content" : messages}
        full_response = ""
        while server_error_cnt < 3:
            try:
                for chunk in openai.ChatCompletion.create(
                    model=self.gpt_model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=self.response_max_tokens,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0, 
                    stream=self.stream,
                ):
                    content = chunk["choices"][0].get("delta", {}).get("content")
                    if content is not None:
                        print(content, end="", flush=True)
                        full_response += content
                print()
                full_response += "\n"
                return full_response
            except Exception as e:
                full_response = ""
                server_error_cnt += 1
                print(traceback.format_exc())
                time.sleep(pow(2, server_error_cnt))   
        raise ValueError("Error with querying GPT")

    def query_gpt(self, messages, temperature=0):
        if self.stream:
            return self.query_gpt_stream(messages, temperature)
        return self.query_gpt_nostream(messages, temperature)

    def format_guesses(self, guesses):
        out = ""
        for guess, judge in guesses:
            out += f"问: {guess}\n答: {judge}\n\n"
        return out
    
    def create_problem(self):
        response = self.query_gpt([{"role": "user", "content": prompt_create_problem}], temperature=self.create_problem_temperature).strip()
        try:
            ret = json.loads(response)
        except:
            raise ValueError(f"invalid response: {response}")
        problem, answer = ret["问题"], ret["答案"]
        return problem, answer
    
    def input_problem(self):
        problem = input('请输入题目: ').strip()
        answer = input('请输入答案: ').strip()
        return problem, answer
    
    def gpt_guess(self, problem, guesses):
        prompt = prompt_guess.format(
            problem=problem, 
            guesses=self.format_guesses(guesses)
        )
        guess = self.query_gpt([{"role": "user", "content": prompt}], temperature=self.player_temperature).strip()
        return guess
    
    def human_guess(self):
        guess = input('请输入你的问题或猜测: ').strip()
        return guess
    
    def gpt_judge(self, problem, guesses, current_guess, answer):
        prompt = prompt_judge.format(
            problem=problem, 
            guesses=self.format_guesses(guesses),
            current_guess=current_guess,
            answer=answer
        )
        judge = self.query_gpt([{"role": "user", "content": prompt}], temperature=self.judge_temperature).strip().strip("。")
        assert judge in ["是", "不是", "不相关", "成功", "退出"], f"Uknown judge: {judge}"
        return judge
    
    def human_judge(self):
        judge = input('请回答"是","不是","不相关","成功"或"退出"，或者用y,n,x,w,q代替，或者直接打字表示提示: ').strip().lower()
        if judge in ["q", "退出"]:
            return "退出"
        elif judge in ["w", "退出"]:
            return "成功"
        elif judge in ["y", "是"]:
            return "是"
        elif judge in ["n", "不是"]:
            return "不是"
        elif judge in ["x", "不相关"]:
            return "不相关"
        raise ValueError(f"Unknown judgement: {judge}")
    
    def run(self, gpt_play=False, gpt_judge=True, gpt_problem=True, problem=None, answer=None):
        if gpt_play:
            print("GPT作为玩家")
        if gpt_judge:
            print("GPT作为裁判")
        
        if problem is not None:
            assert answer is not None
            print(f"题目: {problem}")
        elif gpt_problem:
            print("GPT生成题目...")
            problem, answer = self.create_problem()
        else:
            problem, answer = self.input_problem()
        
        guesses = []
        i = 0
        while True:
            print("问: ", end="")
            if gpt_play:
                guess = self.gpt_guess(problem, guesses)
            else:
                guess = self.human_guess()
                
            print("答: ", end="")
            if gpt_judge:
                judge = self.gpt_judge(problem, guesses, guess, answer)
            else:
                judge = self.human_judge()
            guesses.append([guess, judge])
            assert judge in ["是", "不是", "不相关", "成功", "退出"]
            if judge == "成功":
                print("成功解决！")
                print(f"答案: {answer}")
                break
            elif judge == "退出" or i >= self.max_iters:
                print("退出")
                print(f"答案: {answer}")
                break
            
            
    def run_player(self, gpt_problem=True, problem=None, answer=None):
        return self.run(gpt_play=True, gpt_judge=False, gpt_problem=gpt_problem, problem=problem, answer=answer)
    
    def run_judge(self, gpt_problem=True, problem=None, answer=None):
        return self.run(gpt_play=False, gpt_judge=True, gpt_problem=gpt_problem, problem=problem, answer=answer)
    
    def run_both(self, gpt_problem=True, problem=None, answer=None):
        return self.run(gpt_play=True, gpt_judge=True, gpt_problem=gpt_problem, problem=problem, answer=answer)
    
            

if __name__ == "__main__":
    with open("openai_key.txt") as f:
        openai.api_key = f.read()
    
    turtle_soup = TurtleSoup(gpt_model="gpt-4")
    # turtle_soup.create_problem()
    # problem = """他是一个人体画家，而曾经的模特不能再给他帮忙了，正当他缺乏灵感的时候，他收到了一封匿名信，信上的人为他提供了几组照片，并索要酬劳。画家拿到照片获得了灵感，很快又有了作品。他把钱打到约定的账户，没多久又收到新的照片，但每次要求的汇款方式都不同。那一天他又收到了信，当他看到内容后他吓疯了。
    # """
    # answer = """人体画家曾经用自己的老婆当模特，但是他老婆有自己的理想不愿意再当，他一怒之下杀死了妻子，并且保存着尸体继续给自己当模特。等到尸体腐败a不堪后，他又画不出画了。他不知道妻子有一个双胞胎a妹妹，妹妹发现姐姐失联了很快知道了内幕，于是妹妹给画家寄了自己的照片，但是脸上都打了马赛克a，画家看到这个模特和自己的老婆身材几乎一模一样，又来了灵感。最后一次妹妹寄来的照片没有把脸打码，而汇款方式也要求是烧纸，画家以为他的老婆复活了，于是吓疯了。
    # """
    
    problem = """一女子某晚进了公厕，里面的灯很昏暗,只见厕所里刚好还有一人，女子打了声招呼便匆忙地进了隔间，第二天，警察因昨晚相同时间厕所发生了杀人案而找上她，质问了她当时为什么没有报警，请推理。
    """
    answer = """凶手在厕所刚杀完人，就听见外面有人进来，为了不暴露，打扮成了在拖地的清洁工，由于灯光的昏暗，女子打招呼所看到的拖地清洁工，其实是凶手倒立着死者，用死者的头发在拖地。
    """
    turtle_soup.run_both(problem=problem, answer=answer)