<script lang="ts">
	import Table from '$lib/components/Table.svelte';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	let loading = true;
	let rowHeaders = ['desc', 'amount', 'date'];
	let fullHeaders = ['Description', 'Amount', 'Date'];
	let title = 'Transactions';
	let requestURL = '';
	let foreignKeyOptions = ['budget', 'category', 'account'];

	onMount(async () => {
		const budgetId = $page.params.budget_id;
		if (budgetId === 'all') {
			const response = await fetch(`/api/budget`, { method: 'GET' });
			const data = await response.json();
			console.log(data);
			if (data['error']) {
				return;
			}
			requestURL = `/api/transaction/${data['budgets'][0].id}`;
		} else {
			requestURL = `/api/transaction/${budgetId}`;
		}
		loading = false;
	});
</script>

{#if loading}
	<div class="placeholder animate-pulse" />
{:else}
	<Table {title} {rowHeaders} {requestURL} {fullHeaders} {foreignKeyOptions} />
{/if}
