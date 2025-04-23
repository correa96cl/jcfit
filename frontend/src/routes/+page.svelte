<script lang="ts">
    import '../app.css';
    import ListaAlunos from '$lib/components/alunos/ListaAlunos.svelte';
    import Cabecalho from '$lib/components/Cabecalho.svelte';
    import Rodape from '$lib/components/Rodape.svelte';
    import Sidebar from '$lib/components/Sidebar.svelte';
    
    let sidebarExpanded = true;
    
    function handleMainClick() {
        if (sidebarExpanded) {
            sidebarExpanded = false;
        }
    }
</script>

<svelte:head>
    <title>JCFIT</title>
</svelte:head>

<div class="app-layout">
    <Sidebar bind:expanded={sidebarExpanded} />
    
    <main class="main-content" on:click={handleMainClick}>
        <Cabecalho />
        <ListaAlunos />
        <Rodape />
    </main>
</div>

<style>
    .app-layout {
        display: flex;
        min-height: 100vh;
    }
    
    .main-content {
        flex-grow: 1;
        padding: 1rem;
        transition: margin-left 0.3s ease;
        margin-left: 250px; /* Match sidebar expanded width */
    }
    
    /* When sidebar is collapsed */
    :global(.sidebar:not(.expanded)) ~ .main-content {
        margin-left: 70px; /* Match sidebar collapsed width */
    }
    
    @media (max-width: 768px) {
        .main-content {
            margin-left: 0;
        }
    }
</style>