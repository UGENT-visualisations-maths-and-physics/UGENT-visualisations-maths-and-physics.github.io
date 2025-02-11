---
layout: page
title: Setup support
excerpt: Guides on setting up LaTeX distribution, for compiling figures and github for accessing repositories.
---

<h2>Github</h2>
<h3>1. Setup Github:</h3>

<!-- Loop Through and select relevant subpage -->
{% assign guide = site.setup_support | where_exp:"guide", "guide.title == 'Setup Github on Windows'" | first %}
<p><a href="{{ site.baseurl }}{{ guide.url }}">{{ guide.title }}</a></p>

{% assign guide = site.setup_support | where_exp:"guide", "guide.title == 'Setup Github on macOS'" | first %}
<p><a href="{{ site.baseurl }}{{ guide.url }}">{{ guide.title }}</a></p>

<!-- VSCODE guide -->
{% assign guide = site.setup_support | where_exp:"guide", "guide.title == 'Using Github on VS Code'" | first %}
<h3><a href="{{ site.baseurl }}{{ guide.url }}">{{ "2: " | append: guide.title }}</a></h3>

<h2>Setup Latex (for use in VS Code)</h2>

{% assign guide = site.setup_support | where_exp:"guide", "guide.title == 'Setup LaTeX on Windows'" | first %}
<p><a href="{{ site.baseurl }}{{ guide.url }}">{{ guide.title }}</a></p>

{% assign guide = site.setup_support | where_exp:"guide", "guide.title == 'Setup LaTeX on macOS'" | first %}
<p><a href="{{ site.baseurl }}{{ guide.url }}">{{ guide.title }}</a></p>


