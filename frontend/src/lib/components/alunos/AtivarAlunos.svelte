<script>
    import Modal from '../Modal.svelte';

    export let aluno;
    export let isOpen = false;
    export let onClose;
    export let onAlunoAtivado;
  
    async function ativarAluno() {
      const response = await fetch(`http://127.0.0.1:5000/api/alunos/ativar/${aluno.id}`, {
        method: 'PATCH',
      });
  
      if (response.ok) {
        if (onAlunoAtivado) {
          onAlunoAtivado();
        }
        fecharModal();
      } else {
        alert('Erro ao ativar aluno.');
      }
    }
  
    function fecharModal() {
      isOpen = false;
      if (onClose) {
        onClose();
      }
    }
  </script>
  
  <Modal isOpen={isOpen} onClose={fecharModal}>
    <h2>Confirmar Ativação</h2>
    <p>Deseja realmente ativar o aluno {aluno.nome} {aluno.sobrenome}?</p>
    <button on:click={ativarAluno}>Sim, Ativar</button>
    <button on:click={fecharModal}>Cancelar</button>
  </Modal>