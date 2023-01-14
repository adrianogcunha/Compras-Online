from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from datetime import date
import mysql.connector

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Cristal@29",
    database="Compras_Online"
)

# variáveis globais

id_logado = 0
verificao = -1
verificacao_pgto = -1
id_cliente = 0
cursor = banco.cursor()


#########################################
# DADOS DA EMPRESA
#########################################

def numero_para_nome(mes):
    if mes == 1:
        nome_mes = "Janeiro"
    elif mes == 2:
        nome_mes = "Fevereiro"
    elif mes == 3:
        nome_mes = "Março"
    elif mes == 4:
        nome_mes = "Abril"
    elif mes == 5:
        nome_mes = "Maio"
    elif mes == 6:
        nome_mes = "Junho"
    elif mes == 7:
        nome_mes = "Julho"
    elif mes == 8:
        nome_mes = "Agosto"
    elif mes == 9:
        nome_mes = "Setembro"
    elif mes == 10:
        nome_mes = "Outubro"
    elif mes == 11:
        nome_mes = "Novembro"
    elif mes == 12:
        nome_mes = "Dezembro"
    return nome_mes


def pro_mais_vendidos():
    cursor.execute(
        "SELECT qtd, nome_pro FROM produtos NATURAL JOIN(SELECT id_pro, sum(qtd_pro) as qtd from itens_pedidos GROUP BY id_pro) AS T1 ORDER BY qtd DESC")
    dados_lidos = cursor.fetchall()

    Estatisticas.tableWidget.setRowCount(len(dados_lidos))
    Estatisticas.tableWidget.setColumnCount(2)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 2):
            Estatisticas.tableWidget.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

    Estatisticas.tableWidget.setColumnWidth(0, 60)
    Estatisticas.tableWidget.setColumnWidth(1, 222)


def todos_meses():
    entrada = Estatisticas.lineEdit.text()
    Estatisticas.tableWidget_2.setColumnWidth(0, 40)
    Estatisticas.tableWidget_2.setColumnWidth(1, 208)
    if entrada == "":
        return
    elif entrada.isdigit() == False:
        mensagem = "O ANO deve ser um número!!!"
        QMessageBox.about(Estatisticas, "ATENÇÃO!!", mensagem)
        return

    query = "SELECT id_cli, nome_cli from cliente NATURAL JOIN(SELECT id_cli, count(mes) FROM(SELECT DISTINCT id_cli, MONTH(data_ped) AS mes, YEAR(data_ped) AS ano FROM pedidos WHERE YEAR(data_ped)= %s) AS T1 GROUP BY Id_Cli HAVING count(mes) = 12) AS T2"
    dados = (str(entrada), )
    cursor.execute(query, dados)
    dados_lidos = cursor.fetchall()

    Estatisticas.tableWidget_2.setRowCount(len(dados_lidos))
    Estatisticas.tableWidget_2.setColumnCount(2)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 2):
            Estatisticas.tableWidget_2.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


def pagamento_muito_utilizado():
    cursor.execute(
        "SELECT Metodo_Pagto, count(Metodo_Pagto) FROM pagamento GROUP BY metodo_pagto ORDER BY count(Metodo_Pagto) DESC LIMIT 1")
    dado = cursor.fetchall()
    pgto_utilizado = dado[0][0]
    if str(pgto_utilizado) == "[]":
        Estatisticas.label_2.setText(str(pgto_utilizado))
    else:
        Estatisticas.label_2.setText(str(pgto_utilizado))


def media_anual_vendas():
    cursor.execute("SELECT AVG(faturamento_anual) FROM(SELECT YEAR(data_ped), sum(Pagamento_Realizado) as faturamento_anual FROM pedidos GROUP BY YEAR(data_ped)) AS T1")
    dado = cursor.fetchall()
    media_final = "R$:"+str(dado[0][0])
    Estatisticas.label_3.setText(media_final)


def maior_numero_vendas():
    cursor.execute("SELECT MONTH(DATA_PED), YEAR(data_ped), Pagamento_Realizado FROM pedidos ORDER BY Pagamento_realizado DESC LIMIT 1")
    dado = cursor.fetchall()
    ano = dado[0][1]
    mes = dado[0][0]

    nome_mes = numero_para_nome(mes)
    Estatisticas.label_5.setText(nome_mes)
    Estatisticas.label_6.setText(str(ano))


def gerar_dados():
    pagamento_muito_utilizado()
    todos_meses()
    pro_mais_vendidos()
    media_anual_vendas()
    maior_numero_vendas()

####################################################
# ABERTURA/FECHAMENTO DE TELA HISTÓRICO DE PAGAMENTO

def abrir_tela_estatisticas():
    Menu_Funcionarios.close()
    Estatisticas.show()
    gerar_dados()


def fechar_tela_estatisticas():
    Estatisticas.close()
    Menu_Funcionarios.show()


#########################################
# ÁREA PAGAMENTO
#########################################

def listar_histórico_pagamento():
    id_ped = Historico_pgto.lineEdit.text()
    mtd_pgto = Historico_pgto.comboBox.currentText()
    if mtd_pgto == "TODOS":
        mtd_pgto = ""

    query = "SELECT Cod_Pagto, Id_Pedido, Metodo_Pagto, valor_pgto, Status_Pagto, data_pgto FROM pagamento WHERE Id_Pedido LIKE %s and Metodo_Pagto LIKE %s ORDER BY data_pgto DESC"
    dados = (('%'+id_ped+'%'), ('%'+mtd_pgto+'%'))
    cursor.execute(query, dados)
    dados_lidos = cursor.fetchall()

    Historico_pgto.tableWidget.setRowCount(len(dados_lidos))
    Historico_pgto.tableWidget.setColumnCount(6)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            Historico_pgto.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
            data = str(dados_lidos[i][5])
            data_formatada = "{}/{}/{}".format(data[8:10], data[5:7], data[0:4])
            Historico_pgto.tableWidget.setItem(i, 5, QtWidgets.QTableWidgetItem(str(data_formatada)))

    Historico_pgto.tableWidget.setColumnWidth(0, 110)
    Historico_pgto.tableWidget.setColumnWidth(1, 75)
    Historico_pgto.tableWidget.setColumnWidth(2, 130)
    Historico_pgto.tableWidget.setColumnWidth(3, 88)
    Historico_pgto.tableWidget.setColumnWidth(4, 90)
    Historico_pgto.tableWidget.setColumnWidth(5, 85)

def verificar_pgto_pendente(id_ped):
    cursor.execute("SELECT Pagamento_Pendente FROM pedidos WHERE Id_Pedido = "+str(id_ped))
    dados_lidos = cursor.fetchall()
    pgto_pendente = dados_lidos[0][0]
    return pgto_pendente


def buscar_pedido_id():
    if verificacao_pgto == 0:
        id = Pedidos_cliente.tableWidget.currentItem().text()
        if id.isdigit() == False:
            mensagem = "É necessário selecionar o ID do pedido na tabela!!!"
            QMessageBox.about(Pedidos_cliente, "ATENÇÃO!!", mensagem)
        else:
            return id
        
    elif verificacao_pgto == 1:
        id = Pedidos_funcionario.tableWidget.currentItem().text()
        if id.isdigit() == False:
            mensagem = "É necessário selecionar o ID do pedido na tabela!!!"
            QMessageBox.about(Pedidos_cliente, "ATENÇÃO!!", mensagem)
        else:
            return id
    return -1


def verificar_status_pgto(id_ped):
    if verificar_pgto_pendente(id_ped) == 0:
        query = "UPDATE pedidos SET Status_Ped = %s WHERE id_pedido = %s"
        dados = ("PAGAMENTO APROVADO", id_ped)
        cursor.execute(query, dados)
        banco.commit()


def efetuar_pagamento():
    try:
        metodo_pgto = None
        id_pedido = buscar_pedido_id()
        data = date.today()

        valor_pgto = Pagamento.lineEdit.text()
        if valor_pgto == "":
            mensagem = "É necessário digitar algum valor!!!"
            QMessageBox.about(Pagamento, "ATENÇÃO!!", mensagem)
            return
        elif float(valor_pgto) <= 0:
            mensagem = "Esse valor não é valido!!!"
            QMessageBox.about(Pagamento, "ATENÇÃO!!", mensagem)
            return
        elif float(valor_pgto) > verificar_pgto_pendente(id_pedido):
            mensagem = "O valor digitado é maior do que o necessário!!!"
            QMessageBox.about(Pagamento, "ATENÇÃO!!", mensagem)
            return

        if Pagamento.radioButton.isChecked():
            metodo_pgto = "PIX"
        elif Pagamento.radioButton_2.isChecked():
            metodo_pgto = "CARTÃO DE DEBITO"
        elif Pagamento.radioButton_3.isChecked():
            metodo_pgto = "CARTÃO DE CREDITO"
        elif Pagamento.radioButton_4.isChecked():
            metodo_pgto = "BOLETO"
        else:
            mensagem = "É necessário selecionar um metodo de pagamento!!!"
            QMessageBox.about(Pagamento, "ATENÇÃO!!", mensagem)
            return

        query = "INSERT INTO pagamento(Id_Pedido, metodo_pagto, status_pagto, valor_pgto, data_pgto) VALUES (%s, %s, %s, %s, %s)"
        dados = (id_pedido, metodo_pgto, "APROVADO", valor_pgto, data)
        cursor.execute(query, dados)

        query = "UPDATE pedidos SET Pagamento_Realizado = (Pagamento_Realizado + %s), Pagamento_Pendente = (Pagamento_Pendente - %s)   WHERE id_pedido = %s"
        dados = (valor_pgto, valor_pgto, id_pedido)
        cursor.execute(query, dados)
        banco.commit()
        fechar_tela_pgto()
        mensagem = "Pagamento Realizado!!!"
        QMessageBox.about(Pagamento, "APROVADO!!", mensagem)
        verificar_status_pgto(id_pedido)
        listar_pedidos()
        listar_pedidos_funcionario()
    except:
        mensagem = "Esse valor não é valido!!!"
        QMessageBox.about(Pagamento, "ATENÇÃO!!", mensagem)

####################################################
# ABERTURA/FECHAMENTO DE TELA 
def abrir_tela_historico():
    listar_histórico_pagamento()
    Historico_pgto.show()


def fechar_tela_historico():
    Historico_pgto.close()

def fechar_tela_pgto():
    Pagamento.close()


def abrir_tela_pgto_funcionario():
    global verificacao_pgto
    verificacao_pgto = 1
    Pagamento.lineEdit.setText("")
    linha = Pedidos_funcionario.tableWidget.currentRow()
    if linha == -1:
        mensagem = "É necessário selecionar um pedido!!!"
        QMessageBox.about(Pedidos_funcionario, "ATENÇÃO!!", mensagem)
        return
    id_ped = buscar_pedido_id()
    
    if id_ped == -1:
        return
    pgto_pendente = verificar_pgto_pendente(id_ped)
    Pagamento.label_3.setText(str(pgto_pendente))
    Pagamento.show()


def abrir_tela_pgto_cliente():
    global verificacao_pgto
    verificacao_pgto = 0
    Pagamento.lineEdit.setText("")
    linha = Pedidos_cliente.tableWidget.currentRow()
    if linha == -1:
        mensagem = "É necessário selecionar um pedido!!!"
        QMessageBox.about(Pedidos_cliente, "ATENÇÃO!!", mensagem)
        return
    id_ped = buscar_pedido_id()
  
    if id_ped == -1:
        return
    pgto_pendente = verificar_pgto_pendente(id_ped)
    Pagamento.label_3.setText(str(pgto_pendente))
    Pagamento.show()

#########################################
# ÁREA PEDIDOS
#########################################


def alterar_status_ped():
    linha = Pedidos_funcionario.tableWidget.currentRow()
    status = Pedidos_funcionario.comboBox.currentText()
    if linha == -1:
        mensagem = "É necessário selecionar um pedido!!!"
        QMessageBox.about(Pedidos_funcionario, "ATENÇÃO!!", mensagem)
        return
    else:
        try:
            global verificacao_pgto
            verificacao_pgto = 1
     
            id_ped = buscar_pedido_id()
            if id_ped == -1:
                return

            comando_SQL = "UPDATE pedidos SET status_ped = %s WHERE Id_pedido = %s"
            dados = (status, id_ped)
            cursor.execute(comando_SQL, dados)
            banco.commit()
            mensagem = "Status alterado com sucesso!!!"
            QMessageBox.about(Pedidos_funcionario, "APROVADO!!", mensagem)
            listar_pedidos_funcionario()

        except:
            mensagem = "Não há nenhum pedido!!!"
            QMessageBox.about(Pedidos_funcionario, "ATENÇÃO!!", mensagem)


def ped_produtos_funcionario():  # botao do funcionario
    try:
        global verificacao_pgto
        verificacao_pgto = 1
        id_ped = buscar_pedido_id()

        if id_ped == -1:
            return
        itens_pedido(id_ped)
        Itens_pedido.show()
    except:
        mensagem = "Não há nenhum pedido!!!"
        QMessageBox.about(Pedidos_funcionario, "ATENÇÃO!!", mensagem)


def ped_produtos_cliente():  # botao do cliente
    linha = Pedidos_cliente.tableWidget.currentRow()
    if linha == -1:
        mensagem = "É necessário selecionar um pedido!!!"
        QMessageBox.about(Pedidos_cliente, "ATENÇÃO!!", mensagem)
        return
    else:
        try:
            Itens_pedido.show()
            cursor.execute(
                "SELECT Id_Pedido FROM pedidos WHERE id_cli = "+str(id_logado))
            dados_lidos = cursor.fetchall()
            id_ped = dados_lidos[linha][0]
            itens_pedido(id_ped)
        except:
            mensagem = "Não há nenhum pedido!!!"
            QMessageBox.about(Pedidos_cliente, "ATENÇÃO!!", mensagem)


def itens_pedido(id_ped):
    cursor.execute("SELECT Qtd_Pro, nome_pro, marca_pro FROM produtos NATURAL JOIN itens_pedidos WHERE Id_Pedido = "+str(id_ped))
    dados_lidos = cursor.fetchall()

    Itens_pedido.tableWidget.setRowCount(len(dados_lidos))
    Itens_pedido.tableWidget.setColumnCount(3)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 3):
            Itens_pedido.tableWidget.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

    Itens_pedido.tableWidget.setColumnWidth(0, 40)
    Itens_pedido.tableWidget.setColumnWidth(1, 200)
    Itens_pedido.tableWidget.setColumnWidth(2, 150)


def listar_pedidos_funcionario():
    
    query = "SELECT id_pedido, nome_cli, data_ped, Pagamento_Pendente, Valor_Total_Ped, Status_Ped FROM pedidos NATURAL JOIN cliente WHERE id_pedido LIKE %s OR nome_cli LIKE %s ORDER BY data_ped DESC"
    filtragem = Pedidos_funcionario.lineEdit.text()
    dados = (('%'+filtragem+'%'), ('%'+filtragem+'%'))
    cursor.execute(query,dados)
    dados_lidos = cursor.fetchall()

    Pedidos_funcionario.tableWidget.setRowCount(len(dados_lidos))
    Pedidos_funcionario.tableWidget.setColumnCount(6)

    for i in range(0, len(dados_lidos)):
        for j in range(3, 6):
            Pedidos_funcionario.tableWidget.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
            Pedidos_funcionario.tableWidget.setItem(
                i, 0, QtWidgets.QTableWidgetItem(str(dados_lidos[i][0])))
            Pedidos_funcionario.tableWidget.setItem(
                i, 1, QtWidgets.QTableWidgetItem(str(dados_lidos[i][1])))

            data = str(dados_lidos[i][2])
            data_formatada = "{}/{}/{}".format(data[8:10], data[5:7], data[0:4])
            Pedidos_funcionario.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(str(data_formatada)))

    Pedidos_funcionario.tableWidget.setColumnWidth(0, 97)
    Pedidos_funcionario.tableWidget.setColumnWidth(1, 180)
    Pedidos_funcionario.tableWidget.setColumnWidth(2, 100)
    Pedidos_funcionario.tableWidget.setColumnWidth(3, 168)
    Pedidos_funcionario.tableWidget.setColumnWidth(4, 140)
    Pedidos_funcionario.tableWidget.setColumnWidth(5, 180)


def listar_pedidos():
    query = "SELECT id_pedido, data_ped, Pagamento_Pendente, Valor_Total_Ped, status_Ped FROM pedidos WHERE id_cli = %s ORDER BY data_ped DESC"
    dados = ((str(id_logado)),)
    cursor.execute(query, dados)
    dados_lidos = cursor.fetchall()
 
    Pedidos_cliente.tableWidget.setRowCount(len(dados_lidos))
    Pedidos_cliente.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(2, 5):
            Pedidos_cliente.tableWidget.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
            Pedidos_cliente.tableWidget.setItem(
                i, 0, QtWidgets.QTableWidgetItem(str(dados_lidos[i][0])))

            data = str(dados_lidos[i][1])
            data_formatada = "{}/{}/{}".format(
                data[8:10], data[5:7], data[0:4])
            Pedidos_cliente.tableWidget.setItem(
                i, 1, QtWidgets.QTableWidgetItem(str(data_formatada)))

    Pedidos_cliente.tableWidget.setColumnWidth(0, 93)
    Pedidos_cliente.tableWidget.setColumnWidth(1, 78)
    Pedidos_cliente.tableWidget.setColumnWidth(2, 162)
    Pedidos_cliente.tableWidget.setColumnWidth(3, 96)
    Pedidos_cliente.tableWidget.setColumnWidth(4, 175)


def custo_total_ped(id_cli):
    comando_SQL = "SELECT sum(preco_total) FROM (SELECT(Qtd_Pro * preco_pro) AS preco_total FROM produtos NATURAL JOIN carrinho_compras WHERE id_cli = %s ) AS T1"
    dados = ((id_cli),)
    cursor.execute(comando_SQL, dados)

    custo_total = cursor.fetchall()

    return custo_total[0][0]


def limpar_carrinho():
    cursor.execute(
        "DELETE FROM carrinho_compras WHERE id_cli = "+str(id_cliente))
    banco.commit()


def adicionar_itens_pedidos():

    comando_SQL = "SELECT max(Id_Pedido) FROM pedidos WHERE id_cli = %s"
    dados = ((id_cliente),)
    cursor.execute(comando_SQL, dados)
    id_ped = cursor.fetchall()

    comando_SQL = "SELECT Id_Pro, qtd_pro FROM carrinho_compras WHERE id_cli = %s"
    dados = ((id_cliente),)
    cursor.execute(comando_SQL, dados)
    id_produtos = cursor.fetchall()

    for i in range(0, len(id_produtos)):

        Id_Pro = id_produtos[i][0]
        Qtd_Pro = id_produtos[i][1]

        comando_SQL = "INSERT INTO itens_pedidos (Id_Pedido, Id_Pro, qtd_pro) VALUES (%s, %s, %s)"
        dados = (str(id_ped[0][0]), str(Id_Pro), str(Qtd_Pro))
        cursor.execute(comando_SQL, dados)
        banco.commit()


def carrinho_para_pedido():
    id_cli = id_cliente
    status_Ped = "AGUARGANDO PAGAMENTO"
    data_Ped = date.today()
    valor_Total_Ped = custo_total_ped(id_cliente)
    pagamento_Realizado = 0
    pagamento_Pendente = valor_Total_Ped
    try:
        comando_SQL = "INSERT INTO pedidos (Id_Cli, Status_Ped, Data_Ped, Valor_Total_Ped, Pagamento_Realizado, Pagamento_Pendente) VALUES (%s, %s, %s, %s, %s, %s)"
        dados = ((id_cli), (status_Ped), (data_Ped), (valor_Total_Ped),
                 (pagamento_Realizado), (pagamento_Pendente))
        cursor.execute(comando_SQL, dados)
        banco.commit()

        adicionar_itens_pedidos()
        limpar_carrinho()
        listar_carrinho()
        listar_catalogo()
        fechar_tela_carrinho_compras()

        mensagem = "Pedido realizado com sucesso !!!"
        QMessageBox.about(Carrinho_Compras, "APROVADO!!", mensagem)
    except:
        mensagem = "Não há nenhum item pra ser feito o PEDIDO !!!"
        QMessageBox.about(Carrinho_Compras, "NEGADO!!", mensagem)


####################################################
# ABERTURA/FECHAMENTO DE TELA

def abrir_tela_pedidos_funcionarios():
    Menu_Funcionarios.close()
    Pedidos_funcionario.show()
    listar_pedidos_funcionario()

def fechar_tela_itens_pedidos():
    Itens_pedido.close()
    
def abrir_tela_meus_pedidos_cli():
    Menu_Inicial_Cliente.close()
    Pedidos_cliente.show()
    listar_pedidos()

def voltar_menu_funcionario():
    Pedidos_funcionario.close()
    Itens_pedido.close()
    Menu_Funcionarios.show()
  

def voltar_menu_cliente2():
    Pedidos_cliente.close()
    Itens_pedido.close()
    Menu_Inicial_Cliente.show()

#########################################
# ÁREA COMPRAS/ CARRINHO
#########################################
    
def buscar_produto_id():
    try:
        id = Comprar_Produto.tableWidget.currentItem().text()

        if id == -1:
            mensagem = "É necessário selecionar um produto!!!"
            QMessageBox.about(Comprar_Produto, "ATENÇÃO!!", mensagem)
        elif id.isdigit() == False:
            mensagem = "É necessário selecionar o ID do produto na tabela!!!"
            QMessageBox.about(Comprar_Produto, "ATENÇÃO!!", mensagem)
        else:
            return id
    except:
        mensagem = "É necessário selecionar um produto!!!"
        QMessageBox.about(Comprar_Produto, "ATENÇÃO!!", mensagem)
        return 


def verificar_se_ja_tem_produto(id_pro):
    try:
        comando_SQL = "SELECT * FROM carrinho_compras WHERE id_pro = %s and id_cli = %s"
        dados = (id_pro, id_logado)
        cursor.execute(comando_SQL, dados)
        dados_lidos = cursor.fetchall()
        x = dados_lidos[0][0]
        return 1
    except:
        return 0


def clicar_compra_cliente():
    global id_cliente
    id_cliente = id_logado
    Menu_Inicial_Cliente.close()
    Comprar_Produto.show()
    listar_catalogo()

##########################################
#Funcionário selecinando o ID do cliente na hora de fazer a compra por telefone
def clicar_compra_funcionario():
    Pegar_id_cli.lineEdit.setText("")
    Pegar_id_cli.show()


def Pegar_id_cli_OK():
    id = Pegar_id_cli.lineEdit.text()
    if id.isdigit() == False or id == "":
        mensagem = "Digite um numero!"
        QMessageBox.about(Comprar_Produto, "ATENÇÃO!!", mensagem)
        return

    cursor.execute("SELECT id_cli FROM cliente WHERE id_cli = "+str(id))
    dados_lidos = cursor.fetchall()

    if str(dados_lidos) == "[]":
        mensagem = "Não há nenhum cliente com esse ID!"
        QMessageBox.about(Comprar_Produto, "ATENÇÃO!!", mensagem)
    else:
        global id_cliente
        id_cliente = id
        Pegar_id_cli.close()
        Menu_Funcionarios.close()
        Comprar_Produto.show()
        listar_catalogo()
        global verificao
        verificao = -2


def Pegar_id_cli_CANCEL():
    Pegar_id_cli.close()

##########################################

def listar_catalogo():
    nome_pro = Comprar_Produto.lineEdit.text()

    comando_SQL = "SELECT id_pro, nome_pro, marca_pro, preco_pro, status_pro FROM produtos WHERE status_pro != %s and nome_pro LIKE %s"
    dados = (str("FORA DE ESTOQUE"), ('%'+nome_pro+'%'))
    cursor.execute(comando_SQL, dados)
    dados_lidos = cursor.fetchall()

    cursor.execute(
        "SELECT count(*) FROM carrinho_compras WHERE id_cli = "+str(id_cliente))
    qtd_pro_carrinho = cursor.fetchall()
    
    Comprar_Produto.label_4.setText(str(qtd_pro_carrinho[0][0]))

    Comprar_Produto.tableWidget.setRowCount(len(dados_lidos))
    Comprar_Produto.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 3):
            Comprar_Produto.tableWidget.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
            Comprar_Produto.tableWidget.setItem(
                i, 3, QtWidgets.QTableWidgetItem(f"R${(dados_lidos[i][3])}"))
            Comprar_Produto.tableWidget.setItem(
                i, 4, QtWidgets.QTableWidgetItem(str(dados_lidos[i][4])))
            

    Comprar_Produto.tableWidget.setColumnWidth(0, 100)
    Comprar_Produto.tableWidget.setColumnWidth(1, 220)
    Comprar_Produto.tableWidget.setColumnWidth(2, 182)
    Comprar_Produto.tableWidget.setColumnWidth(3, 100)
    Comprar_Produto.tableWidget.setColumnWidth(4, 119)


def listar_carrinho():
    Carrinho_Compras.label_4.setText("")
    cursor.execute("SELECT nome_pro, Qtd_Pro, preco_pro, (Qtd_Pro * preco_pro) AS preco_total FROM produtos NATURAL JOIN carrinho_compras WHERE id_cli =" + str(id_cliente))
    dados_lidos = cursor.fetchall()

    custo_total = custo_total_ped(id_cliente)

    Carrinho_Compras.tableWidget.setRowCount(len(dados_lidos))
    Carrinho_Compras.tableWidget.setColumnCount(4)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 4):
            Carrinho_Compras.tableWidget.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

    Carrinho_Compras.label_4.setText(str(custo_total))

    Carrinho_Compras.tableWidget.setColumnWidth(0, 200)
    Carrinho_Compras.tableWidget.setColumnWidth(1, 50)
    Carrinho_Compras.tableWidget.setColumnWidth(2, 111)
    Carrinho_Compras.tableWidget.setColumnWidth(3, 105)


def mandar_para_carrinho():
    quantidade = Comprar_Produto.spinBox.value()

    if quantidade == 0:
        mensagem = "É necessário inserir uma quantidade maior que zero!"
        QMessageBox.about(Comprar_Produto, "NEGADO!!", mensagem)
        return
    else:
        id_pro = buscar_produto_id()
        if id_pro == None:
            return

        if verificar_se_ja_tem_produto(id_pro) == 1:
            comando_SQL = "UPDATE carrinho_compras SET qtd_pro = (qtd_pro + %s) WHERE id_cli = %s and id_pro = %s"
            dados = (quantidade, str(id_cliente), str(id_pro))
            cursor.execute(comando_SQL, dados)
            banco.commit()

        else:
            comando_SQL = "INSERT INTO carrinho_compras (Id_cli, id_pro, qtd_pro) VALUES (%s,%s,%s)"
            dados = (str(id_cliente), str(id_pro), str(quantidade))
            cursor.execute(comando_SQL, dados)
            banco.commit()

    mensagem = "O Produto foi adicionado no carrinho"
    QMessageBox.about(Comprar_Produto, "APROVADO!!", mensagem)
    Comprar_Produto.spinBox.setValue(0)
    listar_catalogo()
    listar_carrinho()


def remover_item_carrinho():
    linha = Carrinho_Compras.tableWidget.currentRow()
    if linha == -1:
        mensagem = "É necessário selecionar um item do carrinho!!!"
        QMessageBox.about(Carrinho_Compras, "ATENÇÃO!!", mensagem)
        return
    else:
        try:
            cursor.execute(
                "SELECT id_pro FROM carrinho_compras WHERE id_cli = "+str(id_cliente))
            dados_lidos = cursor.fetchall()
            id_pro = dados_lidos[linha][0]


            comando_SQL = "DELETE FROM carrinho_compras WHERE Id_pro = %s and id_cli = %s"
            dados = (id_pro, id_cliente)
            cursor.execute(comando_SQL, dados)
            banco.commit()
            listar_carrinho()
            mensagem = "Produto removido com Sucesso!!!"
            QMessageBox.about(Carrinho_Compras, "APROVADO!!", mensagem)
            listar_catalogo()

        except:
            mensagem = "Não há nenhum produto para ser removido!!!"
            QMessageBox.about(Carrinho_Compras, "ATENÇÃO!!", mensagem)

####################################################
# ABERTURA/FECHAMENTO DE TELA

def abrir_tela_carrinho_compras():
    listar_carrinho()
    Carrinho_Compras.show()


def fechar_tela_carrinho_compras():
    Carrinho_Compras.close()


def voltar_menu_cliente():
    Comprar_Produto.close()
    Carrinho_Compras.close()
    global verificao
    if verificao != -2:
        Menu_Inicial_Cliente.show()
    else:
        Menu_Funcionarios.show()

    verificao = -1
    

#########################################
# ÁREA FUNCIONARIO
#########################################
    

def verifica_usuário_existe_funcionario(nome_usu):

    comando_SQL = "SELECT Usuario_Func FROM funcionario WHERE Usuario_Func = %s"
    dados = (nome_usu,)
    cursor.execute(comando_SQL, dados)

    for x in cursor:
        if x[0] == nome_usu:
            return True
    return False


def listar_funcionarios():
    comando_SQL = "SELECT id_func, nome_func, usuario_func, e_mail_func, RG_func, CPF_func, telefone_func, data_nasc_func, gerente  FROM funcionario"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()


    Gerenciar_Funcionario.tableWidget.setRowCount(len(dados_lidos))
    Gerenciar_Funcionario.tableWidget.setColumnCount(9)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 7):
            Gerenciar_Funcionario.tableWidget.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
            data = str(dados_lidos[i][7])
            data_formatada = "{}/{}/{}".format(
                data[8:10], data[5:7], data[0:4])
            Gerenciar_Funcionario.tableWidget.setItem(
                i, 7, QtWidgets.QTableWidgetItem(str(data_formatada)))
            gerente = dados_lidos[i][8]
            if gerente == 1:
                ger = "SIM"
                Gerenciar_Funcionario.tableWidget.setItem(
                    i, 8, QtWidgets.QTableWidgetItem(ger))
            elif gerente == 0:
                ger = "NÃO"
                Gerenciar_Funcionario.tableWidget.setItem(
                    i, 8, QtWidgets.QTableWidgetItem(ger))

    Gerenciar_Funcionario.tableWidget.setColumnWidth(0, 38)
    Gerenciar_Funcionario.tableWidget.setColumnWidth(1, 155)
    Gerenciar_Funcionario.tableWidget.setColumnWidth(2, 127)
    Gerenciar_Funcionario.tableWidget.setColumnWidth(3, 148)
    Gerenciar_Funcionario.tableWidget.setColumnWidth(4, 110)
    Gerenciar_Funcionario.tableWidget.setColumnWidth(5, 96)
    Gerenciar_Funcionario.tableWidget.setColumnWidth(6, 105)
    Gerenciar_Funcionario.tableWidget.setColumnWidth(7, 83)
    Gerenciar_Funcionario.tableWidget.setColumnWidth(8, 67)

def limpar_canais_funcionario():
    C_Funcionario.label_9.setText("")
    C_Funcionario.lineEdit_1.setText("")
    C_Funcionario.lineEdit_2.setText("")
    C_Funcionario.lineEdit_3.setText("")
    C_Funcionario.lineEdit_4.setText("")
    C_Funcionario.lineEdit_5.setText("")
    C_Funcionario.lineEdit_6.setText("")
    C_Funcionario.lineEdit_7.setText("")
    C_Funcionario.lineEdit_11.setText("")
    

def cadastrar_funcionarios():
    C_Funcionario.label_9.setText("")
    nome_completo = C_Funcionario.lineEdit_1.text()
    e_mail = C_Funcionario.lineEdit_2.text()
    cpf = C_Funcionario.lineEdit_3.text()
    if len(cpf) < 14 or (cpf[0:3].isdigit() == False or cpf[4:7].isdigit() == False or cpf[8:11].isdigit() == False or cpf[12:14].isdigit() == False):
        mensagem = "O CPF deve seguir este formato (123.456.789-10)!"
        QMessageBox.about(C_Funcionario, "ATENÇÃO!!", mensagem)
        return
    rg = C_Funcionario.lineEdit_4.text()
    nome_usu = C_Funcionario.lineEdit_5.text()
    senha = C_Funcionario.lineEdit_6.text()
    c_senha = C_Funcionario.lineEdit_7.text()
    date = C_Funcionario.dateEdit.date()
    data_nasc = '{:04d}{:02d}{:02d}'.format(
        date.year(), date.month(), date.day())
    telefone = C_Funcionario.lineEdit_11.text()
    if len(telefone) < 14 or (telefone[1:4].isdigit() == False or telefone[5:9].isdigit() == False or telefone[11:14].isdigit() == False):
        mensagem = "O TELEFONE deve seguir este formato [(021)91234-5678]!"
        QMessageBox.about(C_Funcionario, "ATENÇÃO!!", mensagem)
        return
    

    # verificar se o nome_usu ta vazio
    if nome_usu == "" or senha == "" or nome_completo == "" or c_senha == "" or cpf == "" or e_mail == "" or telefone == "":
        C_Funcionario.label_9.setText(
            "É necessário preencher os campos obrigatórios!!")
        return
    elif senha != c_senha:
        C_Funcionario.label_9.setText(
            "As senhas não correspondem!")
        return
    elif verifica_usuário_existe_funcionario(nome_usu) == True:
        C_Funcionario.label_9.setText(
            "Esse Nome de Usuário já existe, cadastre outro!")
        return
    else:
        comando_SQL = "INSERT INTO funcionario (usuario_func, nome_func, senha_func, gerente, rg_func, cpf_func, e_mail_func, data_nasc_func, telefone_func) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        dados = (str(nome_usu), str(nome_completo), str(
            senha), 0, str(rg), str(cpf), str(e_mail), str(data_nasc), str(telefone))
        cursor.execute(comando_SQL, dados)
        banco.commit()

    mensagem = "Seu Cadastro foi Concluido!!!"
    QMessageBox.about(C_Funcionario, "PARABÉNS!!", mensagem)
    listar_funcionarios()
    C_Funcionario.close()


def buscar_funcionario_id():
    linha = Gerenciar_Funcionario.tableWidget.currentRow()
    if linha == -1:
        mensagem = "É necessário selecionar um funcionário!!!"
        QMessageBox.about(Gerenciar_Funcionario, "ATENÇÃO!!", mensagem)
        return
    else:
        cursor.execute("SELECT id_func FROM funcionario")
        dados_lidos = cursor.fetchall()
        valor_id = dados_lidos[linha][0]
        return valor_id


def demitir_funcionarios():
    try:
        valor_id = buscar_funcionario_id()
        if valor_id == id_logado:
            mensagem = "Você não pode se demitir!!!"
            QMessageBox.about(Gerenciar_Funcionario, "ATENÇÃO!!", mensagem)
        else:
            cursor.execute(
                "DELETE FROM funcionario WHERE Id_func = "+str(valor_id))
            banco.commit()
            listar_funcionarios()
            mensagem = "Funcionario Demitido com Sucesso!!!"
            QMessageBox.about(C_Cliente, "ATENÇÃO!!", mensagem)
    except:
        return


def alterar_gerente():
    gerente = Gerenciar_Funcionario.comboBox.currentText()
    if gerente == "GERENTE":
        gerente = 1
    else:
        gerente = 0

    valor_id = buscar_funcionario_id()
    
    comando_SQL = "UPDATE funcionario SET gerente = %s WHERE Id_func = %s"
    dados = (gerente, valor_id)
    cursor.execute(comando_SQL, dados)
    banco.commit()

    mensagem = "Alteração executada com sucesso!!!"
    QMessageBox.about(Gerenciar_Funcionario, "APROVADO!!", mensagem)
    listar_funcionarios()


def verificar_permissao_func():
    comando_SQL = "SELECT gerente FROM funcionario WHERE id_func = %s"
    dados = (str(id_logado),)
    cursor.execute(comando_SQL, dados)
    permissao = cursor.fetchall()
    if permissao[0][0] == 1:
        abrir_tela_ger_funcionario()
    else:
        mensagem = "O acesso a essa área é RESTRITO a gerentes!!!"
        QMessageBox.about(Menu_Funcionarios, "ATENÇÃO!!", mensagem)

####################################################
# ABERTURA/FECHAMENTO DE TELA

def abre_tela_cadastro_funcionario():
    limpar_canais_funcionario()
    C_Funcionario.show()


def abrir_tela_ger_funcionario():
    Gerenciar_Funcionario.show()
    Menu_Funcionarios.close()
    listar_funcionarios()
   
    
def cancelar_cadastro_funcionario():
    C_Funcionario.close()
    

#########################################
# ÁREA DE PRODUTOS
#########################################
def listar_produtos():
    comando_SQL = "SELECT id_pro, nome_pro, marca_pro, preco_pro, status_pro FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    Gerenciar_Produto.tableWidget.setRowCount(len(dados_lidos))
    Gerenciar_Produto.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            Gerenciar_Produto.tableWidget.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

    Gerenciar_Produto.tableWidget.setColumnWidth(0, 95)
    Gerenciar_Produto.tableWidget.setColumnWidth(1, 180)
    Gerenciar_Produto.tableWidget.setColumnWidth(2, 140)
    Gerenciar_Produto.tableWidget.setColumnWidth(3, 80)
    Gerenciar_Produto.tableWidget.setColumnWidth(4, 120)


def cadastrar_produto():
    C_Produto.label_4.setText("")
    nome_produto = C_Produto.lineEdit.text()
    preco_produto = C_Produto.lineEdit_2.text()
    marca_produto = C_Produto.lineEdit_3.text()

    if (nome_produto == "" or preco_produto == ""):
        C_Produto.label_4.setText("É necessário preencher tudo!")
    else:
        comando_SQL = "INSERT INTO Produtos (Nome_Pro, Preco_Pro, Marca_Pro, Status_Pro) VALUES (%s, %s,%s,%s)"
        dados = (str(nome_produto), str(preco_produto), str(marca_produto), str("EM ESTOQUE"))
        cursor.execute(comando_SQL, dados)
        banco.commit()
        listar_produtos()
        mensagem = "O Produto foi cadastrado!!!"
        QMessageBox.about(C_Cliente, "CONCLUIDO", mensagem)
        C_Produto.close()


def cancelar_cadastro_produto():
    C_Produto.close()


def alterar_status_produto():
    linha = Gerenciar_Produto.tableWidget.currentRow()
    status = Gerenciar_Produto.comboBox.currentText()

    cursor.execute("SELECT id_pro FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]

    comando_SQL = "UPDATE produtos SET Status_Pro = %s WHERE Id_Pro = %s"
    dados = (str(status), str(valor_id))

    cursor.execute(comando_SQL, dados)
    banco.commit()
    listar_produtos()

####################################################
# ABERTURA/FECHAMENTO DE TELA

def abrir_tela_gerenciar_produtos():
    listar_produtos()
    Gerenciar_Produto.show()
    Menu_Funcionarios.close()


def abrir_tela_cadastro_produto():
    C_Produto.lineEdit.setText("")
    C_Produto.lineEdit_2.setText("")
    C_Produto.show()


def voltar_menu():
    Gerenciar_Produto.close()
    Gerenciar_Cliente.close()
    Gerenciar_Funcionario.close()
    Menu_Funcionarios.show()
    

#########################################
# ÁREA CLIENTE
#########################################


def filtragem_cliente():
    nome = Gerenciar_Cliente.lineEdit.text()
    bairro = Gerenciar_Cliente.lineEdit_2.text()
    cidade = Gerenciar_Cliente.lineEdit_3.text()
    estado = Gerenciar_Cliente.lineEdit_4.text()
    query = "SELECT id_cli, nome_cli, e_mail_cli, usuario_cli, cpf_cli, bairro_cli, cidade_cli, estado_cli, telefone_cli, data_nasc_cli, status_cli FROM cliente WHERE nome_cli LIKE %s and Bairro_Cli LIKE %s and cidade_cli LIKE %s and estado_cli LIKE %s ;"
    dados = (('%'+nome+'%'), ('%'+bairro+'%'),
             ('%'+cidade+'%'), ('%'+estado+'%'))
    cursor.execute(query, dados)
    dados_lidos = cursor.fetchall()

    Gerenciar_Cliente.tableWidget.setRowCount(len(dados_lidos))
    Gerenciar_Cliente.tableWidget.setColumnCount(11)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 11):
            Gerenciar_Cliente.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
            data = str(dados_lidos[i][9])
            data_formatada = "{}/{}/{}".format(
                data[8:10], data[5:7], data[0:4])
            Gerenciar_Cliente.tableWidget.setItem(i, 9, QtWidgets.QTableWidgetItem(str(data_formatada)))
            Gerenciar_Cliente.tableWidget.setItem(i, 10, QtWidgets.QTableWidgetItem(str(dados_lidos[i][10])))


def listar_cliente():
    filtragem_cliente()
    status = Gerenciar_Cliente.comboBox_2.currentText()
    if status == "TODOS":
        status = ""    
    
    query = "select count(id_cli) from cliente where status_cli like %s"
    dados = ((str(status)+"%"),)
    cursor.execute(query, dados)
    resultado = cursor.fetchall()
    Gerenciar_Cliente.label_3.setText(str(resultado[0][0]))

    Gerenciar_Cliente.tableWidget.setColumnWidth(0, 50)
    Gerenciar_Cliente.tableWidget.setColumnWidth(1, 190)
    Gerenciar_Cliente.tableWidget.setColumnWidth(2, 190)
    Gerenciar_Cliente.tableWidget.setColumnWidth(3, 120)
    Gerenciar_Cliente.tableWidget.setColumnWidth(4, 100)
    Gerenciar_Cliente.tableWidget.setColumnWidth(5, 125)
    Gerenciar_Cliente.tableWidget.setColumnWidth(6, 125)
    Gerenciar_Cliente.tableWidget.setColumnWidth(7, 125)
    Gerenciar_Cliente.tableWidget.setColumnWidth(8, 100)
    Gerenciar_Cliente.tableWidget.setColumnWidth(9, 90)
    Gerenciar_Cliente.tableWidget.setColumnWidth(10, 74)


def desativar_cliente():
    status = "INATIVO"
    valor_id = id_logado


    comando_SQL = "UPDATE cliente SET status_cli = %s WHERE Id_cli = %s"
    dados = (status, valor_id)

    cursor.execute(comando_SQL, dados)
    banco.commit()

    mensagem = "Você desativou a sua conta!!!"
    QMessageBox.about(Gerenciar_Cliente, "APROVADO!!", mensagem)
    fechar_tela_desativar_conta()
    logout()


def verifica_usuário_existe(nome_usu):
    comando_SQL = "SELECT Usuario_Cli FROM cliente where Usuario_Cli = %s"
    dados = (nome_usu,)
    cursor.execute(comando_SQL, dados)

    for x in cursor:
        if x[0] == nome_usu:
            return True
    return False


def alterar_status_cli():
    status = Gerenciar_Cliente.comboBox.currentText()

    valor_id = buscar_cliente_id()
    if (valor_id == None):
        return
    else:
        comando_SQL = "UPDATE cliente SET status_cli = %s WHERE Id_cli = %s"
        dados = (status, valor_id)

        cursor.execute(comando_SQL, dados)
        banco.commit()

        mensagem = "Alteração executada com sucesso!!!"
        QMessageBox.about(Gerenciar_Cliente, "APROVADO!!", mensagem)
        listar_cliente()


def limpar_canais_texto():
    C_Cliente.label_9.setText("")
    C_Cliente.lineEdit_1.setText("")
    C_Cliente.lineEdit_5.setText("")
    C_Cliente.lineEdit_6.setText("")
    C_Cliente.lineEdit_7.setText("")
    C_Cliente.lineEdit_8.setText("")
    C_Cliente.lineEdit_9.setText("")
    C_Cliente.lineEdit_10.setText("")
    C_Cliente.lineEdit_11.setText("")
    C_Cliente.lineEdit_12.setText("")
    C_Cliente.lineEdit_13.setText("")


def cadastrar_cliente():
    C_Cliente.label_9.setText("")
    nome_usu = C_Cliente.lineEdit_5.text()
    nome_completo = C_Cliente.lineEdit_1.text()
    e_mail = C_Cliente.lineEdit_10.text()
    senha = C_Cliente.lineEdit_6.text()
    c_senha = C_Cliente.lineEdit_7.text()
    cidade = C_Cliente.lineEdit_9.text()
    bairro = C_Cliente.lineEdit_8.text()
    estado = C_Cliente.lineEdit_12.text()
    cpf = C_Cliente.lineEdit_13.text()
    if len(cpf) < 14 or (cpf[0:3].isdigit() == False or cpf[4:7].isdigit() == False or cpf[8:11].isdigit() == False or cpf[12:14].isdigit() == False):
        mensagem = "O CPF deve seguir este formato (123.456.789-10)!"
        QMessageBox.about(C_Cliente, "ATENÇÃO!!", mensagem)
        return
    
    date = C_Cliente.dateEdit.date()
    data_nasc = '{:04d}{:02d}{:02d}'.format(
        date.year(), date.month(), date.day())
    telefone = C_Cliente.lineEdit_11.text()
    if len(telefone) < 14 or (telefone[1:4].isdigit() == False or telefone[5:9].isdigit() == False or telefone[11:14].isdigit() == False):
        mensagem = "O TELEFONE deve seguir este formato [(021)91234-5678]!"
        QMessageBox.about(C_Cliente, "ATENÇÃO!!", mensagem)
        return

    # verificar se o nome_usu ta vazio
    if nome_usu == "" or senha == "" or nome_completo == "" or e_mail == "" or senha == "" or c_senha == "" or cidade == "" or estado == "" or cpf == "":
        C_Cliente.label_9.setText(
            "É necessário preencher os campos obrigatórios")
        return
    elif senha != c_senha:
        C_Cliente.label_9.setText("As senhas não correspondem!")
        return
    elif verifica_usuário_existe(nome_usu) == True:
        C_Cliente.label_9.setText(
            "Esse Nome de Usuário já existe, cadastre outro!")
        return
    else:
        comando_SQL = "INSERT INTO Cliente (Usuario_Cli, Nome_Cli, E_Mail_Cli, Status_Cli, Senha_Cli, Cidade_Cli, Bairro_Cli, Estado_Cli, cpf_cli, data_nasc_cli, telefone_cli) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"
        dados = (str(nome_usu), str(nome_completo), str(e_mail), str(
            "ATIVO"), str(senha), str(cidade), str(bairro), str(estado), str(cpf), str(data_nasc), str(telefone))
        cursor.execute(comando_SQL, dados)
        banco.commit()

    listar_cliente()
    mensagem = "Seu Cadastro foi Concluido!!!"
    QMessageBox.about(C_Cliente, "PARABÉNS!!", mensagem)
    C_Cliente.close()


def buscar_cliente_id():
    linha = Gerenciar_Cliente.tableWidget.currentItem().text()

    if linha == -1:
        mensagem = "É necessário selecionar um cliente!!!"
        QMessageBox.about(Gerenciar_Cliente, "ATENÇÃO!!", mensagem)
    elif linha.isdigit() == False:
        mensagem = "É necessário selecionar o ID do cliente na tabela!!!"
        QMessageBox.about(Gerenciar_Cliente, "ATENÇÃO!!", mensagem)
    else:
        return linha


def apertar_botao_funcionario():
    global verificacao
    verificacao = 1
    valor_id = buscar_cliente_id()

    abrir_tela_alterar_dados(valor_id)


def apertar_botao_cliente():
    global verificacao
    verificacao = 0
    abrir_tela_alterar_dados(id_logado)


def alterar_dados_cli():

    global verificacao

    if verificacao == 0:
        id_cli = id_logado
    elif verificacao == 1:
        valor_id = buscar_cliente_id()

        id_cli = valor_id

    nome_completo = Alterar_Dados.lineEdit_1.text()
    e_mail = Alterar_Dados.lineEdit_10.text()
    cidade = Alterar_Dados.lineEdit_9.text()
    bairro = Alterar_Dados.lineEdit_8.text()
    estado = Alterar_Dados.lineEdit_12.text()
    telefone = Alterar_Dados.lineEdit_13.text()

    comando_SQL = "UPDATE cliente SET Nome_Cli = %s, E_Mail_Cli = %s, Cidade_Cli = %s, Bairro_Cli = %s, Estado_Cli = %s, telefone_cli = %s WHERE Id_cli = %s"
    dados = (str(nome_completo), str(e_mail), str(cidade), str(
        bairro), str(estado), str(telefone), str(id_cli))

    cursor.execute(comando_SQL, dados)
    banco.commit()

    mensagem = "Alteração executada com sucesso!!!"
    QMessageBox.about(Gerenciar_Cliente, "APROVADO!!", mensagem)

    Alterar_Dados.close()
    listar_cliente()


def cancelar_alterar_dados():
    Alterar_Dados.close()

####################################################
# ABERTURA/FECHAMENTO DE TELA
def abrir_tela_desativar_conta():
    Aviso_desativar_cliente.show()


def fechar_tela_desativar_conta():
    Aviso_desativar_cliente.close()


def abre_tela_gerenciar_cliente():
    listar_cliente()
    Menu_Funcionarios.close()
    Gerenciar_Cliente.show()


def abre_tela_cadastro_cliente():
    limpar_canais_texto()
    C_Cliente.show()

    
def abrir_tela_alterar_dados(id_cli):
    try:
        comando_SQL = "SELECT Nome_Cli, E_Mail_Cli, Cidade_Cli, Bairro_Cli, Estado_Cli, telefone_cli FROM cliente WHERE id_cli = %s"
        dados = (id_cli,)
        cursor.execute(comando_SQL, dados)
        dados_lidos = cursor.fetchall()

        Alterar_Dados.lineEdit_1.setText(dados_lidos[0][0])
        Alterar_Dados.lineEdit_10.setText(dados_lidos[0][1])
        Alterar_Dados.lineEdit_9.setText(dados_lidos[0][2])
        Alterar_Dados.lineEdit_8.setText(dados_lidos[0][3])
        Alterar_Dados.lineEdit_12.setText(dados_lidos[0][4])
        Alterar_Dados.lineEdit_13.setText(dados_lidos[0][5])
        Alterar_Dados.show()
    except:
        return


def Cancelar_cadastro_cliente():
    C_Cliente.close()

#########################################
# LOGIN
#########################################

def salvar_id_logado_funcionario(nome_usuario):
    # SALVA O ID LOGADO NO PROGRAMA, PARA PODER EXECUTAR ALGUMAS INTRUÇÕES FUTURAS DENTRO DO PROGRAMA
    comando_SQL = "SELECT Id_Func FROM funcionario WHERE Usuario_Func = %s"
    dados = (str(nome_usuario),)
    cursor.execute(comando_SQL, dados)
    Id_Func = cursor.fetchall()
    global id_logado
    id_logado = Id_Func[0][0]


def salvar_id_logado_cliente(nome_usuario):
    # SALVA O ID LOGADO NO PROGRAMA, PARA PODER EXECUTAR ALGUMAS INTRUÇÕES FUTURAS DENTRO DO PROGRAMA
    comando_SQL = "SELECT Id_Cli FROM cliente WHERE Usuario_Cli = %s"
    dados = (str(nome_usuario),)
    cursor.execute(comando_SQL, dados)
    Id_cli = cursor.fetchall()
    global id_logado
    id_logado = Id_cli[0][0]


def login_funcionario(nome_usuario):
    # BUSCA NO BANCO DE DADOS A SENHA, TENDO COMO CONDIÇÃO O NOME DO USUÁRIOS
    try:
        comando_SQL = "SELECT Senha_Func FROM funcionario WHERE Usuario_Func = BINARY %s"
        dados = (str(nome_usuario),)
        cursor.execute(comando_SQL, dados)
        senha_bd = cursor.fetchall()
        return senha_bd[0][0]
    except:
        return 0


def login_cliente(nome_usuario):
    # BUSCA NO BANCO DE DADOS A SENHA, TENDO COMO CONDIÇÃO O NOME DO USUÁRIOS
    try:
        comando_SQL = "SELECT Senha_Cli, status_cli FROM cliente WHERE Usuario_Cli = BINARY %s"
        dados = (str(nome_usuario),)
        cursor.execute(comando_SQL, dados)
        dados_bd = cursor.fetchall()
        return dados_bd
    except:
        return 0


def login():
    # CHAMA AS FUNÇÕES PARA VERIFICAR O LOGIN, PARA PERMITIR O ACESSO NO PROGRAMA
    Tela_login.label_6.setText("")
    nome_usuario = Tela_login.lineEdit.text()
    senha = Tela_login.lineEdit_2.text()
    if Tela_login.radioButton.isChecked():
        dados = login_cliente(nome_usuario)
        try:
            if senha == dados[0][0]:
                if dados[0][1] == "INATIVO":
                    Tela_login.label_6.setText("Esse usuário está inativo!")
                else:
                    salvar_id_logado_cliente(nome_usuario)
                    Tela_login.close()
                    Menu_Inicial_Cliente.show()
            else:
                Tela_login.label_6.setText("Dados de login incorretos")
        except:
            Tela_login.label_6.setText("Dados de login incorretos")

    elif Tela_login.radioButton_2.isChecked():
        senha_bd = login_funcionario(nome_usuario)
        if senha == senha_bd:
            salvar_id_logado_funcionario(nome_usuario)
            Tela_login.close()
            Menu_Funcionarios.show()
        else:
            Tela_login.label_6.setText("Dados de login incorretos")

    else:
        Tela_login.label_6.setText(
            "Você precisa selecionar uma das opções acima!")


####################################################
# ABERTURA/FECHAMENTO DE TELA
def abre_tela_login():
    Tela_login.lineEdit.setText("")
    Tela_login.lineEdit_2.setText("")
    Tela_login.show()


def logout():
    id_logado = 0
    Menu_Inicial_Cliente.close()
    Menu_Funcionarios.close()
    abre_tela_login()

#########################################
# Inicializar as telas
#########################################

app = QtWidgets.QApplication([])

C_Produto = uic.loadUi("Cadastro_Produto.ui")
C_Cliente = uic.loadUi("Cadastro_Cliente.ui")
C_Funcionario = uic.loadUi("Cadastro_Funcionario.ui")

Tela_login = uic.loadUi("Tela_login.ui")

Comprar_Produto = uic.loadUi("Comprar_produto.ui")

Menu_Inicial_Cliente = uic.loadUi("Menu_Inicial_Cliente.ui")
Menu_Funcionarios = uic.loadUi("Menu_Funcionarios.ui")

Gerenciar_Produto = uic.loadUi("Gerenciar_Produto.ui")
Gerenciar_Cliente = uic.loadUi("Gerenciar_Cliente.ui")
Gerenciar_Funcionario = uic.loadUi("Gerenciar_Funcionarios.ui")

Alterar_Dados = uic.loadUi("Alterar_Dados.ui")

Carrinho_Compras = uic.loadUi("Carrinho_Compras.ui")

Pegar_id_cli = uic.loadUi("Pegar_id_cliente.ui")

Aviso_desativar_cliente = uic.loadUi("A_desativar_cliente.ui")

Pedidos_cliente = uic.loadUi("Pedidos_cliente.ui")
Pedidos_funcionario = uic.loadUi("Pedidos_funcionários.ui")

Itens_pedido = uic.loadUi("Itens_pedidos.ui")

Pagamento = uic.loadUi("Pagamento.ui")

Estatisticas = uic.loadUi("Estatisticas_Empresa.ui")

Historico_pgto = uic.loadUi("Historico_pgto.ui")

Tela_login.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)

#########################################
# Começar
#########################################

abre_tela_login()

#########################################
# Butões
#########################################

# Tela de Login (OK)
Tela_login.pushButton_2.clicked.connect(login)
Tela_login.pushButton.clicked.connect(abre_tela_cadastro_cliente)

# Cadastro Cliente (OK)
C_Cliente.pushButton.clicked.connect(cadastrar_cliente)
C_Cliente.pushButton_2.clicked.connect(Cancelar_cadastro_cliente)

# Tela Cadastro Produto (OK)
C_Produto.pushButton.clicked.connect(cancelar_cadastro_produto)
C_Produto.pushButton_2.clicked.connect(cadastrar_produto)

# Tela Cadastro Funcionario (OK)
C_Funcionario.pushButton.clicked.connect(cadastrar_funcionarios)
C_Funcionario.pushButton_2.clicked.connect(cancelar_cadastro_funcionario)


# Tela Menu Incial Cliente
Menu_Inicial_Cliente.logout.triggered.connect(logout)
Menu_Inicial_Cliente.Alterar_dados.triggered.connect(apertar_botao_cliente)
Menu_Inicial_Cliente.Desativar_Conta.triggered.connect(abrir_tela_desativar_conta)
Menu_Inicial_Cliente.pushButton.clicked.connect(clicar_compra_cliente)
Menu_Inicial_Cliente.pushButton_3.clicked.connect(abrir_tela_meus_pedidos_cli)

# Tela desativar cliente
Aviso_desativar_cliente.pushButton_2.clicked.connect(fechar_tela_desativar_conta)
Aviso_desativar_cliente.pushButton_3.clicked.connect(desativar_cliente)


# Tela alterar dados (OK)
Alterar_Dados.pushButton.clicked.connect(alterar_dados_cli)
Alterar_Dados.pushButton_2.clicked.connect(cancelar_alterar_dados)

# Tela Menu Incial Funcionario
Menu_Funcionarios.pushButton_3.clicked.connect(abre_tela_gerenciar_cliente)
Menu_Funcionarios.pushButton_4.clicked.connect(clicar_compra_funcionario)
Menu_Funcionarios.pushButton_5.clicked.connect(abrir_tela_gerenciar_produtos)
Menu_Funcionarios.pushButton_6.clicked.connect(verificar_permissao_func)
Menu_Funcionarios.pushButton_7.clicked.connect(logout)
Menu_Funcionarios.pushButton_2.clicked.connect(abrir_tela_pedidos_funcionarios)
Menu_Funcionarios.pushButton.clicked.connect(abrir_tela_estatisticas)


# Tela Pegar ID (OK)
Pegar_id_cli.pushButton.clicked.connect(Pegar_id_cli_OK)
Pegar_id_cli.pushButton_2.clicked.connect(Pegar_id_cli_CANCEL)


# Tela Compras Cliente (OK)
Comprar_Produto.pushButton_4.clicked.connect(voltar_menu_cliente)
Comprar_Produto.pushButton.clicked.connect(abrir_tela_carrinho_compras)
Comprar_Produto.pushButton_2.clicked.connect(mandar_para_carrinho)
Comprar_Produto.pushButton_3.clicked.connect(listar_catalogo)

# Tela Gerenciamento de Produtos (OK)
Gerenciar_Produto.pushButton_4.clicked.connect(abrir_tela_cadastro_produto)
Gerenciar_Produto.pushButton_5.clicked.connect(voltar_menu)
Gerenciar_Produto.pushButton_6.clicked.connect(alterar_status_produto)

# Tela Gerenciamento de Cliente (OK)
Gerenciar_Cliente.pushButton.clicked.connect(filtragem_cliente)
Gerenciar_Cliente.pushButton_2.clicked.connect(listar_cliente)
Gerenciar_Cliente.pushButton_3.clicked.connect(alterar_status_cli)
Gerenciar_Cliente.pushButton_4.clicked.connect(abre_tela_cadastro_cliente)
Gerenciar_Cliente.pushButton_5.clicked.connect(voltar_menu)
Gerenciar_Cliente.pushButton_6.clicked.connect(apertar_botao_funcionario)


# Tela Gerenciamento de Funcionarios (OK)
Gerenciar_Funcionario.pushButton_4.clicked.connect(abre_tela_cadastro_funcionario)
Gerenciar_Funcionario.pushButton_5.clicked.connect(voltar_menu)
Gerenciar_Funcionario.pushButton_6.clicked.connect(demitir_funcionarios)
Gerenciar_Funcionario.pushButton_7.clicked.connect(alterar_gerente)

# Carrinho de Compras (OK)
Carrinho_Compras.pushButton_6.clicked.connect(carrinho_para_pedido)
Carrinho_Compras.pushButton_7.clicked.connect(remover_item_carrinho)
Carrinho_Compras.pushButton_8.clicked.connect(fechar_tela_carrinho_compras)

# Ver Pedidos
Pedidos_cliente.pushButton_3.clicked.connect(voltar_menu_cliente2)
Pedidos_cliente.pushButton_2.clicked.connect(ped_produtos_cliente)
Pedidos_cliente.pushButton.clicked.connect(abrir_tela_pgto_cliente)

# Consultar Pedidos Funcionarios
Pedidos_funcionario.pushButton.clicked.connect(abrir_tela_historico)
Pedidos_funcionario.pushButton_2.clicked.connect(alterar_status_ped)
Pedidos_funcionario.pushButton_3.clicked.connect(voltar_menu_funcionario)
Pedidos_funcionario.pushButton_4.clicked.connect(ped_produtos_funcionario)
Pedidos_funcionario.pushButton_5.clicked.connect(abrir_tela_pgto_funcionario)
Pedidos_funcionario.pushButton_6.clicked.connect(listar_pedidos_funcionario)

# Itens_pedido (OK)
Itens_pedido.pushButton.clicked.connect(fechar_tela_itens_pedidos)

# Tela Pagamento
Pagamento.pushButton.clicked.connect(efetuar_pagamento)
Pagamento.pushButton_2.clicked.connect(fechar_tela_pgto)

# Tela Estatisticas_Empresa
Estatisticas.pushButton.clicked.connect(fechar_tela_estatisticas)
Estatisticas.pushButton_3.clicked.connect(todos_meses)

# Historioco Pagamento
Historico_pgto.pushButton.clicked.connect(fechar_tela_historico)
Historico_pgto.pushButton_2.clicked.connect(listar_histórico_pagamento)

app.exec()


# proximas etapas
'''
CPF - Somente numero e limitar (OK)
telefeno - somente numeto e limitar (OK)
1 - Criar janela de configuração na qual posso desativar minha conta (OK)
2 - Verificar se o cliente está ativo (OK)

3 - Terminar carrinho (OK)
4 - Criar o pedido (OK)
5 - Verificar o pedido (OK)
6 - Listar pedidos (OK)
7 - Efetuar pagamento

6 - Fazer as consultas mais detalhadas
1.4.1.  Todos os pedidos associados a uma conta; (OK)
1.4.2.  Todos os produtos contidos em um determinado carrinho de compras; (OK)
1.4.3.  Dados (e a quantidade) dos usuarios cadastrados no sistema; (OK)
1.4.5.  Filtrar usuarios por bairro, cidade e estado; (OK)
1.4.4.  Forma de pagamento mais utilizada; Pronto
1.4.6.  Media anual de vendas; Pronto
1.4.7.  Mês e ano com maior numero de vendas;
1.4.8.  Usuarios que realizaram compras em todos os meses de um determinado ano; Pronto

7- Extras
-> Filtrar cliente e produto por nome (OK)
-> Produtos mais vendido (OK)
-> Lista histórico de pagamento e filtar ID Pedido e Mtd_pagamento (OK)
-> Filtrar pedidos por id e nome (OK)

    ARRUMAR :
    -> Imagem dos meus pedidos, está muito mal formatada (cliente)
    -> Arrumar cadastro funcionário, assim como já está arrumado o cadastro de cliente
    ->
    
'''
 