import docker

# Connects to the local Docker daemon
client = docker.from_env()


def execute_code(code: str) -> dict:
    """
    Spins up a temporary Docker container, runs the code, and destroys the container.
    """
    try:
        print("--> Spawning isolated Docker container...")

        output = client.containers.run(
            image="python:3.12-slim",
            command=["python", "-c", "import os; exec(os.environ['USER_CODE'])"],
            environment={"USER_CODE": code},
            mem_limit="128m",
            network_disabled=True,
            remove=True,  # Crucial: Automatically deletes the container when finished
            stdout=True,
            stderr=True
        )

        return {
            "status": "COMPLETED",
            "output": output.decode("utf-8").strip(),
            "error": None
        }

    except docker.errors.ContainerError as e:
        # This catches errors in the USER's code (e.g., SyntaxError, ZeroDivisionError)
        return {
            "status": "FAILED",
            "output": None,
            "error": e.stderr.decode("utf-8").strip()
        }
    except Exception as e:
        # This catches system errors (e.g., Docker daemon offline)
        return {
            "status": "FAILED",
            "output": None,
            "error": str(e)
        }


# --- Local Test Block ---
if __name__ == "__main__":
    test_code = """
print('Hello from inside the isolated Docker container!')
x = 10 * 5
print(f'Calculation: 10 * 5 = {x}')
"""
    result = execute_code(test_code)
    print("\n--- Execution Result ---")
    print(result)