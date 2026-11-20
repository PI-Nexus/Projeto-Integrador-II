
/* ==========================================================================
 * ADIÇÃO DE COLABORADORES — validação do formulário #adicao-colab
 *
 * Ordem dos scripts na página: utils.js → mascaras.js → adicao-colab.js
 *
 * Segue o padrão dos demais formulários:
 * - Lista REGRAS (uma por campo).
 * - Erros inline com role="alert" + aria-invalid.
 * - Foco no primeiro campo inválido.
 * - Envio nativo para /api/adicao-colab, sem fetch.
 * ========================================================================== */

(function () {
  'use strict';

  var COR_ERRO = '#C62828';
  var CLASSE_ERRO = 'campo__ajuda';

  var TAMANHO_MAXIMO_MATRICULA = 20;
  var TAMANHO_CPF = 11;

  /* ================================================== INICIALIZAÇÃO ==== */

  document.addEventListener('DOMContentLoaded', inicializar);

  function inicializar() {
    var formulario = document.getElementById('adicao-colab');
    if (!formulario) return;

    // Desativa as mensagens nativas do navegador.
    formulario.noValidate = true;

    var botaoEnviar =
      formulario.querySelector('.formulario__acoes .btn--primario') ||
      formulario.querySelector('button[type="submit"]');

    formulario.addEventListener('submit', function (evento) {
      evento.preventDefault();
      aoEnviar(formulario, botaoEnviar);
    });

    formulario.addEventListener('input', function (evento) {
      limparErro(evento.target);
    });

    formulario.addEventListener('change', function (evento) {
      limparErro(evento.target);
    });

    // Restaura o botão caso a página volte pelo histórico.
    window.addEventListener('pageshow', function (evento) {
      if (evento.persisted) desativarCarregando(botaoEnviar);
    });
  }

  /* ===================================================== VALIDAÇÃO ==== */

  var REGRAS = [
    {
      id: 'matricula_colab',

      validar: function (formulario) {
        var campo = formulario.elements.matricula_colab;
        var valor = campo ? campo.value : '';

        if (!valor.trim()) {
          return 'Informe a matrícula do colaborador.';
        }

        if (!/^\d+$/.test(valor)) {
          return 'A matrícula deve conter somente números.';
        }

        if (valor.length > TAMANHO_MAXIMO_MATRICULA) {
          return 'A matrícula pode ter no máximo ' +
            TAMANHO_MAXIMO_MATRICULA + ' dígitos.';
        }

        return '';
      }
    },

    {
      id: 'cpf',

      validar: function (formulario) {
        var campo = formulario.elements.cpf;
        var valor = campo ? campo.value : '';

        if (!valor.trim()) {
          return 'Informe o CPF do colaborador.';
        }

        var cpf = limparCPF(valor);

        if (!/^\d+$/.test(cpf)) {
          return 'O CPF deve conter somente números.';
        }

        if (cpf.length !== TAMANHO_CPF) {
          return 'CPF incompleto. Digite os 11 números.';
        }

        if (!validarCPF(cpf)) {
          return 'CPF inválido. Confira os números digitados.';
        }

        return '';
      }
    }
  ];

  /* ==================================================== FUNÇÕES CPF ==== */

  // Remove pontos, hífen e outros caracteres.
  function limparCPF(valor) {
    return valor.replace(/\D/g, '');
  }

  // Valida os dois dígitos verificadores do CPF.
  function validarCPF(valor) {
    var cpf = limparCPF(valor);

    if (cpf.length !== 11) return false;

    // Impede CPFs com todos os números iguais.
    if (/^(\d)\1{10}$/.test(cpf)) return false;

    var soma = 0;
    var resto;

    // Primeiro dígito verificador.
    for (var i = 0; i < 9; i++) {
      soma += Number(cpf.charAt(i)) * (10 - i);
    }

    resto = (soma * 10) % 11;
    if (resto === 10) resto = 0;

    if (resto !== Number(cpf.charAt(9))) return false;

    // Segundo dígito verificador.
    soma = 0;

    for (var j = 0; j < 10; j++) {
      soma += Number(cpf.charAt(j)) * (11 - j);
    }

    resto = (soma * 10) % 11;
    if (resto === 10) resto = 0;

    return resto === Number(cpf.charAt(10));
  }

  /* ================================================= NORMALIZAÇÃO ==== */

  function normalizarDados(formulario) {
    var matricula = formulario.elements.matricula_colab;
    var cpf = formulario.elements.cpf_colab;

    if (matricula) {
      matricula.value = matricula.value.trim();
    }

    if (cpf) {
      // Envia o CPF sem pontuação para o backend.
      cpf.value = limparCPF(cpf.value);
    }
  }

  /* ================================================= ORQUESTRAÇÃO ==== */

  function aoEnviar(formulario, botaoEnviar) {
    if (botaoEnviar && botaoEnviar.disabled) return;

    normalizarDados(formulario);

    var primeiroCampoInvalido = null;

    REGRAS.forEach(function (regra) {
      var campo = formulario.elements[regra.id];
      var mensagem = regra.validar(formulario);

      if (mensagem) {
        mostrarErro(campo, mensagem);

        if (!primeiroCampoInvalido) {
          primeiroCampoInvalido = campo;
        }
      } else {
        limparErro(campo);
      }
    });

    if (primeiroCampoInvalido) {
      primeiroCampoInvalido.focus();
      return;
    }

    ativarCarregando(botaoEnviar);

    // Envio nativo para o action do formulário.
    formulario.submit();
  }

  /* ================================================ ESTADO DE ENVIO ==== */

  function ativarCarregando(botao) {
    if (!botao) return;

    botao.dataset.textoOriginal = botao.textContent;
    botao.textContent = 'Enviando...';
    botao.disabled = true;
    botao.setAttribute('aria-busy', 'true');
  }

  function desativarCarregando(botao) {
    if (!botao) return;

    if (botao.dataset.textoOriginal) {
      botao.textContent = botao.dataset.textoOriginal;
    }

    botao.disabled = false;
    botao.removeAttribute('aria-busy');
  }

  /* ================================================= ERROS INLINE ==== */

  function chaveDoCampo(campo) {
    return campo.name || campo.id;
  }

  function mostrarErro(campo, mensagem) {
    if (!campo) return;

    var elementoErro = obterOuCriarElementoErro(campo);

    elementoErro.textContent = mensagem;
    elementoErro.style.color = COR_ERRO;
    elementoErro.style.fontWeight = '600';

    campo.setAttribute('aria-invalid', 'true');
  }

  function limparErro(campo) {
    if (!campo) return;

    var chave = chaveDoCampo(campo);
    if (!chave) return;

    var elementoErro = document.getElementById('erro-' + chave);

    if (elementoErro) {
      elementoErro.textContent = '';
    }

    campo.removeAttribute('aria-invalid');
  }

  function obterOuCriarElementoErro(campo) {
    var id = 'erro-' + chaveDoCampo(campo);
    var existente = document.getElementById(id);

    if (existente) return existente;

    var elemento = document.createElement('p');

    elemento.id = id;
    elemento.className = CLASSE_ERRO;
    elemento.setAttribute('role', 'alert');

    campo.insertAdjacentElement('afterend', elemento);

    var descritores = (
      campo.getAttribute('aria-describedby') || ''
    ).split(/\s+/).filter(Boolean);

    if (descritores.indexOf(id) === -1) {
      descritores.push(id);
      campo.setAttribute('aria-describedby', descritores.join(' '));
    }

    return elemento;
  }

})();