import sys
import parser
import planner
import executor

def main():
    if len(sys.argv) < 2:
        print("Usage: python try.py 'your command here'")
        return

    user_input = " ".join(sys.argv[1:])

    # Signal start of agent execution for the GUI
    print("[NEURO_START]", flush=True)

    print(f"\n🧠 User Input:\n{user_input}\n")

    parsed = parser.parse_intent(user_input)
    print(f"\n🔍 Parsed Intent:\n{parsed}\n")

    steps = planner.plan_steps(parsed)
    print(f"\n🪜 Planned Steps:\n{steps}\n")

    executions = executor.execute_steps(steps, parsed)
    print(f"\n⚙️ Execution Results:")
    for i, result in enumerate(executions, 1):
        print(f"\nStep {i}: {result['description']}")
        print(f"Command: {result['executableCommand']}")
        print(f"Output:\n{result['output']}")
        print(f"✅ Success: {result['isDone']}")

    # Signal end of agent execution for the GUI
    print("[NEURO_END]", flush=True)

if __name__ == "__main__":
    main()
