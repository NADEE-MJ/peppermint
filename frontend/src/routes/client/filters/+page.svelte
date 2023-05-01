<script lang="ts">
	import Table from '$lib/components/Table.svelte';

	let rowHeaders = ['filter_by'];
	let fullHeaders = ['Filter By'];
	let title = 'Filters';
	let getRequestURL = '/api/filter';
	let postPutDeleteRequestURL = '/api/filter';
	let foreignKeyOptions = ['category'];
	let dataKey = 'filters';
</script>

<Table {title} {rowHeaders} {getRequestURL} {postPutDeleteRequestURL} {fullHeaders} {foreignKeyOptions} {dataKey} />
