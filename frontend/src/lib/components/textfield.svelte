<script lang="ts">
	import ErrorCircle from '$lib/assets/ErrorCircle.svg';

	export let errorMessages: Array<string> | null | undefined;
	export let type: string;
	export let placeholder: string;
	export let name: string;
	export let value: string | null | undefined = undefined;
</script>

<div class="space-y-2">
	{#if type === 'email'}
		<input class="input max-w-md {errorMessages ? 'input-invalid' : ''}" type="email" {placeholder} {name} bind:value />
	{:else if type === 'password'}
		<input class="input max-w-md {errorMessages ? 'input-invalid' : ''}" type="password" {placeholder} {name} bind:value />
	{:else}
		<input class="input max-w-md {errorMessages ? 'input-invalid' : ''}" type="text" {placeholder} {name} bind:value />
	{/if}

	<label for={name} class="label max-w-md space-y-1">
		{#if errorMessages}
			{#each errorMessages as message}
				<aside class="alert alert-error">
					<img src={ErrorCircle} alt="ErrorCicle" class="w-6 h-6" />
					<div class="alert-message">
						<p>{message}</p>
					</div>
				</aside>
			{/each}
		{/if}
	</label>
</div>
