<script>
  let aulas = [];

  async function carregarAulas() {
    const response = await fetch('http://127.0.0.1:5000/api/aulas');
    aulas = await response.json();
  }

  carregarAulas();
</script>

<h2>Lista de Aulas</h2>

{#if aulas.length > 0}
  <table>
    <thead>
      <tr>
        <th>Descrição</th>
        <th>Data e Hora</th>
        <th>Duração</th>
        <th>Localização</th>
      </tr>
    </thead>
    <tbody>
      {#each aulas as aula}
        <tr>
          <td>{aula.descricao}</td>
          <td>{aula.data_hora}</td>
          <td>{aula.duracao.hours}h {aula.duracao.minutes}m</td>
          <td>{aula.localizacao}</td>
        </tr>
      {/each}
    </tbody>
  </table>
{:else}
  <p>Carregando aulas...</p>
{/if}

<style>
  table {
    width: 100%;
    border-collapse: collapse;
  }
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
</style>