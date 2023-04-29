<script lang="ts">
	import Table from '$lib/components/Table.svelte';
	import type { PageData } from './$types';

	export let data: PageData;

	let tableData = data.transactions;
	let pageNumber = 1;
	let headers = ['Amount', 'Date', 'Desc'];
	let title = 'Transactions';
	let actionURL = "?/getTransactionsByBudget"
</script>

<Table {title} {headers} bind:pageNumber {tableData} {actionURL}  />

