import csv
import os

# Configurações
OUTPUT_FILE = "data/carga.sql"
BATCH_SIZE = 1000

print("🔮 Gerando o Script Mestre (Schema + Dados)...")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:
    # 1. CONEXÃO
    # Usamos 'remote:localhost' porque o comando vai rodar DENTRO do container
    f_out.write("CONNECT remote:localhost/osCriar root rootpassword;\n")
    
    # 2. Configurações para evitar erros
    f_out.write("set echo false;\n")
    f_out.write("set ignoreErrors true;\n") # Se um registro der erro, continua o resto
    f_out.write("ALTER DATABASE WRITEQUORUM 1;\n") # Fundamental para o cluster
    
    # 3. RECRIAR O SCHEMA (Limpeza e Criação)
    f_out.write("DROP CLASS TRABALHA_EM UNSAFE IF EXISTS;\n")
    f_out.write("DROP CLASS Pessoas UNSAFE IF EXISTS;\n")
    f_out.write("DROP CLASS Empresa UNSAFE IF EXISTS;\n")
    
    f_out.write("CREATE CLASS Pessoas EXTENDS V;\n")
    f_out.write("CREATE PROPERTY Pessoas.id STRING;\n")
    f_out.write("CREATE PROPERTY Pessoas.nome STRING;\n")
    f_out.write("CREATE PROPERTY Pessoas.cidade STRING;\n")
    f_out.write("CREATE INDEX Pessoas.id_idx ON Pessoas (id) UNIQUE;\n")
    
    f_out.write("CREATE CLASS Empresa EXTENDS V;\n")
    f_out.write("CREATE PROPERTY Empresa.id STRING;\n")
    f_out.write("CREATE PROPERTY Empresa.nome STRING;\n")
    f_out.write("CREATE INDEX Empresa.id_idx ON Empresa (id) UNIQUE;\n")
    
    f_out.write("CREATE CLASS TRABALHA_EM EXTENDS E;\n")
    
    # 4. INSERIR DADOS
    
    # --- IMPORTAR PESSOAS ---
    print("Processando Pessoas...")
    f_out.write("BEGIN;\n")
    count = 0
    with open("data/pessoas.csv", "r", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)
        for row in reader:
            nome = row['nome'].replace("'", "\\'")
            cidade = row['cidade'].replace("'", "\\'")
            # Tratamento simples para evitar erro se email nao existir no CSV antigo
            email = row.get('email', '') 
            
            cmd = f"CREATE VERTEX Pessoas SET id = '{row['id']}', nome = '{nome}', cidade = '{cidade}';\n"
            f_out.write(cmd)
            count += 1
            if count % BATCH_SIZE == 0:
                f_out.write("COMMIT;\nBEGIN;\n")
    f_out.write("COMMIT;\n")

    # --- IMPORTAR EMPRESAS ---
    print("Processando Empresas...")
    f_out.write("BEGIN;\n")
    count = 0
    with open("data/empresas.csv", "r", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)
        for row in reader:
            nome = row['nome_empresa'].replace("'", "\\'")
            cmd = f"CREATE VERTEX Empresa SET id = '{row['id']}', nome = '{nome}';\n"
            f_out.write(cmd)
            count += 1
            if count % BATCH_SIZE == 0:
                f_out.write("COMMIT;\nBEGIN;\n")
    f_out.write("COMMIT;\n")

    # --- IMPORTAR RELAÇÕES ---
    print("Processando Relações...")
    f_out.write("BEGIN;\n")
    count = 0
    with open("data/relacoes.csv", "r", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)
        for row in reader:
            cmd = (
                f"CREATE EDGE TRABALHA_EM FROM "
                f"(SELECT FROM Pessoas WHERE id = '{row['id_pessoa']}') TO "
                f"(SELECT FROM Empresa WHERE id = '{row['id_empresa']}');\n"
            )
            f_out.write(cmd)
            count += 1
            if count % BATCH_SIZE == 0:
                f_out.write("COMMIT;\nBEGIN;\n")
    
    f_out.write("COMMIT;\n")
    f_out.write("exit;\n")

print(f"Script Mestre gerado em '{OUTPUT_FILE}'.")