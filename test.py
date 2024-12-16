import subprocess

def generate_requirements(modules, output_file="requirements.txt"):
    """
    Generate a requirements.txt file with the installed versions of the specified modules.

    Args:
        modules (list): List of module names to include in the requirements file.
        output_file (str): The output file name for requirements.txt.
    """
    requirements = []

    for module in modules:
        try:
            # Get the version of the installed module
            result = subprocess.run(
                ["pip", "show", module], capture_output=True, text=True
            )
            if result.returncode == 0:
                for line in result.stdout.split("\n"):
                    if line.startswith("Version:"):
                        version = line.split(": ")[1]
                        requirements.append(f"{module}=={version}")
                        break
            else:
                print(f"Module {module} not found.")
        except Exception as e:
            print(f"Error retrieving version for {module}: {e}")

    # Write to the output file
    with open(output_file, "w") as f:
        f.write("\n".join(requirements))

    print(f"Requirements written to {output_file}")

# List of modules from your script
modules = [
    "datetime", "flask", "os", "pandas", "gensim", "numpy", "nltk",
    "sklearn", "fitz", "groq", "re", "csv", "pinecone", "sentence-transformers",
    "snowflake-connector-python", "uuid", "redis"
]

# Generate the requirements.txt file
generate_requirements(modules)