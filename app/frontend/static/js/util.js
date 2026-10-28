/* ==========================================================================
   UTILS — validadores e formatadores puros do formulário de solicitação
   ==========================================================================

   Tudo aqui é função pura: recebe um valor, devolve um resultado, não toca
   no DOM. Quem manipula tela é o main.js — este arquivo só sabe validar e
   formatar texto.

   Sobre static/js/mascaras.js: aquele arquivo já cuida da máscara "ao vivo"
   (o que aparece no campo enquanto a pessoa digita) para CPF, celular e data
   de nascimento, incluindo o reposicionamento do cursor. Não duplicamos essa
   parte aqui para não ter dois listeners de "input" brigando pelo mesmo
   campo. Este arquivo expõe as mesmas regras de formatação como funções
   reaproveitáveis (ex.: formatar o CPF no card de confirmação) e adiciona o
   que ainda faltava: dígito verificador de CPF, validação de e-mail, checagem
   de obrigatoriedade, formatação de moeda e validação de CNPJ (numérico e
   alfanumérico).

   Exposto em window.DMUtils para o main.js e o adicao.js consumirem.
   ========================================================================== */


   (function () {
    'use strict';

    /* ============================================================ HELPERS === */

    var apenasDigitos = function (texto) {
      return String(texto == null ? '' : texto).replace(/\D/g, '');
    };

    /* Verdadeiro se o valor tem algo além de espaços em branco. */
    var campoPreenchido = function (valor) {
      return typeof valor === 'string' ? valor.trim().length > 0 : Boolean(valor);
    };

    /* ================================================ VALIDADOR DE CPF ==== */
    /*
      Algoritmo real do dígito verificador (módulo 11), não só a contagem de
      11 dígitos:
        1º dígito: soma d[0..8] * pesos 10..2, resto da divisão por 11 (regra
                   do "resto >= 10 vira 0").
        2º dígito: mesma conta incluindo o 1º dígito recém-calculado, com
                   pesos 11..2.
      Também reprova sequências repetidas (000.000.000-00, 111.111.111-11...),
      que passam na conta do dígito verificador mas nunca são CPFs válidos.
    */
    var calcularDigitoVerificador = function (base) {
      var pesoInicial = base.length + 1;
      var soma = 0;
      for (var i = 0; i < base.length; i++) {
        soma += Number(base[i]) * (pesoInicial - i);
      }
      var resto = (soma * 10) % 11;
      return resto === 10 ? 0 : resto;
    };

    var validarCPF = function (valor) {
      var cpf = apenasDigitos(valor);

      if (cpf.length !== 11) return false;
      if (/^(\d)\1{10}$/.test(cpf)) return false; // todos os dígitos iguais

      var digito1 = calcularDigitoVerificador(cpf.slice(0, 9));
      if (digito1 !== Number(cpf[9])) return false;

      var digito2 = calcularDigitoVerificador(cpf.slice(0, 10));
      if (digito2 !== Number(cpf[10])) return false;

      return true;
    };

    /* =============================================== VALIDADOR DE CNPJ ==== */
    /*
      Aceita o CNPJ numérico (todos os que existiam até jul/2026) e o
      alfanumérico, que a Receita Federal passou a emitir em jul/2026
      (IN RFB 2.229/2024): as 12 primeiras posições aceitam dígitos 0-9 e
      letras A-Z maiúsculas (as 26, sem exclusão); as 2 últimas, os dígitos
      verificadores, são sempre numéricas.

      Cálculo do DV (módulo 11): cada caractere vale o seu código ASCII − 48
      ('0'-'9' → 0-9, 'A' → 17 ... 'Z' → 42); para um CNPJ só com números o
      resultado é idêntico ao cálculo tradicional. Pesos de 2 a 9, da direita
      para a esquerda, reiniciando em 2; resto 0 ou 1 vira DV 0, senão
      DV = 11 − resto. O 2º DV repete a conta incluindo o 1º DV.

      Também reprova sequências repetidas (00000000000000...), que passam na
      conta do dígito verificador mas nunca são CNPJs válidos.

      Atenção: para limpar um CNPJ, nunca use /\D/ (isso apaga as letras).
    */
    var limparCNPJ = function (valor) {
      return String(valor == null ? '' : valor).replace(/[^0-9A-Za-z]/g, '').toUpperCase();
    };

    var calcularDvCNPJ = function (base) {
      var soma = 0;
      var peso = 2;
      for (var i = base.length - 1; i >= 0; i--) {
        soma += (base.charCodeAt(i) - 48) * peso;
        peso = peso === 9 ? 2 : peso + 1;
      }
      var resto = soma % 11;
      return resto < 2 ? 0 : 11 - resto;
    };

    var validarCNPJ = function (valor) {
      var cnpj = limparCNPJ(valor);

      if (!/^[0-9A-Z]{12}[0-9]{2}$/.test(cnpj)) return false;
      if (/^(.)\1{13}$/.test(cnpj)) return false; // todos os caracteres iguais

      if (calcularDvCNPJ(cnpj.slice(0, 12)) !== Number(cnpj[12])) return false;
      if (calcularDvCNPJ(cnpj.slice(0, 13)) !== Number(cnpj[13])) return false;

      return true;
    };

    /* ========================================================== E-MAIL ==== */
    /*
      Regex baseada na recomendação do WHATWG para <input type="email">: mais
      rigorosa que "tem um @ no meio", sem entrar no território de RFC 5322
      completo (que aceita coisas que nenhum provedor de e-mail real usa).
    */
    var EMAIL_REGEX = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/;

    var validarEmail = function (valor) {
      return EMAIL_REGEX.test(String(valor || '').trim());
    };

    /* ==================================================== FORMATADORES ==== */
    /* Mesmas regras de máscara do mascaras.js, como funções puras reutilizáveis. */

    var formatarCPF = function (valor) {
      var d = apenasDigitos(valor).slice(0, 11);
      var texto = d.slice(0, 3);
      if (d.length > 3) texto += '.' + d.slice(3, 6);
      if (d.length > 6) texto += '.' + d.slice(6, 9);
      if (d.length > 9) texto += '-' + d.slice(9, 11);
      return texto;
    };

    var formatarData = function (valor) {
      var d = apenasDigitos(valor).slice(0, 8);
      var texto = d.slice(0, 2);
      if (d.length > 2) texto += '/' + d.slice(2, 4);
      if (d.length > 4) texto += '/' + d.slice(4, 8);
      return texto;
    };

    var formatarTelefone = function (valor) {
      var d = apenasDigitos(valor).slice(0, 11);
      if (d.length === 0) return '';
      var texto = '(' + d.slice(0, 2);
      if (d.length > 2) texto += ') ' + d.slice(2, d.length > 10 ? 7 : 6);
      if (d.length > 6) texto += '-' + (d.length > 10 ? d.slice(7, 11) : d.slice(6, 10));
      return texto;
    };

    /*
      Moeda BRL para exibição (ex.: no card de confirmação). O campo "renda" é
      <input type="number">: o navegador não aceita "R$" nem "," dentro dele,
      então não existe máscara de digitação possível nesse campo sem trocar o
      seu type — e isso está fora do escopo (não alterar a marcação). Por isso
      esta função formata só para exibição, não para o campo em si.
    */
    var formatarMoedaBRL = function (valor) {
      var numero = typeof valor === 'number' ? valor : parseFloat(String(valor || '').replace(',', '.'));
      if (isNaN(numero)) return '';
      return numero.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
    };

    /* ==================================================== EXPORTAÇÃO ==== */

    window.DMUtils = {
      apenasDigitos: apenasDigitos,
      campoPreenchido: campoPreenchido,
      validarCPF: validarCPF,
      limparCNPJ: limparCNPJ,
      validarCNPJ: validarCNPJ,
      validarEmail: validarEmail,
      formatarCPF: formatarCPF,
      formatarData: formatarData,
      formatarTelefone: formatarTelefone,
      formatarMoedaBRL: formatarMoedaBRL
    };
  })();

//mostrei esse código pro claude, e ele adicionou uma função nova para diferenciar nome de id, e mais dois valores para evitar possíveis bugs