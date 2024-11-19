cadeia = ''
pos_cadeia = 0

def fim_cadeia():
	global pos_cadeia
	global cadeia
	if pos_cadeia == len(cadeia):
		return True
	else:
		return False

def casa(terminal):
	global pos_cadeia
	global cadeia
	if not fim_cadeia() and terminal == cadeia[pos_cadeia]:
		pos_cadeia += 1
		return True
	else:
		return False

def prox_entrada():
	global pos_cadeia
	global cadeia
	if not fim_cadeia():
		return cadeia[pos_cadeia]
	else:
		return None

def E():
	if prox_entrada() == 'a' or prox_entrada() == '(':
		if T():
			if Elinha():
				return True
			else:
				return False
		else:
			return False
	else:
		return False

def Elinha():
	if prox_entrada() == ')' or fim_cadeia():
		return True
	elif casa('+'):
		if T():
			if Elinha():
				return True
			else:
				return False
		else:
			return False
	else:
		return False

def T():
	if prox_entrada() == 'a' or prox_entrada() == '(':
		if F():
			if Tlinha():
				return True
			else:
				return False
		else:
			return False
	else:
		return False
	
def Tlinha():
	if prox_entrada() == '+' or prox_entrada() == ')' or fim_cadeia():
		return True
	elif casa('*'):
		if F():
			if Tlinha():
				return True
			else:
				return False
		else:
			return False
	else:
		return False
	

def F():
	if casa('a'):
		return True
	elif casa('('):
		if E():
			if casa(')'):
				return True
			else:
				return False
		else:
			return False
	else:
		return False
		

cadeia = input('Digite a cadeia a ser verificada\n')
if E() and fim_cadeia():
	print('Reconheceu a cadeia')
else:
	print('Cadeia não reconhecida')
