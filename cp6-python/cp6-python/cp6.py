#RM 558380 – Diogo Paquete Weyne
#RM 555290 – João Victor de Souza
#RM 555393 – Gustavo Tonato Maia


import oracledb

# Configurações de conexão
USERNAME = "----"
PASSWORD = "----"
DSN = "-----"


# Função para conectar ao banco de dados
def conectar():
    try:
        conn = oracledb.connect(user=USERNAME, password=PASSWORD, dsn=DSN)
        print("Conexão realizada com sucesso!")
        return conn
    except oracledb.Error as e:
        print(f"Erro ao conectar ao Oracle: {e}")
        return None


# Função para inserir um locatário
def inserir_locatario(conn, locatario_id, nome, data_nascimento, cpf, renda):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Locatario (locatario_id, nome, data_nascimento, cpf, renda)
            VALUES (:locatario_id, :nome, TO_DATE(:data_nascimento, 'YYYY-MM-DD'), :cpf, :renda)
        """, [locatario_id, nome, data_nascimento, cpf, renda])
        conn.commit()
        print("Locatário inserido com sucesso!")
    except oracledb.Error as e:
        print(f"Erro ao inserir locatário: {e}")


# Função para ler os locatários
def ler_locatarios(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Locatario")
        for row in cursor.fetchall():
            print(row)
    except oracledb.Error as e:
        print(f"Erro ao ler locatários: {e}")


# Função para atualizar um locatário
def atualizar_locatario(conn, locatario_id, novo_nome):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Locatario SET nome = :novo_nome
            WHERE locatario_id = :locatario_id
        """, [novo_nome, locatario_id])
        conn.commit()
        print("Locatário atualizado com sucesso!")
    except oracledb.Error as e:
        print(f"Erro ao atualizar locatário: {e}")


# Função para excluir um locatário
def excluir_locatario(conn, locatario_id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Locatario WHERE locatario_id = :locatario_id", [locatario_id])
        conn.commit()
        print("Locatário excluído com sucesso!")
    except oracledb.Error as e:
        print(f"Erro ao excluir locatário: {e}")


# Função para inserir um imóvel
def inserir_imovel(conn, locatario_id, tipo, cidade, endereco, valoraluguel):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Imovel (imovel_id, Locatario_locatario_id, imovel_tipo, 
                                imovel_cidade, imovel_endereco, imovel_valoraluguel)
            VALUES (imovel_seq.NEXTVAL, :locatario_id, :tipo, :cidade, :endereco, :valoraluguel)
        """, [locatario_id, tipo, cidade, endereco, valoraluguel])
        conn.commit()
        print("Imóvel inserido com sucesso!")
    except oracledb.Error as e:
        print(f"Erro ao inserir imóvel: {e}")


# Função para ler imóveis
def ler_imoveis(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Imovel")
        for row in cursor.fetchall():
            print(row)
    except oracledb.Error as e:
        print(f"Erro ao ler imóveis: {e}")


# Função para atualizar um imóvel
def atualizar_imovel(conn, imovel_id, novo_tipo, nova_cidade, novo_endereco, novo_valoraluguel):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Imovel SET imovel_tipo = :novo_tipo, imovel_cidade = :nova_cidade,
                              imovel_endereco = :novo_endereco, imovel_valoraluguel = :novo_valoraluguel
            WHERE imovel_id = :imovel_id
        """, [novo_tipo, nova_cidade, novo_endereco, novo_valoraluguel, imovel_id])
        conn.commit()
        print("Imóvel atualizado com sucesso!")
    except oracledb.Error as e:
        print(f"Erro ao atualizar imóvel: {e}")


# Função para excluir um imóvel
def excluir_imovel(conn, imovel_id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Imovel WHERE imovel_id = :imovel_id", [imovel_id])
        conn.commit()
        print("Imóvel excluído com sucesso!")
    except oracledb.Error as e:
        print(f"Erro ao excluir imóvel: {e}")

# RELATÓRIO 1: Imóveis por locatário
def relatorio_imoveis_por_locatario(conn, locatario_id):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT I.imovel_id, I.imovel_tipo, I.imovel_cidade, I.imovel_endereco, I.imovel_valoraluguel
            FROM Imovel I
            WHERE I.Locatario_locatario_id = :locatario_id
        """, [locatario_id])
        imoveis = cursor.fetchall()
        if imoveis:
            print(f"Imóveis do locatário com ID {locatario_id}:")
            for imovel in imoveis:
                print(imovel)
        else:
            print(f"Nenhum imóvel encontrado para o locatário com ID {locatario_id}.")
    except oracledb.Error as e:
        print(f"Erro ao gerar relatório de imóveis por locatário: {e}")

# RELATÓRIO 2: Imóveis em São Paulo com locatários de 30 a 48 anos
def relatorio_imoveis_sp_locatarios_idade(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT I.imovel_id, I.imovel_tipo, I.imovel_cidade, I.imovel_endereco, I.imovel_valoraluguel,
                   L.locatario_id, L.nome
            FROM Imovel I
            JOIN Locatario L ON I.Locatario_locatario_id = L.locatario_id
            WHERE I.imovel_cidade = 'São Paulo'
            AND FLOOR(MONTHS_BETWEEN(SYSDATE, L.data_nascimento) / 12) BETWEEN 30 AND 48
        """)
        imoveis = cursor.fetchall()
        if imoveis:
            print("Imóveis em São Paulo com locatários entre 30 e 48 anos:")
            for imovel in imoveis:
                print(imovel)
        else:
            print("Nenhum imóvel encontrado em São Paulo com locatários nessa faixa etária.")
    except oracledb.Error as e:
        print(f"Erro ao gerar relatório de imóveis em São Paulo com locatários de 30 a 48 anos: {e}")

# RELATÓRIO 3: Imóveis do tipo apartamento com aluguel acima de 2500
def relatorio_apartamentos_aluguel_alto(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT imovel_id, imovel_tipo, imovel_cidade, imovel_endereco, imovel_valoraluguel
            FROM Imovel
            WHERE imovel_tipo = 'Apartamento' AND imovel_valoraluguel > 2500
        """)
        imoveis = cursor.fetchall()
        if imoveis:
            print("Imóveis do tipo apartamento com aluguel superior a 2500:")
            for imovel in imoveis:
                print(imovel)
        else:
            print("Nenhum apartamento encontrado com aluguel superior a 2500.")
    except oracledb.Error as e:
        print(f"Erro ao gerar relatório de apartamentos com aluguel acima de 2500: {e}")


if __name__ == "__main__":
    conn = conectar()
    if conn:
        while True:
            print("\nEscolha uma opção:")
            print("1. Inserir locatário")
            print("2. Ler locatários")
            print("3. Atualizar locatário")
            print("4. Excluir locatário")
            print ("-------------------------")
            print("5. Inserir imóvel")
            print("6. Ler imóveis")
            print("7. Atualizar imóvel")
            print("8. Excluir imóvel")
            print("-------------------------")

            print("9. Relatório: Imóveis por locatário")
            print("10. Relatório: Imóveis em São Paulo com locatários de 30 a 48 anos")
            print("11. Relatório: Apartamentos com aluguel superior a 2500")


            opcao = input("Opção: ")

            if opcao == "1":
                locatario_id = int(input("Digite o ID do locatário: "))
                nome = input("Digite o nome do locatário: ")
                data_nascimento = input("Digite a data de nascimento (YYYY-MM-DD): ")
                cpf = input("Digite o CPF do locatário: ")
                renda = float(input("Digite a renda do locatário: "))
                inserir_locatario(conn, locatario_id, nome, data_nascimento, cpf, renda)


            elif opcao == "2":
                ler_locatarios(conn)

            elif opcao == "3":
                locatario_id = int(input("Digite o ID do locatário: "))
                novo_nome = input("Digite o novo nome do locatário: ")
                atualizar_locatario(conn, locatario_id, novo_nome)

            elif opcao == "4":
                locatario_id = int(input("Digite o ID do locatário para excluir: "))
                excluir_locatario(conn, locatario_id)

            elif opcao == "5":
                locatario_id = int(input("Digite o ID do locatário: "))
                tipo = input("Digite o tipo do imóvel: ")
                cidade = input("Digite a cidade do imóvel: ")
                endereco = input("Digite o endereço do imóvel: ")
                valoraluguel = float(input("Digite o valor do aluguel: "))
                inserir_imovel(conn, locatario_id, tipo, cidade, endereco, valoraluguel)

            elif opcao == "6":
                ler_imoveis(conn)

            elif opcao == "7":
                imovel_id = int(input("Digite o ID do imóvel: "))
                novo_tipo = input("Digite o novo tipo do imóvel: ")
                nova_cidade = input("Digite a nova cidade do imóvel: ")
                novo_endereco = input("Digite o novo endereço do imóvel: ")
                novo_valoraluguel = float(input("Digite o novo valor do aluguel: "))
                atualizar_imovel(conn, imovel_id, novo_tipo, nova_cidade, novo_endereco, novo_valoraluguel)

            elif opcao == "8":
                imovel_id = int(input("Digite o ID do imóvel para excluir: "))
                excluir_imovel(conn, imovel_id)


            elif opcao == "9":
                    locatario_id = int(input("Digite o ID do locatário para o relatório: "))
                    relatorio_imoveis_por_locatario(conn, locatario_id)

            elif opcao == "10":
                    relatorio_imoveis_sp_locatarios_idade(conn)

            elif opcao == "11":
                    relatorio_apartamentos_aluguel_alto(conn)


            else:
                print("Opção inválida. Tente novamente.")

        conn.close()
