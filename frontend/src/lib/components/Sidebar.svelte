<script>
  import { page } from '$app/stores';
  import { fade } from 'svelte/transition';
  import { sidebarExpanded } from '$lib/stores.js';
  import { onMount } from 'svelte';

  $: expanded = $sidebarExpanded;
  
  function toggleSidebar() {
      sidebarExpanded.update(n => !n);
  }

  export let expanded = true;
  
  const navItems = [
      { path: '/', label: 'Home', icon: 'ri-home-line' },
      { path: '/alunos', label: 'Alunos', icon: 'ri-user-line' },
      { path: '/exercicios', label: 'Exercicios', icon: 'ri-cup-fill' },
      { path: '/aulas', label: 'Aulas', icon: 'ri-book-line' },
      { path: '/relatorios', label: 'Relatorios', icon: 'ri-settings-line' }
  ];
  
  let mobileOpen = false;
  let isMobile = false;

  function checkMobile() {
      isMobile = window.innerWidth <= 768;
      if (isMobile) {
          expanded = false;
          mobileOpen = false;
      }
  }

  onMount(() => {
      checkMobile();
      window.addEventListener('resize', checkMobile);
      return () => window.removeEventListener('resize', checkMobile);
  });
</script>

<div class="sidebar-container">
  <!-- Mobile Toggle Button (Hamburger) -->
  <button 
      class="mobile-toggle"
      aria-label={mobileOpen ? 'Fechar menu' : 'Abrir menu'}
      on:click={() => mobileOpen = !mobileOpen}
  >
      <span class="ri-menu-line" />
  </button>
  
  <!-- Overlay (visible when sidebar is open on mobile) -->
  {#if mobileOpen}
      <div 
          class="sidebar-overlay"
          on:click={() => mobileOpen = false}
          transition:fade
      />
  {/if}
  
  <!-- Sidebar -->
  <aside 
      class="sidebar"
      class:expanded={expanded && !isMobile}
      class:mobile-open={mobileOpen}
      aria-label="Navegação principal"
  >
      <!-- Mobile Close Button (X icon) -->
      {#if isMobile}
          <button 
              class="mobile-close"
              on:click={() => mobileOpen = false}
              aria-label="Fechar menu"
          >
              <span class="ri-close-line" />
          </button>
      {/if}
      
      <!-- Sidebar Header -->
      <div class="sidebar-header">
          {#if expanded || isMobile}
              <h2 class="logo"></h2>
          {:else}
              <div class="logo-icon">JC</div>
          {/if}
      </div>
      
      <!-- Navigation Links -->
      <nav>
          <ul>
              {#each navItems as item}
                  <li>
                      <a
                          href={item.path}
                          class:active={$page.url.pathname === item.path}
                          aria-current={$page.url.pathname === item.path ? 'page' : undefined}
                          on:click={() => isMobile ? mobileOpen = false : null}
                      >
                          <span class={item.icon} aria-hidden="true" />
                          <span class="label">{item.label}</span>
                      </a>
                  </li>
              {/each}
          </ul>
      </nav>
      
      <!-- Desktop Expand/Collapse Toggle -->
      {#if !isMobile}
          <div class="toggle-container">
              <button 
                  class="toggle-expand"
                  on:click={toggleSidebar}
                  aria-label={expanded ? 'Recolher menu' : 'Expandir menu'}
              >
                  {#if expanded}
                      <span class="ri-arrow-left-circle-line" />
                  {:else}
                      <span class="ri-arrow-right-circle-line" />
                  {/if}
              </button>
          </div>
      {/if}
  </aside>
</div>

<style>
  :global(:root) {
      --sidebar-width: 250px;
      --sidebar-collapsed-width: 70px;
      --sidebar-bg: #1e293b;
      --sidebar-text: #f8fafc;
      --sidebar-active: #ffc107;
      --sidebar-hover: #334155;
      --sidebar-transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  /* Container Styles */
  .sidebar-container {
      position: relative;
  }

  /* Mobile Toggle Button (Hamburger) */
  .mobile-toggle {
      display: none;
      position: fixed;
      top: 1rem;
      left: 1rem;
      z-index: 100;
      background: var(--sidebar-bg);
      color: var(--sidebar-text);
      border: none;
      border-radius: 4px;
      padding: 0.75rem;
      cursor: pointer;
      box-shadow: 0 2px 4px rgba(0,0,0,0.2);
      transition: all 0.2s ease;
  }

  .mobile-toggle:hover {
      background: var(--sidebar-hover);
      transform: scale(1.05);
  }

  /* Overlay Styles */
  .sidebar-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.5);
      z-index: 90;
      backdrop-filter: blur(3px);
  }

  /* Sidebar Styles */
  .sidebar {
      position: fixed;
      top: 0;
      left: 0;
      bottom: 0;
      width: var(--sidebar-width);
      background: var(--sidebar-bg);
      color: var(--sidebar-text);
      transition: all var(--sidebar-transition);
      z-index: 100;
      display: flex;
      flex-direction: column;
      padding: 1rem 0;
      box-shadow: 2px 0 10px rgba(0,0,0,0.1);
      transform: translateX(-100%);
  }

  /* Mobile Close Button (X icon) */
  .mobile-close {
      position: absolute;
      top: 1rem;
      right: 1rem;
      background: transparent;
      border: none;
      color: var(--sidebar-text);
      font-size: 1.5rem;
      cursor: pointer;
      padding: 0.5rem;
      z-index: 101;
      transition: all 0.2s ease;
  }

  .mobile-close:hover {
      color: var(--sidebar-active);
      transform: scale(1.1);
  }

  /* Sidebar Header */
  .sidebar-header {
      position: relative;
      padding: 0 1.5rem 1rem;
      padding-right: 3rem; /* Space for close button */
      border-bottom: 1px solid rgba(255,255,255,0.1);
      margin-bottom: 1rem;
  }

  .logo {
      margin: 0;
      font-size: 1.25rem;
      font-weight: 600;
      white-space: nowrap;
      transition: opacity 0.2s ease;
      background-image: url('/imagens/logojcfit.png');
      background-repeat: no-repeat;
      background-size: cover;
      background-position: center center;
      height: 50px;
  }

  .logo-icon {
      font-size: 1.5rem;
      font-weight: bold;
      text-align: center;
      padding: 0.5rem 0;
      color: var(--amarelo);

  }

  /* Navigation Styles */
  nav ul {
      list-style: none;
      padding: 0;
      margin: 0;
      flex-grow: 1;
  }

  nav li a {
      display: flex;
      align-items: center;
      gap: 1rem;
      padding: 0.75rem 1.5rem;
      color: inherit;
      text-decoration: none;
      transition: all 0.2s ease;
      white-space: nowrap;
  }

  nav li a:hover {
      background: var(--sidebar-hover);
  }

  nav li a.active {
      background: var(--sidebar-active);
      color: #000;
  }

  nav li a.active .icon {
      color: #000;
  }

  .label {
      transition: opacity 0.2s ease;
  }

  /* Desktop Toggle Button */
  .toggle-container {
      display: flex;
      padding: 0.5rem;
      border-top: 1px solid rgba(255,255,255,0.1);
      margin-top: auto;
  }

  .toggle-expand {
      background: none;
      border: none;
      color: inherit;
      padding: 0.5rem;
      cursor: pointer;
      display: flex;
      justify-content: center;
      align-items: center;
      margin-left: auto;
      transition: all 0.3s ease;
      font-size: 1.5rem;
      border-radius: 50%;
  }

  .toggle-expand:hover {
      background: var(--sidebar-hover);
  }

  /* Expanded/Collapsed States */
  .sidebar.expanded {
      width: var(--sidebar-width);
  }

  .sidebar:not(.expanded) {
      width: var(--sidebar-collapsed-width);
  }

  .sidebar:not(.expanded) .label {
      opacity: 0;
      width: 0;
  }

  .sidebar:not(.expanded) .logo {
      opacity: 0;
      width: 0;
  }

  .sidebar:not(.expanded) .toggle-expand {
      margin-left: 0;
      width: 100%;
      justify-content: center;
  }

  /* Mobile Responsive Styles */
  @media (max-width: 768px) {
      .mobile-toggle {
          display: block;
      }

      .sidebar {
          transform: translateX(-100%);
          display: none;
      }

      .sidebar.mobile-open {
          transform: translateX(0);
          display: flex;
      }
  }

  /* Desktop Styles */
  @media (min-width: 769px) {
      .sidebar {
          transform: translateX(0) !important;
          display: flex !important;
      }
      
      .mobile-toggle,
      .mobile-close {
          display: none !important;
      }
      
      .sidebar-header {
          padding-right: 1.5rem; /* Reset padding without close button */
      }
  }
</style>