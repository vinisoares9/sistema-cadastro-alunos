# Interface Gráfica (GUI):

import tkinter as tk
from tkinter import ttk, messagebox
from poo import GerenciadorAlunos

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Sistema de Cadastro de Alunos (CRUD simples)')
        self.root.geometry('700x500')
        self.gerenciador = GerenciadorAlunos()
        self.criar_frames()
        self.criar_widgets_formulario()
        self.criar_widgets_botoes()
        self.criar_treeview_lista()
        self.atualizar_lista_alunos()

    def criar_frames(self):
        self.frame_formulario = ttk.Frame(self.root, padding=10)
        self.frame_formulario.pack(fill='x')
        self.frame_botoes = ttk.Frame(self.root, padding=10)
        self.frame_botoes.pack(fill='x')
        self.frame_lista = ttk.Frame(self.root, padding=10)
        self.frame_lista.pack(fill='both', expand=True)

    def criar_widgets_formulario(self):
        ttk.Label(self.frame_formulario, text='Matrícula:').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_matricula = ttk.Entry(self.frame_formulario, width=40)
        self.entry_matricula.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.frame_formulario, text='Nome:').grid(row=1, column=0, padx=5,pady=5, sticky='w')
        self.entry_nome = ttk.Entry(self.frame_formulario, width=40)
        self.entry_nome.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self.frame_formulario, text='Curso:').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.entry_curso = ttk.Entry(self.frame_formulario, width=40)
        self.entry_curso.grid(row=2, column=1, padx=5, pady=5)

    def criar_widgets_botoes(self):
        self.botao_adicionar = ttk.Button(self.frame_botoes, text='Adicionar', command=self.adicionar_aluno)
        self.botao_adicionar.pack(side='left',padx=5)
        self.botao_atualizar = ttk.Button(self.frame_botoes,text = 'Atualizar', command=self.atualizar_aluno)
        self.botao_atualizar.pack(side='left', padx=5)
        self.botao_deletar = ttk.Button(self.frame_botoes, text='Deletar', command=self.deletar_aluno)
        self.botao_deletar.pack(side='left', padx=5)
        self.botao_buscar = ttk.Button(self.frame_botoes, text='Buscar (por matrícula)', command=self.buscar_aluno)
        self.botao_buscar.pack(side='left', padx=5)
        self.botao_limpar = ttk.Button(self.frame_botoes, text='Limpar campos', command=self.limpar_campos)
        self.botao_limpar.pack(side='left', padx=5)

    def criar_treeview_lista(self):
        colunas = ('matricula', 'nome', 'curso')
        self.tree_alunos = ttk.Treeview(self.frame_lista, columns=colunas, show='headings')
        self.tree_alunos.heading('matricula', text='Matrícula')
        self.tree_alunos.heading('nome', text='Nome')
        self.tree_alunos.heading('curso', text='Curso')
        self.tree_alunos.column('matricula', width=100, stretch=tk.NO)
        self.tree_alunos.column('nome', width=250)
        self.tree_alunos.column('curso', width=250)
        scrollbar = ttk.Scrollbar(self.frame_lista, orient='vertical', command=self.tree_alunos.yview)
        self.tree_alunos.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.tree_alunos.pack(fill='both', expand=True)
        self.tree_alunos.bind('<<TreeviewSelect>>', self.ao_selecionar_item)

    def adicionar_aluno(self):
        try:
            matricula = self.entry_matricula.get()
            nome = self.entry_nome.get()
            curso = self.entry_curso.get()
            self.gerenciador.adicionar_aluno(matricula, nome, curso)
            messagebox.showinfo('Sucesso', 'Aluno adicionado com sucesso!')
            self.limpar_campos()
            self.atualizar_lista_alunos()
        except ValueError as e:
            messagebox.showerror('Erro de validação',str(e))

    def atualizar_aluno(self):
        try:
            matricula = self.entry_matricula.get()
            nome = self.entry_nome.get()
            curso = self.entry_curso.get()
            if self.gerenciador.atualizar_aluno(matricula, nome, curso):
                messagebox.showinfo('Sucesso', 'Cadastro do aluno atualizado!')
                self.limpar_campos()
                self.atualizar_lista_alunos()
            else:
                messagebox.showwarning('Erro', 'Aluno não encontrado. Escreva a matrícula correta!')
        except ValueError as e:
            messagebox.showerror('Erro de validação', str(e))

    def deletar_aluno(self):
        matricula = self.entry_matricula.get()
        if not matricula:
            messagebox.showwarning('Aviso', 'Informe a matrícula do aluno a ser deletado:')
            return
        if messagebox.askyesno('Confirmar', f'Tem certeza que deseja deletar o aluno de matrícula {matricula}?'):
            if self.gerenciador.deletar_aluno(matricula):
                messagebox.showinfo('Sucesso', 'Aluno deletado com sucesso.')
                self.limpar_campos()
                self.atualizar_lista_alunos()
            else:
                messagebox.showerror('Erro', 'Aluno não encontrado.')

    def buscar_aluno(self):
        matricula = self.entry_matricula.get()
        if not matricula:
            messagebox.showwarning('Aviso', 'Informe a matrícula para buscar o aluno')
            return
        aluno = self.gerenciador.buscar_aluno(matricula)
        if aluno:
            self.limpar_campos(limpar_matricula=False)
            self.entry_nome.insert(0,aluno.nome)
            self.entry_curso.insert(0,aluno.curso)
        else:
            messagebox.showerror('Erro', 'Aluno não encontrado!')

    def atualizar_lista_alunos(self):
        for row in self.tree_alunos.get_children():
            self.tree_alunos.delete(row)
        lista_de_alunos = self.gerenciador.listar_alunos()
        for aluno in lista_de_alunos:
            self.tree_alunos.insert('','end', values=(aluno.matricula, aluno.nome,aluno.curso))

    def limpar_campos(self, limpar_matricula=True):
        if limpar_matricula:
            self.entry_matricula.delete(0,'end')
        self.entry_nome.delete(0,'end')
        self.entry_curso.delete(0,'end')
        self.tree_alunos.selection_remove(self.tree_alunos.selection())

    def ao_selecionar_item(self,event):
        selected_item = self.tree_alunos.selection()
        if not selected_item:
            return
        item = self.tree_alunos.item(selected_item)
        valores = item['values']
        self.limpar_campos()
        self.entry_matricula.insert(0,valores[0])
        self.entry_nome.insert(0,valores[1])
        self.entry_curso.insert(0,valores[2])

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()