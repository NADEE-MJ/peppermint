<script lang="ts">
	import Next from '$lib/assets/Next.svg.svelte';
	import Back from '$lib/assets/Back.svg.svelte';
	import Trash from '$lib/assets/Trash.svg.svelte';
	import Edit from '$lib/assets/Edit.svg.svelte';
	import Plus from '$lib/assets/Plus.svg.svelte';

	import { modalStore, type ModalSettings, ProgressRadial } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';
	import { toast } from '$lib/toasts';

	onMount(async () => {
		await getTableData();
	});

	export let rowHeaders: string[];
	export let fullHeaders: string[];
	export let title: string;
	export let requestURL: string;
	export let foreignKeyOptions: Array<string> | undefined = undefined;

	let totalPages: number;
	let tableData: Array<{ [key: string]: any }> = [];
	let pageNumber: number = 1;
	let checkedBoxes: Array<{ [key: string]: any }> = [];
	let loading = true;

	const getTableData = async () => {
		loading = true;
		const response = await fetch(`${requestURL}?page=${pageNumber}`, { method: 'GET' });
		const data = await response.json();
		tableData = data['transactions'];
		totalPages = data['totalPages'];
		loading = false;
	};

	$: nextPageDisabled = pageNumber >= totalPages;
	const nextPage = async () => {
		pageNumber++;
		checkedBoxes = [];
		await getTableData();
	};

	$: previousPageDisabled = pageNumber === 1;
	const previousPage = async () => {
		pageNumber--;
		checkedBoxes = [];
		await getTableData();
	};

	const formattedDate = (date: string) => {
		const dateObj = new Date(date);
		const month = dateObj.toLocaleString('default', { month: 'long' });
		const day = dateObj.getDate();
		const year = dateObj.getFullYear();
		return `${month} ${day}, ${year}`;
	};

	const addRemoveSelected = (e: Event) => {
		const target = e.target as HTMLInputElement;
		const valueString = target.value;
		const value = JSON.parse(valueString);
		if (target.checked) {
			checkedBoxes.push(value);
		} else {
			let filteredCheckedBoxes = checkedBoxes.filter((item: any) => (item.id === value.id ? item : null));
			const firstOccurrence = checkedBoxes.indexOf(filteredCheckedBoxes[0]);

			checkedBoxes.splice(firstOccurrence, 1);
		}
		checkedBoxes = checkedBoxes;
	}

	const deleteTableData = async (jsonData: object) => {
		loading = true;
		const response = await fetch(`${requestURL}`, {
			method: 'DELETE',
			body: JSON.stringify(jsonData),
			headers: { 'Content-Type': 'application/json' }
		});
		const data = await response.json();
		if (data['success']) {
			checkedBoxes = [];
			toast.success('Successfully deleted selected rows');
			await getTableData();
		} else {
			toast.error('Unable to delete rows');
		}
		loading = false;
	};

	$: deleteDisabled = checkedBoxes.length < 1;
	const startDeleteModal = () => {
		const confirmDeletion: ModalSettings = {
			type: 'confirm',
			title: 'Please Confirm',
			body: 'Are you sure you want to delete the selected rows?',
			response: (res: boolean) => (res ? deleteTableData(checkedBoxes) : null)
		};
		modalStore.trigger(confirmDeletion);
	};

	const updateTableData = async (jsonData: object, id: number) => {
		loading = true;
		const response = await fetch(`${requestURL}`, {
			method: 'PUT',
			body: JSON.stringify({...jsonData, id}),
			headers: { 'Content-Type': 'application/json' }
		});
		const data = await response.json();
		if (data['success']) {
			checkedBoxes = [];
			toast.success('Successfully updated selected row');
			await getTableData();
		} else {
			toast.error('Unable to update row');
		}
		loading = false;
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

		const value = JSON.parse(target.value);
		const editModal: ModalSettings = {
			type: 'component',
			component: 'editModal',
			meta: { rowData: value, rowHeaders, fullHeaders },
			title: 'Edit Row',
			response: (res: { [key: string]: any }) => (res ? updateTableData(res, value.id) : null)
		};
		modalStore.trigger(editModal);
	};

	const addTableData = async (jsonData:  {[key: string]: any} ) => {
		loading = true;
		const response = await fetch(`${requestURL}`, {
			method: 'POST',
			body: JSON.stringify(jsonData),
			headers: { 'Content-Type': 'application/json' }
		});
		const data = await response.json();
		if (data['success']) {
			checkedBoxes = [];
			toast.success('Successfully added selected row');
			await getTableData();
		} else {
			toast.error('Unable to add row');
		}
		loading = false;
	};

	const startCreateModal = (e: Event) => {
		let target = e.target as HTMLInputElement;
		if (target) {
			if (target.tagName !== 'BUTTON') {
				target.closest('button')?.click();
			}
		}
		if (!target?.value) {
			return;
		}

		const createModal: ModalSettings = {
			type: 'component',
			component: 'createModal',
			meta: { rowHeaders, fullHeaders, foreignKeyOptions: (foreignKeyOptions ? foreignKeyOptions : null) },
			title: 'Create Row',
			response: (res: { [key: string]: any }) => (res ? addTableData(res) : null)
		};
		modalStore.trigger(createModal);
	};
</script>

{#if !loading}
	<div class="card p-4">
		<div class="card-header grid grid-cols-2">
			<strong class="text-5xl">{title}</strong>
			<div class="flex justify-end space-x-4">
				<button type="button" class="btn btn-lg variant-filled-primary" value={requestURL} on:click|preventDefault={(e) => startCreateModal(e)}>
					<Plus classOverride="w-6 h-6" />
				</button>
				<button type="button" disabled={deleteDisabled} class={'btn btn-lg variant-filled-primary'} on:click={startDeleteModal}>
					<Trash classOverride="w-6 h-6" />
				</button>
			</div>
		</div>

		<div class="table-container p-4">
			<table class="table table-hover">
				<thead>
					<tr>
						<th />
						{#each fullHeaders as fullHeader}
							<th>{fullHeader}</th>
						{/each}
						<th>Edit</th>
					</tr>
				</thead>
				<tbody>
					{#each tableData as rowData}
						<tr>
							<td>
								<input
									type="checkbox"
									checked={checkedBoxes.includes(rowData)}
									class="checkbox"
									value={JSON.stringify(rowData)}
									on:change={addRemoveSelected}
								/>
							</td>
							{#each rowHeaders as rowHeader}
								{#if rowHeader === 'date'}
									<td>{formattedDate(rowData[rowHeader])}</td>
								{:else}
									 <td>{rowData[rowHeader]}</td>
								{/if}
							{/each}
							<td>
								<button
									type="button"
									class="btn btn-sm variant-filled-surface"
									value={JSON.stringify(rowData)}
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
				<button class="btn btn-lg variant-filled-surface" disabled={previousPageDisabled} on:click={previousPage}>
					<Back classOverride="w-6 h-6" />
				</button>
				<button class="btn btn-lg variant-filled-surface" disabled={nextPageDisabled} on:click={nextPage}>
					<Next classOverride="w-6 h-6" />
				</button>
			</div>
		</div>
	</div>
{:else}
	<div class="card p-4">
		<div class="card-header">
			<strong class="text-5xl">{title}</strong>
		</div>
		<div class="flex justify-center">
			<ProgressRadial width="w-96" />
		</div>
	</div>
{/if}
