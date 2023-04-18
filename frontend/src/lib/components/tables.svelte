<script lang="ts">

import { Table } from '@skeletonlabs/skeleton';
import type { TableSource } from '@skeletonlabs/skeleton';
import { tableMapperValues } from '@skeletonlabs/skeleton';

export let sourceData: Array<{}>;
export let headerName: Array<string>;
export let count: 10;
export let current: 0;

</script>


<div class="table-container">
	<table class="table table-hover">
		<thead>
			<tr>
				{#each headerName as column, i}
					<th>{headerName[i]}</th>
				{/each}
            </tr>
		</thead>
		<tbody>
            {#each sourceData as data, i}
				<tr>
					{#each data as column, i}
						<td>{column}</td>
					{/each}
				</tr>
			{/each}
		</tbody>
		<tfoot>
			<tr>
				<td>Prev</td>
				<td>Next</td>
			</tr>
		</tfoot>
	</table>
</div>
