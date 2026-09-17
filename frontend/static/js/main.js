/* ==========================================================================
   MAIN — submit do formulário de solicitação (solicitar.html)
   ========================================================================== */


   
(function () {
  'use strict';

  var COR_ERRO = '#C62828';
  var ATRASO_SIMULADO_MS = 1200;

  document.addEventListener('DOMContentLoaded', inicializar);

  function inicializar() {
    var formulario = document.getElementById('formulario');
    if (!formulario) return;

    var campoUf = formulario.elements.uf;
    var campoCep = formulario.elements.cep;
    if (campoCep) {
      campoCep.addEventListener('blur', consultarCep);
      campoCep.addEventListener('change', consultarCep);
    }

    if (campoUf) {
      campoUf.addEventListener('change', carregarLojasParceiras);
      campoUf.addEventListener('input', carregarLojasParceiras);
      if (campoUf.value) carregarLojasParceiras();
    }

    formulario.addEventListener('submit', function (evento) {
      evento.preventDefault();
      aoEnviar(formulario);
    });

    formulario.addEventListener('input', function (evento) {
      limparErro(evento.target);
    });
    formulario.addEventListener('change', function (evento) {
      limparErro(evento.target);
    });
  }

  function consultarCep() {
    var formulario = document.getElementById('formulario');
    var campoCep = formulario && formulario.elements.cep;
    var campoUf = formulario && formulario.elements.uf;
    if (!campoCep || !campoUf) return;

    var cep = campoCep.value.replace(/\D/g, '');
    if (cep.length !== 8) return;

    var apiBase = window.API_BASE_URL || 'http://127.0.0.1:5000';
    fetch(apiBase + '/consultar-cep/' + cep)
      .then(function (resposta) {
        if (!resposta.ok) throw new Error('CEP não encontrado.');
        return resposta.json();
      })
      .then(function (endereco) {
        if (!endereco.uf) throw new Error('UF não encontrada para este CEP.');

        preencherCampo(formulario, 'logradouro', endereco.logradouro);
        preencherCampo(formulario, 'bairro', endereco.bairro);
        preencherCampo(formulario, 'cidade', endereco.cidade);
        campoUf.value = endereco.uf.toUpperCase();
        carregarLojasParceiras();
      })
      .catch(function () {
        campoUf.value = '';
        var lista = formulario && formulario.elements.loja;
        if (lista) {
          lista.replaceChildren();
          var opcao = document.createElement('option');
          opcao.value = '';
          opcao.textContent = 'Informe um CEP válido primeiro';
          lista.appendChild(opcao);
        }
      });
  }

  function preencherCampo(formulario, nome, valor) {
    var campo = formulario.elements[nome];
    if (campo && valor) campo.value = valor;
  }

  function carregarLojasParceiras() {
    var formulario = document.getElementById('formulario');
    var campoUf = formulario && formulario.elements.uf;
    var lista = formulario && formulario.elements.loja;
    if (!campoUf || !lista) return;

    var uf = campoUf.value;
    lista.replaceChildren();
    var opcaoInicial = document.createElement('option');
    opcaoInicial.value = '';
    opcaoInicial.textContent = uf ? 'Carregando lojas...' : 'Selecione primeiro o estado';
    lista.appendChild(opcaoInicial);
    if (!uf) return;

    var apiBase = window.API_BASE_URL || 'http://127.0.0.1:5000';
    fetch(apiBase + '/filtrar-lojas-parceiras/uf/' + encodeURIComponent(uf))
      .then(function (resposta) {
        if (!resposta.ok) throw new Error('Não foi possível carregar as lojas.');
        return resposta.json();
      })
      .then(function (dados) {
        lista.replaceChildren();
        if (!dados.lojas || dados.lojas.length === 0) {
          var opcaoVazia = document.createElement('option');
          opcaoVazia.value = '';
          opcaoVazia.textContent = 'Nenhuma loja encontrada neste estado';
          lista.appendChild(opcaoVazia);
          return;
        }

        var opcaoInicial = document.createElement('option');
        opcaoInicial.value = '';
        opcaoInicial.textContent = 'Selecione uma loja';
        lista.appendChild(opcaoInicial);
        (dados.lojas || []).forEach(function (loja) {
          var opcao = document.createElement('option');
          opcao.value = loja.id;
          opcao.textContent = loja.nome + ' — ' + loja.cidade + '/' + loja.uf;
          lista.appendChild(opcao);
        });
      })
      .catch(function () {
        lista.replaceChildren();
        var opcaoErro = document.createElement('option');
        opcaoErro.value = '';
        opcaoErro.textContent = 'Não foi possível carregar as lojas';
        lista.appendChild(opcaoErro);
      });
  }

  /* ===================================================== VALIDAÇÃO ==== */

  function obrigatorioSimples(idCampo, mensagem) {
    return function (formulario) {
      var campo = formulario.elements[idCampo];
      var valor = campo ? campo.value.trim() : '';
      return DMUtils.campoPreenchido(valor) ? '' : mensagem;
    };
  }

  var REGRAS = [
    {
      id: 'tipo_cartao',
      grupo: true,
      validar: function (formulario) {
        var marcado = formulario.querySelector('input[name="tipo_cartao"]:checked');
        return marcado ? '' : 'Selecione o cartão que você quer pedir.';
      }
    },
    {
      id: 'nome',
      validar: function (formulario) {
        var valor = formulario.nome ? formulario.nome.value.trim() : '';
        if (!DMUtils.campoPreenchido(valor)) return 'Informe seu nome completo.';
        if (valor.length < 5) return 'Digite o nome completo, como está no documento.';
        return '';
      }
    },
    {
      id: 'cpf',
      validar: function (formulario) {
        var valor = formulario.cpf ? formulario.cpf.value : '';
        if (!DMUtils.campoPreenchido(valor)) return 'Informe seu CPF.';
        if (!DMUtils.validarCPF(valor)) return 'CPF inválido. Confira os números digitados.';
        return '';
      }
    },
    {
      id: 'nascimento',
      validar: function (formulario) {
        var campo = formulario.nascimento;
        if (!campo || !DMUtils.campoPreenchido(campo.value)) return 'Informe sua data de nascimento.';
        return campo.validity.customError || !campo.checkValidity()
          ? (campo.validationMessage || 'Data de nascimento inválida.')
          : '';
      }
    },
    {
      id: 'email',
      validar: function (formulario) {
        var valor = formulario.email ? formulario.email.value.trim() : '';
        if (!DMUtils.campoPreenchido(valor)) return 'Informe seu e-mail.';
        if (!DMUtils.validarEmail(valor)) return 'Digite um e-mail válido, no formato voce@email.com.';
        return '';
      }
    },
    {
      id: 'celular',
      validar: function (formulario) {
        var campo = formulario.celular;
        if (!campo || !DMUtils.campoPreenchido(campo.value)) return 'Informe seu celular.';
        if (!campo.checkValidity()) return 'Digite um celular válido, com DDD.';
        return '';
      }
    },
    {
      id: 'renda',
      validar: function (formulario) {
        var valor = formulario.renda ? formulario.renda.value : '';
        if (!DMUtils.campoPreenchido(valor)) return 'Informe sua renda mensal.';
        var numero = parseFloat(valor);
        if (isNaN(numero) || numero <= 0) return 'Informe uma renda maior que zero.';
        return '';
      }
    },
    {
      id: 'matricula',
      validar: function (formulario) {
        var colaborador = formulario.colaborador ? formulario.colaborador.checked : false;
        var valor = formulario.matricula ? formulario.matricula.value.trim() : '';
        if (colaborador && !DMUtils.campoPreenchido(valor)) {
          return 'Informe sua matrícula DM — obrigatória para colaboradores.';
        }
        return '';
      }
    },
    {
      id: 'cep',
      validar: function (formulario) {
        var campo = formulario.cep;
        if (!campo || !DMUtils.campoPreenchido(campo.value)) return 'Informe seu CEP.';
        if (!campo.checkValidity()) return 'Digite um CEP válido, no formato 00000-000.';
        return '';
      }
    },
    { id: 'logradouro', validar: obrigatorioSimples('logradouro', 'Informe a rua ou avenida.') },
    { id: 'numero', validar: obrigatorioSimples('numero', 'Informe o número.') },
    { id: 'bairro', validar: obrigatorioSimples('bairro', 'Informe o bairro.') },
    { id: 'cidade', validar: obrigatorioSimples('cidade', 'Informe a cidade.') },
    {
      id: 'uf',
      validar: function (formulario) {
        return formulario.uf && formulario.uf.value ? '' : 'Selecione o estado.';
      }
    },
    {
      id: 'loja',
      validar: function (formulario) {
        var tipoCartao = (formulario.querySelector('input[name="tipo_cartao"]:checked') || {}).value;
        var precisaDeLoja = tipoCartao === 'loja' || tipoCartao === 'loja_digital';
        if (precisaDeLoja && (!formulario.loja || !DMUtils.campoPreenchido(formulario.loja.value))) {
          return 'Escolha a loja parceira — obrigatório fora do Cartão DM Visa.';
        }
        return '';
      }
    },
    {
      id: 'consentimento',
      grupo: true,
      validar: function (formulario) {
        return formulario.consentimento && formulario.consentimento.checked
          ? ''
          : 'É preciso autorizar a consulta dos seus dados para continuar.';
      }
    }
  ];

  /* ==================================================== ORQUESTRAÇÃO ==== */

  function aoEnviar(formulario) {
    var primeiroCampoInvalido = null;

    REGRAS.forEach(function (regra) {
      var mensagem = regra.validar(formulario);
      var campo = campoDaRegra(formulario, regra.id);

      if (mensagem) {
        mostrarErro(campo, mensagem, regra.grupo);
        if (!primeiroCampoInvalido) primeiroCampoInvalido = campo;
      } else {
        limparErro(campo);
      }
    });

    if (primeiroCampoInvalido) {
      if (primeiroCampoInvalido instanceof NodeList || primeiroCampoInvalido.length) {
        if (primeiroCampoInvalido[0] && typeof primeiroCampoInvalido[0].focus === 'function') {
          primeiroCampoInvalido[0].focus();
        }
      } else if (typeof primeiroCampoInvalido.focus === 'function') {
        primeiroCampoInvalido.focus();
      }
      return;
    }

    simularEnvio(formulario);
  }

  function campoDaRegra(formulario, id) {
    return formulario.elements[id];
  }

  /* ================================================ ESTADO DE ENVIO ==== */

  function simularEnvio(formulario) {
    var botao = formulario.querySelector('.formulario__acoes .btn--primario') || formulario.querySelector('button[type="submit"]');
    ativarCarregando(botao);

    window.setTimeout(function () {
      exibirCardEmAnalise(formulario);
    }, ATRASO_SIMULADO_MS);
  }

  function ativarCarregando(botao) {
    if (!botao) return;
    botao.dataset.textoOriginal = botao.textContent;
    botao.textContent = 'Enviando...';
    botao.disabled = true;
    botao.setAttribute('aria-busy', 'true');
  }

  /* ============================================== CARD "EM ANÁLISE" ==== */

  function exibirCardEmAnalise(formulario) {
    var protocolo = gerarProtocolo();
    var nomeCartao = rotuloDoCartao(formulario);
    var emailDigitado = formulario.email ? formulario.email.value.trim() : '';

    formulario.hidden = true;

    var card = document.createElement('section');
    card.className = 'resultado resultado--em-analise';
    card.id = 'em-analise';
    card.setAttribute('role', 'status');
    card.setAttribute('aria-live', 'polite');
    card.tabIndex = -1;

    card.innerHTML =
      '<h2>Sua solicitação está em análise</h2>' +
      '<p class="resultado__mensagem">' +
      'Recebemos seus dados e eles já estão sob consulta do nosso motor de crédito. ' +
      'Isso é normal e não significa que foi negado.' +
      '</p>' +
      '<h3>O que acontece agora</h3>' +
      '<ol class="resultado__passos">' +
      '<li>Nosso motor de decisão analisa as informações que você enviou.</li>' +
      '<li>Você recebe o resultado por e-mail assim que a análise terminar.</li>' +
      '<li>Se precisarmos de algum documento extra, avisamos pelo mesmo e-mail.</li>' +
      '</ol>' +
      '<dl class="resultado__resumo">' +
      '<dt>Protocolo</dt><dd>' + protocolo + '</dd>' +
      '<dt>Cartão solicitado</dt><dd>' + nomeCartao + '</dd>' +
      '<dt>E-mail de contato</dt><dd>' + escaparHtml(emailDigitado) + '</dd>' +
      '</dl>';

    formulario.insertAdjacentElement('afterend', card);
    card.focus();
  }

  function rotuloDoCartao(formulario) {
    var marcado = formulario.querySelector('input[name="tipo_cartao"]:checked');
    if (!marcado) return '—';
    var label = formulario.querySelector('label[for="' + marcado.id + '"]');
    return label ? label.textContent.trim() : marcado.value;
  }

  function gerarProtocolo() {
    return 'DM-' + Date.now().toString().slice(-8);
  }

  function escaparHtml(texto) {
    var div = document.createElement('div');
    div.textContent = texto;
    return div.innerHTML;
  }

  /* ============================================== ERROS INLINE ==== */

  function mostrarErro(campo, mensagem, ehGrupo) {
    if (!campo) return;
    var elementoErro = obterOuCriarElementoErro(campo, ehGrupo);
    elementoErro.textContent = mensagem;
    elementoErro.style.color = COR_ERRO;
    elementoErro.style.fontWeight = '600';

    if (ehGrupo) return;
    if (typeof campo.setAttribute === 'function') {
      campo.setAttribute('aria-invalid', 'true');
    }
  }
      // adicionar um helper e usar em vez de `el.id` nos dois lugares:

    function chaveDoCampo(elemento) {

    return elemento.name || elemento.id;

    }

    // obterOuCriarElementoErro:

    var id = 'erro-' + chaveDoCampo(el);



    // limparErro:

    var elementoErro = document.getElementById('erro-' + chaveDoCampo(el));



  function limparErro(campo) {
    if (!campo) return;
    var el = campo instanceof NodeList || campo.length ? campo[0] : campo;
    if (!el || !el.id) return;
    var elementoErro = document.getElementById('erro-' + el.id);
    if (elementoErro) elementoErro.textContent = '';
    if (typeof el.removeAttribute === 'function') {
      el.removeAttribute('aria-invalid');
    }
  }

  function obterOuCriarElementoErro(campo, ehGrupo) {
    var el = campo instanceof NodeList || campo.length ? campo[0] : campo;
    var id = 'erro-' + el.id;
    var existente = document.getElementById(id);
    if (existente) return existente;

    var elemento = document.createElement('p');
    elemento.id = id;
    elemento.className = 'campo__ajuda';
    elemento.setAttribute('role', 'alert');

    var ancora = ehGrupo ? ancoraDoGrupo(el) : el;
    ancora.insertAdjacentElement('afterend', elemento);

    var descritores = (el.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean);
    if (descritores.indexOf(id) === -1) {
      descritores.push(id);
      el.setAttribute('aria-describedby', descritores.join(' '));
    }

    return elemento;
  }

  function ancoraDoGrupo(campo) {
    if (campo.name === 'tipo_cartao') {
      return document.querySelector('.opcoes-cartao') || campo;
    }
    return campo.closest('.campo, .campo--checkbox') || campo;
  }
  
})();