# uic lê o arquivo .ui // QtWidgets monta os componentes na tela
from PyQt5 import uic, QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas
import sqlite3

# Conexão com o Banco de Dados
banco = mysql.connector.connect(

    host='127.0.0.1',
    user='root',
    password='',
    database='cadastro_produtos'
)

# Login no Sistema
def show_form_logged():

    # Definição do usuário e senha
    login.label_4.setText('')
    user = login.lineEdit.text()
    password = login.lineEdit_2.text()

    # Validação do usuário e senha 
    try:
        cursor = banco.cursor()
        query = "SELECT pass FROM cadastro_produtos.usuarios WHERE usuario = '{}'".format(user)
        cursor.execute(query)
        pass_to_confirm = cursor.fetchall()[0][0]

        if password == pass_to_confirm:
            login.close()
            form.show()

    except:
        print('Erro na validação de dados')
        login.label_4.setText('Dados incorretos.')


# Emissão do documento em PDF
def create_pdf():
    cursor = banco.cursor()
    query = 'SELECT * FROM produtos'
    cursor.execute(query)
    received_data = cursor.fetchall()

    y=0
    pdf = canvas.Canvas('cadastro_produtos.pdf')
    pdf.setFont('Times-Bold',14)
    pdf.drawString(200,800,'Produtos Cadastrados')
    pdf.setFont('Times',12)

    pdf.drawString(10,750,'ID')
    pdf.drawString(110,750,'Produto')
    pdf.drawString(210,750,'Preço')
    pdf.drawString(310,750,'Código')
    pdf.drawString(410,750,'Categoria')

    for i in range(0, len(received_data)):
        y = y + 50
        pdf.drawString(10,750 - y, str(received_data[i][0]))
        pdf.drawString(110,750 - y, str(received_data[i][1]))
        pdf.drawString(220,750 - y, str(received_data[i][2]))
        pdf.drawString(330, 750 - y, str(received_data[i][3]))
        pdf.drawString(440,750 - y, str(received_data[i][4]))

    pdf.save()
    print('PDF emitido com sucesso!')

def principal_function():

    # Textos digitados nas caixas do formulário
    line1 = form.lineEdit.text()
    line2 = form.lineEdit_2.text()
    line3 = form.lineEdit_3.text()
    category = ''

    if form.radioButton.isChecked():
        category = "Perecíveis"
    if form.radioButton_2.isChecked():
        category = "Álcool"
    if form.radioButton_3.isChecked():
        category = "Não Perecíveis"
    if form.radioButton_4.isChecked():
        category = "Bebidas"
    if form.radioButton_5.isChecked():
        category = "Pet"
    if form.radioButton_6.isChecked():
        category = "Utensílhos"

    # Cadastro de produtos
    cursor = banco.cursor()
    query = "INSERT INTO produtos (produto, preco, codigo, categoria) VALUES (%s,%s,%s,%s)"
    dados = (str(line1), str(line2), str(line3), category)
    cursor.execute(query,dados)
    banco.commit()

    # Limpar os campos  para um novo preenchimento
    form.lineEdit.setText("")
    form.lineEdit_2.setText("")
    form.lineEdit_3.setText("")
    
def show_data_list():
    
    # Comandos ao MySQL
    
    form.close()
    data_list.show()
    cursor = banco.cursor()
    query = "SELECT * FROM produtos"
    cursor.execute(query)
    received_data = cursor.fetchall()
    
    # Definição da tabela 
    data_list.tableWidget.setRowCount(len(received_data))
    data_list.tableWidget.setColumnCount(5)

    # Inserção de dados na tabela
    for i in range(0, len(received_data)): # Número de linhas
        for j in range(0,5): # Número de colunas
            data_list.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(received_data[i][j]))) 

def delete_data():
    # Nesta etapa é realizada a exclusão na tabela, apenas.
    number_line = data_list.tableWidget.currentRow()
    data_list.tableWidget.removeRow(number_line)
    
    # Exclusão de dados no banco
    cursor = banco.cursor()
    query = 'SELECT id FROM produtos' # Seleciona o ID para execução da query
    cursor.execute(query)
    received_data = cursor.fetchall()
    id = received_data[number_line][0]
    
    query_to_delete = ('DELETE FROM produtos WHERE id =' + (str(id)))
    cursor.execute(query_to_delete)
    banco.commit()
    confirm_delete_form.close()


def update_data():
    data_list.close()
    number_line = data_list.tableWidget.currentRow()
    
    # Edição de dados no banco
    cursor = banco.cursor()
    query = 'SELECT id FROM produtos' # Seleciona o ID para execução da query
    cursor.execute(query)
    received_data = cursor.fetchall()
    id = received_data[number_line][0]
    
    query_to_update = ('SELECT * FROM produtos WHERE id =' + (str(id)))
    cursor.execute(query_to_update)
    data_to_update = cursor.fetchall()
    #data_to_update = [(id, produto, preço, código, categoria)]
    #print(data_to_update[number_line][4]) = Categoria

    update_form.show()
    update_form.lineEdit.setText(str(data_to_update[0][1])) # Produto
    update_form.lineEdit_2.setText(str(data_to_update[0][2])) # Preço
    update_form.lineEdit_3.setText(str(data_to_update[0][3])) # Código
    category_to_confirm = (str(data_to_update[0][4])) #categoria


    if category_to_confirm == 'Perecíveis':
        update_form.radioButton.setChecked(True)
    elif category_to_confirm == 'Álcool':
        update_form.radioButton_2.setChecked(True)
    elif category_to_confirm == 'Não Perecíveis':
        update_form.radioButton_3.setChecked(True)
    elif category_to_confirm == 'Bebidas':
        update_form.radioButton_4.setChecked(True)
    elif category_to_confirm == 'Pet':
        update_form.radioButton_5.setChecked(True)
    elif category_to_confirm == 'Utensílhos':
        update_form.radioButton_6.setChecked(True)
    else:
        print('Erro em Update Data')
    
    # Obtendo dados para atualizar 

def save_update():

    # Seleção do ID
    number_line = data_list.tableWidget.currentRow()
    data_list.tableWidget.removeRow(number_line)

    cursor = banco.cursor()
    query = 'SELECT id FROM produtos' # Seleciona o ID para execução da query
    cursor.execute(query)
    received_data = cursor.fetchall()
    id = received_data[number_line][0]

    print('teste')
    new_product = update_form.lineEdit.text()
    print(new_product)
    new_price = update_form.lineEdit_2.text()
    print(new_price)
    new_cod = update_form.lineEdit_3.text()
    print(new_cod)

    new_category = ''
    if update_form.radioButton.isChecked():
        new_category = "Perecíveis"
    elif update_form.radioButton_2.isChecked():
        new_category = "Álcool"
    elif update_form.radioButton_3.isChecked():
        new_category = "Não Perecíveis"
    elif update_form.radioButton_4.isChecked():
        new_category = "Bebidas"
    elif update_form.radioButton_5.isChecked():
        new_category = "Pet"
    elif update_form.radioButton_6.isChecked():
        new_category = "Utensílhos"
    else:
        print('Erro no Update')
    print(new_category)
    # Edição no Banco de Dados 
    
    cursor = banco.cursor()
    query = f"UPDATE produtos SET produto = '{new_product}', preco = '{new_price}', codigo = '{new_cod}', categoria = '{new_category}' WHERE id = '{id}';"
    print(query)
    cursor.execute(query)
    banco.commit()


    
def register():
    user = register_form.lineEdit.text()
    password = register_form.lineEdit_2.text()
    confirmerd_password = register_form.lineEdit_3.text()
    email = register_form.lineEdit_4.text()

    if (password == confirmerd_password):
        try:
            cursor = banco.cursor()
            query = 'INSERT INTO cadastro_produtos.usuarios (usuario, pass, email) VALUES (%s,%s,%s)'
            dados = (str(user), (str(password)), str(email))
            cursor.execute(query,dados)
            banco.commit()
            register_form.label_5.setText('Cadastro realizado com sucesso.')
        except sqlite3.Error as erro:
            print('Erro ao cadastrar: ',erro)
            register_form.label_5.setText('Erro ao cadastrar.')
    else:
        register_form.label_5.setText('As senhas não podem ser diferentes.')

#____________________________________________________
# Controle te telas

def back_to_login():
    register_form.close()
    login.show()

def show_login():
    form.close()
    login.show()

def show_register_form():
    login.close()
    register_form.show()

def back_to_data_list():
    update_form.close()
    data_list.show()

def back_to_data_list_2():
    confirm_delete_form.close()
    data_list.show()

def back_to_form():
    data_list.close()
    form.show()

def confirm_delete():
    confirm_delete_form.show() 

#____________________________________________________

# Declarações

app = QtWidgets.QApplication([])
login = uic.loadUi('login.ui')
form = uic.loadUi('form.ui')
data_list = uic.loadUi('data_list.ui')
update_form = uic.loadUi('update.ui')
register_form = uic.loadUi('cadastro.ui')
confirm_delete_form = uic.loadUi('confirm_delete.ui')

# Chamadas
#____________________________________________________
form.pushButton.clicked.connect(principal_function)
form.pushButton_2.clicked.connect(show_data_list)
form.pushButton_3.clicked.connect(show_login) # Log Out
#____________________________________________________
login.pushButton.clicked.connect(show_form_logged) # Entra na página principal
login.pushButton_2.clicked.connect(show_register_form) # Efetua o cadastro
login.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password) # Senha anônima
#____________________________________________________
register_form.pushButton.clicked.connect(register)
register_form.pushButton_2.clicked.connect(back_to_login)
#____________________________________________________
update_form.pushButton.clicked.connect(save_update) # Salvar os dados modificados
update_form.pushButton_2.clicked.connect(back_to_data_list)
#____________________________________________________
confirm_delete_form.pushButton.clicked.connect(delete_data) # Confirmação de exclusão
confirm_delete_form.pushButton_2.clicked.connect(back_to_data_list_2)
#____________________________________________________
data_list.pushButton.clicked.connect(create_pdf)
data_list.pushButton_3.clicked.connect(confirm_delete)
data_list.pushButton_2.clicked.connect(update_data)
data_list.pushButton_4.clicked.connect(back_to_form)
#____________________________________________________
# Start 

login.show()
app.exec()