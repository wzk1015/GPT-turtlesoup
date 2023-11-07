import openai
import argparse

from turtlesoup_playground import TurtleSoup
from guessperson_playground import GuessPerson


parser = argparse.ArgumentParser("GPT turtlesoup")
parser.add_argument("--game", type=str, default="turtle_soup")
parser.add_argument("--gpt_model", type=str, default="gpt-4")
parser.add_argument("--key_path", type=str, default="openai_key.txt")
parser.add_argument("--gpt_play", action="store_true")
parser.add_argument("--gpt_judge", action="store_true")
parser.add_argument("--gpt_problem", action="store_true", default=True)
parser.add_argument("--problem_path", type=str, default=None)
parser.add_argument("--max_iters", type=int, default=100)

args = parser.parse_args()

with open(args.key_path) as f:
    openai.api_key = f.read()



if args.game == "turtle_soup":
    if args.problem_path:
        with open(args.problem_path) as f2:
            lines = f2.readlines()
        problem, answer = lines[0].strip(), lines[1].strip()
    else:
        problem, answer = None, None
    turtle_soup = TurtleSoup(gpt_model=args.gpt_model, max_iters=args.max_iters)
    turtle_soup.run(
        gpt_play=args.gpt_play, 
        gpt_judge=args.gpt_judge, 
        gpt_problem=args.gpt_problem,
        problem=problem,
        answer=answer
    )
    
elif args.game == "guess_person":
    if args.problem_path:
        with open(args.problem_path) as f2:
            answer = f2.read().strip()
    else:
        answer = None
    guess_person = GuessPerson(gpt_model=args.gpt_model, max_iters=args.max_iters)
    guess_person.run(
        gpt_play=args.gpt_play, 
        gpt_judge=args.gpt_judge, 
        gpt_problem=args.gpt_problem,
        answer=answer
    )