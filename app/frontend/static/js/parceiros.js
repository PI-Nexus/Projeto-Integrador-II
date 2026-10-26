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

  let vendedores = [];
  const listaVendedores = document.getElementById("listaVendedores");

  /* ================================================== INICIALIZAÇÃO ==== */

  document.addEventListener('DOMContentLoaded', inicializar);

  function inicializar() {
    var formulario = document.getElementById('adicao');
    var Vformulario = document.getElementById('Vformulario');
    if (!formulario || !Vformulario) return;

    // Sem isso, o navegador bloqueia o envio com as bolhas nativas (required,
    // maxlength) antes do evento "submit" e as mensagens abaixo nunca aparecem.
    formulario.noValidate = true;
    Vformulario.noValidate = true;

    var botaoEnviar = formulario.querySelector('.formulario__acoes .btn--primario') ||
      formulario.querySelector('button[type="submit"]');
    var botaoLimpar = document.getElementById('clear_btn');

    formulario.addEventListener('submit', function (evento) {
      evento.preventDefault();
      aoEnviar(formulario, botaoEnviar, evento);
    });

    formulario.addEventListener('input', function (evento) {
      limparErro(evento.target);
    });
    formulario.addEventListener('change', function (evento) {
      limparErro(evento.target);
    });

    Vformulario.addEventListener("submit", (evento) => {
      evento.preventDefault();
      cadastrarVendedor(Vformulario);
      
    });

    listaVendedores.addEventListener("click", (evento) => {
      removerVendedores(evento);
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

  var REGRAS_Vendedor = [
    {
      id: 'vendedor_nome',
      validar: function (formulario) {
        var valor = formulario.vendedor_nome ? formulario.vendedor_nome.value.trim() : '';
        if (!DMUtils.campoPreenchido(valor)) return 'Informe o nome completo do vendedor.';
        if (valor.length < 5) return 'Digite o nome completo, como está no documento.';
        return '';
      }
    },
    {
      id: 'vendedor_codigo',
      validar: function (formulario) {
        var valor = formulario.vendedor_codigo ? formulario.vendedor_codigo.value.trim() : '';
        if (!DMUtils.campoPreenchido(valor)) return 'Informe o código do vendedor.';
      }
    },
    {
      id: 'vendedor_cpf',
      validar: function (formulario) {
        var valor = formulario.vendedor_cpf ? formulario.vendedor_cpf.value : '';
        if (!DMUtils.campoPreenchido(valor)) return 'Informe o CPF do vendedor.';
        if (!DMUtils.validarCPF(valor)) return 'CPF inválido. Confira os números digitados.';
        return '';
      }
    },
    {
      id: 'vendedor_email',
      validar: function (formulario) {
        var valor = formulario.vendedor_email ? formulario.vendedor_email.value.trim() : '';
        if (!DMUtils.campoPreenchido(valor)) return 'Informe o email do vendedor.';
        if (!DMUtils.validarEmail(valor)) return 'Digite um e-mail válido, no formato voce@email.com.';
        return '';
      }
    },
    {
      id: 'vendedor_tel',
      validar: function (formulario) {
        var campo = formulario.vendedor_tel;
        if (!campo || !DMUtils.campoPreenchido(campo.value)) return 'Informe o celular do vendedor.';
        if (!campo.checkValidity()) return 'Digite um celular válido, com DDD.';
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

  async function aoEnviar(formulario, botaoEnviar, evento) {
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

    //Agrupa os valores do form e os vendedores e manda para o back
    const formObject = Object.fromEntries(new FormData(evento.target));

    const response = await fetch("/api/adicao", {
      method: "POST",
      headers: {
        "Content-Type": "application/JSON"
      },
      body: JSON.stringify({
        ...formObject,
        vendedores
      })
    });

    const result = await response.json();
    console.log(result);
  }

  
  function limparFormulario(formulario) {
    formulario.reset();
    REGRAS.forEach(function (regra) {
      limparErro(formulario.elements[regra.id]);
    });
    var primeiro = formulario.elements[REGRAS[0].id];
    if (primeiro) primeiro.focus();
  }

  function criarTexto(tag, classe, texto) {
    const elemento = document.createElement(tag);
    elemento.className = classe;
    elemento.textContent = texto;
    return elemento;
  }
  
  function cadastrarVendedor(Vform) {

    var primeiroCampoInvalido = null;

    REGRAS_Vendedor.forEach(function (regra) {
      var campo = Vform.elements[regra.id];
      var mensagem = regra.validar(Vform);

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

    

    const vendedor = {
    nome: Vform.elements["vendedor_nome"].value,
    codigo: Vform.elements["vendedor_codigo"].value,
    cpf: Vform.elements["vendedor_cpf"].value,
    email: Vform.elements["vendedor_email"].value,
    tel: Vform.elements["vendedor_tel"].value
    };


    vendedores.push(vendedor);

    document.getElementById("modalVendedor").close();

    renderizarVendedores();
    Vform.reset();
  }

  function renderizarVendedores() {
    
    listaVendedores.replaceChildren();

    if (vendedores.length === 0) {
      const vazio = document.createElement("div");
      vazio.className = "estado-vazio";

      vazio.append(
        criarTexto("p", "", "Nenhum vendedor adicionado."),
        criarTexto(
          "span",
          "",
          'Clique em "+" para começar.'
        )
      );

      listaVendedores.append(vazio);
      return;
    }

    vendedores.forEach((vendedor, indice) => {
      const card = document.createElement("article");
      card.className = "card-vendedor";

      const topo = document.createElement("div");
      topo.className = "card-Vtopo";

      const avatar = criarTexto(
        "div",
        "avatar",
        vendedor.nome
          .split(/\s+/)
          .slice(0, 2)
          .map(nome => nome.charAt(0))
          .join("")
          .toUpperCase()
      );

      const nome = criarTexto(
        "h3",
        "card-Vnome",
        vendedor.nome
      );

      topo.append(avatar, nome);

      const cpf = criarTexto(
        "p", "card-Vinfo", `CPF: ${vendedor.cpf}`
      );

      const telefone = criarTexto(
        "p", "card-Vinfo", `Telefone: ${vendedor.tel}`
      );

      const email = criarTexto(
        "p", "card-Vinfo", `E-mail: ${vendedor.email}`
      );

      const acoes = document.createElement("div");
      acoes.className = "card-Vacoes";

      const remover = criarTexto(
        "button", "btn-pequeno btn-remover", "Remover"
      );
      remover.type = "button";
      remover.dataset.acao = "remover";
      remover.dataset.indice = indice;

      acoes.append(remover);
      card.append(topo, cpf, telefone, email, acoes);
      listaVendedores.append(card);
    });
    }

    function removerVendedores(evento) {
      const botao = evento.target.closest("button[data-acao]");

      if (!botao) return;

      const indice = Number(botao.dataset.indice);

      if (botao.dataset.acao === "remover") {
        vendedores.splice(indice, 1);
        renderizarVendedores();
      }

      };

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