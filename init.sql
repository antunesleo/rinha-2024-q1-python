CREATE TABLE clientes (id SERIAL PRIMARY KEY, limite INT NOT NULL, saldo INT NOT NULL, versao INT NOT NULL);

INSERT INTO clientes (id, limite, saldo, versao) VALUES (1, 100000, 0, 1);
INSERT INTO clientes (id, limite, saldo, versao) VALUES (2, 80000, 0, 1);
INSERT INTO clientes (id, limite, saldo, versao) VALUES (3, 1000000, 0, 1);
INSERT INTO clientes (id, limite, saldo, versao) VALUES (4, 10000000, 0, 1);
INSERT INTO clientes (id, limite, saldo, versao) VALUES (5, 500000, 0, 1);

CREATE TABLE transacoes (
    cliente_id INT NOT NULL, 
    tipo CHAR NOT NULL, 
    descricao VARCHAR(10) NOT NULL, 
    valor INT NOT NULL, 
    realizada_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now()) NOT NULL,
    CONSTRAINT fk_clientes FOREIGN KEY(cliente_id) REFERENCES clientes(id)
);

CREATE INDEX idx_client_id ON transacoes(cliente_id);

-- CREATE EXTENSION pg_stat_statements; 
