import dis

with open("app/routers/__pycache__/categories.cpython-313.pyc", "rb") as f:
    f.seek(16)  # Skip the header (magic number, timestamp, etc.)
    bytecode = f.read()

dis.dis(bytecode)
