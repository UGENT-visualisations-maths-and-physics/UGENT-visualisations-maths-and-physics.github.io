---
layout: default
title: "Calculus III"
thumbnail: "assets/manual_figures/{{ page.title | replace: ' ', '_' }}/thumbnail.png"
underscore_title: "{{ page.title | replace: ' ', '_' }}"
figures_data: "{{ page.underscore_title }}_figures"
figures_pdf : "assets/generated_figures/{{ page.underscore_title }}/{{ page.underscore_title }}.pdf"
excerpt: "<strong>Vector analysis</strong>: curves, fields , line- and surface integrals... <br>
<strong>Complex analysis</strong>: holomorphic functions, series, residue theorem..."  
---
<h1>{{ page.title }}</h1>

{% include figures.html %}

<h2>PDF of all the figures:</h2>

{% include figures_PDF.html %}


