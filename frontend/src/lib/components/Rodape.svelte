<script>
 let anoAtual = new Date().getFullYear();

</script>

<svelte:head>
    <title>JCFIT</title>
</svelte:head>

<footer>
    &#174;
    Copyright JCFIT - {anoAtual}
</footer>

<style>
    footer {
        background-color: #0f0f0f;
        height: 100px;
        font-weight: 700;
        color: var(--amarelo);

        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>