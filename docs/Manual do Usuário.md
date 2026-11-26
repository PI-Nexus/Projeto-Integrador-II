## 📖 Manual do Usuário

### 1. Apresentação

O site de **captação e pré-qualificação de clientes** permite que qualquer pessoa conheça os cartões da **DM**, escolha o que mais combina com ela e **solicite o cartão online**, recebendo o resultado da pré-qualificação na mesma hora: **Aprovado**, **Em análise** ou **Não aprovado** (com oferta de outros produtos).

Os cartões disponíveis são:

* **Cartão DM Visa** — bandeirado, aceito em qualquer estabelecimento que aceite Visa, em todo o Brasil.
* **Cartão Loja** — private label, válido apenas nas unidades da rede parceira escolhida.
* **Cartão Loja Digital** — versão digital do Cartão Loja, sem cartão físico e sem restrição de estado.


---

### 2. Público-alvo e Dores Atendidas 👤💳

#### Usuários atendidos

* **Clientes interessados em crédito:** Pessoas maiores de 18 anos, com CPF regular, que querem solicitar um cartão DM.
* **Clientes de lojas parceiras:** Pessoas que desejam o cartão da sua loja preferida (Cartão Loja).
* **Clientes que preferem o digital:** Pessoas que querem um cartão sem versão física e sem restrição de estado (Cartão Loja Digital).
* **Colaboradores da DM:** Funcionários cujo CPF foi cadastrado como colaborador e que possuem regras próprias de aprovação.
* **Administradores:** Pessoas responsáveis por cadastrar parceiros, colaboradores e vendedores e acompanhar as solicitações no painel administrativo (veja a [seção 5](#5-painel-administrativo)).
* **Vendedores:** Funcionários das lojas parceiras que analisam as solicitações feitas na sua unidade (veja a [seção 6](#6-área-do-vendedor)).

#### Dores que o site atende

* **Dificuldade em escolher o cartão:** A página inicial compara os três cartões lado a lado, com as diferenças de aceitação e de restrição geográfica.
* **Processo demorado:** O pedido é 100% online e leva menos de cinco minutos; a resposta sai na hora.
* **Preenchimento cansativo de endereço:** Ao digitar o CEP, rua, bairro, cidade e estado são preenchidos automaticamente.
* **Escolha de loja confusa:** A lista de unidades das lojas parceiras é filtrada pelo estado do seu CEP.
* **Ficar sem alternativa quando o cartão não é aprovado:** Mesmo quando o pedido não é aprovado, o site apresenta outros produtos (DM Cred e Empréstimo Pessoal).

---

### 3. Acessando o Site

1. Abra o navegador (computador ou celular).
2. Acesse o endereço do site. Ao executar o projeto na sua máquina (veja o [Manual de Instalação](Manual%20de%20Instala%C3%A7%C3%A3o.md)), o endereço é `http://localhost` (Docker) ou `http://localhost:5000` (execução manual).
3. A página inicial será exibida.

> **Requisito:** é necessária conexão com a Internet. O site consulta o CEP no serviço ViaCEP, o salário mínimo vigente no Banco Central e carrega a fonte do Google Fonts.

---

### 4. Fluxo principal de uso

#### 4.1 Página inicial

A página inicial apresenta, de cima para baixo:

* **Cabeçalho:** logo DM, links `Cartões`, `Benefícios`, `Como funciona` e `Dúvidas`, os botões `Peça seu cartão` e `Já sou cliente` (este abre o portal da DM em outra aba) e o ícone de engrenagem, que leva ao painel administrativo.
* **Destaque (hero):** chamada principal e o botão `Peça seu cartão`.
* **Escolha o cartão ideal pra você:** os três cartões, cada um com suas características.
* **Um cartão, vários benefícios:** aprovação em minutos, aumento de limite automático, pagamento por aproximação, código de segurança dinâmico, descontos em lojas e mais prazo para pagar.
* **Peça agora, é fácil!:** os três passos do pedido.
* **Sobre a DM** e **Dúvidas frequentes** (clique em uma pergunta para ver a resposta).
* **Rodapé:** links de produtos e de ajuda.

Qualquer botão `Peça seu cartão` / `Pedir o ...` leva ao formulário de solicitação.

---

#### 4.2 Escolhendo o cartão

| | Cartão DM Visa | Cartão Loja | Cartão Loja Digital |
|---|---|---|---|
| **Onde vale** | Qualquer lugar que aceite Visa | Unidades da rede parceira escolhida | Parceiros do ramo digital; pronto para uso assim que aprovado |
| **Restrição de estado** | Nenhuma | Unidade do mesmo estado do seu CEP | Nenhuma |
| **Cartão físico** | Sim | Sim | **Não é emitido** |

A escolha do cartão é feita na **Etapa 1** do formulário.

---

#### 4.3 Preenchendo o formulário de solicitação

O formulário fica em uma única página, organizado em **quatro etapas** (com um indicador de progresso no topo) mais a confirmação final.

**Etapa 1 · Qual cartão você quer?**
Selecione uma das três opções: `Cartão DM Visa`, `Cartão Loja` ou `Cartão Loja Digital`.

**Etapa 2 · Seus dados**

| Campo | O que informar | Observações |
|---|---|---|
| Nome completo | Como está no documento | Mínimo de 5 caracteres |
| CPF | Somente números | A pontuação entra sozinha; o CPF é validado (dígito verificador) |
| Data de nascimento | `DD/MM/AAAA` | É preciso ter **18 anos ou mais** |
| E-mail | `voce@email.com` | É por ele que o resultado é comunicado |
| Celular | Com DDD | O formato `(12) 99999-9999` entra sozinho |
| Renda mensal | Em reais | Use **vírgula** para os centavos (ex.: `3500,00` ou `3.500,00`). É usada na análise |

**Etapa 3 · Onde você está**

1. Digite o **CEP**. Ao sair do campo, `Rua`, `Bairro`, `Cidade` e `Estado` são preenchidos automaticamente.
2. Informe o **número** e, se quiser, o **complemento**.
3. Se o CEP não for encontrado, você ainda pode preencher os campos e escolher o estado manualmente na lista.

> O estado do seu CEP define quais unidades de lojas parceiras aparecem na Etapa 4.

**Etapa 4 · Sua loja**

* **Loja parceira:** a lista depende do cartão escolhido. No **Cartão Loja**, ela mostra as **unidades** das lojas parceiras do **estado selecionado**, no formato *Nome da loja — Cidade/UF (CEP)*. No **Cartão Loja Digital**, mostra as **lojas digitais**, que não têm restrição de estado nem cartão físico. Parceiros e unidades recém-cadastrados no painel administrativo aparecem aqui imediatamente.
* **Vendedor que te atendeu** *(opcional)*: se alguém da loja te ajudou a fazer o pedido, informe o nome ou o código. Se ninguém te atendeu, deixe em branco.
* Para **Cartão Loja** e **Cartão Loja Digital**, escolher a loja é **obrigatório**.

> 💡 **Dica:** no **Cartão DM Visa**, a Etapa 4 não precisa ser preenchida: a lista de lojas fica desativada e o pedido é avaliado da mesma forma em qualquer estado.

**Confirmação**

Marque a autorização para consulta dos seus dados na análise de crédito e clique em **`Enviar solicitação`**. O botão muda para *Enviando...* enquanto o pedido é processado.

Se algum campo estiver incorreto ou faltando, uma mensagem em vermelho aparece abaixo dele (por exemplo: *"CPF inválido. Confira os números digitados."* ou *"Você precisa ter 18 anos ou mais."*) e o cursor vai para o primeiro campo com problema.

---

#### 4.4 Resultado da solicitação

Ao enviar, você é levado automaticamente a uma das três telas:

**✅ Aprovado!**

```
Aprovado!
Boa notícia: seu cartão foi aprovado. Agora é só concluir a ativação.

Próximos passos
1. Confirme seu e-mail pelo link que acabamos de enviar.
2. Separe um documento com foto para a retirada.
3. Assim que o cartão estiver pronto, avisamos por e-mail e SMS.
```

**🕒 Sua solicitação está em análise**

```
Recebemos seu pedido e ele está passando por uma análise mais detalhada.
Isso é normal e não significa que foi negado.

O que acontece agora
1. Nosso time analisa as informações que você enviou.
2. Você recebe o resultado por e-mail em até 48 horas.
3. Se precisarmos de algum documento, avisamos pelo mesmo e-mail.
```

**❌ Não foi dessa vez**

```
Não conseguimos aprovar seu cartão agora. Isso pode mudar com o tempo —
você pode tentar de novo em 90 dias.

Mas temos outras opções pra você
• DM Cred — microcrédito para resolver o que não pode esperar, com parcelas que cabem no bolso.
• Empréstimo Pessoal — dinheiro na conta pra quitar dívidas, cobrir um imprevisto ou tirar um plano do papel.
```

As telas **Aprovado** e **Em análise** mostram também um resumo do pedido (cartão solicitado e loja) e o botão `Voltar para o início`. Na tela **Não foi dessa vez**, os botões `Conhecer o DM Cred` e `Simular empréstimo` abrem o portal da DM em outra aba; para voltar ao site, clique no logo DM no cabeçalho.

Nas três telas, depois de alguns segundos, aparece uma faixa na parte de baixo com os produtos **DM Cred** e **Empréstimo Pessoal**. Para fechá-la, clique no `X` ou pressione `Esc`; ela não volta a aparecer enquanto você continuar na mesma aba do navegador.

---

#### 4.5 Como o pedido é avaliado (regras de pré-qualificação)

O resultado depende do seu perfil e do cartão escolhido:

| Perfil | Cartão DM Visa | Cartão Loja / Loja Digital |
|---|---|---|
| **Colaborador DM** (CPF cadastrado como colaborador ativo) | Aprovado | Não aprovado |
| **Não colaborador**, renda ≥ 1,5 × salário mínimo | Em análise | Em análise |
| **Não colaborador**, renda < 1,5 × salário mínimo | Não aprovado | Não aprovado |

* O **colaborador da DM** é reconhecido pelo **CPF** informado na Etapa 2: o CPF precisa ter sido cadastrado pelo administrador (veja a [seção 5.4](#54-cadastrando-colaboradores)). Colaboradores utilizam apenas o **Cartão DM Visa**; pedidos de Cartão Loja de colaboradores não são aprovados.
* O **salário mínimo** usado no cálculo é o vigente, consultado no Banco Central. Por exemplo, com o salário mínimo em R$ 1.621,00, a renda mínima é de R$ 2.431,50. Se o serviço do Banco Central estiver indisponível no momento do envio, o pedido segue para **Em análise**.
* Os pedidos de Cartão Loja que ficam **Em análise** são decididos por um vendedor da unidade escolhida (veja a [seção 6](#6-área-do-vendedor)).

**Restrições geográficas**

| Cartão | Regra |
|---|---|
| **DM Visa** | Pode ser solicitado de **qualquer estado**, sem exigir a escolha de uma loja |
| **Cartão Loja** | Só permite escolher unidades do **mesmo estado do CEP** informado |
| **Cartão Loja Digital** | **Sem restrição de estado**. Não é emitido cartão físico |

---

### 5. Painel administrativo

Esta seção é voltada ao **administrador** da DM. O painel permite acompanhar as solicitações e incluir novos parceiros, colaboradores e vendedores sem depender da equipe de desenvolvimento nem de acesso direto ao banco de dados.

---

#### 5.1 Acessando o painel

1. Clique no ícone de engrenagem do cabeçalho da página inicial ou acesse `/admin` (por exemplo, `http://localhost/admin`).
2. Informe a **senha de administrador**, definida na variável `ADMIN_PASSWORD` durante a instalação (veja o [Manual de Instalação](Manual%20de%20Instala%C3%A7%C3%A3o.md)).

Sem a senha, o acesso às telas do painel é bloqueado. Todos os administradores usam a mesma senha. Para encerrar a sessão, clique em `Sair`. Na tela de login há ainda o link **Acesse a área do vendedor**, para quem é vendedor.

Depois de entrar, o painel apresenta quatro abas: **Solicitações de cartão**, **Adição de parceiros**, **Adição de colaboradores** e **Cadastro de vendedores**.

---

#### 5.2 Acompanhando as solicitações

A aba **Solicitações de cartão** mostra:

* **Resumo:** total de solicitações e quantas estão em análise, aprovadas e negadas.
* **Tabela:** as 200 solicitações mais recentes, da mais nova para a mais antiga, com número, cliente, se é colaborador, CPF, renda mensal, cartão, loja, data e status (**Aprovado**, **Em análise** ou **Negado**).
* **Detalhes:** ao clicar em uma linha, abre-se a janela *Detalhes da solicitação*, com os dados do cliente (nome, CPF, renda e vínculo com a DM) e do pedido (cartão, loja, data e status).

---

#### 5.3 Cadastrando um parceiro

Na aba **Adição de parceiros**, preencha:

| Campo | O que informar | Observações |
|---|---|---|
| Nome da Loja | Nome do estabelecimento | Obrigatório |
| CNPJ da Loja | CNPJ do parceiro | Obrigatório. É validado (inclusive o CNPJ alfanumérico) e **não pode repetir** um CNPJ já cadastrado |
| A loja é digital? | Marque para lojas digitais | Lojas digitais não têm sede nem unidades físicas |
| Estado / Cidade | Localização da sede | Obrigatórios para lojas físicas |
| Unidades físicas | CEPs das unidades da loja | Obrigatórios para lojas físicas (veja abaixo) |

**Unidades físicas**

Escolha uma das duas formas de informar as unidades:

* **Adicionar manualmente:** digite o CEP de cada unidade. O botão `+ Adicionar outra unidade` abre um novo campo e o botão `Remover` exclui um campo.
* **Importar CSV:** envie um arquivo `.csv` com uma coluna chamada `cep` e um CEP por linha. O arquivo deve estar em UTF-8 e ter até 2 MB.

Cada cadastro aceita até **200 unidades**. A cidade e o estado de cada unidade são identificados automaticamente a partir do CEP (é necessária conexão com a Internet) e CEPs repetidos são ignorados. Os CEPs das unidades são independentes da sede. O botão `Limpar` apaga o que foi preenchido no formulário.

Depois de salvar, o parceiro já fica disponível na **Etapa 4** do formulário do cliente:

* **Unidades físicas:** cada unidade aparece apenas para clientes do **mesmo estado** da unidade, no Cartão Loja.
* **Parceiro digital:** aparece para **todos os estados**, no Cartão Loja Digital, com o aviso de que não há cartão físico.

Se algum dado estiver incorreto ou o CNPJ já estiver cadastrado, o parceiro não é gravado e o sistema mostra uma mensagem de erro.

---

#### 5.4 Cadastrando colaboradores

Na aba **Adição de colaboradores**, informe:

| Campo | O que informar | Observações |
|---|---|---|
| Matrícula do Colaborador | Matrícula DM | Obrigatório. Até 20 caracteres |
| CPF do Colaborador DM | CPF do colaborador | Obrigatório. 11 dígitos; a pontuação entra sozinha |

A partir do cadastro, quem solicitar um cartão com esse CPF é tratado como **colaborador da DM** (veja a [seção 4.5](#45-como-o-pedido-é-avaliado-regras-de-pré-qualificação)): o Cartão DM Visa é aprovado automaticamente e o Cartão Loja não é aprovado. A aba mostra o total de colaboradores cadastrados. Não é possível cadastrar a mesma matrícula ou o mesmo CPF duas vezes.

---

#### 5.5 Cadastrando vendedores

Na aba **Cadastro de vendedores**, siga os passos:

1. Em **Loja parceira**, digite ao menos duas letras do nome da loja e selecione-a na lista. Só aparecem lojas físicas ativas. O botão `Alterar loja` permite escolher outra.
2. Em **Unidade**, digite ao menos duas letras da cidade ou do CEP da unidade e selecione-a na lista. O botão `Alterar unidade` permite escolher outra.
3. Informe o **nome**, o **CPF** e o **e-mail** do vendedor e clique em `Cadastrar vendedor`. O botão só fica ativo depois que a loja e a unidade são escolhidas.

O vendedor fica vinculado à unidade escolhida e passa a acessar a [área do vendedor](#6-área-do-vendedor) com o e-mail e o CPF cadastrados. Um CPF ou e-mail já cadastrado é rejeitado. O botão `Limpar` apaga o que foi preenchido no formulário.

---

### 6. Área do vendedor

Esta seção é voltada ao **vendedor** de uma loja parceira. Na área do vendedor ele acompanha as solicitações feitas na sua unidade e decide as que estão em análise.

---

#### 6.1 Acessando a área do vendedor

1. Acesse `/vendedor` (por exemplo, `http://localhost/vendedor`) ou use o link **Acesse a área do vendedor**, na tela de login administrativo.
2. Informe o **e-mail** e o **CPF** cadastrados pelo administrador.

Se os dados não conferirem, a tela mostra *"E-mail ou CPF incorretos."*. Para encerrar a sessão, clique em `Sair`.

---

#### 6.2 Acompanhando as solicitações da unidade

Depois de entrar, o painel mostra:

* **Identificação:** o nome do vendedor, a loja e a unidade.
* **Resumo:** total de solicitações e quantas estão em análise, aprovadas e negadas.
* **Tabela:** as solicitações da sua unidade, da mais recente para a mais antiga, com número, cliente, cartão, renda mensal, data e status.
* **Detalhes:** o botão `Ver detalhes` abre a janela *Detalhes da solicitação*, com os dados do cliente, os dados do pedido (cartão, loja, unidade, data e status) e as informações da análise (quem analisou e o motivo da decisão).

O vendedor vê apenas as solicitações da própria unidade.

---

#### 6.3 Decidindo uma solicitação

Nas solicitações **em análise**, a janela de detalhes mostra a área **Realizar análise**:

* `Aprovar solicitação` aprova o pedido.
* `Recusar solicitação` nega o pedido. Antes, é obrigatório preencher o **Motivo da negativa**.

Depois da decisão, o status é atualizado e ficam registrados o vendedor que analisou e o motivo. Uma solicitação que já foi decidida, ou que não pertence à sua unidade, não pode ser alterada: nesse caso a tela mostra *"Não foi possível atualizar. A solicitação pode já ter sido analisada ou não pertencer à sua unidade."*.

---

### 7. Dúvidas e problemas comuns

| Situação | O que fazer |
|---|---|
| *"CPF inválido"* | Confira os números digitados. Digite apenas os 11 dígitos |
| *"Você precisa ter 18 anos ou mais"* | O pedido só pode ser feito por maiores de 18 anos |
| Endereço não foi preenchido | Confira o CEP (8 dígitos) e sua conexão. Você pode preencher manualmente e escolher o estado na lista |
| Lista de lojas mostra *"Informe primeiro seu CEP"* | Digite um CEP válido ou selecione o estado manualmente |
| *"Nenhuma unidade encontrada neste estado"* | Escolha outro estado, o Cartão DM Visa ou o Cartão Loja Digital |
| *"Nenhuma loja digital disponível"* | Ainda não há loja digital cadastrada. Escolha outro cartão |
| *"Este CPF já possui uma solicitação cadastrada."* | Cada CPF só pode ter uma solicitação |
| Alerta *"Erro de comunicação com o servidor"* | Verifique sua conexão e tente novamente. Se persistir, confirme com a equipe que o servidor está em execução |
| Painel: acesso bloqueado | Informe a senha de administrador (`ADMIN_PASSWORD`). Se não souber qual é, consulte quem instalou o sistema |
| Painel: parceiro não foi gravado | Confira se o CNPJ é válido, se o parceiro já não foi cadastrado e se os CEPs das unidades têm 8 dígitos |
| Painel: erro ao importar o CSV | Confira se o arquivo é `.csv`, está em UTF-8, tem até 2 MB e possui a coluna `cep` |
| Painel: vendedor não foi cadastrado | Confira se todos os campos foram preenchidos e se o CPF e o e-mail já não estão cadastrados |
| Área do vendedor: *"E-mail ou CPF incorretos."* | Confira os dados informados. Se estiverem certos, peça ao administrador para verificar o seu cadastro |
| Tela de erro ao enviar | Veja as [Limitações conhecidas](#8-limitações-conhecidas-desta-versão) |

---

### 8. Limitações conhecidas desta versão

Este manual descreve as **Sprints 1, 2 e 3** do projeto. Os pontos abaixo estão em ajuste e podem ser removidos deste manual quando forem corrigidos:

* **Um CPF, uma solicitação:** enviar novamente o mesmo CPF não cria um novo pedido e exibe a mensagem de que o CPF já possui uma solicitação.
* **Complemento do endereço:** o complemento informado na Etapa 3 ainda não é salvo no banco de dados.
* **Campo Vendedor do formulário:** o nome ou código informado na Etapa 4 ainda não é gravado; o pedido fica ligado à unidade escolhida e ao vendedor que o decide.
* **Resumo nas telas de resultado:** o campo *Protocolo* aparece com "—".
* **Solicitações sem unidade:** os pedidos de Cartão DM Visa e de Cartão Loja Digital que ficam em análise não pertencem a nenhuma unidade e, por isso, não aparecem na área do vendedor. No painel administrativo as solicitações só podem ser consultadas.
* **Sem edição ou exclusão:** o painel permite apenas cadastrar parceiros, colaboradores e vendedores.
* **Acesso sem usuários individuais:** o painel administrativo usa uma única senha compartilhada, e o vendedor entra apenas com e-mail e CPF, sem senha.

---

### 9. Observações

* O servidor precisa estar **em execução** para o site responder.
* O tempo de resposta pode levar alguns segundos, pois o site consulta serviços externos (CEP e salário mínimo).
* Os prazos exibidos nas telas de resultado (48 horas, 90 dias) e as mensagens de e-mail/SMS são **ilustrativos**: o envio de cartão, e-mail e SMS está fora do escopo deste projeto.