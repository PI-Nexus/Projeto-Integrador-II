
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("adicao-vendedor");

  if (!form) return;

  const pesquisaLoja = document.getElementById("pesquisa-loja-vendedor");
  const resultadosLojas = document.getElementById("resultados-lojas-vendedor");
  const idLoja = document.getElementById("id-loja-vendedor");

  const pesquisaUnidade = document.getElementById("pesquisa-unidade-vendedor");
  const resultadosUnidades = document.getElementById("resultados-unidades-vendedor");
  const idUnidade = document.getElementById("id-unidade-vendedor");

  const lojaSelecionada = document.getElementById("loja-selecionada-vendedor");
  const nomeLojaSelecionada = document.getElementById("nome-loja-selecionada");
  const campoUnidade = document.getElementById("campo-unidade-vendedor");

  const unidadeSelecionada = document.getElementById("unidade-selecionada-vendedor");
  const dadosUnidadeSelecionada = document.getElementById("dados-unidade-selecionada");

  const alterarLoja = document.getElementById("alterar-loja-vendedor");
  const alterarUnidade = document.getElementById("alterar-unidade-vendedor");
  const botaoCadastrar = document.getElementById("cadastrar-vendedor");

  let temporizadorLoja;
  let temporizadorUnidade;
  let buscaLojaAtual = 0;
  let buscaUnidadeAtual = 0;

  function atualizarCadastro() {
    botaoCadastrar.disabled = !(idLoja.value && idUnidade.value);
  }

  function criarBotao(texto, aoClicar) {
    const botao = document.createElement("button");

    botao.type = "button";
    botao.className = "btn btn--ghost";
    botao.textContent = texto;
    botao.style.marginTop = "8px";

    botao.addEventListener("click", aoClicar);

    return botao;
  }

  function limparUnidade() {
    idUnidade.value = "";
    pesquisaUnidade.value = "";
    pesquisaUnidade.disabled = false;

    resultadosUnidades.replaceChildren();
    unidadeSelecionada.hidden = true;

    atualizarCadastro();
  }

  // Pesquisa de lojas
  pesquisaLoja.addEventListener("input", () => {
    clearTimeout(temporizadorLoja);

    const termo = pesquisaLoja.value.trim();
    const busca = ++buscaLojaAtual;

    idLoja.value = "";
    lojaSelecionada.hidden = true;
    campoUnidade.hidden = true;

    limparUnidade();
    resultadosLojas.replaceChildren();

    atualizarCadastro();

    if (termo.length < 2) return;

    temporizadorLoja = setTimeout(async () => {
      try {
        const resposta = await fetch(
          `/api/buscar-lojas-vendedor?termo=${encodeURIComponent(termo)}`
        );

        const dados = await resposta.json();

        if (busca !== buscaLojaAtual) return;

        if (!resposta.ok) {
          throw new Error(dados.erro || "Erro ao buscar lojas.");
        }

        if (!dados.lojas.length) {
          resultadosLojas.textContent = "Nenhuma loja encontrada.";
          return;
        }

        dados.lojas.forEach((loja) => {
          const botao = criarBotao(loja.nome_loja, () => {
            idLoja.value = loja.id_loja;
            pesquisaLoja.value = loja.nome_loja;

            nomeLojaSelecionada.textContent = loja.nome_loja;
            lojaSelecionada.hidden = false;

            resultadosLojas.replaceChildren();
            pesquisaLoja.disabled = true;

            campoUnidade.hidden = false;
            pesquisaUnidade.disabled = false;
            pesquisaUnidade.focus();

            limparUnidade();
          });

          resultadosLojas.appendChild(botao);
        });

      } catch (erro) {
        if (busca === buscaLojaAtual) {
          resultadosLojas.textContent = erro.message;
        }
      }
    }, 300);
  });

  // Alterar loja selecionada
  alterarLoja.addEventListener("click", () => {
    buscaLojaAtual++;

    idLoja.value = "";
    pesquisaLoja.value = "";
    pesquisaLoja.disabled = false;

    lojaSelecionada.hidden = true;
    campoUnidade.hidden = true;

    resultadosLojas.replaceChildren();
    limparUnidade();

    pesquisaLoja.focus();
  });

  // Pesquisa de unidades da loja
  pesquisaUnidade.addEventListener("input", () => {
    clearTimeout(temporizadorUnidade);

    const termo = pesquisaUnidade.value.trim();
    const busca = ++buscaUnidadeAtual;

    idUnidade.value = "";
    unidadeSelecionada.hidden = true;
    resultadosUnidades.replaceChildren();

    atualizarCadastro();

    if (termo.length < 2 || !idLoja.value) return;

    temporizadorUnidade = setTimeout(async () => {
      try {
        const resposta = await fetch(
          `/api/buscar-unidades-loja/${idLoja.value}?termo=${encodeURIComponent(termo)}`
        );

        const dados = await resposta.json();

        if (busca !== buscaUnidadeAtual) return;

        if (!resposta.ok) {
          throw new Error(dados.erro || "Erro ao buscar unidades.");
        }

        if (!dados.unidades.length) {
          resultadosUnidades.textContent = "Nenhuma unidade encontrada.";
          return;
        }

        dados.unidades.forEach((unidade) => {
          const texto = `${unidade.cidade} - ${unidade.uf} | CEP: ${unidade.cep} | Unidade: ${unidade.id_unidade}`;

          const botao = criarBotao(texto, () => {
            idUnidade.value = unidade.id_unidade;

            dadosUnidadeSelecionada.textContent = texto;
            unidadeSelecionada.hidden = false;

            pesquisaUnidade.value = "";
            pesquisaUnidade.disabled = true;

            resultadosUnidades.replaceChildren();

            atualizarCadastro();
          });

          resultadosUnidades.appendChild(botao);
        });

      } catch (erro) {
        if (busca === buscaUnidadeAtual) {
          resultadosUnidades.textContent = erro.message;
        }
      }
    }, 300);
  });

  // Alterar unidade selecionada
  alterarUnidade.addEventListener("click", () => {
    buscaUnidadeAtual++;

    limparUnidade();
    pesquisaUnidade.focus();
  });

  // Máscara simples de CPF
  const campoCpf = document.getElementById("cpf-vendedor");

  campoCpf.addEventListener("input", () => {
    let cpf = campoCpf.value.replace(/\D/g, "").slice(0, 11);

    cpf = cpf.replace(/(\d{3})(\d)/, "$1.$2");
    cpf = cpf.replace(/(\d{3})(\d)/, "$1.$2");
    cpf = cpf.replace(/(\d{3})(\d{1,2})$/, "$1-$2");

    campoCpf.value = cpf;
  });

  // Limpar formulário
  form.addEventListener("reset", () => {
    setTimeout(() => {
      buscaLojaAtual++;
      buscaUnidadeAtual++;

      idLoja.value = "";
      idUnidade.value = "";

      pesquisaLoja.disabled = false;
      pesquisaUnidade.disabled = false;

      lojaSelecionada.hidden = true;
      campoUnidade.hidden = true;
      unidadeSelecionada.hidden = true;

      resultadosLojas.replaceChildren();
      resultadosUnidades.replaceChildren();

      atualizarCadastro();
    }, 0);
  });

  // Validação antes do envio
  form.addEventListener("submit", (evento) => {
    if (!idLoja.value || !idUnidade.value) {
      evento.preventDefault();
      alert("Selecione uma loja e uma unidade antes de cadastrar.");
    }
  });
});

document.addEventListener("DOMContentLoaded", () => {

  const modal = document.getElementById("modalDetalhesVendedor");

  if (!modal) return;

  const botoes = document.querySelectorAll(".abrir-detalhes");

  const fechar = document.getElementById("fecharModalVendedor");
  const botaoFechar = document.getElementById("botaoFecharModalVendedor");

  const areaDecisao = document.getElementById("areaDecisaoVendedor");

  const formAprovar = document.getElementById("formAprovarVendedor");
  const formNegar = document.getElementById("formNegarVendedor");

  const motivoNegativa = document.getElementById("motivoNegativaVendedor");

  function preencher(id, valor) {
    document.getElementById(id).textContent = valor || "—";
  }

  function fecharModal() {
    modal.close();
  }

  botoes.forEach(botao => {

    botao.addEventListener("click", () => {

      const dados = botao.dataset;

      preencher(
        "modalIdentificadorVendedor",
        `Solicitação #${dados.id}`
      );

      preencher("modalNome", dados.nome);
      preencher("modalCpf", dados.cpf);
      preencher("modalRenda", dados.renda);
      preencher("modalCartao", dados.cartao);
      preencher("modalLoja", dados.loja);
      preencher("modalUnidade", dados.unidade);
      preencher("modalData", dados.data);
      preencher("modalAnalisador", dados.analisador);
      preencher("modalMotivo", dados.motivo);

      const status = dados.status.toUpperCase();

      const statusElement = document.getElementById("modalStatus");

      const rotulos = {
        ANALISE: "Em análise",
        EM_ANALISE: "Em análise",
        APROVADO: "Aprovado",
        NEGADO: "Negado",
        REPROVADO: "Reprovado"
      };

      statusElement.textContent = rotulos[status] || dados.status;
      statusElement.className =
        `status status--${dados.status.toLowerCase().replaceAll("_", "-")}`;

      const emAnalise = [
        "ANALISE",
        "EM_ANALISE",
        "EM_ANÁLISE"
      ].includes(status);

      // Define a rota da solicitação selecionada
      const rota = `/vendedor/solicitacao/${dados.id}/decidir`;

      formAprovar.action = rota;
      formNegar.action = rota;

      // Só permite analisar solicitações pendentes
      areaDecisao.hidden = !emAnalise;

      // Limpa o motivo ao abrir outra solicitação
      motivoNegativa.value = "";

      modal.showModal();
    });

  });

  fechar.addEventListener("click", fecharModal);
  botaoFechar.addEventListener("click", fecharModal);

  // Fecha ao clicar fora do conteúdo
  modal.addEventListener("click", evento => {
    if (evento.target === modal) {
      fecharModal();
    }
  });

});