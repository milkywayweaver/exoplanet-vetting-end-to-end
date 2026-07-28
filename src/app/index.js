const neededParams = {
    ra: {
        display: 'RA',
        minValue: 0,
        maxValue: 360,
        value: 0,
        type: 'pos'
    },
    dec: {
        display: 'Declination',
        minValue: -90,
        maxValue: 90,
        value: 0,
        type: 'pos'
    },
    st_pmra: {
        display: 'Stellar PM RA',
        minValue: null,
        maxValue: null,
        value: 0,
        type: 'pos'
    },
    st_pmdec: {
        display: 'Stellar PM Dec',
        minValue: null,
        maxValue: null,
        value: 0,
        type: 'pos'
    },
    st_tmag: {
        display: 'Stellar Magnitude',
        minValue: 0,
        maxValue: null,
        value: 0,
        type: 'stellar'
    },
    st_dist: {
        display: 'Stellar Distance',
        minValue: 0,
        maxValue: null,
        value: 0,
        type: 'stellar'
    },
    st_teff: {
        display: 'Stellar Effective Temperature',
        minValue: 0,
        maxValue: null,
        value: 0,
        type: 'stellar'
    },
    st_logg: {
        display: 'Stellar log(g)',
        minValue: 0,
        maxValue: null,
        value: 0,
        type: 'stellar'
    },
    st_rad: {
        display: 'Stellar Radius',
        minValue: 0,
        maxValue: null,
        value: 0,
        type: 'stellar'
    },
    pl_tranmid: {
        display: 'Planetary Transit Midpoint',
        minValue: 0,
        maxValue: null,
        value: 0,
        type: 'planet'
    },
    pl_orbper: {
        display: 'Planetary Orbital Period',
        minValue: 0,
        maxValue: null,
        value: 0,
        type: 'planet'
    },
    pl_trandurh: {
        display: 'Planetary Transit Duration',
        minValue: 0,
        maxValue: null,
        value: 0,
        type: 'planet'
    },
    pl_trandep: {
        display: 'Planetary Transit Depth',
        minValue: 0,
        maxValue: null,
        value: 0,
        type: 'planet'
    },
    pl_rade: {
        display: 'Planetary Radius',
        minValue: 0,
        maxValue: null,
        value: 0,
        type: 'planet'
    },
    pl_insol: {
        display: 'Planetary Insolation',
        minValue: 0,
        maxValue: null,
        value: 0,
        type: 'planet'
    },
    pl_eqt: {
        display: 'Planetary Equillibrium Temperature',
        minValue: 0,
        maxValue: null,
        value: 0,
        type: 'planet'
    }
}
 
for (const [key,value] of Object.entries(neededParams)) {
    const divEl = document.createElement('div')
    divEl.classList.add('input-container')

    const inputTitleEl = document.createElement('h4')
    inputTitleEl.classList.add('input-title')
    inputTitleEl.textContent = value.display

    const inputFieldEl = document.createElement('input')
    inputFieldEl.type = 'number'
    inputFieldEl.classList.add('input-field')
    inputFieldEl.min = value.minValue
    inputFieldEl.max = value.maxValue
    
    let placeholderText = `${key}: `
    if (value.minValue != null && value.maxValue != null) {
        placeholderText += `${value.minValue} - ${value.maxValue}`
    } else if (value.minValue != null) {
        placeholderText += `> ${value.minValue}`
    } else if (value.maxValue != null) {
        placeholderText += `< ${value.maxValue}`
    } else {
        placeholderText += `Any`
    }
    inputFieldEl.placeholder = placeholderText

    inputFieldEl.addEventListener('input',function() {
        if (value.minValue != null && this.value < value.minValue) {
            this.value = value.minValue
        }
        if (value.maxValue != null && this.value > value.maxValue) {
            this.value = value.maxValue
        }
        value.value = Number(this.value)
        console.log(value.value)
    })
    
    divEl.appendChild(inputTitleEl)
    divEl.appendChild(inputFieldEl)
    inputTypeEl = document.querySelector(`#${value.type}`)
    inputTypeEl.appendChild(divEl)
}