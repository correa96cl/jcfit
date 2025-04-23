<script>
  export let isOpen = false;
   export let onClose;

  function handleClose() {
    isOpen = false;
    if (onClose) {
      onClose();
    }
  }
</script>

{#if isOpen}
  <div class="modal-overlay">
    <div class="modal">
      <slot></slot>
      
    </div>
  </div>
{/if}

<style>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .modal {
    background-color:var(--amarelo);
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  }
  
</style>