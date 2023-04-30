<script lang="ts">
	import ErrorCircle from '$lib/assets/ErrorCircle.svg.svelte';
	import EyeClosed from '$lib/assets/EyeClosed.svg.svelte';
	import EyeOpen from '$lib/assets/EyeOpen.svg.svelte';

	export let errorMessages: Array<string> | null | undefined;
	export let type: string;
	export let label: string | null | undefined = null;
	export let placeholder: string = "default";
	export let name: string;
	export let value: string | null | undefined = undefined;

	let date: string =  "";
	let time: string = "";
	let passwordHidden = true;

	function formatDate() {
		if (value === null || value === undefined) {
			return;
		}
		date = value.slice(0, 10);
		time = value.slice(11, 16);
		value = date;
	}
	if (type === "Date") { formatDate(); }

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
	{:else if type === "Date"}
		<input class="input {errorMessages ? 'input-invalid' : ''}" type="date" {placeholder} {name} bind:value />
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
