
document.addEventListener("DOMContentLoaded", () => {
    const formulario = document.getElementById("adicao-parc");

    if (!formulario) return;

    const opcoesModo = formulario.querySelectorAll(
        'input[name="modo_unidades"]'
    );

    const areaManual = document.getElementById("unidades-manual");
    const areaCSV = document.getElementById("unidades-csv");

    const listaCEPs = document.getElementById("lista-ceps");
    const botaoAdicionar = document.getElementById("adicionar-cep");

    const arquivoCSV = document.getElementById("arquivo_unidades");
    const nomeArquivo = document.getElementById("nome-arquivo");

    const campoDigital = document.getElementById("eh_digital");
    const areaUnidades = document.getElementById("campos-unidades");

    if (
        !areaManual ||
        !areaCSV ||
        !listaCEPs ||
        !botaoAdicionar ||
        !arquivoCSV
    ) {
        console.error("Elementos da seção de unidades não encontrados.");
        return;
    }

    let contadorCEPs = 1;

    // Retorna o modo selecionado.
    function obterModo() {
        return formulario.querySelector(
            'input[name="modo_unidades"]:checked'
        )?.value || "manual";
    }

    // Atualiza o estado dos botões de remoção.
    function atualizarBotoesRemover() {
        const campos = listaCEPs.querySelectorAll(".unidade-cep");

        campos.forEach((campo) => {
            const botao = campo.querySelector(".unidade-cep__remover");

            if (botao) {
                botao.disabled = campos.length === 1;
            }
        });
    }

    // Atualiza o campo conforme o modo selecionado.
    function atualizarModo() {
        const modo = obterModo();
        const digital = campoDigital?.checked || false;

        const modoManual = modo === "manual";

        areaManual.hidden = !modoManual || digital;
        areaCSV.hidden = modoManual || digital;

        // Campos escondidos não são enviados no formulário.
        listaCEPs.querySelectorAll('input[name="ceps_unidades"]')
            .forEach((input) => {
                input.disabled = !modoManual || digital;
                input.required = modoManual && !digital;
            });

        arquivoCSV.disabled = modoManual || digital;
        arquivoCSV.required = !modoManual && !digital;

        areaUnidades.hidden = digital;

        atualizarBotoesRemover();
    }

    // Aplica máscara ao CEP.
    function formatarCEP(input) {
        let valor = input.value.replace(/\D/g, "").slice(0, 8);

        if (valor.length > 5) {
            valor = valor.replace(/^(\d{5})(\d{1,3})$/, "$1-$2");
        }

        input.value = valor;
    }

    // Adiciona um novo campo de CEP.
    function adicionarCEP() {
        const identificador = contadorCEPs++;

        const elemento = document.createElement("div");
        elemento.className = "unidade-cep";

        elemento.innerHTML = `
            <div class="campo">
                <label for="cep_unidade_${identificador}">
                    CEP da unidade
                </label>

                <input
                    type="text"
                    id="cep_unidade_${identificador}"
                    name="ceps_unidades"
                    maxlength="9"
                    placeholder="00000-000"
                    inputmode="numeric"
                    required
                >
            </div>

            <button
                type="button"
                class="unidade-cep__remover"
            >
                Remover
            </button>
        `;

        listaCEPs.appendChild(elemento);

        const novoCampo = elemento.querySelector("input");
        novoCampo.focus();

        atualizarModo();
    }

    // Remove um campo de CEP.
    function removerCEP(botao) {
        const campo = botao.closest(".unidade-cep");

        if (!campo) return;

        const quantidade = listaCEPs.querySelectorAll(".unidade-cep").length;

        if (quantidade <= 1) return;

        campo.remove();

        atualizarBotoesRemover();
    }

    // Alternância entre manual e CSV.
    opcoesModo.forEach((opcao) => {
        opcao.addEventListener("change", atualizarModo);
    });

    // Adicionar CEP.
    botaoAdicionar.addEventListener("click", adicionarCEP);

    // Remover CEP usando delegação de eventos.
    listaCEPs.addEventListener("click", (evento) => {
        const botao = evento.target.closest(".unidade-cep__remover");

        if (botao) {
            removerCEP(botao);
        }
    });

    // Máscara nos campos de CEP, inclusive nos criados dinamicamente.
    listaCEPs.addEventListener("input", (evento) => {
        if (evento.target.matches('input[name="ceps_unidades"]')) {
            formatarCEP(evento.target);
        }
    });

    // Exibe o nome do arquivo selecionado.
    arquivoCSV.addEventListener("change", () => {
        const arquivo = arquivoCSV.files[0];

        nomeArquivo.textContent = arquivo
            ? `Arquivo selecionado: ${arquivo.name}`
            : "";

        if (arquivo && !arquivo.name.toLowerCase().endsWith(".csv")) {
            alert("Selecione um arquivo com extensão .csv.");

            arquivoCSV.value = "";
            nomeArquivo.textContent = "";
        }
    });

    // Atualiza a seção quando a loja for marcada como digital.
    if (campoDigital) {
        campoDigital.addEventListener("change", atualizarModo);
    }

    // Estado inicial.
    atualizarModo();
});
