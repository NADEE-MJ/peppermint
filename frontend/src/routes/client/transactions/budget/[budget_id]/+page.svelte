<script lang="ts">
	import { enhance } from '$app/forms';
    import Table from '$lib/components/Table.svelte';
	import { tableMapperValues, tableSourceMapper, type TableSource } from '@skeletonlabs/skeleton';
	import type { PageData, SubmitFunction } from './$types';


	export let data: PageData;
	let tableData = data.transactions;
	let dataLength: number = tableData.length;
	let pageNumber = 1;

	const updateTableData: SubmitFunction = ({data}) => {
		data.set('pageNumber', pageNumber);
		return async ({ result, update }) => {
			// console.log('here3', result);
			if (result.type !== 'failure') {
				if (result.data) {
					tableData = result.data['transactions'];
					dataLength = tableData.length;
					console.log('transactions from action', tableData);
				}
			}
			update({ reset: false });
		};
	};
	const headers = Object.keys(tableData[0]);
	
</script>

<form class="card p-4" method="POST" action="?/getTransactionsByBudget" use:enhance={updateTableData}>
	<Table bind:pageNumber={pageNumber} tableData={tableData} dataLength={dataLength} />
</form>
