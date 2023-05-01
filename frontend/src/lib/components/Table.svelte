<script lang="ts">
	import Next from '$lib/assets/Next.svg.svelte';
	import Back from '$lib/assets/Back.svg.svelte';
	import Trash from '$lib/assets/Trash.svg.svelte';
	import Edit from '$lib/assets/Edit.svg.svelte';
	import Plus from '$lib/assets/Plus.svg.svelte';
	import Check from '$lib/assets/Check.svg.svelte';
	import ArrowRightCircle from '$lib/assets/ArrowRightCircle.svg.svelte';

	import { modalStore, type ModalSettings, ProgressRadial } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';
	import { toast } from '$lib/toasts';
	import { goto } from '$app/navigation';

	onMount(async () => {
		await getTableData();
		if (title === 'Filters') {
			categoryData = await getAllCategories();
		}
		loading = false;
	});

	export let rowHeaders: string[];
	export let fullHeaders: string[];
	export let excludeUpdateHeaders: string[] | undefined = undefined;
	export let title: string;
	export let getRequestURL: string;
	export let postPutDeleteRequestURL: string;
	export let foreignKeyOptions: Array<string> | undefined = undefined;
	export let dataIndex = 'transactions';
	export let uploadModal: any | undefined = undefined;
	export let addButton = true;

	let categoryData: Array<{ [key: string]: any }> = [];
	let totalPages: number;
	let tableData: Array<{ [key: string]: any }> = [];
	let pageNumber = 1;
	let checkedBoxes: Array<{ [key: string]: any }> = [];
	let loading = true;

	const getTableData = async () => {
		const response = await fetch(`${getRequestURL}?page=${pageNumber}`, { method: 'GET' });
		const data = await response.json();
		tableData = data[dataIndex];
		totalPages = data['totalPages'];
	};

	const getAllCategories = async () => {
		const response = await fetch(`/api/category`, { method: 'GET' });
		const data = await response.json();
		if (data['error']) {
			return [];
		}
		return data['categories'];
	};

	const getCategoryForTransaction = (categoryId: number) => {
		const category = categoryData.find((category) => category.id === categoryId);
		return category ? category.name : '';
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
	};

	const deleteTableData = async (jsonData: object) => {
		loading = true;
		const response = await fetch(`${postPutDeleteRequestURL}`, {
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
		const response = await fetch(`${postPutDeleteRequestURL}`, {
			method: 'PUT',
			body: JSON.stringify({ ...jsonData, id }),
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
			meta: { rowData: value, rowHeaders, fullHeaders, excludeUpdateHeaders },
			title: 'Edit Row',
			response: (res: { [key: string]: any }) => (res ? updateTableData(res, value.id) : null)
		};
		modalStore.trigger(editModal);
	};

	const addTableData = async (jsonData: { [key: string]: any }) => {
		loading = true;
		const response = await fetch(`${postPutDeleteRequestURL}`, {
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
			meta: { rowHeaders, fullHeaders, foreignKeyOptions: foreignKeyOptions ? foreignKeyOptions : null },
			title: 'Create Row',
			response: (res: { [key: string]: any }) => (res ? addTableData(res) : null)
		};
		modalStore.trigger(createModal);
	};

	const redirectToTransactionsPage = (e: Event) => {
		let target = e.target as HTMLInputElement;
		if (target) {
			if (target.tagName !== 'BUTTON') {
				target.closest('button')?.click();
			}
		}
		if (!target?.value) {
			return;
		}

		const account = JSON.parse(target.value);
		goto(`/client/accounts/${account.id}?accountName=${account.name}`);
	};
</script>

{#if !loading}
	<div class="card p-4">
		<div class="card-header grid grid-cols-2">
			<strong class="text-5xl">{title}</strong>
			<div class="flex justify-end space-x-4">
				{#if uploadModal}
					<button class="btn btn-lg variant-filled-secondary" on:click={uploadModal}>Upload CSV</button>
				{/if}
				{#if addButton}
					<button
						type="button"
						class="btn btn-lg variant-filled-primary"
						value={postPutDeleteRequestURL}
						on:click|preventDefault={(e) => startCreateModal(e)}
					>
						<Plus classOverride="w-6 h-6" />
					</button>
				{/if}
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
							{#if fullHeader !== 'Password'}
								<th>{fullHeader}</th>
							{/if}
						{/each}
						{#if title === 'Accounts'}
							<th>Transactions</th>
						{:else if title === 'Filters'}
							<th>Category</th>
						{/if}
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
								{#if rowHeader === 'date' || rowHeader === 'last_login'}
									<td>{formattedDate(rowData[rowHeader])}</td>
								{:else if rowHeader === 'is_admin' || rowHeader === 'is_active'}
									{#if rowData[rowHeader]}
										<td><Check classOverride="w-4 h-4" /></td>
									{:else}
										<td>-</td>
									{/if}
								{:else if rowHeader === 'password'}
									<!-- skip password -->
								{:else}
									<td>{rowData[rowHeader]}</td>
								{/if}
							{/each}
							{#if title === 'Accounts'}
								<td>
									<button
										type="button"
										class="btn btn-sm variant-filled-surface"
										value={JSON.stringify(rowData)}
										on:click|preventDefault={(e) => {
											redirectToTransactionsPage(e);
										}}
									>
										<ArrowRightCircle classOverride="w-6 h-6" />
									</button>
								</td>
							{:else if title === 'Filters'}
								<td>{getCategoryForTransaction(rowData['category_id'])}</td>
							{/if}
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
