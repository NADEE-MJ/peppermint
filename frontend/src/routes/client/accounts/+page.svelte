<script lang="ts">
	import Table from '$lib/components/Table.svelte';

	let rowHeaders = ['name', 'account_type'];
	let fullHeaders = ['Name', 'Account Type'];
	let title = 'Accounts';
	let getRequestURL = '/api/accounts';
	let postPutDeleteRequestURL = '/api/account';
	let dataKey = 'accounts';
</script>

<Table {title} {rowHeaders} {getRequestURL} {postPutDeleteRequestURL} {fullHeaders} {dataKey} />
