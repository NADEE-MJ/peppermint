<script lang="ts">
	import Table from '$lib/components/Table.svelte';
	import { page } from '$app/stores';

	let rowHeaders = ['desc', 'amount', 'date', ];
	let fullHeaders = ['Description', 'Amount', 'Date', ];
	let title = 'Transactions';
	let requestURL = $page.url.pathname.toString();
</script>

<Table {title} {rowHeaders} {requestURL} {fullHeaders} />
