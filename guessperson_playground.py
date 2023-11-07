import openai
import time
import traceback
import logging
import os
import json

from guessperson_prompts import prompt_create_problem, prompt_guess, prompt_judge
from turtlesoup_playground import TurtleSoup


class GuessPerson(TurtleSoup):
    def create_problem(self):
        answer = self.query_gpt([{"role": "user", "content": prompt_create_problem}], temperature=self.create_problem_temperature).strip()
        return answer
    
    def input_problem(self):
        answer = input('请输入答案: ').strip()
        return answer
    
    def gpt_guess(self, guesses):
        prompt = prompt_guess.format(
            guesses=self.format_guesses(guesses)
        )
        guess = self.query_gpt([{"role": "user", "content": prompt}], temperature=self.player_temperature).strip()
        return guess
    
    def human_guess(self):
        guess = input('请输入你的问题或猜测: ').strip()
        return guess
    
    def gpt_judge(self, current_guess, answer):
        prompt = prompt_judge.format(
            current_guess=current_guess,
            answer=answer
        )
        judge = self.query_gpt([{"role": "user", "content": prompt}], temperature=self.judge_temperature).strip().strip("。")
        assert judge in ["是", "不是", "成功", "退出"], f"Uknown judge: {judge}"
        return judge
    
    def human_judge(self):
        judge = input('请回答"是","不是","成功"或"退出"，或者用y,n,x,z,w,q代替，或者直接打字表示提示: ').strip().lower()
        if judge in ["q", "退出"]:
            return "退出"
        elif judge in ["w", "退出"]:
            return "成功"
        elif judge in ["y", "是"]:
            return "是"
        elif judge in ["n", "不是"]:
            return "不是"
        raise ValueError(f"Unknown judgement: {judge}")
    
    def run(self, gpt_play=False, gpt_judge=True, gpt_problem=True, answer=None):
        if gpt_play:
            print("GPT作为玩家")
        if gpt_judge:
            print("GPT作为裁判")
        
        if answer is not None:
            pass
        elif gpt_problem:
            print("GPT生成题目...")
            answer = self.create_problem()
        else:
            answer = self.input_problem()
        
        guesses = []
        i = 0
        while True:
            print("问: ", end="")
            if gpt_play:
                guess = self.gpt_guess(guesses)
            else:
                guess = self.human_guess()
                
            print("答: ", end="")
            if gpt_judge:
                judge = self.gpt_judge(guess, answer)
            else:
                judge = self.human_judge()
            guesses.append([guess, judge])
            assert judge in ["是", "不是", "成功", "退出"]
            if judge == "成功":
                print("成功！")
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
    
    guess_person = GuessPerson(gpt_model="gpt-4")
    guess_person.run_both(answer="姚明")