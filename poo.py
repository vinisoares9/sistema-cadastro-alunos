# Lógica de negócio (POO):

class Aluno:
    def __init__(self, matricula, nome, curso):
        self.matricula = matricula
        self.nome = nome
        self.curso = curso

class GerenciadorAlunos:
    def __init__(self):
        self.alunos = []

    def adicionar_aluno(self, matricula, nome, curso):
        if not matricula or not nome or not curso:
            raise ValueError('Todos os campos devem estar preenchidos!')
        if self.buscar_aluno(matricula):
            raise ValueError('Matrícula já cadastrada!')
        aluno = Aluno(matricula, nome, curso)
        self.alunos.append(aluno)
        return True

    def listar_alunos(self):
        return self.alunos

    def buscar_aluno(self, matricula):
        for aluno in self.alunos:
            if aluno.matricula == matricula:
                return aluno
        return None

    def atualizar_aluno(self, matricula, novo_nome, novo_curso):
        aluno = self.buscar_aluno(matricula)
        if not aluno:
            return False
        if not novo_nome or not novo_curso:
            raise ValueError('"Nome" e "Curso" não podem ficar em branco!')
        aluno.nome = novo_nome
        aluno.curso = novo_curso
        return True

    def deletar_aluno(self, matricula):
        aluno = self.buscar_aluno(matricula)
        if aluno:
            self.alunos.remove(aluno)
            return True
        return False