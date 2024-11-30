-- Tabela de produtos
CREATE TABLE produtos (
  id_produto INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  descricao TEXT,
  codigo_barras VARCHAR(50),
  fornecedor_id INT,
  preco_custo DECIMAL(10,2),
  preco_venda DECIMAL(10,2),
  data_validade DATE,
  lote VARCHAR(50),
  categoria VARCHAR(50),
  imagem VARCHAR(255),
  informacoes_nutricionais TEXT,
  FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id_fornecedor)
);


-- Tabela de fornecedores
CREATE TABLE fornecedores (
  id_fornecedor INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100),
  contato VARCHAR(100),
  endereco VARCHAR(255)
);


-- Tabela de clientes
CREATE TABLE clientes (
  id_cliente INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100),
  email VARCHAR(100),
  telefone VARCHAR(20),
  endereco VARCHAR(255)
);


-- Tabela de pedidos
CREATE TABLE pedidos (
  id_pedido INT AUTO_INCREMENT PRIMARY KEY,
  cliente_id INT,
  data_pedido DATE,
  status VARCHAR(20),
  FOREIGN KEY (cliente_id) REFERENCES clientes(id_cliente)
);


-- Tabela de itens de pedidos
CREATE TABLE itens_pedidos (
  id_item_pedido INT AUTO_INCREMENT PRIMARY KEY,
  pedido_id INT,
  produto_id INT,
  quantidade INT,
  valor_unitario DECIMAL(10,2),
  FOREIGN KEY (pedido_id) REFERENCES pedidos(id_pedido),
  FOREIGN KEY (produto_id) REFERENCES produtos(id_produto)
);


-- Tabela de pagamentos
CREATE TABLE pagamentos (
  id_pagamento INT AUTO_INCREMENT PRIMARY KEY,
  pedido_id INT,
  forma_pagamento_id INT,
  valor DECIMAL(10,2),
  data_pagamento DATE,
  id_venda int,
  FOREIGN KEY (pedido_id) REFERENCES pedidos(id_pedido),
  FOREIGN KEY (forma_pagamento_id) REFERENCES formas_pagamento(id_forma_pagamento),
  FOREIGN KEY (id_venda) REFERENCES vendas(id_venda)
);


-- Tabela de formas de pagamento
CREATE TABLE formas_pagamento (
  id_forma_pagamento INT AUTO_INCREMENT PRIMARY KEY,
  descricao VARCHAR(50)
);


-- Tabela de notas fiscais
CREATE TABLE notas_fiscais (
  id_nota_fiscal INT AUTO_INCREMENT PRIMARY KEY,
  pedido_id INT,
  data_emissao DATE,
  valor_total DECIMAL(10,2),
  id_venda int,
  FOREIGN KEY (id_venda) REFERENCES vendas(id_venda),
  FOREIGN KEY (pedido_id) REFERENCES pedidos(id_pedido)
);


-- Tabela de funcionários
CREATE TABLE funcionarios (
  id_funcionario INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100),
  cargo VARCHAR(50),
  contato VARCHAR(100)
);


-- Tabela de estoque local
CREATE TABLE estoque_local (
  id_estoque_local INT AUTO_INCREMENT PRIMARY KEY,
  descricao VARCHAR(100),
  endereco VARCHAR(255)
);


-- Tabela de estoque
CREATE TABLE estoque (
  id_estoque INT AUTO_INCREMENT PRIMARY KEY,
  produto_id INT,
  estoque_local_id INT,
  nivel_minimo INT DEFAULT 10,
  quantidade INT,
  FOREIGN KEY (produto_id) REFERENCES produtos(id_produto),
  FOREIGN KEY (estoque_local_id) REFERENCES estoque_local(id_estoque_local)
);

CREATE TABLE vendas (
    id_venda INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT,
    quantidade INT,
    preco_venda DECIMAL(10, 2),
    data_venda DATETIME,
    FOREIGN KEY (produto_id) REFERENCES produtos(id_produto)
);

#Nova tabela!!!
 CREATE TABLE IF NOT EXISTS historico_vendas (
    id_venda INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT,
    quantidade INT,
    data_venda DATETIME,
    preco_venda DECIMAL(10, 2),
    total DECIMAL(10, 2)
);


#Fiquei com preguiça de implementar uma função pra isso, basta inserir manualmente!
INSERT INTO estoque_local(descricao,endereco) VALUES("Teste","Rua Teste");



-- Funções, Procedures, triggers -->

-- add produto 
DELIMITER $$
CREATE PROCEDURE AdicionarProduto(
    IN p_nome VARCHAR(100),
    IN p_descricao TEXT,
    IN p_preco_custo DECIMAL(10, 2),
    IN p_preco_venda DECIMAL(10, 2)
)
BEGIN
    IF p_preco_venda <= p_preco_custo THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Preço de venda deve ser maior que o preço de custo.';
    END IF;

    INSERT INTO produtos (nome, descricao, preco_custo, preco_venda)
    VALUES (p_nome, p_descricao, p_preco_custo, p_preco_venda);
END $$
DELIMITER ;

-- gera relatorio estoque baixo
DELIMITER $$
CREATE PROCEDURE RelatorioEstoqueBaixo()
BEGIN
    SELECT p.nome, e.quantidade, e.nivel_minimo
    FROM estoque e
    JOIN produtos p ON e.produto_id = p.id_produto
    WHERE e.quantidade < e.nivel_minimo;
END $$
DELIMITER ;

-- registrar venda "Trigger"

CREATE TRIGGER RegistrarVenda AFTER INSERT ON historico_vendas
FOR EACH ROW
BEGIN
    INSERT INTO relatorio_diario (produto_id, quantidade, total, data)
    VALUES (NEW.produto_id, NEW.quantidade, NEW.total, NEW.data_venda);
END;

-- estoque total

DELIMITER $$
CREATE FUNCTION EstoqueTotal(produto_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE total INT;

    SELECT SUM(quantidade)
    INTO total
    FROM estoque
    WHERE produto_id = produto_id;

    RETURN COALESCE(total, 0);
END $$
DELIMITER ;
