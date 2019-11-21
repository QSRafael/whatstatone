import numpy as np 
# import matplotlib.pyplot as plt 
# import matplotlib.dates as mdates
from datetime import date, datetime, timedelta
import time

def nome(p):
    i = 3
    nome = ""
    aux = True
   
    while p[i][-1] != ":":
        nome = nome + p[i] + " "
        i += 1
        if i >= (len(p)):
            i = i-1
            break
    
    if p[i][-1] == ":":
        aux = False

    nome = nome + p[i]
    nome = nome.replace(":","")
    if aux or len(nome) > 50:
        nome = " "
    return nome

dia = 3600*12

def leitor_msg(fname, person_name,ling):

    # ling = int(input('In which language was the smatphone? Enter 1 for PT or EN, enter 2 for DE, enter 3 for FR.\n'))
    aux1 = 0
    if ling == 3:
        aux1 = 1

    pessoa = []
    nmsg1 = [] #numero de mensagens da pessoa 1
    nmsg2 = [] #numero de mensagens da pessoa 2

    lista_dias = []

    d = 0
    with open(fname, encoding="utf8") as f:
        for line in f:
            palavras = line.split()
            #verifica se é mensagem
            if len(palavras) > 4 and palavras[3][0:1] != '\u200e':
                # verifica se há data
                if palavras[0][0:2].isdigit() and palavras[1][0:2].isdigit() and palavras[2+aux1] == '-':
                    # identifica as pessoas
                    if len(pessoa) < 2:
                        name = nome(palavras)
                        if name != " ":
                            if len(pessoa) == 0:
                                pessoa.append(name)
                            elif pessoa[0] != name:
                                pessoa.append(name)
                    # obtém a data da primeria mensagem
                    if ling == 2:
                        if len(nmsg1) == 0 and len(nmsg2) == 0:
                            data0 = date(int(palavras[0][6:8]) + 2000, int(palavras[0][3:5]), int(palavras[0][0:2]))
                            data_ant = data0
                            nmsg1.append(0)
                            nmsg2.append(0)
                        else:
                            data = date(int(palavras[0][6:8]) + 2000, int(palavras[0][3:5]), int(palavras[0][0:2]))
                            tl = data - data_ant 
                            # verifica se passaram dias entre as mensagens
                            if tl.total_seconds()/86400 >= 1:
                                for i in range(int(tl.total_seconds()/86400)):
                                    nmsg1.append(0)
                                    nmsg2.append(0)
                                    d += 1
                                    lista_dias.append(data_ant + timedelta(days=i))
                            data_ant = data
                    elif ling == 1:
                        if len(nmsg1) == 0 and len(nmsg2) == 0:
                            data0 = date(int(palavras[0][6:10]), int(palavras[0][3:5]), int(palavras[0][0:2]))
                            data_ant = data0
                            nmsg1.append(0)
                            nmsg2.append(0)
                        else:
                            data = date(int(palavras[0][6:10]), int(palavras[0][3:5]), int(palavras[0][0:2]))
                            tl = data - data_ant 
                            # verifica se passaram dias entre as mensagens
                            if tl.total_seconds()/86400 >= 1:
                                for i in range(int(tl.total_seconds()/86400)):
                                    nmsg1.append(0)
                                    nmsg2.append(0)
                                    d += 1
                                    lista_dias.append(data_ant + timedelta(days=i))
                            data_ant = data


                    # Adiciona mensagem a posição d referente ao dia após data0
                    if (len(pessoa) > 0):
                        name = nome(palavras)
                        if name == pessoa[0]:
                            nmsg1[d] += 1
                        elif name == pessoa[1]:
                            nmsg2[d] += 1
        lista_dias.append(data)

    nmsg1 = np.array(nmsg1)
    nmsg2 = np.array(nmsg2)
 
    # cumulative values
    nmsg1 = nmsg1 + nmsg2
    for i in range(1,len(nmsg1)):
        nmsg1[i] += nmsg1[i-1] 
    
    with open('results/' + person_name[0:len(person_name)-4]+"_result.csv", "w", encoding="utf8") as f:
        f.write("name," + "date,"+ "value" + "\n")
        for i in range(len(nmsg1)):
            f.write(person_name[0:len(person_name)-4] + ",{}, {}\n".format(lista_dias[i], nmsg1[i]))

    print("Saved file {}\n".format(person_name[0:len(person_name)-4]+"_result.csv"))

    return(str(lista_dias[-1]))


def leitor_words(fname, person_name,ling):

    # ling = int(input('In which language was the smatphone? Enter 1 for PT or EN, enter 2 for DE, enter 3 for FR.\n'))
    aux1 = 0
    if ling == 3:
        aux1 = 1

    pessoa = []
    nmsg1 = [] #numero de mensagens da pessoa 1
    nmsg2 = [] #numero de mensagens da pessoa 2

    lista_dias = []

    d = 0
    message_valid = False
    with open(fname, encoding="utf8") as f:
        for line in f:
            palavras = line.split()
            #verifica se é mensagem
            if len(palavras) > 4 and palavras[3][0:1] != '\u200e':
                # verifica se há data
                if palavras[0][0:2].isdigit() and palavras[1][0:2].isdigit() and palavras[2+aux1] == '-':
                    # identifica as pessoas
                    if len(pessoa) < 2:
                        name = nome(palavras)
                        if name != " ":
                            if len(pessoa) == 0:
                                pessoa.append(name)
                            elif pessoa[0] != name:
                                pessoa.append(name)
                        else:
                            message_valid = False
                    # obtém a data da primeria mensagem
                    if ling == 2:
                        if len(nmsg1) == 0 and len(nmsg2) == 0:
                            data0 = date(int(palavras[0][6:8]) + 2000, int(palavras[0][3:5]), int(palavras[0][0:2]))
                            data_ant = data0
                            nmsg1.append(0)
                            nmsg2.append(0)
                        else:
                            data = date(int(palavras[0][6:8]) + 2000, int(palavras[0][3:5]), int(palavras[0][0:2]))
                            tl = data - data_ant 
                            # verifica se passaram dias entre as mensagens
                            if tl.total_seconds()/86400 >= 1:
                                for i in range(int(tl.total_seconds()/86400)):
                                    nmsg1.append(0)
                                    nmsg2.append(0)
                                    d += 1
                                    lista_dias.append(data_ant + timedelta(days=i))
                            data_ant = data
                    elif ling == 1:
                        if len(nmsg1) == 0 and len(nmsg2) == 0:
                            data0 = date(int(palavras[0][6:10]), int(palavras[0][3:5]), int(palavras[0][0:2]))
                            data_ant = data0
                            nmsg1.append(0)
                            nmsg2.append(0)
                        else:
                            data = date(int(palavras[0][6:10]), int(palavras[0][3:5]), int(palavras[0][0:2]))
                            tl = data - data_ant 
                            # verifica se passaram dias entre as mensagens
                            if tl.total_seconds()/86400 >= 1:
                                for i in range(int(tl.total_seconds()/86400)):
                                    nmsg1.append(0)
                                    nmsg2.append(0)
                                    d += 1
                                    lista_dias.append(data_ant + timedelta(days=i))
                            data_ant = data


                    # Adiciona mensagem a posição d referente ao dia após data0
                    if (len(pessoa) > 0):
                        name = nome(palavras)
                        if name == pessoa[0]:
                            nmsg1[d] += len(palavras)
                        elif name == pessoa[1]:
                            nmsg2[d] += len(palavras)
                        d_prev_msg = d # dia da mensagem anterior
                        message_valid = True 
            else: 
                if message_valid:
                    if name == pessoa[0]:
                        nmsg1[d_prev_msg] += len(palavras)
                    elif name == pessoa[1]:
                        nmsg2[d_prev_msg] += len(palavras)                  

        lista_dias.append(data)

    nmsg1 = np.array(nmsg1)
    nmsg2 = np.array(nmsg2)
 
    # cumulative values
    nmsg1 = nmsg1 + nmsg2
    for i in range(1,len(nmsg1)):
        nmsg1[i] += nmsg1[i-1] 
    
    with open('results/' + person_name[0:len(person_name)-4]+"_result.csv", "w", encoding="utf8") as f:
        f.write("name," + "date,"+ "value" + "\n")
        for i in range(len(nmsg1)):
            f.write(person_name[0:len(person_name)-4] + ",{}, {}\n".format(lista_dias[i], nmsg1[i]))

    print("Saved file {}\n".format(person_name[0:len(person_name)-4]+"_result.csv"))

    return(str(lista_dias[-1]))
