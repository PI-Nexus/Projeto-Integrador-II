/* ==========================================================================
   POP-UP DE PRODUTOS — telas de resultado (aprovado, analise, negado)
   Faixa discreta na base; aparece após um instante; fechar salva em sessionStorage.
   ========================================================================== */
(function () {
  'use strict';

  var CHAVE = 'dm-popup-produtos-fechado';
  var ATRASO_MS = 1500;

  function foiFechado() {
    try { return sessionStorage.getItem(CHAVE) === '1'; } catch (e) { return false; }
  }

  function iniciar() {
    var popup = document.getElementById('popup-produtos');
    if (!popup || foiFechado()) return;

    function abrir() {
      popup.hidden = false;
      // A faixa é fixa na base: reserva o espaço dela para o rodapé não ficar coberto.
      document.body.style.paddingBottom = popup.offsetHeight + 'px';
      window.requestAnimationFrame(function () {
        popup.classList.add('popup-produtos--visivel');
      });
    }

    function fechar() {
      popup.classList.remove('popup-produtos--visivel');
      popup.hidden = true;
      document.body.style.paddingBottom = '';
      document.removeEventListener('keydown', aoTeclar);
      try { sessionStorage.setItem(CHAVE, '1'); } catch (e) { /* storage bloqueado: fecha só agora */ }
    }

    function aoTeclar(evento) {
      if (evento.key === 'Escape') fechar();
    }

    popup.querySelector('[data-popup-fechar]').addEventListener('click', fechar);
    document.addEventListener('keydown', aoTeclar);

    window.setTimeout(abrir, ATRASO_MS);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', iniciar);
  } else {
    iniciar();
  }
})();