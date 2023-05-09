#-*- coding: cp1252 -*-
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import conexao.conexao as conexao


tela = tk.Tk()
def calendario():
    
    exec(open('calendario.py').read(),locals())

### limpar tela ###
def limpar():
    txtcodigo.delete(0,"end")
    txtnome.delete(0,"end")
    txtclassificacao.delete(0,"end")
    txtcelular.delete(0,"end")
    txttelefone.delete(0,"end")
    txtemail.delete(0,"end")
    txtobservacao.delete("1.0","end")
    txtcodigo.focus_set()





    ### buscar nome ##
def buscar():
    var_codigo = txtcodigo.get()
 
    con=conexao.conexao()
    sql_txt = f"select codigo,nome,classificacao,celular,telefone,email,observacao from agenda where codigo = {var_codigo}"
    rs=con.consultar(sql_txt)

    if rs:
    
        limpar()

        txtcodigo.insert(0, rs[0])
        txtnome.insert(0, rs[1])
        txtclassificacao.insert(0, rs[2])
        txtcelular.insert(0, rs[3])
        txttelefone.insert(0,rs[4])
        txtemail.insert(0,rs[5])
        txtobservacao.insert("1.0",(rs[6]))
    
    else:
        messagebox.showwarning("Aviso", "C�digo n�o Encontrado")
        limpar()
        txtcodigo.focus_set()

   

    con.fechar()

### clicar limpar ###
def duplo_click(event):
    limpar()
    item = tree.item(tree.selection())
    txtcodigo.insert(0, item['values'][0])
    buscar()

def visualizar():
    con=conexao.conexao()
    sql_txt = f"select * from agenda "
    rs=con.consultar_tree(sql_txt)

    tree.bind("<Double-1>", duplo_click)
    
    for linha in tree.get_children():
        tree.delete(linha)
    
    for linha in rs:
        tree.insert("", tk.END, values=linha)

    con.fechar()

### pesquisar nomes ###
def pesquisar_nome(p):
    con=conexao.conexao()
    sql_txt = f"select * from agenda where nome like '%{p}%'"
    
    rs=con.consultar_tree(sql_txt)

    tree.bind("<Double-1>", duplo_click)
    
    for linha in tree.get_children():
        tree.delete(linha)
    
    for linha in rs:
        tree.insert("", tk.END, values=linha)

    con.fechar()

    return True






### gravar banco de dados ###

def gravar():
    var_codigo = txtcodigo.get()
    var_nome = txtnome.get()
    var_classificacao = txtclassificacao.get()
    var_celular = txtcelular.get()
    var_telefone = txttelefone.get()
    var_email = txtemail.get()
    var_observacao = txtobservacao.get("1.0","end")


    con=conexao.conexao()
    sql_txt = f"select codigo,nome,classificacao,celular,telefone,email,observacao from agenda where codigo = {var_codigo}"

    rs=con.consultar(sql_txt)

    if rs:
        sql_text = f"update agenda set nome='{var_nome}', classificao=',{var_classificacao}',celular='{var_celular}', telefone='{var_telefone}',email='{var_email}',observacao='{var_observacao}' where codigo = '{var_codigo}'"
    else:
        sql_text = f"insert into agenda(codigo,nome,classificacao,celular,telefone,email,observacao) values ({var_codigo},'{var_nome}','{var_classificacao}','{var_celular}','{var_telefone}','{var_email}','{var_observacao}')"
    
    if con.gravar(sql_text):
        messagebox.showinfo("Aviso", "Item Gravado com Sucesso")
        limpar()
        visualizar()
    else:
        messagebox.showerror("Erro", "Houve um Erro na Gravaca o")

    con.fechar()


    ### aviso para excluir ###
def excluir():
    var_del = messagebox.askyesno("Excluido", "Tem certeza que deseja excluir?")
    if var_del == True:
        var_codigo = txtcodigo.get()

        con=conexao.conexao()
        sql_text = f"delete from agenda where codigo = '{var_codigo}'"
        if con.gravar(sql_text):
              messagebox.showinfo("Aviso", "Item Excluido com Sucesso")
              limpar()
              visualizar()
        else:
            messagebox.showerror("Erro", "Houve um Erro na Exclusao")

            
        con.fechar()

       
    else:
        limpar()
### tela do sistema ###
tela.geometry('1366x768+0+0')
tela.state('zoomed')
tela['bg'] = 'dimgray'
tela.title('agenda')
pes_nome = tela.register(func=pesquisar_nome)



### texto codigo ###
lblcodigo = tk.Label (tela, text = 'Codigo:', bg='dimgray', fg='white', font=('Calibri', 12), anchor = 'w')
lblcodigo.place(x = 50, y = 60, width= 80, height = 25)


#digitacao do texto do codigos
txtcodigo = tk.Entry(tela,width = 35,font=('Calibri', 12))
txtcodigo.place(x= 150, y=60, width = 100,height= 25)

buscabtn = tk.Button(tela, text ='Pesquisar',
                     bg ='purple',foreground='white', font=('Calibri', 12, 'bold'), command = buscar)
buscabtn.place(x = 280, y = 60, width = 200, height = 25)

### texto Nome ###
lblnome = tk.Label (tela, text = 'Nome:', bg='dimgray', fg='white', font=('Calibri', 12), anchor = 'w')
lblnome.place(x = 50, y = 100, width= 90, height = 25)

### digitacao do texto do nome ###
txtnome = tk.Entry(tela,width = 100,font=('Calibri', 12))
txtnome.place(x= 150, y=100, width = 360,height= 25)

## texto classificacao ###
lblclassificacao = tk.Label (tela, text = 'Classificao:', bg='dimgray', fg='white', font=('Calibri', 12), anchor = 'w')
lblclassificacao.place(x = 50, y = 140, width= 90, height = 25)

### digitacao do texto do classificacao ###
txtclassificacao = tk.Entry(tela,width = 100,font=('Calibri', 12))
txtclassificacao.place(x= 150, y=140, width = 360,height= 25)

### texto celular ###
lblcelular = tk.Label (tela, text = 'celular:', bg='dimgray', fg='white', font=('Calibri', 12), anchor = 'w')
lblcelular.place(x = 50, y = 180, width= 90, height = 25)

### digitacao do texto do celular ###
txtcelular = tk.Entry(tela,width = 100,font=('Calibri', 12))
txtcelular.place(x= 150, y=180, width = 360,height= 25)

### texto telefone ###
lbltelefone = tk.Label (tela, text = 'Telefone:', bg='dimgray', fg='white', font=('Calibri', 12), anchor = 'w')
lbltelefone.place(x = 50, y = 220, width= 360, height = 25)


### digitacao do texto telefone ###
entry = tk.Entry(tela,width = 100, font=('Calibri', 12))
txttelefone = tk.Entry(tela,width = 35,font=('Calibri', 12))
txttelefone.place(x = 150, y = 220, width= 360, height = 25)

### texto email ###
lblemail = tk.Label (tela, text = 'email:', bg='dimgray',fg='white',font=('Calibri', 12), anchor = 'w')
lblemail.place(x = 50, y = 260, width =90, height = 25)

### digitacao do email ###
txtemail = tk.Entry(tela,width = 35, font=('Calibri',12))
txtemail.place(x = 150, y = 260, width = 360, height = 25)


### texto observacao ###
lblobservaco = tk.Label (tela, text = 'Observaco:', bg='dimgray',fg='white',font=('Calibri', 12), anchor = 'w')
lblobservaco.place(x = 50, y = 300, width = 90, height = 25)

### digitacao da observacao ###
txtobservacao= tk.Text(tela, font=('Calibri', 12))
txtobservacao.place(x=150, y=300, width=360, height=80)

### pequisa por nome ###
lbl_pes_nome = tk.Label(tela, text ="Pesquisar por Nome :", bg="purple", fg="white", font=('Calibri', 12, 'bold'), anchor = "w")
lbl_pes_nome.place(x = 50, y = 480, width=200, height = 25)

txt_pes_nome = tk.Entry(tela, width = 35, font=('Calibri', 12),validate='key', validatecommand=(pes_nome,'%P'))
txt_pes_nome.place(x = 210, y = 480, width = 360, height = 25)




### botao Gravar ###

btngravar = tk.Button(tela, text = 'Gravar',
                      bg = 'purple',foreground='white',font=('Calibri', 12, 'bold'),command = gravar)
btngravar.place(x = 150, y =400, width = 65)

### botao excluir ####

btnexcluir = tk.Button(tela, text = 'Excluir',
                       bg = 'red', foreground='white', font=('Calibri', 12, 'bold'), command = excluir)
btnexcluir.place(x = 250, y =400, width = 65)

### botao limpar ###

btnlimpar =tk.Button(tela, text = 'Limpar',
                     bg = 'purple', foreground='white', font=('Calibri', 12, 'bold'), command = limpar)
btnlimpar.place(x = 350, y = 400, width =65)



style = ttk.Style()
style.configure("mystyle.Treeview", font=("Calibri", 10))
style.configure("mystyle.Treeview.Heading", font=("Calibri", 12, "bold"))

tree = ttk.Treeview(tela, column=("c1", "c2", "c3", "c4", "c5","c6","c7"), show='headings', style="mystyle.Treeview")

tree.column("#1")
tree.heading("#1", text="Codigo")
tree.column("#1", width = 100, anchor ='c')

tree.column("#2")
tree.heading("#2", text="Nome")
tree.column("#2", width = 200, anchor ='c')

tree.column("#3")
tree.heading("#3", text="Classificacao")
tree.column("#3", width = 150, anchor ='c')

tree.column("#4")
tree.heading("#4", text="Celular")
tree.column("#4", width = 100, anchor ='c')

tree.column("#5")
tree.heading("#5", text="Telefone")
tree.column("#5", width = 100, anchor ='w')

tree.column("#6")
tree.heading("#6", text="E-mail")
tree.column("#6", width = 150, anchor ='c')

tree.column("#7")
tree.heading("#7", text="Observacao")
tree.column("#7", width = 350, anchor ='c')

tree.place(x=50,y=510,height=140)

scrollbar = ttk.Scrollbar(tela, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.place(x = 1134, y = 510,height=140)

visualizar()


txtcodigo.focus_set()
tela.mainloop()

