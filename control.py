# uic lê o arquivo .ui // QtWidgets monta os componentes na tela
from PyQt5 import uic, QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas 

# Conexão com o Banco de Dados
banco = mysql.connector.connect(

    host='127.0.0.1',
    user='root',
    password='',
    database='cadastro_produtos'
)

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
    
    print('Produto: ',line1)
    print('Preço: ',line2)
    print('Código: ',line3)

    if form.radioButton.isChecked():
        print('Perecíveis selecionado.')
        category = 'Perecíveis'
    if form.radioButton_2.isChecked():
        print('Álcool selecionado.')
        category = 'Álcool'
    if form.radioButton_3.isChecked():
        print('Não perecíveis selecionado.')
        category = 'Não Perecíveis'
    if form.radioButton_4.isChecked():
        print('Bebidas selecionado.')
        category = 'Bebidas'
    if form.radioButton_5.isChecked():
        print('Pet selecionado.')
        category = 'Pet'
    if form.radioButton_6.isChecked():
        print('Utensílhos selecionado.')
        category = 'Utensílhos'

    # Comandos ao MySQL
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


def update_data():
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
    
    update_form.show()
    update_form.lineEdit.setText(str(data_to_update[0][1]))
    update_form.lineEdit_2.setText(str(data_to_update[0][2]))
    update_form.lineEdit_3.setText(str(data_to_update[0][3]))
    update_form.lineEdit_4.setText(str(data_to_update[0][4]))

    # parou aqui

    


app = QtWidgets.QApplication([])
form = uic.loadUi('form.ui')
data_list = uic.loadUi('data_list.ui')
update_form = uic.loadUi('update.ui')
form.pushButton.clicked.connect(principal_function)
form.pushButton_2.clicked.connect(show_data_list)
data_list.pushButton.clicked.connect(create_pdf)
data_list.pushButton_3.clicked.connect(delete_data)
data_list.pushButton_2.clicked.connect(update_data)

form.show()
app.exec()