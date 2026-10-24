/* ==========================================================================
   MÁSCARAS DE DIGITAÇÃO — CPF, data de nascimento e celular
   ========================================================================== */

(function () {
  'use strict';

  var apenasDigitos = function (texto) {
    return texto.replace(/\D/g, '');
  };

  /* CNPJ alfanumérico (Receita Federal, a partir de jul/2026): dígitos e letras A-Z. */
  var apenasAlfanumericos = function (texto) {
    return texto.replace(/[^0-9A-Za-z]/g, '').toUpperCase();
  };

  /* "significativo" é a regex do que conta como caractere digitado (dígito, ou dígito/letra). */
  var posicaoDoDigito = function (texto, quantidade, significativo) {
    if (quantidade === 0) return 0;

    var vistos = 0;
    for (var i = 0; i < texto.length; i++) {
      if (significativo.test(texto[i])) {
        vistos++;
        if (vistos === quantidade) return i + 1;
      }
    }
    return texto.length;
  };

  /*
    alfanumerico = false (padrão): só dígitos contam (CPF, data, celular, CEP).
    alfanumerico = true: dígitos e letras contam, e as letras viram maiúsculas
    (CNPJ alfanumérico).
  */
  var aplicarMascara = function (campo, formatar, maxCaracteres, alfanumerico) {
    if (!campo) return;

    var limpar = alfanumerico ? apenasAlfanumericos : apenasDigitos;
    var significativo = alfanumerico ? /[0-9A-Za-z]/ : /\d/;

    var montar = function (valor) {
      return formatar(limpar(valor).slice(0, maxCaracteres));
    };

    var escrever = function (texto, caracteresAntesDoCursor) {
      campo.value = texto;
      var cursor = posicaoDoDigito(texto, caracteresAntesDoCursor, significativo);
      campo.setSelectionRange(cursor, cursor);
    };

    campo.addEventListener('input', function () {
      var cursor = campo.selectionStart;
      var caracteresAntes = limpar(campo.value.slice(0, cursor)).length;
      escrever(montar(campo.value), caracteresAntes);
    });

    campo.addEventListener('keydown', function (evento) {
      if (evento.key !== 'Backspace') return;

      var inicio = campo.selectionStart;
      if (inicio !== campo.selectionEnd || inicio === 0) return;
      if (significativo.test(campo.value[inicio - 1])) return;

      evento.preventDefault();

      var antes = limpar(campo.value.slice(0, inicio)).slice(0, -1);
      var depois = limpar(campo.value.slice(inicio));
      escrever(montar(antes + depois), antes.length);
    });

    if (campo.value) campo.value = montar(campo.value);
  };

  /* ==================================================== FORMATADORES ==== */

  var formatarCpf = function (d) {
    var texto = d.slice(0, 3);
    if (d.length > 3) texto += '.' + d.slice(3, 6);
    if (d.length > 6) texto += '.' + d.slice(6, 9);
    if (d.length > 9) texto += '-' + d.slice(9, 11);
    return texto;
  };

  var formatarData = function (d) {
    var texto = d.slice(0, 2);
    if (d.length > 2) texto += '/' + d.slice(2, 4);
    if (d.length > 4) texto += '/' + d.slice(4, 8);
    return texto;
  };

  var formatarCelular = function (d) {
    if (d.length === 0) return '';

    var texto = '(' + d.slice(0, 2);
    if (d.length > 2) texto += ') ' + d.slice(2, d.length > 10 ? 7 : 6);
    if (d.length > 6) texto += '-' + (d.length > 10 ? d.slice(7, 11) : d.slice(6, 10));
    return texto;
  };

  var formatarCEP = function (d) {
    var texto = d.slice(0, 5);
    if (d.length > 5) texto += "-" + d.slice(5, 8);
    return texto;
  }

  var formatarCNPJ = function (d) {
    var texto = d.slice(0, 2);
    if (d.length > 2) texto += "." + d.slice(2, 5);
    if (d.length > 5) texto += "." + d.slice(5, 8);
    if (d.length > 8) texto += "/" + d.slice(8, 12);
    if (d.length > 12) texto += "-" + d.slice(12, 14);
    return texto;
  }

  /* ================================ VALIDAÇÃO DA DATA DE NASCIMENTO ==== */

  var IDADE_MINIMA = 18;
  var ANO_MINIMO = 1900;

  var lerData = function (texto) {
    var partes = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(texto);
    if (!partes) return null;

    var dia = Number(partes[1]);
    var mes = Number(partes[2]);
    var ano = Number(partes[3]);

    var data = new Date(ano, mes - 1, dia);
    if (data.getDate() !== dia || data.getMonth() !== mes - 1 || data.getFullYear() !== ano) {
      return null;
    }
    return data;
  };

  var idadeEm = function (nascimento, hoje) {
    var idade = hoje.getFullYear() - nascimento.getFullYear();
    var mes = hoje.getMonth() - nascimento.getMonth();
    if (mes < 0 || (mes === 0 && hoje.getDate() < nascimento.getDate())) idade--;
    return idade;
  };

  var validarNascimento = function (campo) {
    if (!campo) return;

    var conferir = function () {
      if (campo.value === '') {
        campo.setCustomValidity('');
        return;
      }

      var data = lerData(campo.value);
      if (!data) {
        campo.setCustomValidity('Informe uma data válida no formato DD/MM/AAAA.');
        return;
      }

      if (data.getFullYear() < ANO_MINIMO) {
        campo.setCustomValidity('Informe um ano a partir de ' + ANO_MINIMO + '.');
        return;
      }

      if (idadeEm(data, new Date()) < IDADE_MINIMA) {
        campo.setCustomValidity('Você precisa ter ' + IDADE_MINIMA + ' anos ou mais.');
        return;
      }

      campo.setCustomValidity('');
    };

    campo.addEventListener('input', conferir);
    campo.addEventListener('blur', conferir);
  };

  /* ================================================== INICIALIZAÇÃO ==== */

  document.addEventListener('DOMContentLoaded', function () {
    aplicarMascara(document.getElementById('cpf'), formatarCpf, 11);
    aplicarMascara(document.getElementById('nascimento'), formatarData, 8);
    aplicarMascara(document.getElementById('celular'), formatarCelular, 11);
    aplicarMascara(document.getElementById('cep'), formatarCEP, 8);
    // CNPJ alfanumérico: o último argumento (true) libera letras A-Z além dos dígitos
    aplicarMascara(document.getElementById('cnpj_loja'), formatarCNPJ, 14, true);

    validarNascimento(document.getElementById('nascimento'));
  });
})();