Projeto FakePinterest, foi usado o framework Flask, projeto desenvolvido com segurança em primeiro lugar, foi usado BCRYPT e CSRF,
bcrypt é um algoritmo de hashing usado para armazenar senhas de maneira segura. Em vez de armazenar a senha em texto claro no banco de dados, 
você armazena o hash da senha. Isso garante que, mesmo que o banco de dados seja comprometido, as senhas dos usuários não sejam reveladas diretamente.
CSRF é um tipo de ataque. No contexto de formulários web, o ataque pode acontecer quando um usuário com sessão ativa envia um formulário malicioso para realizar ações no sistema, 
como mudar configurações ou realizar compras.
Para prevenir ataques CSRF, é recomendado o uso de tokens CSRF. Em Flask, você pode usar a extensão Flask-WTF, que integra o gerenciamento de formulários com proteção CSRF.
site: https://fakepinterest-94da.onrender.com
