<script lang="ts">
	import ErrorCircle from '$lib/assets/ErrorCircle.svg.svelte';
	import { ListBox, ListBoxItem } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';

	export let value: string;
	export let label: string;
	export let errorMessages: Array<string> | null = null;
	export let selectType: string;

	let listItems: Array<{ value: string; displayName: string }> = [];

	onMount(() => {
		if (selectType === 'account_type') {
			listItems = [
				{ value: 'checking', displayName: 'Checking' },
				{ value: 'savings', displayName: 'Savings' },
				{ value: 'credit', displayName: 'Credit' }
			];
		}
	});
</script>

<div class="space-y-2">
	{#if label}
		<strong class="text-md">{label.charAt(0).toUpperCase() + label.slice(1)}</strong>
	{/if}
	<div class="space-y-4 border border-surface-500 p-4 rounded-container-token">
		<ListBox>
			{#each listItems as listItem}
				<ListBoxItem bind:group={value} name={listItem.value} value={listItem.value}>{listItem.displayName}</ListBoxItem>
			{/each}
		</ListBox>
	</div>
	{#if errorMessages}
		<label for={selectType} class="label">
			{#if errorMessages}
				{#each errorMessages as message}
					<aside class="alert variant-soft-error">
						<ErrorCircle classOverride="w-6 h-6" />
						<div class="alert-message">
							<p>{message === 'Required' ? 'Please select an option from the list' : message}</p>
						</div>
					</aside>
				{/each}
			{/if}
		</label>
	{/if}
</div>
