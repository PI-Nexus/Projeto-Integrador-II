/* ==========================================================================
   MÁSCARAS DE DIGITAÇÃO — CPF, data de nascimento e celular
   ========================================================================== */

(function () {
  'use strict';

  var apenasDigitos = function (texto) {
    return texto.replace(/\D/g, '');
  };

  var posicaoDoDigito = function (texto, quantidade) {
    if (quantidade === 0) return 0;

    var vistos = 0;
    for (var i = 0; i < texto.length; i++) {
      if (/\d/.test(texto[i])) {
        vistos++;
        if (vistos === quantidade) return i + 1;
      }
    }
    return texto.length;
  };

  var aplicarMascara = function (campo, formatar, maxDigitos) {
    if (!campo) return;

    var montar = function (valor) {
      return formatar(apenasDigitos(valor).slice(0, maxDigitos));
    };

    var escrever = function (texto, digitosAntesDoCursor) {
      campo.value = texto;
      var cursor = posicaoDoDigito(texto, digitosAntesDoCursor);
      campo.setSelectionRange(cursor, cursor);
    };

    campo.addEventListener('input', function () {
      var cursor = campo.selectionStart;
      var digitosAntes = apenasDigitos(campo.value.slice(0, cursor)).length;
      escrever(montar(campo.value), digitosAntes);
    });

    campo.addEventListener('keydown', function (evento) {
      if (evento.key !== 'Backspace') return;

      var inicio = campo.selectionStart;
      if (inicio !== campo.selectionEnd || inicio === 0) return;
      if (/\d/.test(campo.value[inicio - 1])) return;

      evento.preventDefault();

      var antes = apenasDigitos(campo.value.slice(0, inicio)).slice(0, -1);
      var depois = apenasDigitos(campo.value.slice(inicio));
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

    validarNascimento(document.getElementById('nascimento'));
  });
})();