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
* **Colaboradores da DM:** Funcionários que possuem regras próprias de aprovação.

#### Dores que o site atende

* **Dificuldade em escolher o cartão:** A página inicial compara os três cartões lado a lado, com as diferenças de aceitação e de restrição geográfica.
* **Processo demorado:** O pedido é 100% online e leva menos de cinco minutos; a resposta sai na hora.
* **Preenchimento cansativo de endereço:** Ao digitar o CEP, rua, bairro, cidade e estado são preenchidos automaticamente.
* **Escolha de loja confusa:** A lista de lojas parceiras é filtrada pelo estado do seu CEP.
* **Ficar sem alternativa quando o cartão não é aprovado:** Mesmo quando o pedido não é aprovado, o site apresenta outros produtos (DM Cred e Empréstimo Pessoal).

---

### 3. Acessando o Site

1. Abra o navegador (computador ou celular).
2. Acesse o endereço do site. Ao executar o projeto na sua máquina (veja o [Manual de Instalação](Manual%20de%20Instalação.md)), o endereço é `http://localhost:5000`.
3. A página inicial será exibida.

> **Requisito:** é necessária conexão com a Internet. O site consulta o CEP no serviço ViaCEP, o salário mínimo vigente no Banco Central e carrega a fonte do Google Fonts.

---

### 4. Fluxo principal de uso

#### 4.1 Página inicial

A página inicial apresenta, de cima para baixo:

* **Cabeçalho:** logo DM, links `Cartões`, `Benefícios`, `Como funciona` e `Dúvidas`, e os botões `Peça seu cartão` e `Já sou cliente` (este abre o portal da DM em outra aba).
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
| **Restrição de estado** | Nenhuma | Loja do mesmo estado do seu CEP | Nenhuma |
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
| Sou colaborador da DM | Marque só se for o seu caso | Ao marcar, informe a **matrícula DM** |

**Etapa 3 · Onde você está**

1. Digite o **CEP**. Ao sair do campo, `Rua`, `Bairro`, `Cidade` e `Estado` são preenchidos automaticamente.
2. Informe o **número** e, se quiser, o **complemento**.
3. Se o CEP não for encontrado, você ainda pode preencher os campos e escolher o estado manualmente na lista.

> O estado do seu CEP define quais lojas parceiras aparecem na Etapa 4.

**Etapa 4 · Sua loja**

* **Loja parceira:** escolha uma loja na lista. Ela mostra as lojas do **estado selecionado** e também a **loja digital** (que não tem restrição de estado).
* **Vendedor que te atendeu** *(opcional)*: se alguém da loja te ajudou, informe o nome ou o código.
* Para **Cartão Loja** e **Cartão Loja Digital**, escolher a loja é **obrigatório**.

> 💡 **Dica:** mesmo no **Cartão DM Visa**, selecione uma loja da lista para que o envio seja concluído com sucesso (veja [Limitações conhecidas](#6-limitações-conhecidas-desta-versão)).

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
Não conseguimos aprovar seu cartão agora.
Você pode tentar de novo em 90 dias.

Mas temos outras opções pra você
• DM Cred — microcrédito, com parcelas que cabem no bolso.
• Empréstimo Pessoal — dinheiro na conta para quitar dívidas ou cobrir imprevistos.
```

Nas telas **Aprovado** e **Em análise** há o botão `Voltar para o início`. Na tela **Não foi dessa vez**, os botões `Conhecer o DM Cred` e `Simular empréstimo` abrem o portal da DM em outra aba; para voltar ao site, clique no logo DM no cabeçalho.

---

#### 4.5 Como o pedido é avaliado (regras de pré-qualificação)

O resultado depende do seu perfil e do cartão escolhido:

| Perfil | Cartão DM Visa | Cartão Loja / Loja Digital |
|---|---|---|
| **Colaborador DM** com CPF e matrícula cadastrados | Aprovado | Não aprovado |
| **Colaborador DM** não localizado na base | Em análise | Não aprovado |
| **Não colaborador**, renda ≥ 1,5 × salário mínimo | Em análise | Em análise |
| **Não colaborador**, renda < 1,5 × salário mínimo | Não aprovado | Não aprovado |

* O **salário mínimo** usado no cálculo é o vigente, consultado no Banco Central. Por exemplo, com o salário mínimo em R$ 1.621,00, a renda mínima é de R$ 2.431,50.
* Colaboradores da DM utilizam apenas o **Cartão DM Visa**; pedidos de Cartão Loja de colaboradores não são aprovados.

**Restrições geográficas**

| Cartão | Regra |
|---|---|
| **DM Visa** | Pode ser solicitado de **qualquer estado** |
| **Cartão Loja** | Só permite escolher lojas do **mesmo estado do CEP** informado |
| **Cartão Loja Digital** | **Sem restrição de estado**. Não é emitido cartão físico |

---

### 5. Dúvidas e problemas comuns

| Situação | O que fazer |
|---|---|
| *"CPF inválido"* | Confira os números digitados. Digite apenas os 11 dígitos |
| *"Você precisa ter 18 anos ou mais"* | O pedido só pode ser feito por maiores de 18 anos |
| Endereço não foi preenchido | Confira o CEP (8 dígitos) e sua conexão. Você pode preencher manualmente e escolher o estado na lista |
| Lista de lojas mostra *"Informe um CEP válido primeiro"* | Digite um CEP válido ou selecione o estado manualmente |
| *"Nenhuma loja encontrada neste estado"* | Escolha outro estado, o Cartão DM Visa ou o Cartão Loja Digital |
| Alerta *"Erro de comunicação com o servidor"* | Verifique sua conexão e tente novamente. Se persistir, confirme com a equipe que o servidor está em execução |
| Tela de erro ao enviar | Veja as [Limitações conhecidas](#6-limitações-conhecidas-desta-versão) |

---

### 6. Limitações conhecidas desta versão

Este manual descreve a **Sprint 1** do projeto. Os pontos abaixo estão em ajuste e podem ser removidos deste manual quando forem corrigidos:

* **Um CPF, uma solicitação:** enviar novamente o mesmo CPF retorna erro do servidor.
* **Loja no Cartão DM Visa:** apesar de a Etapa 4 indicar que pode ser pulada, o envio sem loja selecionada retorna erro. Selecione uma loja da lista.
* **Aprovação automática de colaborador:** como o CPF do colaborador já precisa existir na base, o envio dessa combinação ainda pode retornar erro do servidor em vez de abrir a tela *Aprovado*.
* **Dados ainda não gravados:** o endereço e o vendedor informados ainda não são salvos no banco de dados (previsto para a Sprint 2).
* **Resumo nas telas de resultado:** os campos *Protocolo*, *Cartão solicitado* e *Loja* aparecem com "—".
* **Lojas de demonstração:** a lista de lojas parceiras vem de um catálogo fixo de 33 lojas usado para desenvolvimento.

---

### 7. Observações

* O servidor precisa estar **em execução** para o site responder.
* O tempo de resposta pode levar alguns segundos, pois o site consulta serviços externos (CEP e salário mínimo).
* Os prazos exibidos nas telas de resultado (48 horas, 90 dias) e as mensagens de e-mail/SMS são **ilustrativos**: o envio de cartão, e-mail e SMS está fora do escopo deste projeto.
