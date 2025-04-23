<script>

interface ExerciciosProps {
    
}

let exercicios = [];

async function carregarExercicios() {
  const response = await fetch('http://127.0.0.1:5000/api/exercicios');
  exercicios = await response.json();
}

carregarExercicios();
</script>

<h2>Lista de Exercícios</h2>

{#if exercicios.length > 0}
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
      {#each exercicios as exercicio}
        <tr>
          <td>{exercicio.descricao}</td>
          <td>{exercicio.data_hora}</td>
          <td>{exercicio.duracao.hours}h {exercicio.duracao.minutes}m</td>
          <td>{exercicio.localizacao}</td>
        </tr>
      {/each}
    </tbody>
  </table>
{:else}
  <p>Nenhum exercício cadastrado.</p>
{/if}