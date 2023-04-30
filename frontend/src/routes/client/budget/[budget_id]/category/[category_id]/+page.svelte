<script lang="ts">
	import Table from '$lib/components/Table.svelte';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	let loading = true;
	let rowHeaders = ['desc', 'amount', 'date'];
	let fullHeaders = ['Description', 'Amount', 'Date'];
	let title = 'Transactions';
	let getRequestURL = '';
	let postPutDeleteRequestURL = '';
	let foreignKeyOptions = ['budget', 'category', 'account'];

	onMount(async () => {
		const budgetId = $page.params.budget_id;
		const categoryId = $page.params.category_id;
		getRequestURL = `/api/transaction/budget/${budgetId}/category/${categoryId}`;
		postPutDeleteRequestURL = `/api/transaction`;
		const categoryName = $page.url.searchParams.get('categoryName');
		title = categoryName ? categoryName : title;

		loading = false;
	});
</script>

{#if loading}
	<div class="placeholder animate-pulse" />
{:else}
	<Table  {title} {rowHeaders} {getRequestURL} {postPutDeleteRequestURL} {fullHeaders} {foreignKeyOptions} />
{/if}
