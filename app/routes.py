# ==============================================================================
# 2. ROTA DE PROCESSAMENTO DO FORMULÁRIO (POST)
# ==============================================================================

@routes_bp.route('/api/solicitacoes', methods=['POST'])
def processar_solicitacao():
    renda_raw = request.form.get('renda', '0')
    e_colaborador = request.form.get('colaborador', '').lower()

    # Tratamento para aceitar valores formatados (ex: R$ 3.000,00 ou 3000)
    if isinstance(renda_raw, str):
        renda_limpa = renda_raw.replace('R$', '').replace('.', '').replace(',', '.').strip()
    else:
        renda_limpa = renda_raw

    try:
        renda = float(renda_limpa) if renda_limpa else 0.0
    except (ValueError, TypeError):
        renda = 0.0

    # TODO: Regras de aprovação/análise/negação serão inseridas aqui pelo colega.

    # Redirecionamento temporário até as regras serem definidas
    return redirect(url_for('routes.analise'))
