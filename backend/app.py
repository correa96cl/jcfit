# Importação
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy.exc import StatementError
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

CORS(app, origins="*")

class Aluno(db.Model):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(500), nullable=False)
    sobrenome = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    telefone = db.Column(db.String(50), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    ativo = db.Column(db.Integer, nullable=False)

class Aula(db.Model):
    __tablename__ = 'aulas'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    duracao = db.Column(db.Interval, nullable=False)
    localizacao = db.Column(db.Text, nullable=False)

class AlunoAula(db.Model):
    __tablename__ = 'aluno_aula'
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    aula_id = db.Column(db.Integer, db.ForeignKey('aulas.id'), nullable=False)
    status = db.Column(db.Integer, nullable=False)

class Exercicio(db.Model):
    __tablename__ = 'exercicios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text, nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    grupo_muscular = db.Column(db.Text, nullable=False)

class ProgressoAluno(db.Model):
    __tablename__ = 'progresso_aluno'
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    peso = db.Column(db.Numeric, nullable=False)
    gordura_corporal = db.Column(db.Numeric, nullable=False)
    musculo = db.Column(db.Numeric, nullable=False)

class Rotina(db.Model):
    __tablename__ = 'rotinas'
    id = db.Column(db.Integer, primary_key=True)
    aula_id = db.Column(db.Integer, db.ForeignKey('aulas.id'), nullable=False)
    nome = db.Column(db.Text, nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    link = db.Column(db.Text, nullable=False)
# Definir uma rota raiz (página inicial) e a função que será executada ao requisitar
@app.route('/api/alunos/add', methods=['POST'])
def add_alunos():
    data = request.json
    print(data)
    if 'nome' in data and 'sobrenome' in data and 'email' in data and 'telefone' in data and 'data_nascimento' in data and 'ativo' in data:
        try:
            data_nascimento = datetime.strptime(data['data_nascimento'],'%d/%m/%Y').date()

            print(data_nascimento)

            # Verificar se o aluno já existe
            aluno_existente = Aluno.query.filter_by(email=data['email']).first()
            if aluno_existente:
                return jsonify({'message': 'Aluno com este email já cadastrado'}), 400

            aluno = Aluno(nome=data['nome'], sobrenome=data['sobrenome'], email=data['email'], telefone=data['telefone'], data_nascimento=data_nascimento, ativo=1)
            db.session.add(aluno)
            db.session.commit()
            return jsonify({'message': f'Aluno adicionado com sucesso! ID: {aluno.id}'}), 201
        except ValueError:
            return jsonify({'message': 'Formato de data inválido. Use o formato AAAA-MM-DD'}), 400
        except StatementError as e:
            db.session.rollback()  # Importante: Desfaz a transação em caso de erro
            return jsonify({'message': f'Erro ao adicionar aluno: {str(e)}'}), 500

    return jsonify({'message': 'Dados inválidos'}), 400

@app.route('/api/alunos/<id>', methods=['GET'])
def get_aluno(id):
    try:
        id_int = int(id)
        aluno = Aluno.query.get(id_int)
        if aluno:
                return jsonify({
                    'id': aluno.id,
                    'nome': aluno.nome,
                    'sobrenome': aluno.sobrenome,
                    'email': aluno.email,
                    'telefone': aluno.telefone,
                    'data_nascimento': aluno.data_nascimento,
                    'ativo': aluno.ativo
                })
        return jsonify({'message': 'Aluno não encontrado'}), 404
    except ValueError:
        return jsonify({'message': 'ID inválido. Deve ser um número inteiro'}), 400

@app.route('/api/alunos/filtros', methods=['POST'])
def get_aluno_por_filtros():
    data = request.json
    alunos = Aluno.query.filter_by(id=data['id'], nome=data['nome'], sobrenome=data['sobrenome'], email=data['email'], telefone=data['telefone'], data_nascimento=data['data_nascimento'], ativo=data['ativo'])
    if alunos:
        alunos_json = []
        for aluno in alunos:
            alunos_json.append({
                'id': aluno.id,
                'nome': aluno.nome,
                'sobrenome': aluno.sobrenome,
                'email': aluno.email,
                'telefone': aluno.telefone,
                'data_nascimento': aluno.data_nascimento,
                'ativo': aluno.ativo
            })
        return jsonify(alunos_json)
    return jsonify({'message': 'Aluno nao encontrado'}), 404

@app.route('/api/alunos', methods=['GET'])
def get_alunos():
    alunos = Aluno.query.all()
    alunos_json = []
    for aluno in alunos:
        alunos_json.append({
            'id': aluno.id,
            'nome': aluno.nome,
            'sobrenome': aluno.sobrenome,
            'email': aluno.email,
            'telefone': aluno.telefone,
            'data_nascimento': aluno.data_nascimento,
            'ativo': aluno.ativo
        })
    return jsonify(alunos_json)

@app.route('/api/alunos/<int:id>', methods=['PUT'])
def update_aluno(id):
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({'message': 'Aluno nao encontrado'}), 404
    data = request.json
    if 'nome' in data:
        aluno.nome = data['nome']
    if 'sobrenome' in data:
        aluno.sobrenome = data['sobrenome']
    if 'email' in data:
        aluno.email = data['email']
    if 'telefone' in data:
        aluno.telefone = data['telefone']
    if 'data_nascimento' in data:
        aluno.data_nascimento = data['data_nascimento']
    db.session.commit()
    return jsonify({'message': 'Aluno atualizado com sucesso!'}), 200

@app.route('/api/alunos/inativar/<int:id>', methods=['PATCH'])
def inativar_aluno(id):
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({'message': 'Aluno nao encontrado'}), 404
    aluno.ativo = 0
    db.session.commit()
    return jsonify({'message': 'Aluno inativado com sucesso!'}), 200

@app.route('/api/alunos/ativar/<int:id>', methods=['PATCH'])
def ativar_aluno(id):
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({'message': 'Aluno nao encontrado'}), 404
    aluno.ativo = 1
    db.session.commit()
    return jsonify({'message': 'Aluno ativado com sucesso!'}), 200

# Rotas para Aula
@app.route('/api/aulas/add', methods=['POST'])
def add_aulas():
    data = request.json
    hours_str = data['duracao']['hours']
    minutes_str = data['duracao']['minutes']
    try:
        print(data['data_hora'])
        data_hora = datetime.strptime(data['data_hora'], '%Y-%m-%d %H:%M:%S')
        print(data_hora)
        hours = int(hours_str)
        minutes = int(minutes_str)
        duracao = timedelta(hours=hours, minutes=minutes)
        aula = Aula(descricao=data['descricao'], data_hora=data_hora, duracao=duracao, localizacao=data['localizacao'])
        db.session.add(aula)
        db.session.commit()
        return jsonify({'message': f'Aula adicionada com sucesso! ID: {aula.id}'}), 201
    except Exception as e:
        return jsonify({'message': f'Erro ao adicionar aula: {str(e)}'}), 400

@app.route('/api/aulas/<int:id>', methods=['GET'])
def get_aula(id):
    aula = Aula.query.get(id)
    try:
        if aula:
            return jsonify({
            'id': aula.id,
            'descricao': aula.descricao,
            'data_hora': aula.data_hora,
            'duracao': {'hours': aula.duracao.seconds // 3600, 'minutes': (aula.duracao.seconds % 3600) // 60},
            'localizacao': aula.localizacao
            })
    except Exception as e:
        return jsonify({'message': f'Erro ao obter aula: {str(e)}'}), 400
    return jsonify({'message': 'Aula não encontrada'}), 404

@app.route('/api/aulas', methods=['GET'])
def get_aulas():
    aulas = Aula.query.all()
    aulas_json = []
    for aula in aulas:
        aulas_json.append({
            'id': aula.id,
            'descricao': aula.descricao,
            'data_hora': aula.data_hora,
            'duracao': {'hours': aula.duracao.seconds // 3600, 'minutes': (aula.duracao.seconds % 3600) // 60},
            'localizacao': aula.localizacao
        })
    return jsonify(aulas_json)

# Rotas para AlunoAula
@app.route('/api/aluno_aula/add', methods=['POST'])
def add_aluno_aula():
    data = request.json
    try:
        aluno_aula = AlunoAula(aluno_id=data['aluno_id'], aula_id=data['aula_id'], status=data['status'])
        db.session.add(aluno_aula)
        db.session.commit()
        return jsonify({'message': f'Registro de aluno_aula adicionado com sucesso! ID: {aluno_aula.id}'}), 201
    except Exception as e:
        return jsonify({'message': f'Erro ao adicionar registro de aluno_aula: {str(e)}'}), 400

@app.route('/api/aluno_aula/<int:id>', methods=['GET'])
def get_aluno_aula(id):
    aluno_aula = AlunoAula.query.get(id)
    if aluno_aula:
        return jsonify({
            'id': aluno_aula.id,
            'aluno_id': aluno_aula.aluno_id,
            'aula_id': aluno_aula.aula_id,
            'status': aluno_aula.status
        })
    return jsonify({'message': 'Registro de aluno_aula não encontrado'}), 404

# Rotas para Exercicio
@app.route('/api/exercicios/add', methods=['POST'])
def add_exercicio():
    data = request.json
    try:
        exercicio = Exercicio(nome=data['nome'], descricao=data['descricao'], grupo_muscular=data['grupo_muscular'])
        db.session.add(exercicio)
        db.session.commit()
        return jsonify({'message': f'Exercício adicionado com sucesso! ID: {exercicio.id}'}), 201
    except Exception as e:
        return jsonify({'message': f'Erro ao adicionar exercício: {str(e)}'}), 400

@app.route('/api/exercicios/<int:id>', methods=['GET'])
def get_exercicio(id):
    exercicio = Exercicio.query.get(id)
    if exercicio:
        return jsonify({
            'id': exercicio.id,
            'nome': exercicio.nome,
            'descricao': exercicio.descricao,
            'grupo_muscular': exercicio.grupo_muscular
        })
    return jsonify({'message': 'Exercício não encontrado'}), 404

@app.route('/api/exercicios', methods=['GET'])
def get_exercicios():
    exercicios = Exercicio.query.all()
    exercicios_json = []
    for exercicio in exercicios:
        exercicios_json.append({
            'id': exercicio.id,
            'nome': exercicio.nome,
            'descricao': exercicio.descricao,
            'grupo_muscular': exercicio.grupo_muscular
        })
    return jsonify(exercicios_json)

# Rotas para ProgressoAluno
@app.route('/api/progresso_aluno/add', methods=['POST'])
def add_progresso_aluno():
    data = request.json
    try:
        progresso = ProgressoAluno(
            aluno_id=data['aluno_id'],
            data=datetime.strptime(data['data'], '%Y-%m-%d').date(),
            peso=data['peso'],
            gordura_corporal=data['gordura_corporal'],
            musculo=data['musculo']
        )
        db.session.add(progresso)
        db.session.commit()
        return jsonify({'message': f'Progresso do aluno adicionado com sucesso! ID: {progresso.id}'}), 201
    except Exception as e:
        return jsonify({'message': f'Erro ao adicionar progresso do aluno: {str(e)}'}), 400

@app.route('/api/progresso_aluno/<int:id>', methods=['GET'])
def get_progresso_aluno(id):
    progresso = ProgressoAluno.query.get(id)
    if progresso:
        return jsonify({
            'id': progresso.id,
            'aluno_id': progresso.aluno_id,
            'data': progresso.data.strftime('%Y-%m-%d'),
            'peso': float(progresso.peso),
            'gordura_corporal': float(progresso.gordura_corporal),
            'musculo': float(progresso.musculo)
        })
    return jsonify({'message': 'Progresso do aluno não encontrado'}), 404

@app.route('/api/progresso_aluno/aluno/<int:aluno_id>', methods=['GET'])
def get_progresso_aluno_por_aluno(aluno_id):
    progressos = ProgressoAluno.query.filter_by(aluno_id=aluno_id).all()
    if progressos:
        progressos_json = []
        for progresso in progressos:
            progressos_json.append({
                'id': progresso.id,
                'aluno_id': progresso.aluno_id,
                'data': progresso.data.strftime('%Y-%m-%d'),
                'peso': float(progresso.peso),
                'gordura_corporal': float(progresso.gordura_corporal),
                'musculo': float(progresso.musculo)
            })
        return jsonify(progressos_json)
    return jsonify({'message': 'Progresso do aluno não encontrado para este aluno'}), 404

# Rotas para Rotina
@app.route('/api/rotinas/add', methods=['POST'])
def add_rotina():
    data = request.json
    try:
        rotina = Rotina(
            aula_id=data['aula_id'],
            nome=data['nome'],
            descricao=data['descricao']
        )
        db.session.add(rotina)
        db.session.commit()
        return jsonify({'message': f'Rotina adicionada com sucesso! ID: {rotina.id}'}), 201
    except Exception as e:
        return jsonify({'message': f'Erro ao adicionar rotina: {str(e)}'}), 400

@app.route('/api/rotinas/<int:id>', methods=['GET'])
def get_rotina(id):
    rotina = Rotina.query.get(id)
    if rotina:
        return jsonify({
            'id': rotina.id,
            'aula_id': rotina.aula_id,
            'nome': rotina.nome,
            'descricao': rotina.descricao
        })
    return jsonify({'message': 'Rotina não encontrada'}), 404

@app.route('/api/rotinas/aula/<int:aula_id>', methods=['GET'])
def get_rotinas_por_aula(aula_id):
    rotinas = Rotina.query.filter_by(aula_id=aula_id).all()
    if rotinas:
        rotinas_json = []
        for rotina in rotinas:
            rotinas_json.append({
                'id': rotina.id,
                'aula_id': rotina.aula_id,
                'nome': rotina.nome,
                'descricao': rotina.descricao
            })
        return jsonify(rotinas_json)
    return jsonify({'message': 'Rotinas não encontradas para esta aula'}), 404

if __name__ == "__main__":
    app.run(debug=True)