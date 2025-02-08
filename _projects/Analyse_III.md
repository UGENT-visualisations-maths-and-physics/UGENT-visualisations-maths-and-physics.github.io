---
layout: default
title: "Analyse III"
thumbnail: "assets/manual_figures/Analyse_III/Analyse_III_thumbnail.png"
figures_data: "Analyse_III_figures"
excerpt: "<strong>Vector analysis</strong>: curves, fields , line- and surface integrals... <br>
<strong>Complex analysis</strong>: holomorphic functions, series, residue theorem..."  
---
<h1>{{ page.title }}</h1>

{% assign figures = site.data[page.figures_data] %}
<div class="figures-gallery">
  {% for figure in figures %}
    <div class="figure-item">
      <h3>{{ figure.title }}:</h3>
      <center><img src="{{ site.baseurl }}/{{ figure.image }}" style="max-width: 70%; height: auto;"/></center>
      <br>
    </div>
  {% endfor %}
</div>

<h2>PDF of all the figures:</h2>

<html>
  <head>
    <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width">
  </head>
  <body>
    <object data="{{ site.baseurl }}/assets/generated_figures/Analyse_III/Analyse_III.pdf" type="application/pdf" style="min-height:100vh;width:100%"></object>
  </body>
</html>


