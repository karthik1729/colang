from .start_tool import run
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m agentman.run.tool <toolname>")
    else:
      run(sys.argv[1])