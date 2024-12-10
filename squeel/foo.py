from pathlib import Path
import subprocess
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

PY_LANGUAGE = Language(tspython.language())

parser = Parser(PY_LANGUAGE)


python = """\
def foo():
    if bar:
        baz()

def kitty():
    pass
"""

# print(python)


tree = parser.parse(bytes(python, "utf8"))

# print(str(tree.root_node))

query = PY_LANGUAGE.query(
    """
    (function_definition) @funcs
    """
)


caps = query.captures(tree.root_node)
start = caps["funcs"][1].start_byte
end = caps["funcs"][1].end_byte
foo = python[start:end]
# print(foo)


def format_sql(sql_code):
    try:
        # Run pg_format using subprocess
        result = subprocess.run(
            ["pg_format"],  # Command
            input=sql_code.encode(),  # Provide SQL code as input (encoded to bytes)
            stdout=subprocess.PIPE,  # Capture standard output
            stderr=subprocess.PIPE,  # Capture standard error
        )

        # Check for errors
        if result.returncode != 0:
            print(f"Error: {result.stderr.decode()}")
            return None

        # Return formatted SQL
        return result.stdout.decode()
    except FileNotFoundError:
        print("Error: pg_format is not installed or not in PATH.")
        return None


def get_matching_files_and_bytes_lazy(dir: str, pattern: str):
    for file in Path(dir).rglob(pattern):
        print("ello?")
        print(file.name)


get_matching_files_and_bytes_lazy("test", "*.py")


# sql = """
# SELECT id,name FROM users WHERE id=1;
# """
# formatted_sql = format_sql(sql)
# print(formatted_sql)
