// Highlight the current page's nav link
(function () {
  const page = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(a => {
    if (a.getAttribute('href') === page) a.classList.add('active');
  });
})();

// Project card renderer — only active on projects.html
const grid = document.getElementById('card-grid');
if (grid) {
  let allProjects = [];
  let activeFilter = 'all';

  function tagHTML(tag) {
    return `<span class="tag tag-${tag}">${tag}</span>`;
  }

  function cardHTML(p) {
    const media = p.image
      ? `<img src="${p.image}" alt="${p.title}" class="card-img" loading="lazy">`
      : `<div class="card-img-placeholder">[ no image ]</div>`;

    const tags = p.tags.map(tagHTML).join('');

    const links = [
      p.github && `<a href="${p.github}" class="card-link" target="_blank" rel="noopener">GitHub ↗</a>`,
      p.demo   && `<a href="${p.demo}"   class="card-link" target="_blank" rel="noopener">Demo ↗</a>`,
      p.paper  && `<a href="${p.paper}"  class="card-link" target="_blank" rel="noopener">Paper ↗</a>`,
    ].filter(Boolean).join('');

    return `
      <article class="card" data-tags="${p.tags.join(',')}">
        ${media}
        <div class="card-body">
          <div class="card-tags">${tags}</div>
          <h2 class="card-title">${p.title}</h2>
          <p class="card-desc">${p.description}</p>
          <div class="card-links">${links}</div>
        </div>
      </article>`;
  }

  function render(filter) {
    activeFilter = filter;
    const visible = filter === 'all'
      ? allProjects
      : allProjects.filter(p => p.tags.includes(filter));

    if (visible.length === 0) {
      grid.innerHTML = `<p class="empty-state">// no projects tagged "${filter}"</p>`;
    } else {
      grid.innerHTML = visible.map(cardHTML).join('');
    }
  }

  // Wire up filter buttons
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      render(btn.dataset.filter);
    });
  });

  // Load projects
  fetch('data/projects.json')
    .then(r => {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    })
    .then(data => {
      allProjects = data;
      render('all');
    })
    .catch(() => {
      grid.innerHTML = `<p class="empty-state">// to preview locally, run: python3 -m http.server 8000</p>`;
    });
}
