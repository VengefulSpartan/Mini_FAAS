import subprocess
import os
import uuid

# Define the root of your project for volume mounting
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def execute_code(code: str, language: str):
    unique_id = str(uuid.uuid4())[:8]

    # 1. Define configurations FIRST
    configs = {
        "python": {"file": f"script_{unique_id}.py", "run": ["python3", f"script_{unique_id}.py"]},
        "c": {"file": f"prog_{unique_id}.c", "compile": ["gcc", f"prog_{unique_id}.c", "-o", f"out_{unique_id}"],
              "run": [f"./out_{unique_id}"]},
        "cpp": {"file": f"prog_{unique_id}.cpp", "compile": ["g++", f"prog_{unique_id}.cpp", "-o", f"out_{unique_id}"],
                "run": [f"./out_{unique_id}"]},
        "java": {"file": "Solution.java", "compile": ["javac", "Solution.java"], "run": ["java", "Solution"]}
    }

    config = configs.get(language, configs["python"])
    filename = config["file"]
    binary_name = f"out_{unique_id}" if "compile" in config else None

    # 2. Define the Docker Base (using absolute path for the volume)
    # Ensure you've run 'sudo usermod -aG docker $USER' so you don't need 'sudo' here
    docker_base = ["docker", "run", "--rm", "-v", f"{BASE_DIR}:/app", "minifaas-polyglot-engine"]

    # 3. Write the code to the root directory
    file_path = os.path.join(BASE_DIR, filename)
    with open(file_path, "w") as f:
        f.write(code)

    try:
        # 4. Compilation Step (C/C++/Java)
        if "compile" in config:
            compile_cmd = docker_base + config["compile"]
            c_res = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=15)
            if c_res.returncode != 0:
                return {"status": "FAILED", "output": "", "error": c_res.stderr}

        # 5. Execution Step
        run_cmd = docker_base + config["run"]
        r_res = subprocess.run(run_cmd, capture_output=True, text=True, timeout=15)

        return {
            "status": "COMPLETED" if r_res.returncode == 0 else "FAILED",
            "output": r_res.stdout,
            "error": r_res.stderr
        }

    except Exception as e:
        return {"status": "FAILED", "output": "", "error": str(e)}

    finally:
        # 6. Cleanup files from the root directory
        if os.path.exists(file_path):
            os.remove(file_path)
        if binary_name and os.path.exists(os.path.join(BASE_DIR, binary_name)):
            os.remove(os.path.join(BASE_DIR, binary_name))
        # Java cleanup for .class files
        if language == "java" and os.path.exists(os.path.join(BASE_DIR, "Solution.class")):
            os.remove(os.path.join(BASE_DIR, "Solution.class"))