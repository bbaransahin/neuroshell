import sys
import parser
import planner
import executor

GRAY = "\033[90m"
RESET = "\033[0m"

def main():
    if len(sys.argv) < 2:
        print("Usage: python try.py 'your command here'")
        return

    user_input = " ".join(sys.argv[1:])

    # Signal start of agent execution for the GUI
    print("[NEURO_START]", flush=True)

    print(f"{GRAY}\nUser Input:\n{user_input}\n{RESET}")

    parsed = parser.parse_intent(user_input)
    print(f"{GRAY}Parsed Intent{RESET}")
    for key, value in parsed.items():
        print(f"{GRAY}{key}: {value}{RESET}")
    print(f"{GRAY}{'-'*32}{RESET}")

    steps = planner.plan_steps(parsed)
    print(f"{GRAY}Steps{RESET}")
    for step in steps:
        print(f"{GRAY}{step}{RESET}")
    print(f"{GRAY}{'-'*32}\nExecution Results:{RESET}")

    for i, result in enumerate(executor.stream_execute_steps(steps, parsed), 1):
        print(
            f"{GRAY}\nStep {i}: {result['description']}\n"
            f"Command: {result['executableCommand']}\n"
            f"Output:\n{result['output']}\n"
            f"Success: {result['isDone']}{RESET}",
            flush=True,
        )

    # Signal end of agent execution for the GUI
    print("[NEURO_END]", flush=True)

if __name__ == "__main__":
    main()
