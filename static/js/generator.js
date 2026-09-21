class QRGeneratorStorage {
  constructor(formId, storageKey) {
    this.form = document.getElementById(formId)
    this.storageKey = storageKey

    if (!this.form) {
      return
    }

    this.init()
  }

  init() {
    this.restoreState()
    this.attachListeners()
  }

  getFormFields() {
    return Array.from(this.form.querySelectorAll('input[name], select[name], textarea[name]'))
  }

  getFieldKey(field) {
    return field.name || field.id || null
  }

  loadState() {
    try {
      const savedData = localStorage.getItem(this.storageKey)

      if (!savedData) {
        return {}
      }

      const parsedData = JSON.parse(savedData)

      return typeof parsedData === 'object' && parsedData !== null ? parsedData : {}
    } catch (error) {
      console.warn('Unable to load QR generator settings:', error)

      return {}
    }
  }

  saveState() {
    const formData = {}

    this.getFormFields().forEach(field => {
      const key = this.getFieldKey(field)

      if (!key) {
        return
      }

      if (field.type === 'checkbox' || field.type === 'radio') {
        formData[key] = field.checked
      } else {
        formData[key] = field.value
      }
    })

    try {
      localStorage.setItem(this.storageKey, JSON.stringify(formData))
    } catch (error) {
      console.warn('Unable to save QR generator settings:', error)
    }
  }

  restoreState() {
    const savedData = this.loadState()

    this.getFormFields().forEach(field => {
      const key = this.getFieldKey(field)

      if (!key || !(key in savedData)) {
        return
      }

      if (field.type === 'checkbox' || field.type === 'radio') {
        field.checked = Boolean(savedData[key])
      } else {
        field.value = savedData[key]
      }
    })
  }

  attachListeners() {
    this.getFormFields().forEach(field => {
      const eventType = field.tagName.toLowerCase() === 'select' || field.type === 'color' ? 'change' : 'input'

      field.addEventListener(eventType, () => {
        this.saveState()
      })
    })
  }
}

/*
|--------------------------------------------------------------------------
| Initialize QR Generator Storage
|--------------------------------------------------------------------------
*/

document.addEventListener('DOMContentLoaded', () => {
  new QRGeneratorStorage('qr-generator-form', 'qr_generator_form')
})
