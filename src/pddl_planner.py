import subprocess

def plan():

    #cmd = ["pyperplan", "pddl/domain.pddl", "pddl/problem.pddl"]
    # updates: since plan.py lives in src/, go up one level to reach the sibling pddl/ folder
    cmd = ["pyperplan", "../pddl/domain.pddl", "../pddl/problem.pddl"]

    print("▶ Running PDDL planner:", " ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Error calling planner:\n", res.stderr)
    else:
        print("Plan found:\n", res.stdout)

if __name__ == "__main__":
    plan()