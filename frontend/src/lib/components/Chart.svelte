<script lang="ts">
    import Chart from 'chart.js/auto';
    import { onMount } from 'svelte';
  
    export let labels: string[] = [];
    export let data: number[] = [];
    export let title: string = 'Minas aulas';
  
    let canvas: HTMLCanvasElement;
  
    onMount(() => {
      if (canvas) {
        new Chart(canvas, {
          type: 'bar',
          data: {
            labels: labels,
            datasets: [{
              label: title,
              data: data,
              backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
              ],
              borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
              ],
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      }
    });
  </script>
  
  <canvas bind:this={canvas}></canvas>