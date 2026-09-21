class TooltipManager {
  constructor(options = {}) {
    // Define defaults and merge with user-provided options
    this.options = {
      animation: true,
      container: 'container', // Common default, or use '.container' as per your snippet
      trigger: 'hover focus',
      customClass: 'custom-tooltip',
      ...options,
    }

    this.init()
  }

  init() {
    // Logic to initialize tooltips once the DOM is ready
    const setup = () => {
      const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')

      tooltipTriggerList.forEach(el => {
        // Check if an instance already exists to prevent memory leaks/re-init
        if (!bootstrap.Tooltip.getInstance(el)) {
          new bootstrap.Tooltip(el, this.options)
        }
      })
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', setup)
    } else {
      setup()
    }
  }
}

// Usage:
const myTooltips = new TooltipManager({
  container: '.container',
  delay: { show: 500, hide: 100 },
})
