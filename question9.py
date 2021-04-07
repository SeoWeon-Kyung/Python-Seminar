import sys
data = sys.argv
print("Prompt에 입력한 것들:", data)

result = 0
for i in data:
    try:
        result += int(i)
    except (ValueError):
        pass

print(result)
    