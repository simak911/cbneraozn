var count = 0;

async function nacitani() {
    const url = window.location.origin + '/getdata';
    const response = await fetch(url);
    const json = await response.json();
    const data = json.data;
    const klikani = document.getElementById('klikani');
    var i = 0;
    data.forEach(line => {
        count = count+1;
        const day = line[0]
        const hrs = line[1]
        const mins = line[2]
        const prog = line[3]
        const willbe = (line[4] == "1")
        const box = document.createElement('input')
        box.type = 'checkbox'
        box.id = `checkbox${i}`
        box.checked = false;
        if (willbe) {
            box.checked = true;
        }
        const label = document.createElement('label')
        label.htmlFor = `checkbox${i}`
        label.textContent = `${prog} - ${day} - ${hrs}:${mins}`
        klikani.appendChild(box);
        klikani.appendChild(label);
        i = i+1;
        const br = document.createElement('br');
        klikani.appendChild(br);
    });
};


function kliknuto () {
    const res = Array(count).fill(0)
    for (let i=0; i<count; i++) {
        const idecko = `checkbox${i}`
        const checkboxik = document.getElementById(idecko)

        if (checkboxik.checked) {
            res[i] = 1
        }
    }
    const additional = document.getElementById('pridano').value;
    const jsonik = {'data': res, 'added': additional};
    const datajs = JSON.stringify(jsonik);
    const url = window.location.origin + '/submit';
    const response = fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: datajs
    });
}

const subbut = document.getElementById('subbut');
subbut.addEventListener('click', kliknuto);

nacitani();
