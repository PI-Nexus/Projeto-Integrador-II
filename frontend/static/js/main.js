/* ==========================================================================
   MAIN — submit do formulário de solicitação (solicitar.html)
   ========================================================================== */

   (function () {
    'use strict';
  
    var COR_ERRO = '#C62828';
  
    document.addEventListener('DOMContentLoaded', inicializar);
  
    function inicializar() {
      var formulario = document.getElementById('formulario');
      if (!formulario) return;
  
      // Listener para o evento de envio (submit)
      formulario.addEventListener('submit', function (evento) {
        evento.preventDefault();
        aoEnviar(formulario);
      });
  
      // Limpa os erros conforme o usuário digita/altera os campos
      formulario.addEventListener('input', function (evento) {
        limparErro(evento.target);
      });
      formulario.addEventListener('change', function (evento) {
        limparErro(evento.target);
      });
  
      // Integração 1: Preenchimento automático ao sair do campo CEP (blur)
      var campoCep = formulario.querySelector('#cep');
      if (campoCep) {
        campoCep.addEventListener('blur', function () {
          var cep = DMUtils.apenasDigitos(campoCep.value);
          if (cep.length !== 8) return;
  
          fetch('/consultar-cep/' + cep)
            .then(function (resposta) {
              return resposta.json();
            })
            .then(function (dados) {
              if (dados.sucesso) {
                if (formulario.elements['logradouro']) formulario.elements['logradouro'].value = dados.logradouro || '';
                if (formulario.elements['bairro']) formulario.elements['bairro'].value = dados.bairro || '';
                if (formulario.elements['cidade']) formulario.elements['cidade'].value = dados.localidade || '';
                if (formulario.elements['uf']) formulario.elements['uf'].value = dados.uf || '';
                limparErro(campoCep);
              } else {
                mostrarErro(campoCep, dados.erro || 'CEP não encontrado.');
              }
            })
            .catch(function () {
              mostrarErro(campoCep, 'Erro ao consultar o CEP no servidor.');
            });
        });
      }
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
  
      // 1. Validações Locais (utils.js)
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
  
      // 2. Integração 2: Validação no servidor (Flask)
      enviarParaServidor(formulario);
    }
  
    function enviarParaServidor(formulario) {
      var botao = formulario.querySelector('.formulario__acoes .btn--primario') || formulario.querySelector('button[type="submit"]');
      ativarCarregando(botao);
  
      var cepCliente = DMUtils.apenasDigitos(formulario.elements['cep'] ? formulario.elements['cep'].value : '');
      var ufLoja = formulario.elements['uf'] ? formulario.elements['uf'].value : 'SP';
      var ehLojaDigital = formulario.elements['tipo_cartao'] ? formulario.elements['tipo_cartao'].value === 'loja_digital' : false;
  
      fetch('/validar-cartao-loja', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          cep_cliente: cepCliente,
          uf_loja: ufLoja,
          eh_loja_digital: ehLojaDigital
        })
      })
      .then(function (resposta) {
        return resposta.json().then(function (dados) {
          return { ok: resposta.ok, dados: dados };
        });
      })
      .then(function (res) {
        if (res.ok && res.dados.sucesso !== false) {
          exibirCardEmAnalise(formulario);
        } else {
          desativarCarregando(botao);
          var campoCep = formulario.elements['cep'];
          mostrarErro(campoCep, res.dados.erro || 'Solicitação não permitida para a sua região.');
        }
      })
      .catch(function () {
        desativarCarregando(botao);
        alert('Erro de comunicação com o servidor. Verifique a conexão.');
      });
    }
  
    function campoDaRegra(formulario, id) {
      return formulario.elements[id];
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
  
    function chaveDoCampo(elemento) {
      var el = elemento instanceof NodeList || elemento.length ? elemento[0] : elemento;
      return el ? (el.name || el.id) : '';
    }
  
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
  
    function limparErro(campo) {
      if (!campo) return;
      var el = campo instanceof NodeList || campo.length ? campo[0] : campo;
      var chave = chaveDoCampo(el);
      if (!chave) return;
  
      var elementoErro = document.getElementById('erro-' + chave);
      if (elementoErro) elementoErro.textContent = '';
      if (typeof el.removeAttribute === 'function') {
        el.removeAttribute('aria-invalid');
      }
    }
  
    function obterOuCriarElementoErro(campo, ehGrupo) {
      var el = campo instanceof NodeList || campo.length ? campo[0] : campo;
      var chave = chaveDoCampo(el);
      var id = 'erro-' + chave;
  
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