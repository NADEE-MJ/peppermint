<script lang="ts">
	import Next from '$lib/assets/Next.svg.svelte';
	import Back from '$lib/assets/Back.svg.svelte';
	import Trash from '$lib/assets/Trash.svg.svelte';
	import Edit from '$lib/assets/Edit.svg.svelte';
	import Plus from '$lib/assets/Plus.svg.svelte';
	import Close from '$lib/assets/Close.svg.svelte';

	import Textfield from './Textfield.svelte';

	import { modalStore, type ModalSettings } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';

	export let headers: string[];
	export let title: string;
	export let getRequestURL: string;
	// export let updateRequestURL: string;
	// export let deleteRequestURL: string;
	export let createRequestURL: string = 'test1233';

	let totalPages: number;
	let tableData: Array<{ [key: string]: any }> = [];
	let pageNumber: number = 1;
	let checkedBoxes: Array<{}> = [];

	onMount(async () => {
		//set loading to true before mount or use placeholders
		await getTableData();
	});

	const getTableData = async () => {
		const response = await fetch(`${getRequestURL}?page=${pageNumber}`, { method: 'GET' });
		const data = await response.json();
		tableData = data['transactions'];
		totalPages = data['totalPages'];
	};

	const nextPage = async () => {
		// modalStore.trigger(d);

		if (pageNumber < totalPages) {
			pageNumber++;
			checkedBoxes = [];
			await getTableData();
		}
	};

	const previousPage = async () => {
		if (pageNumber > 1) {
			pageNumber--;
			checkedBoxes = [];
			await getTableData();
		}
	};

	function addRemoveSelected(event: any) {
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
		// console.log("Files being deleted: ",checkedBoxes);
		const confirmDeletion: ModalSettings = {
			type: 'confirm',
			title: 'Please Confirm',
			body: 'Are you sure you want to delete this?',
			// TRUE if confirm pressed, FALSE if cancel pressed
			response: (r: boolean) => console.log('response:', r)
		};
		modalStore.trigger(confirmDeletion);
	};

	const startEditModal = (e: Event) => {
		let target = e.target as HTMLInputElement;
		if (target) {
			if (target.tagName !== 'BUTTON') {
				target.closest('button')?.click();
			}
		}
		if (!target?.value) {
			return;
		}

		//figure out what data to pass
		//prob just need headers, and row data, then can have
		const value = JSON.parse(target.value);
		const editModal: ModalSettings = {
			type: 'component',
			component: 'editModal',
			meta: { rowData: value, headers: headers },
			title: 'Edit'
		};
		modalStore.trigger(editModal);
	};

	const startCreateModal = (e: Event) => {
		let target = e.target as HTMLInputElement;
		if (!target?.value) {
			return;
		}
		if (target) {
			if (target.tagName !== 'BUTTON') {
				target.closest('button')?.click();
			}
		}

		//figure out what data to pass
		//prob just need headers, and row data, then can have
		const createModal: ModalSettings = {
			type: 'component',
			component: 'createModal',
			meta: { rowData: target.value, headers: headers },
			title: 'Create'
		};
		modalStore.trigger(createModal);
	};
</script>

<div class="card p-4">
	<div class="card-header grid grid-cols-2">
		<strong class="text-5xl">{title}</strong>
		<div class="flex justify-end space-x-4">
			<button type="button" class="btn btn-lg variant-filled-primary" value={createRequestURL} on:click|preventDefault={(e) => startCreateModal(e)}>
				<Plus classOverride="w-6 h-6" />
			</button>
			<button
				type="button"
				disabled={checkedBoxes.length < 1}
				class={`btn btn-lg variant-${checkedBoxes.length < 1 ? 'ghost-primary' : 'filled-primary'}`}
				on:click={deleteModal}
			>
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
						<!-- need to figure out how to remove item from list when deselected -->
						<td>
							<input
								type="checkbox"
								checked={checkedBoxes.includes(row)}
								class="checkbox"
								value={JSON.stringify(row)}
								on:change={addRemoveSelected}
							/>
						</td>
						{#each headers as header}
							<td>{row[header.toLowerCase()]}</td>
						{/each}
						<td>
							<button
								type="button"
								class="btn btn-sm variant-filled-surface"
								value={JSON.stringify(row)}
								on:click|preventDefault={(e) => {
									startEditModal(e);
								}}
							>
								<Edit classOverride="w-6 h-6" />
							</button>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>

	<div class="card-footer grid grid-cols-2">
		<strong class="text-lg p-2">Page {pageNumber} / {totalPages}</strong>
		<div class="flex justify-end space-x-4">
			<button
				class={`btn btn-lg variant-${pageNumber === 1 ? 'ghost-surface' : 'filled-surface'}`}
				type={pageNumber === 1 ? 'button' : 'submit'}
				on:click={previousPage}
			>
				<Back classOverride="w-6 h-6" />
			</button>
			<button
				class={`btn btn-lg variant-${pageNumber >= totalPages ? 'ghost-surface' : 'filled-surface'}`}
				type={pageNumber >= totalPages ? 'button' : 'submit'}
				on:click={nextPage}
			>
				<Next classOverride="w-6 h-6" />
			</button>
		</div>
	</div>
</div>
