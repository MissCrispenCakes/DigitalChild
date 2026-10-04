/* Custom JavaScript for GRIMdata website */

// Run page enhancements on initial load and Material instant navigation.
function initializePageEnhancements() {
  // Preserve old root fragment destinations after relocating the technical home.
  const legacy = document.querySelector('.grim-legacy');
  let fragment = window.location.hash.slice(1);
  try { fragment = decodeURIComponent(fragment); } catch (_) { /* Keep malformed fragments inert. */ }
  if (legacy && fragment && Array.from(legacy.querySelectorAll('span[id]')).some(node => node.id === fragment)) {
    window.location.replace(new URL('docs/technical-overview/#' + encodeURIComponent(fragment), window.location.href).href);
    return;
  }
  addRainbowEffects();
  markExternalLinks();
}

if (window.document$ && typeof window.document$.subscribe === 'function') {
  window.document$.subscribe(initializePageEnhancements);
} else if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializePageEnhancements);
} else {
  initializePageEnhancements();
}

/**
 * Add one divider per heading after every page transition.
 */
function addRainbowEffects() {
  document.querySelectorAll('article h1:first-of-type').forEach(heading => {
    if (heading.classList.contains('no-rainbow')) return;
    const sibling = heading.nextElementSibling;
    if (sibling && sibling.classList.contains('rainbow-underline')) return;
    const underline = document.createElement('div');
    underline.className = 'rainbow-underline';
    underline.style.cssText = 'height: 4px; background: linear-gradient(90deg, #e40303, #ff8c00, #ffed00, #008026, #24408e, #732982); margin-top: 0.5rem; margin-bottom: 1rem;';
    heading.after(underline);
  });
}

/**
 * Mark external links with an indicator icon
 */
function markExternalLinks() {
  const links = document.querySelectorAll('a[href^="http"]');
  const currentDomain = window.location.hostname;

  links.forEach(link => {
    const linkDomain = new URL(link.href).hostname;

    if (linkDomain !== currentDomain) {
      // Add external link indicator
      link.classList.add('external-link');
      const iconOnly = !link.textContent.trim();
      // Preserve the visitor's and author's normal navigation choice.
      if (link.target === '_blank') {
        link.setAttribute('rel', 'noopener noreferrer');
        if (iconOnly && !link.hasAttribute('aria-label')) {
          link.setAttribute('aria-label', (link.title || linkDomain) + ' (opens a new tab)');
        }
        if (!link.querySelector('.external-new-tab')) {
          const notice = document.createElement('span');
          notice.className = 'external-new-tab';
          notice.textContent = ' (opens a new tab)';
          link.appendChild(notice);
        }
      }

      // Add visual indicator
      if (!link.querySelector('.external-icon')) {
        const icon = document.createElement('span');
        icon.className = 'external-icon';
        icon.textContent = ' ↗';
        icon.setAttribute('aria-hidden', 'true');
        icon.style.fontSize = '0.8em';
        icon.style.opacity = '0.6';
        link.appendChild(icon);
      }
    }
  });
}

// Anchor navigation is handled by Material and the browser.

// Material provides the single accessible back-to-top control.

/**
 * Utility: Fetch and parse CSV data (for future use)
 */
async function fetchCSVData(url) {
  try {
    const response = await fetch(url);
    const text = await response.text();
    const rows = text.split('\n').map(row => row.split(','));
    const headers = rows[0];
    const data = rows.slice(1).map(row => {
      const obj = {};
      headers.forEach((header, index) => {
        obj[header] = row[index];
      });
      return obj;
    });
    return data;
  } catch (error) {
    console.error('Error fetching CSV:', error);
    return [];
  }
}

/**
 * Utility: Format date consistently
 */
function formatDate(dateString) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString('en-US', options);
}

/**
 * Utility: Debounce function for search/filter inputs
 */
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Export functions for use in other scripts
window.GRIMdata = {
  fetchCSVData,
  formatDate,
  debounce
};
