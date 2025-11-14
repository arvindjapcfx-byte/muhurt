
filename = "example.txt"

content = "This file was created by a Python script running in GitHub Actions."

with open(filename, "w") as f:
    f.write(content)

print(f"File '{filename}' created successfully!")
