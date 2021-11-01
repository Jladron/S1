CREATE TABLE Stock(
Cproducto INT PRIMARY KEY NOT NULL,
Cantidad INT
);

CREATE TABLE Pedido(
Cpedido INT PRIMARY KEY NOT NULL,
Ccliente VARCHAR(30),
Fechapedido DATE
);

CREATE TABLE Detallepedido(
Cpedido INT REFERENCES Pedido(Cpedido),
Cproducto INT REFERENCES Stock(CProducto),
Cantidad INT,
PRIMARY KEY(Cpedido,Cproducto)
);

DESCRIBE Stock;
DESCRIBE Pedido;
DESCRIBE Detallepedido;

INSERT INTO Stock VALUES (1,10);
INSERT INTO Stock VALUES (2,15);
INSERT INTO Stock VALUES (3,4);
INSERT INTO Stock VALUES (4,30);
INSERT INTO Stock VALUES (5,20);
INSERT INTO Stock VALUES (6,23);
INSERT INTO Stock VALUES (7,29);
INSERT INTO Stock VALUES (8,15);
INSERT INTO Stock VALUES (9,11);
INSERT INTO Stock VALUES (10,29);

INSERT INTO Pedido VALUES (1001,'Paco',TO_DATE('22/10/2021','dd/mm/yyyy'));
INSERT INTO Pedido VALUES (1002,'Manolo',TO_DATE('21/10/2021','dd/mm/yyyy'));
INSERT INTO Pedido VALUES (1003,'Pepe',TO_DATE('21/10/2021','dd/mm/yyyy'));
INSERT INTO Pedido VALUES (1004,'Pepe',TO_DATE('21/10/2021','dd/mm/yyyy'));
INSERT INTO Pedido VALUES (1005,'Paco',TO_DATE('18/10/2021','dd/mm/yyyy'));
INSERT INTO Pedido VALUES (1006,'Manolo',TO_DATE('18/10/2021','dd/mm/yyyy'));
INSERT INTO Pedido VALUES (1007,'Pepe',TO_DATE('16/10/2021','dd/mm/yyyy'));
INSERT INTO Pedido VALUES (1008,'Paco',TO_DATE('15/10/2021','dd/mm/yyyy'));
INSERT INTO Pedido VALUES (1009,'Pepe',TO_DATE('14/10/2021','dd/mm/yyyy'));
INSERT INTO Pedido VALUES (1010,'Manolo',TO_DATE('14/10/2021','dd/mm/yyyy'));

SELECT * FROM Stock;
select * from pedido where fechapedido=TO_DATE('22/10/2021','dd/mm/yyyy');
