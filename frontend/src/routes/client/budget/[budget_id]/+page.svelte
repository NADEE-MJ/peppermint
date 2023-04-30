<script lang="ts">
	import Table from '$lib/components/Table.svelte';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	let loading = true;
	let rowHeaders = ['desc', 'amount', 'date'];
	let fullHeaders = ['Description', 'Amount', 'Date'];
	let title = 'Transactions';
	let getRequestURL = '';
	let postPutDeleteRequestURL = '/api/transaction';
	let foreignKeyOptions = ['budget', 'category', 'account'];

	onMount(async () => {
		const budgetId = $page.params.budget_id;
		if (budgetId === 'all') {
			const response = await fetch(`/api/budget`, { method: 'GET' });
			const data = await response.json();
			if (data['error']) {
				return;
			}
			getRequestURL = `/api/transaction/budget/${data['budgets'][0].id}`;
		} else {
			getRequestURL = `/api/transaction/budget/${budgetId}`;
		}
		loading = false;
	});
</script>

{#if loading}
	<div class="placeholder animate-pulse" />
{:else}
	<Table  {title} {rowHeaders} {getRequestURL} {postPutDeleteRequestURL} {fullHeaders} {foreignKeyOptions} />
{/if}
