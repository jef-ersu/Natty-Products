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


#produtos
INSERT INTO produtos (nome, descricao, categoria, preco_custo, preco_venda) VALUES 
("Lavanda", "Auxilia no tratamento da insônia e promove o bem-estar emocional.", "Chás aromáticos", 5.20, 6.50),
("Frutas vermelhas", "Saboroso e refrescante, rico em antioxidantes.", "Chás aromáticos", 6.00, 7.20),
("Mate", "Estimulante natural, aumenta a energia e a concentração.", "Chás puros", 4.30, 5.00),
("Hortaliças desidratadas", "Espinafre, couve, beterraba, etc.", "Chás puros", 3.00, 4.50),
("Ervas puras", "Boldo, carqueja, cavalinha, etc.", "Chás puros", 3.50, 5.00),
("Manjericão", "Ideal para pratos italianos e mediterrâneos.", "Ervas culinárias", 2.50, 3.50),
("Alecrim", "Combina com carnes e assados.", "Ervas culinárias", 2.80, 3.80),
("Orégano", "Típico da culinária italiana e mexicana.", "Ervas culinárias", 2.40, 3.20),
("Alfazema", "Utilizada em aromatizadores de ambiente e produtos de banho.", "Ervas aromáticas", 5.00, 6.50),
("Capim-limão", "Ideal para chás e aromatizadores.", "Ervas aromáticas", 3.00, 4.00),
("Hortelã", "Refrescante e versátil, utilizada em chás, bebidas e culinária.", "Ervas aromáticas", 2.90, 3.90),
("Quinoa", "Rica em proteínas e aminoácidos essenciais.", "Grãos integrais", 10.00, 12.00),
("Aveia", "Fonte de fibras e auxilia na redução do colesterol.", "Grãos integrais", 5.00, 6.50),
("Lentilha", "Fonte de proteínas e fibras, fácil de preparar.", "Leguminosas", 6.50, 7.50),
("Grão de bico", "Versátil, pode ser utilizado em diversas receitas.", "Leguminosas", 7.00, 8.50),
("Chia", "Rica em ômega-3 e fibras, auxilia na saciedade.", "Sementes", 8.00, 9.50),
("Linhaça", "Fonte de fibras e antioxidantes, auxilia na saúde intestinal.", "Sementes", 7.50, 9.00),
("Eucalipto", "Possui propriedades expectorantes e antissépticas, aliviando sintomas de gripes, resfriados e bronquite.", "Ervas para o Sistema Respiratório", 4.00, 5.50),
("Guaco", "Anti-inflamatório e expectorante, utilizado para tratar problemas respiratórios como asma e bronquite.", "Ervas para o Sistema Respiratório", 5.00, 6.50),
("Própolis", "Antibiótico natural, fortalece o sistema imunológico e auxilia no tratamento de infecções de garganta.", "Ervas para o Sistema Respiratório", 8.50, 10.00),
("Boldo", "Estimula a produção de bile e melhora a digestão.", "Ervas para o Sistema Digestivo", 3.50, 4.50),
("Carqueja", "Auxilia no tratamento de problemas digestivos como azia e má digestão.", "Ervas para o Sistema Digestivo", 4.00, 5.00),
("Cúrcuma", "Possui ação anti-inflamatória e antioxidante, auxiliando no tratamento de problemas digestivos e doenças crônicas.", "Ervas para o Sistema Digestivo", 6.00, 7.50),
("Valeriana", "Calmante natural, auxilia no tratamento da insônia e ansiedade.", "Ervas para o Sistema Nervoso", 6.50, 8.00),
("Passiflora", "Sedativo natural, alivia a ansiedade e promove o relaxamento.", "Ervas para o Sistema Nervoso", 5.00, 6.50),
("Kava Kava", "Ansiolítico natural, utilizado para tratar ansiedade e insônia.", "Ervas para o Sistema Nervoso", 8.00, 10.00),
("Unha de Gato", "Estimula o sistema imunológico, possui propriedades anti-inflamatórias e antioxidantes. Auxilia no tratamento de doenças como artrite, infecções e doenças crônicas.", "Ervas para o Sistema Imunológico", 7.00, 8.50),
("Babosa", "Cicatrizante, hidratante e anti-inflamatória, utilizada para tratar queimaduras, picadas de insetos e problemas de pele.", "Outras Ervas com Diversos Benefícios", 6.00, 7.50),
("Ginseng", "Estimulante natural, aumenta a energia e a resistência física e mental.", "Outras Ervas com Diversos Benefícios", 10.00, 12.50),
("Calêndula", "Cicatrizante, anti-inflamatória e antisséptica. Auxilia no tratamento de feridas, eczema e psoríase.", "Outras Ervas com Diversos Benefícios", 5.50, 7.00),
("Óleo de coco", "Hidrata a pele e os cabelos.", "Cosméticos naturais", 15.00, 18.00),
("Argila", "Purifica a pele e remove impurezas.", "Cosméticos naturais", 8.00, 10.00),
("BCAA", "Auxiliam na recuperação muscular após o exercício.", "Aminoácidos", 20.00, 25.00),
("Glutamina", "Fortalece o sistema imunológico e auxilia na recuperação muscular.", "Aminoácidos", 18.00, 22.00),
("Vitamina C", "Fortalece o sistema imunológico.", "Vitaminas e minerais", 12.00, 15.00),
("Vitamina D", "Essencial para a saúde dos ossos.", "Vitaminas e minerais", 15.00, 18.50),
("Cálcio", "Essencial para a formação dos ossos e dentes.", "Vitaminas e minerais", 10.00, 12.50);

