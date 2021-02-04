import string
import os

error_str = ["operator can't be end of line","expected ')'"]

operators = ['(',')','&','$','@','!','%','^','/','*','+','-']
#operators = ['[',']','+']

error_code = -1
END_VALUE = 'Q'

def factorial(num, sum = 1):
	if(num == 1):
		return sum
	return factorial(num-1,sum*num)

def operate(equation, index, strength):
	# list of only numbers
	tmp = equation[:]
	digits = []
	var = ''
	for ch in tmp:
		if ch == '-' and not var:
			var += str(ch)
		elif str(ch).isdigit():
			var += str(ch)
			
		else:
			if var:
				digits.append(var)
			var = ''
	if var:
		digits.append(var)
	# result
	operator = operators[strength]
	duo_operator = True 
	if operator == '!':
		duo_operator = False
	
	result = 0
	nums_indices = []
	count = 0
	# iterate over equation str
	for i in range(len(equation)):
		# if char on index is operator
		if equation[i] in operators:
			# if index is of our operator
			if i == index:
				if not duo_operator and i and equation[i-1] in operators:
					if operator == '!':
						raise SyntaxError("Expected value before '!'")
					count-=1				
				
				# duo operators can't start 
				duo_operator = duo_operator and i
				
				if duo_operator:
					nums_indices.append(i - len(digits[count]))
					nums_indices.append(i + len(digits[count+1]) + 1)
				else:
					if operator  == '!':
						nums_indices.append(0)
						nums_indices.append(i + 1)
					if operator == '-':
						nums_indices.append(i - len(digits[count]))
						nums_indices.append(0)
				
				print('opI ' + str(count))
				print('I ' + str(i))
				print('operator ' + operator)
				print('duo? ' + str(duo_operator))
				print(digits)

				nums_indices.append(i)
				if duo_operator:
					values = [int(digits[count]), int(digits[count + 1])]
				else:
					if operator == '!':
						values = [int(digits[count]), 0]
					if operator == '-':
						values = [0, int(digits[count])]
				if operator == '+':
					result = values[0] + values[1]
				if operator == '-':
					print('operating minus')
					
					if i:
						result = values[0] - values[1]
					else:
						duo_operator = False
						result = -values[1]
				if operator == '*':
					result = values[0] * values[1]
				if operator == '/':
					result = values[0] / values[1]
				if operator == '%':
					result = values[0] % values[1]
				if operator == '^':
					result = values[0] ** values[1]
				if operator == '$':
					result = max(values[0], values[1])
				if operator == '&':
					result = min(values[0], values[1])
				if operator == '@':
					result = (values[0] + values[1])/2
				if operator == '!':
					result = factorial(values[0])
			count += 1
	if duo_operator:
		equation = equation[0:nums_indices[0]] + str(result) + equation[nums_indices[1]:len(equation)]
	else:
		if operator == '!':
			equation = equation[0:nums_indices[2] - 1] + str(result) + equation[nums_indices[1]:len(equation)]
		else:
			equation += END_VALUE
	print('res ' + str(result))
	print(equation)
	print('=======')
	return equation

def interpret(equation,strength=0, last_index = None):
	# remove white space
	equation = equation.translate({ord(c): None for c in string.whitespace})

	try:
		# end of calculation
		if strength == len(operators):
			return int(equation)
		
		if END_VALUE in equation:
			return int(equation[:-1])
			
		
		print('strength ' + str(strength))
		# index of current operator in equation
		index = equation.index(operators[strength])
		
		
		# taking care of brackets
		if(strength < 2):
			# if opening bracket
			if not strength:
				# opening bracket search for first closing bracket
				return interpret(equation, strength + 1, index)
			# if closing bracket
			if strength:
				# closing bracket calculate brackets and start recursion again
				print('outside strength ' + str(strength))
				brackets_str = str(interpret(equation[last_index + 1: index]))
				print('a')
				equation = equation[0:last_index] + brackets_str + equation[index: len(equation) - 1]
				print('done brackets')
				print('t equation ' + equation)
				return interpret(equation, 0, None)
		# normal operation
		else:
			print('b operator is ' + str(operators[strength]))
			equation = operate(equation,index,strength)
			return interpret(equation, strength, last_index)
	
	except ValueError:
		# operator not found
		if(strength < 2):
			if strength:
				raise SyntaxError("Expected ')'")
			else:
				return interpret(equation, strength + 2, None)
		return interpret(equation, strength + 1, None)
	except SyntaxError as msg:
		print("Syntax Error: " + str(msg))
		return

def ui():
	while True:
		equation = input()
		print(interpret(equation))
		input("Press Enter to Continue")
		os.system('cls')

#15*7+64+4!*(22+31*-5)
ui()