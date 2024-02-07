import re
import os.path

path = ''
# print(os.path.exists(path))
while True:
    path = input("Please input the file name (with .py) > ")
    if (os.path.exists(path)):
        f = open(path, 'r')
        print("exist")
        break
    else:
        path = input("We can't find your file, please enter full path to the file > ")
        try:
            f = open(path, 'r')
            print("exist")
            print("Processing...")
            print("Done!")
            break
        except:
            print('Cannot find')

lines_0 = f.readlines()


def make_tabs(n):
    str = ""
    for i in range(n):
        str += "    "
    return str


def indent_space(x):
    str = "    "
    count = x.count(str)
    return count


lines_1 = []
code = []
elif_indent = 0
indent = 0
indent_old = 0

if len(lines_0) > 1:
    for i in range(0, len(lines_0)-1):
        lines_0[i] = lines_0[i][:-1]

for i in lines_0:
    indent = indent_space(i)
    if 'elif' in i:
        code.append(make_tabs(indent+elif_indent)+"else:")
        elif_indent += 1
    if indent_space(i)+1 < indent_old:
        elif_indent = 0
    code.append(make_tabs(elif_indent)+i)
    indent_old = indent
#     if 'elif' in z:
#         z = z.replace('elif', 'if')

code = [w.replace('elif', 'if') for w in code]
# for i in code:
#     print(i)
# print(1)

#--------------------------------------------------------- RETURN AS code
#
indentation = []

for x in range (0, len(code)):
    i = code[x]
    if 'input("' in i:
        indentation.append(indent_space(i))

        if " int(" in i:
            indentation.append(indent_space(i))
    indentation.append(indent_space(i))

code = [j.replace("    " ,'') for j in code]

arr = []

def find_string(line, obj):
	position = []
	value = 0
	for a in range (0, len(line)- len(obj) + 1):
		appearance = 0
		for b in range (0, len(obj)):
			if line[a+b] == obj[b]:
				appearance += 1

		if appearance == len(obj):
			for c in range (0, len(obj)):
				position.append(a+c)

			value = 1
			break

	if value == 1:
		return position[-1]

def not_in_string(line, obj):
	counter = 0

	for i in range (0, find_string(line, obj)+2-len(obj)):
		x = line[i]

		if x == "\"":
			counter += 1

		if counter % 2 == 0 and i == find_string(line, obj)+1-len(obj):
			return True

def make_capital(line, obj):
	res = list(line)
	last_letter_position = find_string(line, obj)

	for e in range (len(obj)):
		res[last_letter_position-e] = obj[len(obj)-e-1].capitalize()

	new_line = "".join(res)

	return new_line

def For(x:str):
	if "for " and " range(":
		list = x.split('range')
		identify = list[0]
		identify = identify.split(' ')
		identify = identify[1]
		list = list[1]
		list = list.replace('(','')
		list = list.replace(')','')

		res = list.split(',')

		#construction
		if len(res) == 1:
			return("FOR {} <-- 1 TO {}\n".format(identify,res[0]))
		elif len(res) == 2:
			return("FOR {} <-- {} TO {}\n".format(identify,res[0],res[1]))
		elif len(res) == 3:
			return("FOR {} <-- {} TO {} STEP {}\n".format(identify,res[0],res[1],res[2]))

fill = open("result.txt", "w")
func = 0

for i in code:

    i = i.replace("_", "")

    operations = ["+", "-", "/", "*"]

    for x in operations:
        change = x + "="
        variable = ""
        value = ""

        if change in i:
            for y in range (0, find_string(i, change)-2):
                variable += i[y]

            for y in range (find_string(i, change)+2, len(i)):
                value += i[y]

            variable_new = variable.lstrip()
            arr.append(variable + " <-- " + variable_new + " " + x + " " + value+"\n")

    if "input(" in i:
        prompt = ""
        variable = ""

        if i[-1] == ")" and i[-2] == ")":
            for x in range (find_string(i, "input")+2, len(i)-2):
                prompt += i[x]
        else:
            for x in range (find_string(i, "input")+2, len(i)-1):
                prompt += i[x]

        if prompt != "":
            arr.append("OUTPUT "+prompt+"\n")

        if "int" not in i:
            for x in range (0, find_string(i, "input")-7):
                variable += i[x]

            arr.append("INPUT "+variable+"\n")

        else:
            for x in range (0, find_string(i, "input")-11):
                variable += i[x]

            arr.append("INPUT "+variable+"\n")
            arr.append(variable + " <-- " + "STRING_TO_NUM(" + variable + ")"+"\n")

    else:
        if " = " in i:
            i = i.replace(" = ", " <-- ")
            arr.append(i+"\n")

    if "print(" in i:
        output = ""

        for x in range (find_string(i, "print")+2, len(i)-1):
            output += i[x]

        output = output.replace("+", ", ")
        arr.append("OUTPUT "+ output + "\n")

    if "def " in i:
        func = 1
        functional = i.split(" ")
        parameter = ""
        start_count = False
        for x in functional[1]:
            if x == ")":
                start_count = False
            if start_count:
                parameter += x
            if x == "(":
                start_count = True

        if parameter == "":
            action = functional[-1].replace("()", "")
            arr.append("PROCEDURE " + action + "\n")
        else:
            arr.append("FUNCTION " + functional[1]+"\n")

    if '(' in i and ')' in i and func == 1:
        lines = i.split('(')
        for x in functional:
            lists = x.split('(')
            if lists[0] == lines[0]:
                arr.append("CALL {}({}\n".format(lines[0], lines[1]))

    if "return" in i:
        i = make_capital(i, "return")
        arr.append(i+"\n")

    if "break" in i:
        arr.append("BREAK\n")

    if "continue" in i:
        arr.append("CONTINUE\n")

    logic = ["and", "or", "not"]
    for x in logic:
        if x in i and not_in_string(i, x) and i[find_string(i, x) - len(x)] == " ":
            i = make_capital(i, x)

    i = i.replace(" == ", " = ")
    i = i.replace(" % ", " MOD ")
    i = i.replace(" != ", " <> ")

    if "if " in i and not_in_string(i, "if"):
        arr.append(make_capital(i, "if")+"\n")

    if "else:" in i and not_in_string(i, "else"):
        arr.append(make_capital(i, "else")+"\n")

    if "for " in i and not_in_string(i, "for"):
        arr.append(For(i))

    if "while " in i and not_in_string(i, "while"):
        arr.append(make_capital(i, "while")+"\n")

    if i == "":
        arr.append(i + "\n")

arr = [w.replace(':', '') for w in arr]
arr = [make_tabs(indentation[i]) + arr[i] for i in range (0, len(arr))]

arr = [i.replace(' str(', ' NUM_TO_STRING(') for i in arr]
arr = [i.replace(' int(', ' STRING_TO_NUM(') for i in arr]



#--------------------------------------------------------- RETURN AS arr

stack = []
indent_stack = []

indent = 0

# for i in range(0, len(lines_1)-1):
#     lines_1[i] = lines_1[i][:-1]
# print(lines)

last_indent = indent_space(arr[-1])

for j in range(indent_space(arr[-1])+1, 0, -1):
    arr.append(make_tabs(j))


# print(lines)

code = []

for x in range(0, len(arr)):
    if indent_space(arr[x]) < indent:
        sub = indent - indent_space(arr[x])
        # print(sub)
        for i in range(sub, 0, -1):
            # print(i)
            # print(indent_stack)
            # print(indent_stack[-1])
            code.append(make_tabs(indent_stack[-1])+"END"+stack[-1].upper()+'\n')
            # print(code[-1])
            indent_stack.pop()
            # print(indent_stack)
            stack.pop()
    if 'FOR' in arr[x]:
        stack.append('for')
        indent_stack.append(indent_space(arr[x]))
    elif 'WHILE' in arr[x]:
        stack.append('while')
        indent_stack.append(indent_space(arr[x]))
    elif 'FUNCTION' in arr[x]:
        stack.append('function')
        indent_stack.append(indent_space(arr[x]))
    elif 'PROCEDURE' in arr[x]:
        stack.append('procedure')
        indent_stack.append(indent_space(arr[x]))
    elif 'IF' in arr[x]:
        stack.append('if')
        indent_stack.append(indent_space(arr[x]))
    elif 'ELSE' in arr[x]:
        stack.append('if')
        indent_stack.append(indent_space(arr[x]))
    code.append(arr[x])
    indent = indent_space(arr[x])

code_2 = code

for item in code_2:
    if not item.strip():
        code_2.remove(item)


endif = []

for k in range(0, len(code_2)):
    if 'WHILE ' in code_2[k]:
        code_2[k] = code_2[k][:-1] + " DO\n"
    if 'IF ' in code_2[k]:
        code_2[k] = code_2[k][:-1] + " THEN\n"
    if "ELSE" in code_2[k]:
        endif.append(k-1)


endif.reverse()

for z in endif:
    code_2.pop(z)

# print(code_2)


for z in code_2:
    fill.write(z)
