<script>
	import Modal from '../Modal.svelte';

	export let aluno;
	let modalAberto = false;
	let showTooltip = false;
	let tooltipTimeout;

	async function inativarAluno() {
		const response = await fetch(`http://127.0.0.1:5000/api/alunos/inativar/${aluno.id}`, {
			method: 'PATCH'
		});

		if (response.ok) {
			aluno.ativo = false;
			modalAberto = false;
		} else {
			alert('Erro ao inativar aluno.');
		}
	}

	function handleMouseEnter() {
		clearTimeout(tooltipTimeout);
		tooltipTimeout = setTimeout(() => {
			showTooltip = true;
		}, 300);
	}

	function handleMouseLeave() {
		clearTimeout(tooltipTimeout);
		showTooltip = false;
	}

	function handleFocus() {
		clearTimeout(tooltipTimeout);
		showTooltip = true;
	}

	function handleBlur() {
		clearTimeout(tooltipTimeout);
		showTooltip = false;
	}
</script>

{#if aluno.ativo}
	<div class="tooltip-wrapper">
		<button
			class="tooltip-container"
			aria-label="Inativar aluno"
			on:mouseenter={handleMouseEnter}
			on:mouseleave={handleMouseLeave}
			on:focus={handleFocus}
			on:blur={handleBlur}
			on:click={() => (modalAberto = true)}
		>
			<span class="icon-button ri-delete-bin-line" aria-hidden="true" />
		</button>

		{#if showTooltip}
			<div class="tooltip" role="tooltip">
				Inativar {aluno.nome}
			</div>
		{/if}
	</div>

	<Modal isOpen={modalAberto} onClose={() => (modalAberto = false)}>
		<h2 class="modal-title">Confirmar Inativação</h2>
		<p class="modal-title">Deseja realmente inativar o aluno {aluno.nome} {aluno.sobrenome}?</p>
		<button class="shadow-modal" on:click={inativarAluno}>Sim, Inativar</button>
		<button class="shadow-modal-cancelar" on:click={() => (modalAberto = false)}>Cancelar</button>
	</Modal>
{:else}
	<span>Inativado</span>
{/if}

<style>
	h2,
	p {
		margin-bottom: 10px;
	}

	.tooltip-wrapper {
		position: relative;
		display: inline-block;
	}

	.tooltip-container {
		background: none;
		border: none;
		padding: 0.5rem;
		cursor: pointer;
		color: inherit;
		font-size: 1.2rem;
		border-radius: 4px;
	}

	.icon-button {
		display: inline-block;
		z-index: 200;
	}

	.tooltip-container:hover,
	.tooltip-container:focus {
		background: rgba(0, 0, 0, 0.1);
		outline: none;
	}

	.tooltip {
		position: absolute;
		bottom: 100%;
		left: 50%;
		transform: translateX(-50%);
		background: var(--amarelo);
		color: var(--cinza-escura);
		padding: 0.5rem;
		border-radius: 4px;
		font-size: 0.875rem;
		white-space: nowrap;
		margin-bottom: 0.5rem;
		z-index: 100;
	}

	.tooltip:after {
		content: '';
		position: absolute;
		top: 100%;
		left: 50%;
		transform: translateX(-50%);
		border-width: 5px;
		border-style: solid;
		border-color: var(--amarelo) transparent transparent transparent;
	}
</style>
