
async function main(){
  reload_dispositivos()
}


async function obter_dispositivos(ambiente_id) {
  const response = await fetch(`${base_url}/${ambiente_id}/dispositivos`, {
    headers: { 'Content-Type': 'application/json' }
  })

  switch(response.status) {
    case 200:
      return await response.json()
    
      case 404:
        alert('Ambiente não encontrado.')
        break
      
      default:
        alert('Ocorreu um erro.')
        break
  }

  window.location = '/'
}


async function reload_dispositivos(){
  const pageTitle = document.querySelector('.titulo')
  
  if (!pageTitle) {
    return
  }
  
  const ambiente_id = url.searchParams.get("ambiente");
  const dispositivos = await obter_dispositivos(ambiente_id)
  pageTitle.textContent = `Dispositivos do ambiente de ID: ${ambiente_id}`

  const buttonAddDispositivo = document.querySelector('.botao-add-dispositivo')
  buttonAddDispositivo.href += `?ambiente=${ambiente_id}`
  
  const table_ambientes = document.getElementById('dispositivos')
  table_ambientes.innerHTML = ''

  for (let { id, description, icone, estado_conexao, status } of dispositivos){
    adicionar_dispositivo(id, description, icone, estado_conexao, status)
  }
}


function adicionar_dispositivo(id, description, icone, estado_conexao, status){
  const table_dispositivos = document.getElementById('dispositivos')

  const linha_item = document.createElement('tr')
  const coluna_id = document.createElement('td')
  const coluna_desc = document.createElement('td')
  const coluna_icone = document.createElement('td')
  const coluna_estado_conexao = document.createElement('td')
  const coluna_status = document.createElement('td')
  const coluna_acoes = document.createElement('td')

  const link_remover = document.createElement('a')
  const link_mover = document.createElement('a')

  coluna_id.textContent = id
  coluna_desc.textContent = description
  coluna_icone.textContent = icone
  coluna_estado_conexao.textContent = estado_conexao
  coluna_status.textContent = status

  coluna_acoes.classList.add('td-acoes')

  link_remover.textContent = 'Remover'
  link_mover.textContent = 'Mover'
  // link_remover.href = 'http://www.uol.com.br'
  link_remover.classList.add('botao-remover-table')
  link_remover.classList.add('botao-table')

  link_mover.classList.add('botao-mover-table')
  link_mover.classList.add('botao-table')

  link_remover.onclick = async () => {
    if (!confirm(`Deseja remover o dispositivo "${description}"?`)){
      return
    }

    link_remover.textContent = 'Aguarde!'

    // alert(`Clicou no ID=${id}`)
    const url_remover = base_url + '/' + ambiente_id + '/dispositivos/' + id
    const init = {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    }
    const response = await fetch(url_remover, init)

    if (response.ok){
      alert(`Dispositivo "${description}" removido!`)
      reload_dispositivos()
    }else{
      alert('Não foi possível remover!')
    }
  }

  const ambiente_id = url.searchParams.get("ambiente");
  link_mover.onclick = async() => {
    const overlay = document.querySelector('.overlay')
    overlay.style.display = 'flex'
    const ambientes = await obter_ambientes()

    const dispositivo_id = document.querySelector('#dispositivo_id')
    dispositivo_id.value = id

    const ambientes_label = document.querySelector('#label_ambientes')

    ambientes_label.innerHTML = ``

    for (ambiente of ambientes) {
      if (ambiente.id == ambiente_id) {
        continue
      }

      let option = document.createElement('option')
      option.textContent = `[${ambiente.id}] ${ambiente.descricao}`
      option.value = ambiente.id

      ambientes_label.appendChild(option)
    }
  }

  coluna_acoes.append(link_remover, link_mover)

  linha_item.append(coluna_id, coluna_desc, coluna_icone, coluna_estado_conexao, coluna_status, coluna_acoes)
  table_dispositivos.appendChild(linha_item)
}


async function mover() {
  const { value: ambiente_destino } = document.querySelector('#label_ambientes')
  const ambiente_id = url.searchParams.get('ambiente')
  const dispositivo_id = document.querySelector('#dispositivo_id')

  const init = {
    method: 'PUT',
    headers: {
      "Content-Type": "application/json",
    }
  }
  const response = await fetch(`${base_url}/${ambiente_id}/dispositivos/${dispositivo_id.value}/mover/${ambiente_destino}`, init)
  if (response.ok) {
    alert("Dispositivo movido com sucesso!")
    cancelar_mover()
    reload_dispositivos()
  } else {
    alert("Ocorreu um erro.")
    cancelar_mover()
  }
}


function cancelar_mover() {
  const overlay = document.querySelector('.overlay')
  overlay.style.display = 'none'

  const ambiente_label = document.querySelector('#label_ambientes')
  ambiente_label.innerHTML = ``
}

main()
