<script lang="ts">
	import ErrorCircle from '$lib/assets/ErrorCircle.svg.svelte';
	import EyeClosed from '$lib/assets/EyeClosed.svg.svelte';
	import EyeOpen from '$lib/assets/EyeOpen.svg.svelte';
	import { SlideToggle } from '@skeletonlabs/skeleton';

	export let errorMessages: Array<string> | null | undefined;
	export let type: string;
	export let label: string | null | undefined = null;
	export let placeholder: string;
	export let name: string;
	export let value: string | null | undefined = undefined;

	let passwordHidden = true;

	const formattedDate = (date: string) => {
		const dateObj = new Date(date);
		const month = `${dateObj.getUTCMonth()}`.padStart(2, '0');
		const day = `${dateObj.getUTCDate()}`.padStart(2, '0');
		const year = dateObj.getFullYear();
		return `${year}-${month}-${day}`;
	};
	if (type === 'date' && typeof value == 'string') {
		value = formattedDate(value);
	}

	function togglePasswordVisibility() {
		passwordHidden = !passwordHidden;
	}
</script>

<div class="space-y-2">
	{#if label}
		<strong class="text-md">{label}</strong>
	{/if}


	{#if type === 'email'}
		<input class="input {errorMessages ? 'input-invalid' : ''}" type="email" {placeholder} {name} bind:value />
	{:else if type === 'password'}
		<div class="relative w-full">
			{#if passwordHidden}
				<input class="input {errorMessages ? 'input-invalid' : ''}" type="password" {placeholder} {name} bind:value />
			{:else}
				<input class="input {errorMessages ? 'input-invalid' : ''}" type="text" {placeholder} {name} bind:value />
			{/if}

			<button type="button" class="absolute inset-y-0 right-0 pr-3 flex items-center" on:click={togglePasswordVisibility}>
				{#if passwordHidden}
					<EyeOpen classOverride="text-white w-6" />
				{:else}
					<EyeClosed classOverride="text-white w-6" />
				{/if}
			</button>
		</div>
	{:else if type === 'date'}
		<input class="input {errorMessages ? 'input-invalid' : ''}" type="date" {placeholder} {name} bind:value />
	{:else if type === 'is_active'}
		<SlideToggle name="slider-label" checked={value.toString() === "true"}></SlideToggle>
	{:else}
		<input class="input {errorMessages ? 'input-invalid' : ''}" type="text" {placeholder} {name} bind:value />
	{/if}

	<label for={name} class="label">
		{#if errorMessages}
			{#each errorMessages as message}
				<aside class="alert variant-soft-error">
					<ErrorCircle classOverride="w-6 h-6" />
					<div class="alert-message">
						<p>{message}</p>
					</div>
				</aside>
			{/each}
		{/if}
	</label>
</div>
