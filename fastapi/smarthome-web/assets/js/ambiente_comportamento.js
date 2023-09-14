async function main(){
  reload_ambientes()
}

async function reload_ambientes(){
  const ambientes = await obter_ambientes()
  const table_ambientes = document.getElementById('ambientes')

  if (!table_ambientes) {
    return
  }

  table_ambientes.innerHTML = ''

  for (let ambiente of ambientes){
    adicionar_ambiente(ambiente.id, ambiente.descricao)
  }
}

async function obter_ambientes() {
  const response = await fetch(base_url)
  return response.ok ? await response.json() : []
}

function adicionar_ambiente(id, descricao){
  const table_ambientes = document.getElementById('ambientes')

  const linha_item = document.createElement('tr')
  const coluna_id = document.createElement('td')
  const coluna_desc = document.createElement('td')
  const coluna_acoes = document.createElement('td')
  const link_remover = document.createElement('a')
  const link_dispositivos = document.createElement('a')

  coluna_id.textContent = id
  coluna_desc.textContent = descricao

  coluna_acoes.classList.add('td-acoes')

  link_remover.textContent = 'Remover'
  link_dispositivos.textContent = 'Dispositivos'
  link_dispositivos.href = `/dispositivos.html?ambiente=${id}`
  // link_remover.href = 'http://www.uol.com.br'
  link_remover.classList.add('botao-remover-table')
  link_remover.classList.add('botao-table')

  link_dispositivos.classList.add('botao-dispositivos-table')
  link_dispositivos.classList.add('botao-table')

  link_remover.onclick = async () => {

    if (!confirm(`Deseja remover "${descricao}"?`)){
      return
    }

    link_remover.textContent = 'Aguarde!!'

    // alert(`Clicou no ID=${id}`)
    const url_remover = base_url + '/' + id
    const init = {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    }
    const response = await fetch(url_remover, init)

    if (response.ok){
      alert(`Ambiente "${descricao}" removido!`)
      reload_ambientes()
    }else{
      alert('Não foi possível remover!')
    }
  }

  coluna_acoes.appendChild(link_remover)
  coluna_acoes.appendChild(link_dispositivos)

  linha_item.append(coluna_id, coluna_desc, coluna_acoes)
  table_ambientes.appendChild(linha_item)
}

main()
