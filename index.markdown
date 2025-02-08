---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

<h2>Projects</h2>

<div class="projects">
  {% for project in site.projects %}
    <div class="project">
      <h3><a href="{{ site.baseurl }}{{ project.url }}">{{ project.title }}</a></h3>
      <img src="{{ project.thumbnail }}" style="max-width: 70%; height: auto;" />
      <p>{{ project.excerpt }}</p>
    </div>
  {% endfor %}
</div>
