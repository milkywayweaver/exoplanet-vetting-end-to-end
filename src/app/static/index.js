const neededParams = {
    ra: {
        display: 'RA',
        minValue: 0,
        maxValue: 360,
        value: 158.325433,
        type: 'pos'
    },
    dec: {
        display: 'Declination',
        minValue: -90,
        maxValue: 90,
        value: 1.762447,
        type: 'pos'
    },
    st_pmra: {
        display: 'Stellar PM RA',
        minValue: null,
        maxValue: null,
        value: -1.641000,
        type: 'pos'
    },
    st_pmdec: {
        display: 'Stellar PM Dec',
        minValue: null,
        maxValue: null,
        value: -3.401000,
        type: 'pos'
    },
    pl_tranmid: {
        display: 'Planetary Transit Midpoint',
        minValue: 0,
        maxValue: null,
        value: 2.459656e6,
        type: 'planet'
    },
    pl_orbper: {
        display: 'Planetary Orbital Period',
        minValue: 0,
        maxValue: null,
        value: 4.127126,
        type: 'planet'
    },
    pl_trandurh: {
        display: 'Planetary Transit Duration',
        minValue: 0,
        maxValue: null,
        value: 2.748000,
        type: 'planet'
    },
    pl_trandep: {
        display: 'Planetary Transit Depth',
        minValue: 0,
        maxValue: null,
        value: 4751.804726,
        type: 'planet'
    },
    pl_rade: {
        display: 'Planetary Radius',
        minValue: 0,
        maxValue: null,
        value: 10.515300,
        type: 'planet'
    },
    pl_insol: {
        display: 'Planetary Insolation',
        minValue: 0,
        maxValue: null,
        value: 378.009275,
        type: 'planet'
    },
    pl_eqt: {
        display: 'Planetary Equillibrium Temperature',
        minValue: 0,
        maxValue: null,
        value: 1194.000000,
        type: 'planet'
    },
    st_tmag: {
        display: 'Stellar Magnitude',
        minValue: 0,
        maxValue: null,
        value: 11.880050,
        type: 'stellar'
    },
    st_dist: {
        display: 'Stellar Distance',
        minValue: 0,
        maxValue: null,
        value: 370.582000,
        type: 'stellar'
    },
    st_teff: {
        display: 'Stellar Effective Temperature',
        minValue: 0,
        maxValue: null,
        value: 5801.000000,
        type: 'stellar'
    },
    st_logg: {
        display: 'Stellar log(g)',
        minValue: 0,
        maxValue: null,
        value: 4.330000,
        type: 'stellar'
    },
    st_rad: {
        display: 'Stellar Radius',
        minValue: 0,
        maxValue: null,
        value: 1.238995,
        type: 'stellar'
    }
}
const url = 'http://127.0.0.1:8000/data/'
 
for (const [key,value] of Object.entries(neededParams)) {
    const divEl = document.createElement('div')
    divEl.classList.add('input-container')

    const inputTitleEl = document.createElement('h4')
    inputTitleEl.classList.add('input-title')
    inputTitleEl.textContent = value.display

    const inputFieldEl = document.createElement('input')
    inputFieldEl.type = 'number'
    inputFieldEl.classList.add('input-field')
    inputFieldEl.id = `input-field-${key}`
    inputFieldEl.min = value.minValue
    inputFieldEl.max = value.maxValue
    inputFieldEl.value = value.value
    
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
    })
    
    divEl.appendChild(inputTitleEl)
    divEl.appendChild(inputFieldEl)
    inputTypeEl = document.querySelector(`#${value.type}`)
    inputTypeEl.appendChild(divEl)
}

const submitBtn = document.querySelector('#submit-btn')
submitBtn.addEventListener('click', async function() {
    let params = {}
    for (const [key,values] of Object.entries(neededParams)) {
        params[key] = Number(values.value)
    }
    const pred = await getPred(params,url)
    console.log('This is the result: ',pred)

    const predEl = document.querySelector('#pred-result')
    const predLabel = (pred == 1) ? 'Likely to be a planet' : 'Not likely to be a planet' 
    predEl.textContent = predLabel
})

async function getPred(params,url) {
    try {
        const response = await fetch(url,{
            method:'POST',
            headers: {'Content-Type':'application/json'},
            body:JSON.stringify(params)}        )
        if (!response.ok) {
            throw new Error(`Failed to post to endpoint with status ${response.status}.`)
        }
        const data = await response.json()
        return data
    } catch(err) {
        console.log('Error during POST request',err)
        return null
    } finally {
        console.log('POST request completed.')
    }
}


