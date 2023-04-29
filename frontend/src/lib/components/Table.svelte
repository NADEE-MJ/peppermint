<script lang="ts">
	import Next from '$lib/assets/Next.svg.svelte';
	import Back from '$lib/assets/Back.svg.svelte';
	import Trash from '$lib/assets/Trash.svg.svelte';
	import Edit from '$lib/assets/Edit.svg.svelte';
	import { enhance } from '$app/forms';
	// import type { ModalSettings } from '@skeletonlabs/skeleton';
	import type { SubmitFunction } from '@sveltejs/kit';
	import Textfield from './Textfield.svelte';
	import { modalStore, type ModalSettings } from '@skeletonlabs/skeleton';
	import Plus from '$lib/assets/Plus.svg.svelte';
	import Close from '$lib/assets/Close.svg.svelte';

	export let pageNumber:number = 1;
	export let tableData: Array<object>;
	export let headers: string[];
	export let title: string;
	export let actionURL: string;
	export let rowData = {};

	// export let lastPageNumber: number;
	let checkedBoxes: Array<{}> = [];
	//this might need to be a bind
	let editMode: boolean = false;
	let dataLength: number = tableData.length;

	// ! this might be a problem if the data is a perfect multiple of 10

	const pageUp = () => {
		if (dataLength >= 10) {
			pageNumber++;
			checkedBoxes = [];
		}
	};

	const pageDown = () => {
		if (pageNumber > 1) {
			pageNumber--;
			checkedBoxes = [];
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
		console.log(checkedBoxes, checkedBoxes.length);
	}

	const deleteModal = () => {
		console.log("Files being deleted: ",checkedBoxes);
		const confirmDeletion: ModalSettings = {
			type: 'confirm',
			// Data
			title: 'Please Confirm',
			body: 'Are you sure you want to delete this?',
			// TRUE if confirm pressed, FALSE if cancel pressed
			response: (r: boolean) => console.log('response:', r)
		};
		modalStore.trigger(confirmDeletion);
	};

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

	const editRowData = (event: any) => {
		editMode = true;
		console.log(event.target.value);
		const valueString = event.target.value;
		const value = JSON.parse(valueString);
		console.log(value);
	};

	const updateTableData: SubmitFunction = ({ data }) => {
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
</script>

{#if !(editMode)}
	<form class="card p-4" method="POST" action={actionURL} use:enhance={updateTableData}>
		<div class="card-header grid grid-cols-2">
			<strong class="text-5xl">{title}</strong>
			<div class="btn-group justify-end">
				<button type="button"
					class='btn btn-sm variant-filled-primary'
					on:click={() => editMode = true}>
					<Plus classOverride="w-6 h-6" />
				</button>
				<button type="button"
					disabled={checkedBoxes.length < 1}
					class={checkedBoxes.length < 1 ? 'btn btn-sm variant-ghost-primary' : 'btn btn-sm variant-filled-primary'}
					on:click={deleteModal}>
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
					{#each tableData as row, i}
						<tr>
							<td>
								<input type="checkbox" checked={checkedBoxes.includes(row)} class="checkbox" value={JSON.stringify(row)} on:change={addSelected} />
							</td>
							{#each headers as header}
								<td>{row[header.toLowerCase()]}</td>
							{/each}
							<td>
								<!-- Doesn't work -->
								<button type="button" 
									class="btn btn-sm variant-filled-surface"
									value={JSON.stringify(row)}
									on:click={editRowData}>
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
{:else}
<form class="card p-4">
	<div class="card-header grid grid-cols-2">
		<strong class="text-3xl">Add/Edit {title}</strong>
		<div class="flex h-12 justify-end">
			<button 
				class="btn btn-sm variant-filled-primary" 
				on:click={() => editMode = false}>
				<Close
					classOverride="w-6 h-6" />
			</button>
		</div>
	</div>
	<div class="grid grid-cols-2 gap-4 p-6">
		<div class="grid-cols-[auto_1fr_auto]">
			<Textfield
				label="Amount"
				name="amount"
				type="text"
				placeholder="Amount"
				errorMessages={[""]}
			/>
		</div>
		<div class="grid-cols-[auto_1fr_auto]">
			<label class="label">
				<span>Date</span>
				<input class="input" type="date" placeholder="01/01/2002" />
			</label>
		</div>
		<div class="grid-cols-[auto_1fr_auto]">
			<Textfield
					label="Description"
					name="description"
					type="text"
					placeholder="Amount"
					errorMessages={[""]}
				/>
		</div>
	</div>
	<div class="card-footer grid grid-cols-1">
		<div class="flex justify-end space-x-4">
			<button class="btn variant-filled-secondary">Submit</button>
		</div>
	</div>	
</form>
{/if}
