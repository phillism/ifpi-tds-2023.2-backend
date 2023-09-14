async function main(){
  const ambiente_id = url.searchParams.get("ambiente");
  await obter_dispositivos(ambiente_id)

  const form = document.getElementById('formulario-dispositivo')

  form.addEventListener('submit', processar_dispositivo)

}

async function processar_dispositivo(event){
  event.preventDefault()

  const cx_descricao = document.getElementById('descricao')
  const cx_icone = document.getElementById('icone')

  const descricao = cx_descricao.value
  const icone = cx_icone.value

  const init = {
    method: 'POST',
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({description: descricao, icone: icone || undefined})
  }

  const ambiente_id = url.searchParams.get('ambiente')
  const response = await fetch(`${base_url}/${ambiente_id}/dispositivos`, init)

  if (response.ok){
    alert('Dispositivo salvo com sucesso!')
    window.location = `/dispositivos.html?ambiente=${ambiente_id}`
  }else{
    alert('Error ao processar!')
  }
}

main()