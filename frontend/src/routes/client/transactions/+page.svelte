<script lang="ts">
	import Table from '$lib/components/Table.svelte';

	let rowHeaders = ['desc', 'amount', 'date'];
	let fullHeaders = ['Description', 'Amount', 'Date'];
	let title = 'Transactions';
	let getRequestURL = '/api/transaction';
	let postPutDeleteRequestURL = '/api/transaction';
	let foreignKeyOptions = ['budget', 'category', 'account'];
</script>

<Table {title} {rowHeaders} {getRequestURL} {postPutDeleteRequestURL} {fullHeaders} {foreignKeyOptions} />
