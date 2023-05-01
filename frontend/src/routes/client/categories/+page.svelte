<script lang="ts">
	import Table from '$lib/components/Table.svelte';

	let rowHeaders = ['name', 'desc', 'amount'];
	let fullHeaders = ['Name', 'Description', 'Amount'];
	let title = 'Categories';
	let getRequestURL = '/api/categories';
	let postPutDeleteRequestURL = '/api/category';
	let foreignKeyOptions = ['budget'];
	let dataKey = 'categories';
</script>

<Table {title} {rowHeaders} {getRequestURL} {postPutDeleteRequestURL} {fullHeaders} {dataKey} {foreignKeyOptions} />
