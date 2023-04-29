<script lang="ts">
	import Next from '$lib/assets/Next.svg.svelte';
	import Back from '$lib/assets/Back.svg.svelte';
	import Trash from '$lib/assets/Trash.svg.svelte';
	import Edit from '$lib/assets/Edit.svg.svelte';

	import { enhance } from '$app/forms';
	// import type { ModalSettings } from '@skeletonlabs/skeleton';
	import type { SubmitFunction } from '@sveltejs/kit';

	export let pageNumber = 1;
	export let tableData: Array<object>;
	export let headers: string[];
	export let title: string;
	export let actionURL: string;
	// export let lastPageNumber: number;
	let checkedBoxes: Array<{}> = []; //this might need to be a bind


	let dataLength: number = tableData.length;

	// ! this might be a problem if the data is a perfect multiple of 10

	const pageUp = () => {
		if (dataLength >= 10) {
			pageNumber++;
		}
	};

	const pageDown = () => {
		if (pageNumber > 1) {
			pageNumber--;
		}
	};

	function addSelected(event: any) {
		const valueString = event.target.value;
		const value = JSON.parse(valueString);
		if (event.target.checked) {
			checkedBoxes = [...checkedBoxes, value];
		} else {
			let item = checkedBoxes.indexOf((item: any) => item === value);
			checkedBoxes.splice(item, 1);
		}
		console.log(checkedBoxes);
	}

	// const confirmDeletion: ModalSettings = {
	// 	type: 'confirm',
	// 	// Data
	// 	title: 'Please Confirm',
	// 	body: 'Are you sure you want to delete this?',
	// 	// TRUE if confirm pressed, FALSE if cancel pressed
	// 	response: (r: boolean) => console.log('response:', r)
	// };

	const updateTableData: SubmitFunction = ({ data }) => {
		data.set('pageNumber', pageNumber.toString());
		return async ({ result, update }) => {
			if (result.type === 'success') {
				if (result.data) {
					tableData = result.data['transactions'];
				}
			}
			update({ reset: false });
		};
	};
</script>

<form class="card p-4" method="POST" action={actionURL} use:enhance={updateTableData}>
	<div class="card-header grid grid-cols-2">
		<strong class="text-5xl">{title}</strong>
		<div class="btn-group justify-end">
			<button type="button"
				disabled={checkedBoxes.length < 1}
				class={checkedBoxes ? 'btn btn-sm variant-ghost-primary' : 'btn btn-sm variant-filled-primary'}>
				<Trash classOverride="w-6 h-6" />
			</button>
		</div>
	</div>
	<div class="table-container p-4">
		<table class="table table-hover">
			<thead>
				<tr>
					<th />
					{#each headers as header}
						<th>{header}</th>
					{/each}
					<th>Edit</th>
				</tr>
			</thead>
			<tbody>
				{#each tableData as row}
					<tr>
						<td>
							<input type="checkbox" class="checkbox" value={JSON.stringify(row)} on:change={addSelected} />
						</td>
						{#each headers as header}
							<td>{row[header.toLowerCase()]}</td>
						{/each}
						<td>
							<button type="button" class="btn btn-sm variant-filled-surface">
								<Edit classOverride="w-6 h-6" />
							</button>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>

	<div class="card-footer grid grid-cols-2">
		<strong class="text-lg p-2">Page {pageNumber}</strong>
		<div class="flex justify-end space-x-4">
			<button
				class={pageNumber === 1 ? 'btn btn-lg  variant-ghost-surface' : 'btn btn-lg variant-filled-surface'}
				type="submit"
				on:click={pageDown}>
				<Back classOverride="w-6 h-6" />
			</button>
			<button
				class={dataLength < 10 ? 'btn btn-lg  variant-ghost-surface' : 'btn btn-lg variant-filled-surface'}
				type="submit"
				on:click={pageUp}>
					<Next classOverride="w-6 h-6" />
			</button>
		</div>
	</div>
</form>
