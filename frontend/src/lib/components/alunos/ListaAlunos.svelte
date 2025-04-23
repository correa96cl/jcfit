<script>
	import { format } from 'date-fns';
	import { ptBR } from 'date-fns/locale/pt-BR';
	import CriarAlunos from './CriarAlunos.svelte';
	import InativarAlunos from './InativarAlunos.svelte';
	import AtivarAlunos from './AtivarAlunos.svelte';
	import { onMount } from 'svelte';

	let alunos = [];
	let alunosFiltrados = [];
	let termoBusca = '';
	let modalAtivarAlunoAberto = false;
	let alunoSelecionado = null;
	let modalAdicionarAlunoAberto = false;
	let isLoading = true;
	let mostrarInativos = false;

	async function carregarAlunos() {
		try {
			await new Promise((resolve) => setTimeout(resolve, 2000));
			const response = await fetch('http://127.0.0.1:5000/api/alunos');
			if (!response.ok) throw new Error('Falha ao carregar alunos');
			alunos = await response.json();
			filtrarAlunos(); // Apply initial filter
		} catch (error) {
			console.error('Erro ao carregar alunos:', error);
		} finally {
			isLoading = false;
		}
	}

	onMount(() => {
		carregarAlunos();
	});

	function alunoAtivado() {
		isLoading = true;
		carregarAlunos();
	}

	function alunoAdicionado() {
		isLoading = true;
		carregarAlunos();
	}

	function filtrarAlunos() {
		// First filter by active status
		let alunosFiltradosPorStatus = mostrarInativos ? alunos : alunos.filter((aluno) => aluno.ativo);

		// Then apply search filter
		if (!termoBusca) {
			alunosFiltrados = alunosFiltradosPorStatus;
			return;
		}

		const termo = termoBusca.toLowerCase();
		alunosFiltrados = alunosFiltradosPorStatus.filter(
			(aluno) =>
				aluno.nome.toLowerCase().includes(termo) ||
				aluno.sobrenome.toLowerCase().includes(termo) ||
				aluno.email.toLowerCase().includes(termo) ||
				aluno.telefone.includes(termo)
		);
	}

	// React to changes in search term or inactive checkbox
	$: {
		if (alunos.length) {
			filtrarAlunos();
		}
	}
</script>

<div class="controls-container">
	<div class="search-wrapper">
		<div class="search-container">
			<input
				type="text"
				placeholder="Buscar aluno..."
				bind:value={termoBusca}
				on:input={filtrarAlunos}
				class="search-input {isLoading ? 'skeleton' : ''}"
				disabled={isLoading}
			/>
			<button
				class="add-button shadow ri-admin-line {isLoading ? 'skeleton' : ''}"
				on:click={() => (modalAdicionarAlunoAberto = true)}
				disabled={isLoading}
			>
				Adicionar Aluno
			</button>
		</div>
	</div>

	<label class="toggle-switch">
		<input
			type="checkbox"
			bind:checked={mostrarInativos}
			on:change={filtrarAlunos}
			disabled={isLoading}
		/>
		<span class="slider round"></span>
		<span class="toggle-text">{mostrarInativos ? 'Mostrando inativos' : 'Ocultando inativos'}</span>
	</label>
</div>

<CriarAlunos
	isOpen={modalAdicionarAlunoAberto}
	onClose={() => (modalAdicionarAlunoAberto = false)}
	onAlunoAdicionado={alunoAdicionado}
/>

{#if isLoading}
	<div class="skeleton-container">
		{#each Array(3) as _, i}
			<div class="skeleton-card">
				<div class="skeleton-line long"></div>
				<div class="skeleton-line medium"></div>
				<div class="skeleton-line medium"></div>
				<div class="skeleton-line short"></div>
				<div class="skeleton-status"></div>
			</div>
		{/each}
	</div>
{:else if alunosFiltrados.length > 0}
	<div class="alunos">
		{#each alunosFiltrados as aluno}
			<div class="categoria-container {!aluno.ativo ? 'inactive' : ''}">
				<h3 class="categoria-nome">{aluno.nome} {aluno.sobrenome}</h3>
				<p class="categoria-info">Email: {aluno.email}</p>
				<p class="categoria-info">Telefone: {aluno.telefone}</p>
				<p class="categoria-info">
					Data de Nascimento: {format(new Date(aluno.data_nascimento), "dd 'de' MMMM 'de' yyyy", {
						locale: ptBR
					})}
				</p>
				{#if aluno.ativo}
					<p class="ativo sim">
						Ativo
						<InativarAlunos {aluno} />
					</p>
				{:else}
					<p class="ativo nao">
						Inativo
						<AtivarAlunos
							{aluno}
							isOpen={modalAtivarAlunoAberto}
							onClose={() => (modalAtivarAlunoAberto = false)}
							onAlunoAtivado={alunoAtivado}
						/>
					</p>
				{/if}
			</div>
		{/each}
	</div>
{:else}
	<p class="no-results">
		{#if termoBusca}
			Nenhum aluno encontrado com o termo "{termoBusca}"
		{:else}
			{mostrarInativos ? 'Nenhum aluno cadastrado' : 'Nenhum aluno ativo'}
		{/if}
	</p>
{/if}

<style>
    .controls-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-bottom: 2rem;
        width: 100%;
        align-items: center;
    }

    .search-wrapper {
        width: 100%;
        max-width: 600px;
    }

    .search-container {
        display: flex;
        gap: 0.75rem;
        align-items: center;
        width: 100%;
    }

	.search-input {
    flex: 1;
    padding: 0.5rem 0.75rem;
    border: 1px solid var(--cinza-escura);
    border-radius: 6px;
    font-size: 0.9rem;
    height: 2.25rem;
    background: transparent;
    color: var(--cinza);
    transition: all 0.3s ease-out;
    outline: none;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

/* Hover State */
.search-input:hover {
    border-color: var(--cinza-escura);
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    background-color: rgba(255,255,255,0.05);
}

/* Focus State */
.search-input:focus {
    border-color: var(--amarelo);
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
    background-color: rgba(255,255,255,0.1);
}

/* Placeholder Styling */
.search-input::placeholder {
    color: var(--cinza-claro);
    opacity: 1;
    transition: opacity 0.2s ease;
}

.search-input:hover::placeholder {
    opacity: 0.8;
}

.search-input:focus::placeholder {
    opacity: 0.5;
}

/* Disabled State */
.search-input:disabled {
    background-color: rgba(255,255,255,0.02);
    cursor: not-allowed;
    opacity: 0.7;
}

    .add-button {
        padding: 0.5rem 0.75rem;
        font-size: 0.9rem;
        height: 2.25rem;
        white-space: nowrap;
    }

	.toggle-switch {
        position: relative;
        display: inline-flex;
        align-items: center;
        gap: 12px;
        cursor: pointer;
        user-select: none;
        margin-top: 8px;
    }

    .toggle-switch input {
        position: absolute;
        opacity: 0;
        width: 0;
        height: 0;
    }

    .slider {
        position: relative;
        display: inline-block;
        width: 52px;
        height: 26px;
        background-color: #ccc;
        transition: .4s;
        border-radius: 34px;
    }

    .slider:before {
        position: absolute;
        content: "";
        height: 22px;
        width: 22px;
        left: 2px;
        bottom: 2px;
        background-color: white;
        transition: .4s;
        border-radius: 50%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }

    input:checked + .slider {
        background-color: #4CAF50;
    }

    input:checked + .slider:before {
        transform: translateX(26px);
    }

    input:disabled + .slider {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .toggle-text {
        font-size: 0.9rem;
        color: var(--branco);
        font-weight: 500;
        transition: color 0.3s ease;
    }

    input:checked ~ .toggle-text {
        color: #4CAF50;
    }

    input:disabled ~ .toggle-text {
        opacity: 0.6;
    }

    .alunos {
        margin-bottom: 4.6875rem;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1.5rem;
    }

    .categoria-container {
        min-height: 100%;
        
        box-shadow: 4px 4px 10px 1px rgba(0, 0, 0, 0.1);
        padding: 1.5rem;
        border: 1px solid var(--branco);
        border-radius: 14px;
        box-sizing: border-box;
        width: 100%;
        max-width: 350px;
        transition: opacity 0.3s;
    }

    .categoria-container.inactive {
        opacity: 0.7;
        background: rgb(71, 70, 70);
        border: 1px solid var(--branco); 
        z-index: -1;
}

    .categoria-nome {
        font-size: 1.125rem;
        font-weight: bold;
        color: var(--branco);
        margin-bottom: 0.875rem;
    }

    .categoria-info {
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
        color: var(--branco);
    }

    .ativo {
        margin-top: 1rem;
        font-weight: bold;
        text-align: center;
    }

    .ativo.sim {
        color: --branco;
    }

    .ativo.nao {
        color: --branco;
    }

    .no-results {
        text-align: center;
        color: var(--branco);
        margin: 2rem 0;
        font-size: 1.1rem;
    }

    /* Skeleton Styles */
    .skeleton {
        background-color: #e0e0e0 !important;
        color: transparent !important;
        border-color: #e0e0e0 !important;
        cursor: default;
        animation: pulse 1.5s infinite ease-in-out;
    }

    .skeleton-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1.5rem;
        margin-bottom: 4.6875rem;
    }

    .skeleton-card {
        background: #747373;
        padding: 1.5rem;
        border-radius: 14px;
        width: 100%;
        max-width: 350px;
        box-shadow: 4px 4px 10px 1px rgba(0, 0, 0, 0.1);
    }

    .skeleton-line {
        height: 1rem;
        background: #e0e0e0;
        margin-bottom: 0.8rem;
        border-radius: 4px;
        animation: pulse 1.5s infinite ease-in-out;
    }

    .skeleton-line.long {
        width: 80%;
    }

    .skeleton-line.medium {
        width: 70%;
    }

    .skeleton-line.short {
        width: 60%;
    }

    .skeleton-status {
        height: 1.5rem;
        width: 30%;
        margin-top: 1rem;
        background: #e0e0e0;
        border-radius: 4px;
        animation: pulse 1.5s infinite ease-in-out;
    }

    @keyframes pulse {
        0%, 100% {
            opacity: 0.6;
        }
        50% {
            opacity: 0.3;
        }
    }

    @media (max-width: 768px) {
        .search-container {
            flex-direction: column;
        }

        .search-input,
        .add-button {
            width: 100%;
        }

        .categoria-container,
        .skeleton-card {a
            width: 100%;
        }
    }

	@media (prefers-color-scheme: dark) {
    .search-input {
        border-color: var(--cinza-escura-dark);
    }
    .search-input:hover {
        background-color: rgba(255,255,255,0.03);
    }
}
</style>
