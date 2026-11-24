# Documentação técnica do controle de estoque

Projeto Integrador de Laboratório de Programação

## Problema e proposta

O projeto considera um pequeno comércio simulado que precisa consultar quantidades disponíveis e registrar entradas e saídas. O programa centraliza o saldo de cada produto em uma aplicação de terminal. O cenário é didático e a avaliação utiliza dados simulados.

O objetivo geral é desenvolver um controle local de estoque com cadastro, consulta, movimentação e recuperação dos dados após encerrar a aplicação. Os objetivos específicos são validar os nomes no cadastro, aceitar quantidades inteiras positivas, impedir saídas superiores ao saldo e salvar as alterações aceitas.

## Escopo da versão

A aplicação foi pensada para uma pessoa por vez, em uma única execução ativa. O saldo representa unidades inteiras. A versão oferece as operações abaixo.

| Opção | Operação | Regra |
|---|---|---|
| 1 | Cadastrar produto | Nome preenchido e ainda não cadastrado, saldo inicial zero |
| 2 | Listar produtos | Exibir nome e saldo de cada produto |
| 3 | Registrar entrada | Produto existente e quantidade inteira positiva |
| 4 | Registrar saída | Mesmas validações da entrada e quantidade até o saldo disponível |
| 0 | Encerrar | Finalizar o laço do menu |

Histórico com datas, relatórios financeiros, autenticação e acesso simultâneo ficam como possibilidades de evolução.

## Instalação e reprodução

1. Instale o Python 3.
2. Baixe o repositório pela opção Code e Download ZIP do GitHub e extraia o conteúdo.
3. Abra o terminal na pasta que contém estoque.py.
4. Execute `python estoque.py`. No Windows, pode usar `py estoque.py`.
5. Escolha uma opção no menu e responda às perguntas.

O projeto usa os módulos json e pathlib da biblioteca padrão. O diretório deve permitir gravação. O arquivo estoque.json é criado ao salvar a primeira mudança. Ele guarda os dados de uso local e pode conter informações diferentes em cada computador.

Para repetir a demonstração desde o início, use uma cópia nova do projeto em outra pasta, sem arquivo de dados.

## Organização do programa

| Elemento | Responsabilidade |
|---|---|
| ARQUIVO | Localizar estoque.json na mesma pasta do código |
| carregar_estoque | Ler o JSON e conferir se os saldos são inteiros não negativos |
| salvar_estoque | Gravar um temporário e substituir o arquivo de dados |
| cadastrar | Normalizar e validar o nome antes de criar saldo zero |
| listar | Percorrer os produtos e exibir seus saldos |
| movimentar | Conferir o produto e a quantidade e calcular o novo saldo |
| main | Coordenar o menu, as operações e a confirmação da gravação |

A condição `if __name__ == "__main__"` inicia o menu quando o arquivo é executado diretamente.

## Modelo dos dados

Em memória, o estoque é um dicionário. A chave identifica o produto e o valor guarda a quantidade.

```python
estoque = {"café": 7, "arroz": 4}
```

O cadastro usa `strip().lower()` para remover espaços das extremidades e converter letras para minúsculas. Assim, Café e CAFÉ são tratados como o mesmo nome. Acentos e espaços internos fazem parte do nome. Por exemplo, cafe e café podem identificar produtos distintos.

O mesmo conteúdo é salvo como objeto JSON. Um saldo precisa ser inteiro e maior ou igual a zero. Produtos com saldo zero continuam cadastrados.

## Fundamentos aplicados ao código

### Entrada e conversão

A função input recebe texto do terminal. A opção do menu é comparada com textos como "1" e "4". Na movimentação, int converte a quantidade para inteiro. O bloco try e except ValueError informa o erro quando o texto fornecido não pode ser convertido.

Uma entrada como 1.5 ou abc é recusada nessa conversão. Uma entrada como -2 é convertida, mas é recusada pela regra de quantidade positiva.

### Decisão e regra de saldo

As condições if, elif e else escolhem a operação solicitada. Na saída, a comparação ocorre antes de subtrair.

```python
if quantidade > estoque[nome]:
    print("Saldo insuficiente.")
    return
estoque[nome] -= quantidade
```

Com saldo de 7 e solicitação de 8, o retorno encerra a função antes da subtração. Com solicitação de 7, a retirada é permitida e o saldo passa a zero. Essa condição traduz uma regra do problema para uma decisão do algoritmo.

### Repetição e funções

O while True reapresenta o menu após cada operação. A opção zero executa break e encerra a repetição. A listagem usa for para percorrer os pares de nome e saldo. As funções agrupam etapas do fluxo para permitir leitura e manutenção separadas.

### Persistência e consistência

O módulo json converte o dicionário em texto na gravação e recupera o dicionário na leitura. O caminho relativo ao próprio código permite abrir o programa a partir de outro diretório e manter os dados ao lado de estoque.py.

O menu cria uma cópia do dicionário antes de alterar o saldo. A gravação escreve em um arquivo temporário e depois substitui estoque.json. O dicionário principal só recebe a cópia após salvar com sucesso. Em caso de OSError, o programa informa a falha e continua com o estado anterior em memória.

Esse procedimento foi projetado para execução local única. O uso de um mesmo temporário e de cópias independentes do saldo exige cuidado se houver duas instâncias simultâneas.

## Metodologia de validação

A revisão realizada em 23 de novembro de 2026 confirmou que a versão local testada tinha o mesmo conteúdo do arquivo publicado no GitHub, identificado pelo blob 0935923021960d059ef1854d7f767483070ad250.

Os nove casos principais foram repetidos pelo terminal em uma pasta isolada, inicialmente sem arquivo de estoque. A sequência do café acumulou as alterações na mesma execução. Uma segunda execução confirmou a persistência. Quatro verificações adicionais exercitaram a função de movimentação com entradas controladas.

Os critérios de aprovação foram a mensagem esperada e o saldo preservado ou atualizado conforme a regra. Esses testes avaliam os cenários descritos na tabela.

## Resultados observados

| Caso | Resultado esperado e observado |
|---|---|
| Listar estoque inicial vazio | Informar que nenhum produto está cadastrado |
| Cadastrar café | Criar o produto com saldo zero |
| Cadastrar CAFÉ novamente | Recusar a duplicidade |
| Entrada de 10 unidades | Atualizar saldo para 10 |
| Saída de 3 unidades | Atualizar saldo para 7 |
| Tentar retirar 8 unidades | Recusar por saldo insuficiente e manter 7 |
| Informar abc na quantidade | Solicitar número inteiro |
| Informar zero na quantidade | Exigir quantidade maior que zero |
| Reabrir e listar | Recuperar saldo de 7 do arquivo |
| Informar quantidade negativa | Recusar e preservar o saldo |
| Informar 1.5 na quantidade | Recusar e preservar o saldo |
| Retirar exatamente o saldo de 7 | Permitir e obter saldo zero |
| Movimentar produto inexistente | Informar produto não encontrado |

Os treze casos passaram na revisão. Também foi verificado que JSON com sintaxe inválida é rejeitado pelo carregamento. Os resultados mostram o vínculo entre as condições implementadas e o comportamento do estoque.

## Limitações identificadas na revisão

- A validação de carregamento confere os saldos, mas um nome vazio inserido manualmente no JSON pode ser aceito.
- A mensagem de novo saldo ou de cadastro aparece antes da confirmação de gravação. Se ocorrer erro ao salvar, o aviso de falha aparece em seguida e a mudança é descartada no dicionário principal.
- A avaliação utilizou dados simulados. Uso real, volume elevado, falhas de energia e gravações simultâneas exigem validação adicional.
- A interface depende da digitação consistente do nome e de quantidades em unidades inteiras.

## Conclusão

A versão atende ao fluxo testado de cadastro, consulta, entrada, saída e recuperação de saldo. As decisões condicionais preservam o saldo quando a movimentação é inválida, enquanto o JSON permite recuperar o estado em outra execução. O projeto permite estudar entrada de dados, conversão de tipos, dicionários, repetição, funções e persistência em um problema delimitado.

## Fontes técnicas para consulta

- [Tutorial oficial do Python sobre controle de fluxo](https://docs.python.org/pt-br/3/tutorial/controlflow.html).
- [Tutorial oficial do Python sobre dicionários](https://docs.python.org/pt-br/3/tutorial/datastructures.html#dictionaries).
- [Documentação oficial do módulo json](https://docs.python.org/pt-br/3/library/json.html).

Esta documentação acompanha o código para consulta no repositório. O relatório acadêmico entregue no AVA deve reunir os elementos exigidos pelo professor, com identificação do estudante, resumo, abstract, introdução, objetivos, fundamentação, metodologia, desenvolvimento, resultados e discussão, conclusão e referências.
