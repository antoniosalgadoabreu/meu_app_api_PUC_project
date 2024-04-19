# Minha API

Neste projeto apresento o um site de reserva de voos de asadelta, em que os cliente podem realizar suas reservas aparetir de dados pessoas, no link reserva, o cliente poderá verificar os dias que ja foram reservados e apartir disso realizar a sua propria reserva ou exclusão da reserva. Neste, fiz com a inteção de apresentar os caminhos da API de registro, deleção e consulta do banco de dados. Esta maneira entendo que nao seria a mais adequada para o tipo de serviço que o site se propoem, porém essa foi a melhor maneira que encontrei de ser assertivo nos requisitos exigidos do trabalho. 

---
## Recomendações para o frontend:

Recomendo abrir o frontend pelo template "index.html" para poder passar por todo o site projetado. 
Como poderá ver, o site não automaticamente adaptavel, por nao ser programador e ter experiencia, fiz todo o projeto se utilizando da definição absolute por considerar mais facil para posicionar os objetos no front.



## Recomendações para o backend:

O backend ficou muito similar a aula 3, coloquei as rotas de consulta, remoção e adição de dados como exigido. Não fiz o segundo banco de dados por ter tido muita dificuldade e pouco tempo disponivel para integrar o o banco de dados para comentario com a pagina do front o qual iria realizar o procedimento de adição.

Como executar:

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
