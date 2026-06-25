// Highlight the current page's nav link
(function () {
  const page = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(a => {
    if (a.getAttribute('href') === page) a.classList.add('active');
  });
})();

// Project card renderer — only active on projects.html
const grid = document.getElementById('card-grid');

// Experience card renderer — only active on experience.html
const expGrid = document.getElementById('experience-grid');
if (expGrid) {
  let allExperience = [];
  let activeExpFilter = 'all';

  function expCardHTML(e) {
    const media = e.image
      ? `<img src="${e.image}" alt="${e.title}" class="card-img" loading="lazy">`
      : `<div class="card-img-placeholder">[ no image ]</div>`;

    const tags = e.tags.map(t => `<span class="tag tag-${t}">${t}</span>`).join('');

    const links = (e.links || [])
      .map(l => `<a href="${l.url}" class="card-link" target="_blank" rel="noopener">${l.label} ↗</a>`)
      .join('');

    return `
      <article class="card" data-tags="${e.tags.join(',')}">
        ${media}
        <div class="card-body">
          <div class="card-tags">${tags}</div>
          <h2 class="card-title">${e.title}</h2>
          <p class="card-meta">${e.company}</p>
          <p class="card-dates">${e.dates}</p>
          <p class="card-desc">${e.description}</p>
          <div class="card-links">${links}</div>
        </div>
      </article>`;
  }

  function renderExp(filter) {
    activeExpFilter = filter;
    const visible = filter === 'all'
      ? allExperience
      : allExperience.filter(e => e.tags.includes(filter));

    if (visible.length === 0) {
      expGrid.innerHTML = `<p class="empty-state">// no experience tagged "${filter}"</p>`;
    } else {
      expGrid.innerHTML = visible.map(expCardHTML).join('');
    }
  }

  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderExp(btn.dataset.filter);
    });
  });

  fetch('data/experience.json')
    .then(r => {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    })
    .then(data => {
      allExperience = data;
      renderExp('all');
    })
    .catch(() => {
      expGrid.innerHTML = `<p class="empty-state">// to preview locally, run: python3 -m http.server 8000</p>`;
    });
}
function slugify(title) {
  return title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}

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

    const links = (p.links || [])
      .map(l => `<a href="${l.url}" class="card-link" target="_blank" rel="noopener" onclick="event.stopPropagation()">${l.label} ↗</a>`)
      .join('');

    const slug = slugify(p.title);

    return `
      <a href="project.html?id=${slug}" class="card-link-wrapper">
        <article class="card" data-tags="${p.tags.join(',')}">
          ${media}
          <div class="card-body">
            <div class="card-tags">${tags}</div>
            <h2 class="card-title">${p.title}</h2>
            <p class="card-desc">${p.description}</p>
            <div class="card-links">${links}</div>
          </div>
        </article>
      </a>`;
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
