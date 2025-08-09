<?php
declare(strict_types=1);

$translations = [
    'pl' => [
        'title'         => 'Konwerter Czasu',
        'meta'          => 'Szybko zamieniaj sekundy, minuty, godziny, dni, miesiące i lata – np. sprawdź, ile sekund ma rok lub ile dni ma miesiąc.',
        'enter_value'   => 'Wpisz wartość',
        'value_help'    => 'Nieujemna liczba',
        'select_unit'   => 'Wybierz jednostkę',
        'convert'       => 'Konwertuj',
        'toggle_lang'   => 'EN',
        'result_intro'  => 'to:',
        'error_invalid' => 'Wprowadź poprawną nieujemną wartość',
        'unit_second'   => 'Sekund',
        'unit_minute'   => 'Minut',
        'unit_hour'     => 'Godzin',
        'unit_day'      => 'Dni',
        'unit_month'    => 'Miesięcy',
        'unit_year'     => 'Lat',
    ],
    'en' => [
        'title'         => 'Time Converter',
        'meta'          => 'Quickly convert seconds, minutes, hours, days, months, and years – for example, find out how many seconds are in a year or how many days are in a month.',
        'enter_value'   => 'Enter value',
        'value_help'    => 'Non-negative number',
        'select_unit'   => 'Select unit',
        'convert'       => 'Convert',
        'toggle_lang'   => 'PL',
        'result_intro'  => 'is:',
        'error_invalid' => 'Please enter a valid non-negative number',
        'unit_second'   => 'Seconds',
        'unit_minute'   => 'Minutes',
        'unit_hour'     => 'Hours',
        'unit_day'      => 'Days',
        'unit_month'    => 'Months',
        'unit_year'     => 'Years',
    ],
];

$lang = $_GET['lang'] ?? 'en';
if (!isset($translations[$lang])) {
    $lang = 'pl';
}
$T = $translations[$lang];
?>
<!DOCTYPE html>
<html lang="<?= $lang ?>">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title><?= htmlspecialchars($T['title']) ?></title>
  <meta name="description" content="<?= htmlspecialchars($T['meta']) ?>" />
  <link rel="stylesheet" href="styles.css" />
  <link rel="icon" type="image/png" href="website-icon.png" />
</head>
<body>

<div class="card">
  <div class="header">
    <h1 id="pageTitle"><?= htmlspecialchars($T['title']) ?></h1>
    <button id="toggleLang"><?= htmlspecialchars($T['toggle_lang']) ?></button>
  </div>

  <form id="converterForm" novalidate>
    <label id="labelValue" for="value"><?= htmlspecialchars($T['enter_value']) ?></label>
    <input id="value" type="number" min="0" step="any" placeholder="50" required aria-describedby="valueHelp">
    <small id="valueHelp"><?= htmlspecialchars($T['value_help']) ?></small>

    <label id="labelUnit" for="unit"><?= htmlspecialchars($T['select_unit']) ?></label>
    <select id="unit">
      <option value="second"><?= htmlspecialchars($T['unit_second']) ?></option>
      <option value="minute"><?= htmlspecialchars($T['unit_minute']) ?></option>
      <option value="hour"><?= htmlspecialchars($T['unit_hour']) ?></option>
      <option value="day"><?= htmlspecialchars($T['unit_day']) ?></option>
      <option value="month"><?= htmlspecialchars($T['unit_month']) ?></option>
      <option value="year"><?= htmlspecialchars($T['unit_year']) ?></option>
    </select>

    <button id="convertBtn" type="submit" disabled><?= htmlspecialchars($T['convert']) ?></button>
  </form>

  <div id="output" class="result" aria-live="polite" hidden></div>
</div>

<script>
(function(){
  const TRANSLATIONS = <?= json_encode($translations, JSON_UNESCAPED_UNICODE) ?>;
  let currentLang = '<?= $lang ?>';

  const f = {
    second:1, minute:60, hour:3600,
    day:86400, month:2592000, year:31536000
  };

  const el = id => document.getElementById(id);
  const pageTitle = el('pageTitle'),
        labelValue= el('labelValue'),
        valueHelp = el('valueHelp'),
        labelUnit = el('labelUnit'),
        toggleBtn = el('toggleLang'),
        convertBtn= el('convertBtn'),
        inputVal  = el('value'),
        selectU   = el('unit'),
        output    = el('output');

  const fmt = n => { let s = n.toFixed(8); return s.replace(/\.?0+$/,''); };

  function refreshTexts(){
    const T = TRANSLATIONS[currentLang];
    pageTitle.textContent    = T.title;
    labelValue.textContent   = T.enter_value;
    valueHelp.textContent    = T.value_help;
    labelUnit.textContent    = T.select_unit;
    toggleBtn.textContent    = T.toggle_lang;
    convertBtn.textContent   = T.convert;
    ['second','minute','hour','day','month','year'].forEach(u=>{
      selectU.querySelector(`option[value="${u}"]`).textContent = T['unit_'+u];
    });
  }

  inputVal.addEventListener('input', ()=>{
    convertBtn.disabled = !inputVal.checkValidity();
  });

  toggleBtn.addEventListener('click', ()=>{
    currentLang = currentLang === 'pl'? 'en':'pl';
    const p = new URLSearchParams(window.location.search);
    p.set('lang', currentLang);
    window.location.search = p.toString();
  });

  convertBtn.addEventListener('click', evt=>{
    evt.preventDefault();
    const val = parseFloat(inputVal.value);
    const unit = selectU.value;
    const T = TRANSLATIONS[currentLang];
    if (isNaN(val) || val < 0) {
      output.innerHTML = `<p>${T.error_invalid}</p>`;
      output.hidden = false;
      return;
    }
    const total = val * f[unit];
    let html = `<p><strong>${fmt(val)} ${T['unit_'+unit]}</strong> ${T.result_intro}</p>`;
    Object.keys(f).forEach(u=>{
      if(u===unit) return;
      html += `<p>– ${fmt(total/f[u])} ${T['unit_'+u]}</p>`;
    });
    output.innerHTML = html;
    output.hidden = false;
  });

  refreshTexts();
})();
</script>

</body>
</html>