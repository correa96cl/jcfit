<script>
	import Modal from '../Modal.svelte';
	import { DatePicker } from '@svelte-plugins/datepicker';
	import { format, parseISO } from 'date-fns';
	import { createForm } from 'felte';
	import { reporter } from '@felte/reporter-svelte';
	import { validator } from '@felte/validator-zod';
	import { z } from 'zod';
	import { ptBR } from 'date-fns/locale';
	import { toast, Toaster } from 'svelte-sonner';


	// Date picker setup
	let startDate = new Date();
	let dateFormat = 'dd/MM/yyyy';
	export let isOpenCalendar = false;
	const toggleDatePicker = () => (isOpenCalendar = !isOpenCalendar);

	const formatDate = (dateString) => {
		if (isNaN(new Date(dateString))) return '';
		return (dateString && format(new Date(dateString), dateFormat)) || '';
	};

	$: formattedStartDate = formatDate(startDate);

	// Modal props
	export let isOpen = false;
	export let onClose;
	export let onAlunoAdicionado;

	// Zod schema for validation
	const schema = z.object({
		nome: z.string().min(2, 'Nome deve ser preenchido'),
		sobrenome: z.string().min(2, 'Sobrenome deve ser prenchido'),
		email: z.string().email('Email inválido'),
		telefone: z
			.string()
			.min(11, 'Telefone deve ter pelo menos 11 dígitos')
			.max(15, 'Telefone deve ter no máximo 15 dígitos'),
		dataNascimento: z
			.string()
			.refine(
				(val) => {
					// Check if the string matches dd/MM/yyyy format
					if (!/^\d{2}\/\d{2}\/\d{4}$/.test(val)) return false;

					// Parse the date in Brazilian format
					const [day, month, year] = val.split('/').map(Number);
					const date = new Date(year, month - 1, day);

					// Check if the date is valid
					return (
						date.getFullYear() === year && date.getMonth() === month - 1 && date.getDate() === day
					);
				},
				{
					message: 'Data inválida (use DD/MM/AAAA)'
				}
			)
			.refine(
				(val) => {
					const birthDate = new Date(val);
					const today = new Date();
					const minAgeDate = new Date(today.getFullYear() - 16, today.getMonth(), today.getDate());
					return birthDate <= minAgeDate;
				},
				{
					message: 'O aluno deve ter pelo menos 16 anos'
				}
			)
	});

	const { form, errors, data } = createForm({
		extend: [validator({ schema }), reporter],
		onSubmit: async (values) => {
			try {
				const response = await fetch('http://127.0.0.1:5000/api/alunos/add', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({
						nome: values.nome,
						sobrenome: values.sobrenome,
						email: values.email,
						telefone: values.telefone,
						data_nascimento: values.dataNascimento,
						ativo: 1
					})
				});

				if (response.ok) {
					// Show success toast
					toast.success('Aluno adicionado com sucesso!', {
						duration: 3000,
						position: 'top-right'
					});
					
					if (onAlunoAdicionado) onAlunoAdicionado();
					fecharModal();
				} else {
					// Show error toast
					toast.error('Erro ao adicionar aluno.', {
						duration: 3000,
						position: 'top-right'
					});
				}
			} catch (error) {
				console.error('Error:', error);
				// Show error toast
				toast.error('Erro ao adicionar aluno.', {
					duration: 3000,
					position: 'top-right'
				});
			}
		}
	});

	function fecharModal() {
		isOpen = false;
		if (onClose) onClose();
	}

	function formatPhoneNumber(value) {
		// Remove all non-digit characters
		const cleaned = value.replace(/\D/g, '');

		// Apply formatting (customize this for your country's format)
		const match = cleaned.match(/^(\d{2})(\d{5})(\d{4})$/);
		if (match) {
			return `(${match[1]}) ${match[2]}-${match[3]}`;
		}
		return cleaned;
	}

	function handlePhoneInput(e) {
		const input = e.target;
		const formatted = formatPhoneNumber(input.value);
		input.value = formatted;
		data.telefone = formatted.replace(/\D/g, ''); // Store only digits in form data
	}

	// Date picker state
	let selectedDate = new Date();
	let isCalendarOpen = false;

	// Format date for display
	$: formattedDate = selectedDate ? format(selectedDate, dateFormat, { locale: ptBR }) : '';

	// Toggle calendar visibility
	const toggleCalendar = () => {
		isCalendarOpen = !isCalendarOpen;
	};

	// Handle date selection
	const handleDateSelect = (event) => {
		selectedDate = event.detail;
		isCalendarOpen = false;
		data.dataNascimento = format(selectedDate, 'dd-MM-yyy');
		formattedDate = format(selectedDate, dateFormat, { locale: ptBR });
	};

	let rawDate = '';
	let formattedDate = '';

	function formatDateInput(event) {
		const input = event.target.value.replace(/\D/g, ''); // Remove all non-digit characters
		let formatted = '';

		if (input.length > 0) {
			formatted = input.substring(0, 2);
		}
		if (input.length > 2) {
			formatted += '/' + input.substring(2, 4);
		}
		if (input.length > 4) {
			formatted += '/' + input.substring(4, 8);
		}

		// Limit to 10 characters (DD/MM/AAAA)
		if (input.length > 8) {
			formatted = formatted.substring(0, 10);
		}

		rawDate = input;
		formattedDate = formatted;
	}
</script>

<Modal {isOpen} onClose={fecharModal}>
	<h2 class="modal-title">Adicionar Aluno</h2>
	<form use:form>
		<div class="form-group">
			<label for="nome">Nome:</label>
			<input
				type="text"
				id="nome"
				name="nome"
				placeholder="Digite o nome do aluno"
				aria-invalid={$errors.nome ? 'true' : 'false'}
			/>
			{#if $errors.nome}
				<span class="error-message">{$errors.nome}</span>
			{/if}
		</div>

		<div class="form-group">
			<label for="sobrenome">Sobrenome:</label>
			<input
				type="text"
				id="sobrenome"
				name="sobrenome"
				placeholder="Digite o sobrenome do aluno"
				aria-invalid={$errors.sobrenome ? 'true' : 'false'}
			/>
			{#if $errors.sobrenome}
				<span class="error-message">{$errors.sobrenome}</span>
			{/if}
		</div>

		<div class="form-group">
			<label for="email">Email:</label>
			<input
				type="email"
				id="email"
				name="email"
				placeholder="Digite o email do aluno"
				aria-invalid={$errors.email ? 'true' : 'false'}
			/>
			{#if $errors.email}
				<span class="error-message">{$errors.email}</span>
			{/if}
		</div>

		<div class="form-group">
			<label for="telefone">Telefone:</label>
			<input
				type="tel"
				id="telefone"
				name="telefone"
				placeholder="(00) 00000-0000"
				aria-invalid={$errors.telefone ? 'true' : 'false'}
				on:input={handlePhoneInput}
				maxlength="15"
				pattern="[0-9]*"
				inputmode="numeric"
			/>
			{#if $errors.telefone}
				<span class="error-message">{$errors.telefone}</span>
			{/if}
		</div>

		<div class="form-group date-picker-group">
			<label for="dataNascimento">Data de Nascimento:</label>
			<div class="date-input-container">
				<input
					type="text"
					id="dataNascimento"
					name="dataNascimento"
					placeholder="DD/MM/AAAA"
					bind:value={formattedDate}
					on:input={formatDateInput}
					on:click={toggleCalendar}
					aria-invalid={$errors.dataNascimento ? 'true' : 'false'}
				/>
				<button
					type="button"
					class="calendar-button"
					on:click={toggleCalendar}
					aria-label="Abrir calendário"
				>
					<span class="ri-calendar-line" />
				</button>

				{#if isCalendarOpen}
					<div class="calendar-popup">
						<DatePicker
							bind:date={selectedDate}
							on:dateSelected={handleDateSelect}
							options={{
								locale: ptBR,
								format: 'dd/MM/yyyy',
								showHeader: true,
								showFooter: true,
								closeOnSelect: true
							}}
						/>
					</div>
				{/if}
			</div>
			{#if $errors.dataNascimento}
				<span class="error-message">{$errors.dataNascimento}</span>
			{/if}
		</div>

		<div class="form-actions">
			<button class="shadow-modal" type="submit">Adicionar</button>
			<button type="button" class="shadow-modal-cancelar" on:click={fecharModal}>Cancelar</button>
		</div>
	</form>
</Modal>

<style>
	form {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.modal-title {
		margin-bottom: 1.5rem;
		color: var(--cinza-escura);
	}

	.form-group {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	label {
		font-weight: 500;
		color: var(--cinza-escura);
	}

	input[type='text'],
	input[type='email'] {
		padding: 0.75rem;
		border: 1px solid var(--cinza-claro);
		border-radius: 6px;
		color: var(--cinza-escura);
		transition: border-color 0.3s ease;
	}

	input[type='text']:focus,
	input[type='email']:focus {
		outline: none;
		border-color: var(--azul-primario);
	}

	input[aria-invalid='true'] {
		border-color: var(--vermelho);
	}

	.error-message {
		color: var(--vermelho);
		font-size: 0.875rem;
		margin-top: 0.25rem;
	}

	.checkbox-group {
		flex-direction: row;
		align-items: center;
		gap: 0.5rem;
	}

	.form-actions {
		display: flex;
		gap: 1rem;
		margin-top: 1rem;
	}

	button {
		padding: 0.75rem 1.5rem;
		border-radius: 6px;
		font-weight: 500;
		cursor: pointer;
		transition: all 0.3s ease;
	}

	.shadow-modal-cancelar:hover {
		background-color: var(--cinza-claro);
	}

	input[type='tel'] {
		padding: 0.75rem;
		border: 1px solid var(--cinza-claro);
		border-radius: 6px;
		color: var(--cinza-escura);
		transition: border-color 0.3s ease;
	}

	/* Hide number input arrows in Chrome, Safari, Edge, Opera */
	input::-webkit-outer-spin-button,
	input::-webkit-inner-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}

	/* Hide number input arrows in Firefox */
	input[type='number'] {
		-moz-appearance: textfield;
	}

	.date-picker-group {
		position: relative;
	}

	.date-input-container {
		position: relative;
		display: flex;
		align-items: center;
	}

	.date-input-container input {
		padding-right: 2.5rem; /* Make space for calendar icon */
		width: 100%;
	}

	.date-picker-group {
		position: relative;
	}

	.date-input-container {
		position: relative;
		display: flex;
		align-items: center;
	}

	.date-input-container input {
		padding-right: 2.5rem;
		width: 100%;
		cursor: pointer;
	}

	.calendar-button {
		position: absolute;
		right: 0.5rem;
		background: none;
		border: none;
		color: var(--cinza-escura);
		cursor: pointer;
		padding: 0.5rem;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.calendar-button:hover {
		color: var(--azul-primario);
	}

	.calendar-popup {
		position: absolute;
		top: 100%;
		left: 0;
		z-index: 1000;
		margin-top: 0.5rem;
		background: white;
		border-radius: 8px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
		width: 300px; /* Add fixed width */
	}

	/* Customize the datepicker styles */
	:global(.datepicker) {
		border: none;
		border-radius: 8px;
		padding: 1rem;
	}

	:global(.datepicker-header) {
		background: var(--azul-primario);
		color: white;
		border-radius: 8px 8px 0 0;
	}

	:global(.datepicker-footer) {
		border-top: 1px solid var(--cinza-claro);
		padding: 0.5rem;
	}

	:global(.datepicker-day.selected) {
		background: var(--azul-primario);
		color: white;
	}

	:global(.datepicker-day:hover) {
		background: var(--azul-claro);
	}
</style>
<svelte:head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/svelte-sonner/dist/style.css">
</svelte:head>

<Toaster position="top-right" />