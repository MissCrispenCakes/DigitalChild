/* Custom JavaScript for GRIMdata / LittleRainbowRights website */

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
  console.log('GRIMdata / LittleRainbowRights website loaded');

  // Add rainbow effect to specific elements
  addRainbowEffects();

  // Initialize scorecard visualizations if on scorecard page
  if (window.location.pathname.includes('scorecard')) {
    initializeScorecardVisualizations();
  }

  // Add copy button functionality to code blocks (if not already present)
  enhanceCodeBlocks();

  // Add external link indicators
  markExternalLinks();
});

/**
 * Add rainbow visual effects to specific elements
 */
function addRainbowEffects() {
  // Add rainbow underline to main headings
  const mainHeadings = document.querySelectorAll('h1');
  mainHeadings.forEach(heading => {
    if (!heading.classList.contains('no-rainbow')) {
      heading.style.borderBottom = '4px solid transparent';
      heading.style.borderImage = 'linear-gradient(90deg, #e40303, #ff8c00, #ffed00, #008026, #24408e, #732982) 1';
      heading.style.paddingBottom = '0.5rem';
    }
  });
}

/**
 * Initialize scorecard visualizations using Plotly
 * Note: This is a placeholder for future implementation
 */
function initializeScorecardVisualizations() {
  console.log('Scorecard page detected - visualizations coming soon');

  // Placeholder: Check if Plotly is available
  if (typeof Plotly !== 'undefined') {
    console.log('Plotly available - ready for visualizations');
    // Future: Create charts here
    // createIndicatorCharts();
    // createCountryMap();
  } else {
    console.log('Plotly not loaded - interactive charts disabled');
  }
}

/**
 * Create indicator distribution charts (placeholder for future)
 */
function createIndicatorCharts() {
  // Example data structure (to be replaced with actual data)
  const sampleData = {
    'AI_Policy_Status': {
      'Comprehensive Strategy': 25,
      'Framework or Guidelines': 48,
      'No Published Policy': 121
    },
    'Data_Protection_Law': {
      'Comprehensive Law': 71,
      'Draft Legislation': 23,
      'No Specific Law': 100
    }
  };

  // Future: Create Plotly charts for each indicator
  // Plotly.newPlot('indicator-chart', data, layout);
}

/**
 * Create country choropleth map (placeholder for future)
 */
function createCountryMap() {
  // Future: Create interactive world map with Plotly
  // showing indicator values color-coded by country
}

/**
 * Enhance code blocks with additional functionality
 */
function enhanceCodeBlocks() {
  const codeBlocks = document.querySelectorAll('pre code');

  codeBlocks.forEach(block => {
    // Add language label if detected
    const language = block.className.match(/language-(\w+)/);
    if (language && language[1]) {
      const label = document.createElement('span');
      label.className = 'code-language-label';
      label.textContent = language[1];
      label.style.cssText = 'position: absolute; top: 0.5rem; right: 0.5rem; background: rgba(0,0,0,0.3); padding: 0.2rem 0.5rem; border-radius: 3px; font-size: 0.7rem; text-transform: uppercase;';

      const pre = block.parentElement;
      if (pre.tagName === 'PRE') {
        pre.style.position = 'relative';
        pre.appendChild(label);
      }
    }
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
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');

      // Add visual indicator
      if (!link.querySelector('.external-icon')) {
        const icon = document.createElement('span');
        icon.className = 'external-icon';
        icon.innerHTML = ' ↗';
        icon.style.fontSize = '0.8em';
        icon.style.opacity = '0.6';
        link.appendChild(icon);
      }
    }
  });
}

/**
 * Smooth scroll to anchors
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const targetId = this.getAttribute('href');
    if (targetId === '#') return;

    const targetElement = document.querySelector(targetId);
    if (targetElement) {
      e.preventDefault();
      targetElement.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });

      // Update URL without triggering navigation
      if (history.pushState) {
        history.pushState(null, null, targetId);
      }
    }
  });
});

/**
 * Add "back to top" button functionality
 */
function addBackToTopButton() {
  const button = document.createElement('button');
  button.innerHTML = '↑ Top';
  button.className = 'back-to-top';
  button.style.cssText = 'position: fixed; bottom: 2rem; right: 2rem; background: var(--md-primary-fg-color); color: white; border: none; padding: 0.75rem 1rem; border-radius: 4px; cursor: pointer; display: none; z-index: 1000; transition: opacity 0.3s;';

  document.body.appendChild(button);

  // Show/hide based on scroll position
  window.addEventListener('scroll', function() {
    if (window.pageYOffset > 300) {
      button.style.display = 'block';
    } else {
      button.style.display = 'none';
    }
  });

  // Scroll to top on click
  button.addEventListener('click', function() {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
}

// Initialize back to top button
addBackToTopButton();

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
  debounce,
  createIndicatorCharts,
  createCountryMap
};

console.log('GRIMdata utilities loaded');
