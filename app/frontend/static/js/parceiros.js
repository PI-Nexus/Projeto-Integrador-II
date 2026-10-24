/* ==========================================================================
   ADIÇÃO DE PARCEIROS — validação do formulário #adicao
   ==========================================================================

   Ordem dos scripts na página:  utils.js → mascaras.js → adicao.js
   (o main.js não é necessário aqui: ele cuida do formulário de solicitação e
   do modal do admin.)

   Segue o mesmo padrão do main.js: uma lista REGRAS (uma por campo), erro
   inline com role="alert" + aria-invalid e foco no primeiro campo inválido.
   As funções de erro foram copiadas de lá porque, no main.js, ficam presas
   dentro da IIFE. A máscara do CNPJ continua no mascaras.js e o cálculo do
   dígito verificador no utils.js (DMUtils.validarCNPJ).

   Se tudo estiver válido, o formulário é enviado normalmente para o action
   do HTML (/api/adicao), sem fetch.
   ========================================================================== */

(function () {
  'use strict';

  var COR_ERRO = '#C62828';
  var CLASSE_ERRO = 'campo__ajuda';

  var UFS = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA',
    'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
  ];

  var TAMANHO_MINIMO = 2;
  var TAMANHO_MAXIMO_PADRAO = 120; // usado só se o campo não tiver maxlength

  var TEM_LETRA = /[A-Za-zÀ-ÖØ-öø-ÿ]/;

  // Começa com letra; depois só letras, espaço, ponto, hífen e apóstrofo
  // (Mogi-Guaçu, Santa Bárbara d'Oeste, São José dos Campos...).
  var NOME_DE_CIDADE = /^[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ\s.'’-]*$/;

  /* ================================================== INICIALIZAÇÃO ==== */

  document.addEventListener('DOMContentLoaded', inicializar);

  function inicializar() {
    var formulario = document.getElementById('adicao');
    if (!formulario) return;

    // Sem isso, o navegador bloqueia o envio com as bolhas nativas (required,
    // maxlength) antes do evento "submit" e as mensagens abaixo nunca aparecem.
    formulario.noValidate = true;

    var botaoEnviar = formulario.querySelector('.formulario__acoes .btn--primario') ||
      formulario.querySelector('button[type="submit"]');
    var botaoLimpar = document.getElementById('clear_btn');

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

    if (botaoLimpar) {
      botaoLimpar.addEventListener('click', function () {
        limparFormulario(formulario);
      });
    }

    // Voltar pelo histórico pode restaurar a página com o botão "Enviando..."
    window.addEventListener('pageshow', function (evento) {
      if (evento.persisted) desativarCarregando(botaoEnviar);
    });
  }

  /* ===================================================== VALIDAÇÃO ==== */

  function limiteDe(campo) {
    return campo && campo.maxLength > 0 ? campo.maxLength : TAMANHO_MAXIMO_PADRAO;
  }

  var REGRAS = [
    {
      id: 'nome_loja',
      validar: function (formulario) {
        var campo = formulario.elements.nome_loja;
        var valor = campo ? campo.value : '';
        if (!DMUtils.campoPreenchido(valor)) return 'Informe o nome da loja.';
        if (valor.length < TAMANHO_MINIMO) return 'O nome da loja precisa ter pelo menos ' + TAMANHO_MINIMO + ' caracteres.';
        if (valor.length > limiteDe(campo)) return 'O nome da loja pode ter no máximo ' + limiteDe(campo) + ' caracteres.';
        if (!TEM_LETRA.test(valor)) return 'O nome da loja precisa conter letras.';
        return '';
      }
    },
    {
      id: 'cnpj_loja',
      validar: function (formulario) {
        var campo = formulario.elements.cnpj_loja;
        var valor = campo ? campo.value : '';
        if (!DMUtils.campoPreenchido(valor)) return 'Informe o CNPJ da loja.';
        if (DMUtils.limparCNPJ(valor).length < 14) return 'CNPJ incompleto. Digite os 14 caracteres.';
        if (!DMUtils.validarCNPJ(valor)) return 'CNPJ inválido. Confira os caracteres digitados.';
        return '';
      }
    },
    {
      id: 'uf',
      validar: function (formulario) {
        var valor = formulario.elements.uf ? formulario.elements.uf.value : '';
        if (!valor) return 'Selecione o estado.';
        if (UFS.indexOf(valor) === -1) return 'Selecione um estado válido da lista.';
        return '';
      }
    },
    {
      id: 'cidade_loja',
      validar: function (formulario) {
        var campo = formulario.elements.cidade_loja;
        var valor = campo ? campo.value : '';
        if (!DMUtils.campoPreenchido(valor)) return 'Informe a cidade da loja.';
        if (valor.length < TAMANHO_MINIMO) return 'Digite o nome completo da cidade.';
        if (valor.length > limiteDe(campo)) return 'A cidade pode ter no máximo ' + limiteDe(campo) + ' caracteres.';
        if (!NOME_DE_CIDADE.test(valor)) return 'Use apenas letras, espaços, hífen ou apóstrofo no nome da cidade.';
        return '';
      }
    }
  ];

  /* ==================================================== ORQUESTRAÇÃO ==== */

  // Tira espaços das pontas e junta espaços repetidos nos campos de texto livre.
  function normalizarTextos(formulario) {
    ['nome_loja', 'cidade_loja'].forEach(function (nome) {
      var campo = formulario.elements[nome];
      if (campo) campo.value = campo.value.replace(/\s+/g, ' ').trim();
    });
  }

  function aoEnviar(formulario, botaoEnviar) {
    if (botaoEnviar && botaoEnviar.disabled) return; // já está enviando

    normalizarTextos(formulario);

    var primeiroCampoInvalido = null;

    REGRAS.forEach(function (regra) {
      var campo = formulario.elements[regra.id];
      var mensagem = regra.validar(formulario);

      if (mensagem) {
        mostrarErro(campo, mensagem);
        if (!primeiroCampoInvalido) primeiroCampoInvalido = campo;
      } else {
        limparErro(campo);
      }
    });

    if (primeiroCampoInvalido) {
      primeiroCampoInvalido.focus();
      return;
    }

    ativarCarregando(botaoEnviar);
    formulario.submit(); // envio nativo para o action do formulário
  }

  function limparFormulario(formulario) {
    formulario.reset();
    REGRAS.forEach(function (regra) {
      limparErro(formulario.elements[regra.id]);
    });
    var primeiro = formulario.elements[REGRAS[0].id];
    if (primeiro) primeiro.focus();
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

  /* ============================================== ERROS INLINE ==== */

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
    if (elementoErro) elementoErro.textContent = '';
    if (typeof campo.removeAttribute === 'function') {
      campo.removeAttribute('aria-invalid');
    }
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

    var descritores = (campo.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean);
    if (descritores.indexOf(id) === -1) {
      descritores.push(id);
      campo.setAttribute('aria-describedby', descritores.join(' '));
    }

    return elemento;
  }

})();