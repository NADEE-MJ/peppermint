<script lang="ts">
	import Table from '$lib/components/Table.svelte';
	import { page } from '$app/stores';

	// let tableData = data.transactions;
	// let totalPages = data.totalPages;
	let headers = ['Amount', 'Date', 'Desc'];
	let title = 'Transactions';
	let requestURL = $page.url.toString();
</script>

<Table {title} {headers} {requestURL} />
