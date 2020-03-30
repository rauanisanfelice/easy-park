INSERT INTO usuario_valorescompra ( descricao,valor,ativo,ordem )
VALUES
  ('R$ 03,00', 3, true,0),
  ('R$ 05,00', 5, true,1),
  ('R$ 10,00', 10, true,2),
  ('R$ 15,00', 15, true,3),
  ('R$ 20,00', 20, true,4);


INSERT INTO usuario_horasestacionar ( descricao_horas,horas,minutos,descricao_valor,valor,ativo,ordem )
VALUES
  ('00:30',0,30,'R$ 03,00',3,true,0),
  ('01:00',1,0,'R$ 04,00',4,true,1),
  ('01:30',1,30,'R$ 05,00',5,true,2),
  ('02:00',2,0,'R$ 06,00',6,true,3),
  ('03:00',3,0,'R$ 07,00',7,true,4);


INSERT INTO usuario_tiponotificacao ( tipo,descricao_titulo,descricao_full,ativo )
VALUES
  ('MONIT','Seu tempo está se esgotando.','Seu tempo esta esgotando, renove seu horário ou caso for necessário compre mais créditos.',true),
  ('ESGOT','Seu tempo se esgotou!','Seu tempo esgotou, renove seu horário ou caso for necessário compre mais créditos.',true),
  ('ALERT','Retire seu carro','Seu carro foi notificado, retire seu carro em 5 min, caso contrário será multado conforme lei ####.',true);
