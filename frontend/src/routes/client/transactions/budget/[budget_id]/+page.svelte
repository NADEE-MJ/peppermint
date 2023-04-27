<script lang="ts">
	import { enhance } from '$app/forms';
    import Table from '$lib/components/Table.svelte';
	import { tableMapperValues, tableSourceMapper, type TableSource } from '@skeletonlabs/skeleton';
	import type { PageData, SubmitFunction } from './$types';

	

	export let data: PageData 
	let tableData = data.transactions;
	let pageNumber = 1;
	const test = (num: number) => {
		// console.log('here', num);
		// console.log(tableData);
		return num;
	} 
	$: something = test(pageNumber);

	const updateTableData: SubmitFunction = ({data}) => {
		console.log()
		data.set('pageNumber', pageNumber);
		return async ({ result, update }) => {
			// console.log('here3', result);
			if (result.type !== 'failure') {
				if (result.data) {
					const { transactions } = result.data;
					
					console.log('transactions from action', transactions);
					const newHeaders = Object.keys(transactions[0]);
					sourceTable = {
						head: newHeaders,
        				body: tableMapperValues(transactions, newHeaders),
						meta: tableSourceMapper(transactions, newHeaders),
					};
				}
			}
			update({ reset: false });
		};
	};

	const headers = Object.keys(tableData[0]);
    let sourceTable: TableSource = {
        head: headers,
        body: tableMapperValues(tableData, headers),
        meta: tableSourceMapper(tableData, headers),
    };
	
</script>

<form class="card p-4" method="POST" action="?/getTransactionsByBudget" use:enhance={updateTableData}>
	<Table bind:pageNumber={pageNumber} sourceTable={sourceTable} />
</form>
