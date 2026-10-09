from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')

button_anchor = '      <button class="learning-topic" type="button" data-learn-topic="q">Q</button>\n      <button class="learning-topic" type="button" data-learn-topic="evidence">● △ ┄</button>'
button_repl = '      <button class="learning-topic" type="button" data-learn-topic="q">Q</button>\n      <button class="learning-topic" type="button" data-learn-topic="empirical">Empirical</button>\n      <button class="learning-topic" type="button" data-learn-topic="evidence">● △ ┄</button>'
assert button_anchor in html
html = html.replace(button_anchor, button_repl, 1)

entry_anchor = "    evidence: {\n      title:'● 実測・△ 借用・┄ モデル',"
entry = """    empirical: {
      title:'Empirical（実測・観測に基づく）',
      one:'「実際に観察・測定したデータにもとづく」という意味です。',
      more:'Formantasiaで Empirical と表示されるときは、研究や公開データで実際に測られた値に根拠があることを示します。',
      tryIt:()=>usingEmpiricalBandwidth()
        ? 'いまは Empirical bandwidth。文献由来の測定データから作った帯域幅の値を使っています。研究モードの ● 実測 表示も見てみよう。'
        : '帯域幅モードを Empirical bandwidth に切り替えられる条件では、Manual Q と聴き比べてみよう。',
      precise:'Empirical は、理論や仮定だけではなく、観察・測定されたデータに根拠があることを表します。Formantasiaでは、生の測定値そのものだけでなく、測定データから計算した群平均や再集計した派生値も含めて empirical と呼ぶ場合があります。empirical だからといって「万人にとって唯一の正解」や「個人差のない値」という意味ではありません。',
      sources:[
        {label:'National Research Council — Scientific Research in Education',url:'https://doi.org/10.17226/10236'}
      ]
    },
    evidence: {
      title:'● 実測・△ 借用・┄ モデル',"""
assert entry_anchor in html
html = html.replace(entry_anchor, entry, 1)

source_anchor = "    'https://www.fon.hum.uva.nl/praat/manual/frequency.html': {\n      short:'Praat Manual',"
source_entry = """    'https://doi.org/10.17226/10236': {
      short:'National Research Council (2002)',
      citation:'National Research Council. (2002). Scientific Research in Education. Washington, DC: The National Academies Press. https://doi.org/10.17226/10236'
    },
    'https://www.fon.hum.uva.nl/praat/manual/frequency.html': {
      short:'Praat Manual',"""
assert source_anchor in html
html = html.replace(source_anchor, source_entry, 1)

marker = '  // Empirical glossary entry v1\n'
script_anchor = '  const GLOSSARY_SOURCE_DETAILS = {'
assert marker not in html
html = html.replace(script_anchor, marker + script_anchor, 1)

path.write_text(html, encoding='utf-8')
print('Added Empirical glossary entry and National Research Council reference.')
