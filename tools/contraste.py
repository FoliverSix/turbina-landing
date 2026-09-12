#!/usr/bin/env python3
"""Auditoria de contraste WCAG 2.1 AA das páginas da landing.

Abre a página num Chromium via Playwright e lê a cor final de cada elemento já
com a cascata resolvida (herança, especificidade e alfa do fundo compostos),
devolvendo só o que fica abaixo do mínimo.

  python tools/contraste.py html/index.html html/termos.html html/privacidade.html
  python tools/contraste.py https://turbinasolucoes.com.br/        # valida produção

Regras aplicadas: 4,5:1 para texto normal; 3:1 para texto grande (24px+, ou
18,66px+ em negrito).

Por que Playwright e não o Chrome de linha de comando: no Windows,
`chrome.exe --headless --dump-dom` (e `--screenshot`) devolve 0 bytes com uma
sessão do Chrome aberta — o lançamento é entregue à instância já existente e o
processo sai rc=0 sem produzir nada. `msedge.exe` e o Chromium do Playwright
sofrem do mesmo mal, porque executáveis GUI não anexam stdout ao pipe do pai.
Playwright fala CDP por pipe e devolve o valor de evaluate() serializado.
"""
import sys
from playwright.sync_api import sync_playwright

JS_AUDITORIA = r"""
() => {
  function num(s){ var m = s && s.match(/[\d.]+/g); return m ? m.slice(0,3).map(Number) : null; }
  function alpha(s){ var m = s && s.match(/[\d.]+/g); return m && m.length > 3 ? parseFloat(m[3]) : 1; }
  function lum(c){ function g(v){ v/=255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); }
    return 0.2126*g(c[0]) + 0.7152*g(c[1]) + 0.0722*g(c[2]); }
  function ratio(a,b){ var la=lum(a), lb=lum(b), hi=Math.max(la,lb), lo=Math.min(la,lb); return (hi+0.05)/(lo+0.05); }

  // primeiro ancestral com fundo opaco; um gradiente no caminho invalida a medida
  function bgOf(el){
    var n = el;
    while (n && n.nodeType === 1) {
      var cs = getComputedStyle(n);
      var c = num(cs.backgroundColor);
      if (c && alpha(cs.backgroundColor) > 0.5) return c;
      if (cs.backgroundImage && cs.backgroundImage.indexOf('gradient') >= 0) return null;
      n = n.parentElement;
    }
    return [13,17,23];
  }

  var fails = [], all = document.body.querySelectorAll('*');
  for (var i = 0; i < all.length; i++) {
    var el = all[i];
    var txt = (el.textContent || '').trim();
    if (!txt || txt.length < 2) continue;
    var temFilhoComTexto = false;                       // só folhas: evita contar o mesmo texto N vezes
    for (var j = 0; j < el.children.length; j++) {
      if ((el.children[j].textContent || '').trim()) { temFilhoComTexto = true; break; }
    }
    if (temFilhoComTexto) continue;
    var cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) continue;
    if (cs.webkitTextFillColor === 'rgba(0, 0, 0, 0)') continue;
    var col = num(cs.color); if (!col) continue;
    var bg = bgOf(el); if (!bg) continue;
    var r = ratio(col, bg);
    var fs = parseFloat(cs.fontSize), fw = parseInt(cs.fontWeight, 10) || 400;
    var grande = fs >= 24 || (fs >= 18.66 && fw >= 700);
    var min = grande ? 3.0 : 4.5;
    if (r < min) fails.push({
      el: el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).trim().split(/\s+/).join('.') : ''),
      texto: txt.slice(0, 48), razao: Math.round(r*100)/100, min: min,
      cor: cs.color, fundo: 'rgb(' + bg.join(',') + ')', fs: cs.fontSize, fw: cs.fontWeight });
  }
  return fails;
}
"""


def auditar(alvo, espera_ms=800):
    url = alvo if "://" in alvo else "file:///" + alvo.replace("\\", "/").replace(" ", "%20")
    with sync_playwright() as pw:
        navegador = pw.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        try:
            pg = navegador.new_page(viewport={"width": 1280, "height": 900}, color_scheme="dark")
            pg.goto(url, wait_until="load")
            pg.wait_for_timeout(espera_ms)
            return pg.evaluate(JS_AUDITORIA)
        finally:
            navegador.close()


def main(alvos):
    total = 0
    for alvo in alvos:
        falhas = auditar(alvo)
        total += len(falhas)
        estado = "OK" if not falhas else f"{len(falhas)} ABAIXO DE AA"
        print(f"\n=== {alvo} -> {estado} ===")
        for f in falhas:
            print(f"  {f['el']}  \"{f['texto']}\"")
            print(f"      {f['cor']} sobre {f['fundo']} = {f['razao']}:1 (min {f['min']}) {f['fs']}/{f['fw']}")
    print(f"\nTOTAL: {total} elemento(s) abaixo do mínimo")
    return 1 if total else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1:]))
