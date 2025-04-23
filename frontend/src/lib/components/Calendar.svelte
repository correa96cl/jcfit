<script>
    import { DatePicker } from "@svelte-plugins/datepicker";
    import { format } from 'date-fns';
  
    let startDate = new Date();
    let dateFormat = 'MM/dd/yy';
    let isOpen = false;
  
    const toggleDatePicker = () => (isOpen = !isOpen);
  
    const formatDate = (dateString) => {
      if (isNaN(new Date(dateString))) {
        return '';
      }
  
      return dateString && format(new Date(dateString), dateFormat) || '';
    };
  
  
    let formattedStartDate = formatDate(startDate);
  
    const onChange = () => {
      startDate = new Date(formattedStartDate);
    };
  
    $: formattedStartDate = formatDate(startDate);
  </script>
  
  <DatePicker bind:isOpen bind:startDate>
    <input type="text" placeholder="Select date" bind:value={formattedStartDate} on:click={toggleDatePicker} />
  </DatePicker>
  
  <style>
    input[type="text"] {
      border: 1px solid #eee;
      border-radius: 4px;
      padding: 8px;
    }
  </style>